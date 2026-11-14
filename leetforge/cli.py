from __future__ import annotations

import argparse
import os
import sys
from datetime import date
from pathlib import Path
from typing import List, Optional

from . import coach, complexity, docs, scaffold, stats
from .fmt import table
from .registry import get, load_all
from .runner import fuzz_problem, run_problem
from .srs import Scheduler


def _home() -> Path:
    return Path(os.getenv("LEETFORGE_HOME", ".leetforge"))


def _select(arg: str):
    if arg == "all":
        return load_all()
    p = get(arg)
    if p is None:
        print(f"unknown problem: {arg}", file=sys.stderr)
        return None
    return [p]


def cmd_list(a) -> int:
    rows = [[p.id, p.slug, p.difficulty, ",".join(p.tags), len(p.approaches)]
            for p in load_all()
            if (not a.tag or a.tag in p.tags) and (not a.difficulty or p.difficulty.lower() == a.difficulty.lower())]
    print(table(["#", "slug", "difficulty", "tags", "impl"], rows))
    return 0


def cmd_test(a) -> int:
    probs = _select(a.problem)
    if probs is None:
        return 2
    failed = 0
    for p in probs:
        for r in run_problem(p, isolate=not a.no_isolate, timeout=a.timeout):
            status = "PASS" if r.ok else "FAIL"
            note = " (timeout)" if r.timed_out else " (crashed)" if r.crashed else ""
            ms = sum(c.ms for c in r.cases)
            print(f"{status}  {p.slug:<42} {r.approach:<18} {r.passed}/{len(r.cases)}  {ms:7.2f} ms{note}")
            for c in r.cases:
                if not c.ok:
                    print(f"        case {c.index}: {c.error}")
            failed += not r.ok
    print(f"\n{'all passed' if not failed else f'{failed} approach(es) failed'}")
    return 1 if failed else 0


def cmd_fuzz(a) -> int:
    probs = _select(a.problem)
    if probs is None:
        return 2
    bad = 0
    for p in probs:
        r = fuzz_problem(p, trials=a.trials, seed=a.seed)
        if r.skipped:
            print(f"SKIP  {p.slug:<42} {r.skipped}")
        elif r.ok:
            print(f"OK    {p.slug:<42} {r.trials} random cases, all approaches agree")
        else:
            bad += 1
            print(f"FAIL  {p.slug}")
            for f in r.failures:
                print(f"        {f}")
    return 1 if bad else 0


def cmd_bench(a) -> int:
    p = get(a.problem)
    if p is None:
        print(f"unknown problem: {a.problem}", file=sys.stderr)
        return 2
    rows = []
    for name in p.approaches:
        if a.approach and name != a.approach:
            continue
        est = complexity.estimate(p, name, budget=a.budget)
        declared = p.complexity[name][0]
        verdict = "match" if complexity.compatible(declared, est.label) else "MISMATCH?"
        rows.append([name, declared, est.label, f"{est.slope:.2f}", f"{est.sizes[0]}..{est.sizes[-1]}" if est.sizes else "-", verdict])
    print(table(["approach", "declared", "estimated", "slope", "n range", "verdict"], rows))
    return 0


def cmd_new(a) -> int:
    try:
        path = scaffold.create(a.slug, a.title, a.difficulty.capitalize(), [t for t in a.tags.split(",") if t], a.id)
    except (ValueError, FileExistsError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(f"created {path}")
    return 0


def cmd_log(a) -> int:
    p = get(a.problem)
    if p is None:
        print(f"unknown problem: {a.problem}", file=sys.stderr)
        return 2
    sched = Scheduler(_home() / "progress.json")
    card = sched.log(p.slug, a.quality)
    sched.save()
    print(f"{p.slug}: next review {card['due']} (interval {card['interval']}d, ease {card['ease']})")
    return 0


def cmd_due(a) -> int:
    due = Scheduler(_home() / "progress.json").due()
    print("\n".join(due) if due else "nothing due")
    return 0


def cmd_stats(a) -> int:
    print(stats.render(load_all(), Scheduler(_home() / "progress.json")))
    return 0


def cmd_next(a) -> int:
    picks = coach.suggest(load_all(), Scheduler(_home() / "progress.json"), n=a.n)
    for slug, why in picks:
        print(f"{slug:<42} {why}")
    return 0


def cmd_docs(a) -> int:
    text = docs.render_problems_md(load_all())
    out = Path(a.out)
    if a.check:
        if not out.exists() or out.read_text(encoding="utf-8") != text:
            print(f"{out} is out of date - run `leetforge docs`", file=sys.stderr)
            return 1
        print(f"{out} is up to date")
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out}")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="leetforge", description="LeetCode practice toolkit")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("list", help="list problems"); s.add_argument("--tag"); s.add_argument("--difficulty"); s.set_defaults(fn=cmd_list)
    s = sub.add_parser("test", help="run test cases (isolated, with timeout)")
    s.add_argument("problem", help="slug, LeetCode number or 'all'")
    s.add_argument("--no-isolate", action="store_true"); s.add_argument("--timeout", type=float, default=10.0); s.set_defaults(fn=cmd_test)
    s = sub.add_parser("fuzz", help="differential fuzzing: all approaches must agree")
    s.add_argument("problem"); s.add_argument("--trials", type=int, default=200); s.add_argument("--seed", type=int, default=0); s.set_defaults(fn=cmd_fuzz)
    s = sub.add_parser("bench", help="estimate empirical time complexity")
    s.add_argument("problem"); s.add_argument("--approach"); s.add_argument("--budget", type=float, default=0.25); s.set_defaults(fn=cmd_bench)
    s = sub.add_parser("new", help="scaffold a new problem module")
    s.add_argument("slug"); s.add_argument("--title", default=""); s.add_argument("--difficulty", default="medium")
    s.add_argument("--tags", default="array"); s.add_argument("--id", type=int, default=0); s.set_defaults(fn=cmd_new)
    s = sub.add_parser("log", help="record a practice session (quality 0-5)")
    s.add_argument("problem"); s.add_argument("--quality", type=int, required=True); s.set_defaults(fn=cmd_log)
    s = sub.add_parser("due", help="problems due for review"); s.set_defaults(fn=cmd_due)
    s = sub.add_parser("stats", help="progress dashboard"); s.set_defaults(fn=cmd_stats)
    s = sub.add_parser("next", help="what to practise next"); s.add_argument("-n", type=int, default=3); s.set_defaults(fn=cmd_next)
    s = sub.add_parser("docs", help="generate / check docs/PROBLEMS.md")
    s.add_argument("--out", default="docs/PROBLEMS.md"); s.add_argument("--check", action="store_true"); s.set_defaults(fn=cmd_docs)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
