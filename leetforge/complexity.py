"""Empirical complexity estimation.

Time the function on inputs of growing size n, then fit  t ~ c * f(n)  for candidate growth models
in log-space and keep the best fit (preferring simpler models on near-ties). This is a sanity check on
your declared Big-O, not a proof: timings are noisy, constants matter, and some classes are practically
indistinguishable (O(1) vs O(log n), O(n) vs O(n log n)) - those are treated as compatible.
"""
from __future__ import annotations

import copy
import math
import random
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence

from .problem import Problem

MODELS = [
    ("O(1)", lambda n: 1.0),
    ("O(log n)", lambda n: math.log2(n)),
    ("O(n)", lambda n: float(n)),
    ("O(n log n)", lambda n: n * math.log2(n)),
    ("O(n^2)", lambda n: float(n) ** 2),
    ("O(n^3)", lambda n: float(n) ** 3),
    ("O(2^n)", lambda n: 2.0 ** n),
]
EQUIVALENT = [{"O(1)", "O(log n)"}, {"O(n)", "O(n log n)"}]
ALIASES = {
    "O(n * 2^n)": "O(2^n)", "O(n*2^n)": "O(2^n)", "O(2^n * n)": "O(2^n)",
    "O(n^2 log n)": "O(n^2)", "O(n + m)": "O(n)", "O(V + E)": "O(n)", "O(n * m)": "O(n)",
    "O(m * n)": "O(n)", "O(n * k)": "O(n)", "O(n log k)": "O(n log n)", "O(amount * coins)": "O(n)",
}


@dataclass
class Estimate:
    label: str
    slope: float
    sizes: List[int] = field(default_factory=list)
    times: List[float] = field(default_factory=list)
    errors: Dict[str, float] = field(default_factory=dict)


def _slope(ns: Sequence[int], ts: Sequence[float]) -> float:
    xs, ys = [math.log(n) for n in ns], [math.log(t) for t in ts]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else 0.0


def fit(sizes: Sequence[int], times: Sequence[float], tolerance: float = 0.005) -> Estimate:
    ns = list(sizes)
    ts = [max(t, 1e-9) for t in times]
    if len(ns) < 4 or min(ns) < 2:
        return Estimate("insufficient data", 0.0, ns, ts)
    errors: Dict[str, float] = {}
    for name, f in MODELS:
        if name == "O(2^n)" and max(ns) > 60:
            continue
        resid = [math.log(t) - math.log(f(n)) for n, t in zip(ns, ts)] if name != "O(1)" else [math.log(t) for t in ts]
        mean = sum(resid) / len(resid)
        errors[name] = sum((r - mean) ** 2 for r in resid) / len(resid)
    best_err = min(errors.values())
    label = next(name for name, _ in MODELS if name in errors and errors[name] <= best_err + tolerance)
    return Estimate(label, _slope(ns, ts), ns, ts, errors)


def compatible(declared: str, estimated: str) -> bool:
    declared = ALIASES.get(declared, declared)
    if declared == estimated:
        return True
    return any(declared in grp and estimated in grp for grp in EQUIVALENT)


def _measure(fn: Callable, args: tuple, min_total: float = 0.003, max_reps: int = 1000) -> float:
    best = math.inf
    for _ in range(3):
        total, reps = 0.0, 0
        while total < min_total and reps < max_reps:
            a = copy.deepcopy(args)          # copy outside the timed region: many solutions mutate input
            t0 = time.perf_counter()
            fn(*a)
            total += time.perf_counter() - t0
            reps += 1
        best = min(best, total / reps)
    return best


def estimate(problem: Problem, approach: str, budget: float = 0.25, max_n: int = 2 ** 16, seed: int = 0) -> Estimate:
    mod = problem.module
    if not hasattr(mod, "gen"):
        return Estimate("no gen()", 0.0)
    sizes = list(getattr(mod, "BENCH_SIZES", [])) or [2 ** k for k in range(8, 17) if 2 ** k <= max_n]
    rng = random.Random(seed)
    fn = problem.approaches[approach]
    used, times = [], []
    for n in sizes:
        t = _measure(fn, mod.gen(n, rng))
        used.append(n)
        times.append(t)
        if t > budget:
            break
    return fit(used, times)
