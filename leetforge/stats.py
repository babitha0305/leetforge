from __future__ import annotations

from collections import Counter
from datetime import date
from typing import List, Optional

from .coach import tag_scores
from .fmt import table
from .problem import Problem
from .srs import Scheduler


def render(problems: List[Problem], sched: Scheduler, today: Optional[date] = None) -> str:
    today = today or date.today()
    by_slug = {p.slug: p for p in problems}
    attempted = [s for s in sched.data if s in by_slug]
    solved = [s for s in attempted if max(q for _, q in sched.data[s]["history"]) >= 3]
    total = Counter(p.difficulty for p in problems)
    done = Counter(by_slug[s].difficulty for s in solved)
    rows = [[d, f"{done[d]}/{total[d]}"] for d in ("Easy", "Medium", "Hard") if total[d]]
    lines = [f"Solved {len(solved)}/{len(problems)}  |  streak {sched.streak(today)} day(s)  |  due today {len(sched.due(today))}", ""]
    lines.append(table(["Difficulty", "Solved"], rows))
    scores = tag_scores(problems, sched)
    weakest = sorted(scores.items(), key=lambda kv: (kv[1], kv[0]))[:5]
    lines += ["", "Weakest topics (avg latest quality, 0 = untouched):",
              table(["Tag", "Score"], [[t, f"{s:.1f}"] for t, s in weakest])]
    return "\n".join(lines)
