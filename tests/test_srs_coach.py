from datetime import date, timedelta

import pytest

from leetforge import coach, stats
from leetforge.registry import load_all
from leetforge.srs import Scheduler

D0 = date(2026, 1, 1)


def test_sm2_interval_ladder(tmp_path):
    s = Scheduler(tmp_path / "p.json")
    assert s.log("a", 5, D0)["interval"] == 1
    assert s.log("a", 5, D0 + timedelta(days=1))["interval"] == 6
    third = s.log("a", 5, D0 + timedelta(days=7))
    assert third["interval"] == round(6 * 2.6) and third["ease"] > 2.5


def test_failure_resets_but_keeps_ease(tmp_path):
    s = Scheduler(tmp_path / "p.json")
    s.log("a", 4, D0)
    s.log("a", 4, D0 + timedelta(days=1))
    ease = s.data["a"]["ease"]
    card = s.log("a", 1, D0 + timedelta(days=7))
    assert card["interval"] == 1 and card["reps"] == 0 and card["ease"] == ease


def test_ease_never_below_floor_and_quality_validated(tmp_path):
    s = Scheduler(tmp_path / "p.json")
    for i in range(30):
        s.log("a", 3, D0 + timedelta(days=i))
    assert s.data["a"]["ease"] >= 1.3
    with pytest.raises(ValueError):
        s.log("a", 6)


def test_due_and_persistence(tmp_path):
    path = tmp_path / "p.json"
    s = Scheduler(path)
    s.log("a", 5, D0)
    s.save()
    again = Scheduler(path)
    assert again.due(D0) == []
    assert again.due(D0 + timedelta(days=1)) == ["a"]


def test_streak(tmp_path):
    s = Scheduler(tmp_path / "p.json")
    for i in range(3):
        s.log("a", 4, D0 + timedelta(days=i))
    assert s.streak(D0 + timedelta(days=2)) == 3
    assert s.streak(D0 + timedelta(days=3)) == 3      # yesterday still counts
    assert s.streak(D0 + timedelta(days=5)) == 0


def test_coach_prefers_due_then_weak_topics(tmp_path):
    problems = load_all()
    s = Scheduler(tmp_path / "p.json")
    s.log("two-sum", 5, D0)                            # strong on array / hash-table
    picks = coach.suggest(problems, s, D0 + timedelta(days=1), n=3)
    assert picks[0] == ("two-sum", "due for review")
    new = [slug for slug, _ in picks[1:]]
    assert "two-sum" not in new and len(new) == 2


def test_coach_untouched_tags_beat_strong_tags(tmp_path):
    problems = load_all()
    s = Scheduler(tmp_path / "p.json")
    scores = coach.tag_scores(problems, s)
    assert set(scores.values()) == {0.0}
    s.log("two-sum", 5, D0)
    scores = coach.tag_scores(problems, s)
    assert scores["array"] == 5.0 and scores["graph"] == 0.0


def test_stats_render(tmp_path):
    s = Scheduler(tmp_path / "p.json")
    s.log("two-sum", 4, D0)
    s.log("coin-change", 2, D0)                        # attempted but not solved
    out = stats.render(load_all(), s, D0)
    assert "Solved 1/" in out and "streak 1" in out and "Easy" in out
