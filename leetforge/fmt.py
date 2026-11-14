from __future__ import annotations

from typing import List, Sequence


def table(headers: Sequence[str], rows: List[Sequence[object]]) -> str:
    cells = [[str(c) for c in r] for r in rows]
    widths = [max(len(h), *(len(r[i]) for r in cells)) if cells else len(h) for i, h in enumerate(headers)]
    fmt = "  ".join("{:<%d}" % w for w in widths)
    out = [fmt.format(*headers), fmt.format(*("-" * w for w in widths))]
    out += [fmt.format(*r) for r in cells]
    return "\n".join(out)
