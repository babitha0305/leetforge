import multiprocessing as mp
import sys
import time
import types

import pytest

from leetforge.problem import Problem
from leetforge.registry import get
from leetforge.runner import fuzz_problem, run_approach, verify


def _module(name, approaches, tests, **extra):
    m = types.ModuleType(name)
    m.META = {"id": 999, "title": name, "difficulty": "Easy", "tags": ["x"], "pattern": "x"}
    m.APPROACHES = approaches
    m.COMPLEXITY = {k: ("O(1)", "O(1)") for k in approaches}
    m.TESTS = tests
    for k, v in extra.items():
        setattr(m, k, v)
    sys.modules[name] = m
    return m


def test_isolated_run_passes():
    r = run_approach(get("two-sum"), "hash_map", isolate=True)
    assert r.ok and r.passed == len(r.cases)


def test_wrong_answer_and_exception_are_reported():
    m = _module("fake_wrong", {"bad": lambda x: x + 1, "boom": lambda x: 1 / 0}, [((1,), 5)])
    p = Problem(m)
    bad = run_approach(p, "bad", isolate=False)
    boom = run_approach(p, "boom", isolate=False)
    assert not bad.ok and "expected" in bad.cases[0].error
    assert not boom.ok and "ZeroDivisionError" in boom.cases[0].error


@pytest.mark.skipif(mp.get_start_method() != "fork", reason="needs fork start method")
def test_timeout_kills_runaway_solution():
    m = _module("fake_slow", {"slow": lambda: time.sleep(30)}, [((), None)])
    t0 = time.time()
    r = run_approach(Problem(m), "slow", isolate=True, timeout=0.5)
    assert r.timed_out and not r.ok and time.time() - t0 < 5


def test_solution_cannot_mutate_shared_test_data():
    m = _module("fake_mutator", {"a": lambda xs: (xs.pop(), 1)[1]}, [(([1, 2],), 1), (([1, 2],), 1)])
    assert run_approach(Problem(m), "a", isolate=False).ok
    assert m.TESTS[0][0][0] == [1, 2]


def test_check_overrides_equality():
    m = _module("fake_check", {"a": lambda x: x}, [((1,), 123)], CHECK=lambda args, out: out == args[0])
    assert verify(m, (1,), 1, 123)


def test_fuzzing_catches_a_buggy_optimisation():
    ref = lambda xs: sorted(xs)
    buggy = lambda xs: sorted(set(xs))                     # drops duplicates
    m = _module("fake_buggy", {"ref": ref, "buggy": buggy}, [(([1],), [1])],
                rand_case=lambda rng: ([rng.randint(0, 3) for _ in range(6)],))
    res = fuzz_problem(Problem(m), trials=50)
    assert not res.ok and "buggy disagrees" in res.failures[0]


def test_fuzz_skips_when_no_reference():
    m = _module("fake_single", {"a": lambda x: x}, [((1,), 1)], rand_case=lambda rng: (1,))
    assert fuzz_problem(Problem(m)).skipped
