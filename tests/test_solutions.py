import pytest

from leetforge.registry import get, load_all
from leetforge.runner import fuzz_problem, run_problem

PROBLEMS = load_all()


def test_catalogue_is_valid_and_unique():
    assert len(PROBLEMS) >= 15
    assert len({p.id for p in PROBLEMS}) == len(PROBLEMS)
    assert len({p.slug for p in PROBLEMS}) == len(PROBLEMS)
    for p in PROBLEMS:
        assert p.validate() == [], f"{p.slug}: {p.validate()}"


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda p: p.slug)
def test_all_approaches_pass_examples(problem):
    for r in run_problem(problem, isolate=False):
        assert r.ok, f"{problem.slug}/{r.approach}: {[c.error for c in r.cases if not c.ok]}"


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda p: p.slug)
def test_approaches_agree_under_fuzzing(problem):
    res = fuzz_problem(problem, trials=150, seed=7)
    assert res.ok, res.failures
    assert res.skipped is None, "every bundled problem should support fuzzing"


def test_lookup_by_slug_and_number():
    assert get("two-sum").id == 1
    assert get("1").slug == "two-sum"
    assert get("Two_Sum").slug == "two-sum"
    assert get("nope") is None
