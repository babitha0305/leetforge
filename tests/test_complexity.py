import random

from leetforge import complexity
from leetforge.complexity import MODELS, compatible, fit
from leetforge.registry import get


def test_fit_recovers_each_growth_class_from_noisy_synthetic_timings():
    rng = random.Random(1)
    for name, f in MODELS:
        sizes = list(range(6, 23, 2)) if name == "O(2^n)" else [2 ** k for k in range(6, 14)]
        times = [1e-9 * f(n) * (1 + rng.uniform(-0.03, 0.03)) for n in sizes]
        est = fit(sizes, times)
        assert est.label == name or compatible(name, est.label), (name, est.label)


def test_distinct_classes_are_not_confused():
    sizes = [2 ** k for k in range(6, 14)]
    assert fit(sizes, [1e-9 * n ** 2 for n in sizes]).label == "O(n^2)"
    assert fit(sizes, [1e-9 * n ** 3 for n in sizes]).label == "O(n^3)"
    assert fit(sizes, [1e-9 * n for n in sizes]).label in ("O(n)", "O(n log n)")


def test_compatible_rules():
    assert compatible("O(n * 2^n)", "O(2^n)")
    assert compatible("O(log n)", "O(1)")
    assert compatible("O(n log n)", "O(n)")
    assert not compatible("O(n)", "O(n^2)")
    assert not compatible("O(n^2)", "O(n^3)")


def test_insufficient_data():
    assert fit([10, 20], [1e-6, 2e-6]).label == "insufficient data"


def test_empirical_estimate_separates_quadratic_from_linear():
    p = get("two-sum")
    brute = complexity.estimate(p, "brute_force", budget=0.1)
    fast = complexity.estimate(p, "hash_map", budget=0.1)
    assert brute.slope > 1.6
    assert fast.slope < 1.4
