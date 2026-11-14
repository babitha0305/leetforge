from __future__ import annotations

import copy
import importlib
import multiprocessing as mp
import random
import time
from dataclasses import dataclass, field
from typing import Any, List, Optional

from .problem import Problem


@dataclass
class CaseResult:
    index: int
    ok: bool
    ms: float
    error: str = ""


@dataclass
class ApproachResult:
    approach: str
    cases: List[CaseResult] = field(default_factory=list)
    timed_out: bool = False
    crashed: bool = False

    @property
    def passed(self) -> int:
        return sum(c.ok for c in self.cases)

    @property
    def ok(self) -> bool:
        return bool(self.cases) and self.passed == len(self.cases) and not self.timed_out and not self.crashed


def verify(module, args: tuple, out: Any, expected: Any) -> bool:
    """CHECK(args, out) wins if defined; otherwise compare after NORMALIZE."""
    check = getattr(module, "CHECK", None)
    if check is not None:
        return bool(check(args, out))
    norm = getattr(module, "NORMALIZE", None) or (lambda x: x)
    return norm(out) == norm(expected)


def _eval_cases(module_name: str, approach: str) -> List[CaseResult]:
    mod = importlib.import_module(module_name)
    fn = mod.APPROACHES[approach]
    results = []
    for i, (args, expected) in enumerate(mod.TESTS):
        try:
            a = copy.deepcopy(args)
            t0 = time.perf_counter()
            got = fn(*a)
            ms = (time.perf_counter() - t0) * 1000
            ok = verify(mod, copy.deepcopy(args), got, expected)
            results.append(CaseResult(i, ok, ms, "" if ok else f"got {got!r:.80}, expected {expected!r:.80}"))
        except Exception as e:  # noqa: BLE001 - report any user-code failure
            results.append(CaseResult(i, False, 0.0, f"{type(e).__name__}: {e}"))
    return results


def _child(module_name: str, approach: str, conn) -> None:
    try:
        conn.send(_eval_cases(module_name, approach))
    finally:
        conn.close()


def run_approach(problem: Problem, approach: str, isolate: bool = True, timeout: float = 10.0) -> ApproachResult:
    """Run every test for one approach. isolate=True uses a subprocess with a hard timeout."""
    if not isolate:
        return ApproachResult(approach, _eval_cases(problem.module_name, approach))
    recv, send = mp.Pipe(False)
    proc = mp.Process(target=_child, args=(problem.module_name, approach, send))
    proc.start()
    send.close()
    try:
        if recv.poll(timeout):
            try:
                return ApproachResult(approach, recv.recv())
            except EOFError:
                return ApproachResult(approach, crashed=True)
        return ApproachResult(approach, timed_out=True)
    finally:
        if proc.is_alive():
            proc.terminate()
        proc.join()


def run_problem(problem: Problem, isolate: bool = True, timeout: float = 10.0) -> List[ApproachResult]:
    return [run_approach(problem, name, isolate, timeout) for name in problem.approaches]


# ---------------------------------------------------------------- differential fuzzing
@dataclass
class FuzzResult:
    slug: str
    trials: int
    failures: List[str] = field(default_factory=list)
    skipped: Optional[str] = None

    @property
    def ok(self) -> bool:
        return not self.failures


def fuzz_problem(problem: Problem, trials: int = 200, seed: int = 0) -> FuzzResult:
    """Run all approaches on random small inputs and check they agree (or satisfy CHECK)."""
    mod = problem.module
    if not hasattr(mod, "rand_case"):
        return FuzzResult(problem.slug, 0, skipped="no rand_case()")
    check = getattr(mod, "CHECK", None)
    names = list(problem.approaches)
    if check is None and len(names) < 2:
        return FuzzResult(problem.slug, 0, skipped="needs >=2 approaches or CHECK()")
    norm = getattr(mod, "NORMALIZE", None) or (lambda x: x)
    rng = random.Random(seed)
    res = FuzzResult(problem.slug, trials)
    for _ in range(trials):
        args = mod.rand_case(rng)
        outs = {}
        for name, fn in problem.approaches.items():
            try:
                outs[name] = fn(*copy.deepcopy(args))
            except Exception as e:  # noqa: BLE001
                res.failures.append(f"{name} raised {type(e).__name__}: {e} on {args!r:.120}")
        if check is not None:
            for name, out in outs.items():
                if not check(copy.deepcopy(args), out):
                    res.failures.append(f"{name} invalid output {out!r:.60} on {args!r:.120}")
        elif names[0] in outs:
            ref = norm(outs[names[0]])
            for name in names[1:]:
                if name in outs and norm(outs[name]) != ref:
                    res.failures.append(f"{name} disagrees with {names[0]} on {args!r:.120}")
        if len(res.failures) >= 5:
            break
    return res
