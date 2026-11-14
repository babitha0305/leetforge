from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import Dict, List, Optional, Tuple

from .problem import DIFFICULTY_ORDER, Problem
from .srs import Scheduler


def tag_scores(problems: List[Problem], sched: Scheduler) -> Dict[str, float]:
    """Mean of the latest review quality per tag; tags never practised score 0 (so they get priority)."""
    by_slug = {p.slug: p for p in problems}
    seen = defaultdict(list)
    for slug, card in sched.data.items():
        if slug in by_slug and card["history"]:
            for tag in by_slug[slug].tags:
                seen[tag].append(card["history"][-1][1])
    scores = {tag: 0.0 for p in problems for tag in p.tags}
    for tag, vals in seen.items():
        scores[tag] = sum(vals) / len(vals)
    return scores


def suggest(problems: List[Problem], sched: Scheduler, today: Optional[date] = None, n: int = 3) -> List[Tuple[str, str]]:
    """Return [(slug, reason)]: due reviews first, then new problems from your weakest topics."""
    today = today or date.today()
    known = {p.slug for p in problems}
    out: List[Tuple[str, str]] = [(s, "due for review") for s in sched.due(today) if s in known]
    if len(out) >= n:
        return out[:n]
    scores = tag_scores(problems, sched)
    fresh = [p for p in problems if p.slug not in sched.data]

    def weakness(p: Problem) -> float:
        return sum(scores[t] for t in p.tags) / len(p.tags)

    fresh.sort(key=lambda p: (weakness(p), DIFFICULTY_ORDER[p.difficulty], p.id))
    for p in fresh[: n - len(out)]:
        weakest = min(p.tags, key=lambda t: scores[t])
        out.append((p.slug, f"new - strengthens '{weakest}' ({p.difficulty})"))
    return out
