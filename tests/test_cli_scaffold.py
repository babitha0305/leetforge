import pytest

from leetforge import cli, scaffold


def test_list_and_filters(capsys):
    assert cli.main(["list", "--difficulty", "hard"]) == 0
    out = capsys.readouterr().out
    assert "trapping-rain-water" in out and "two-sum" not in out


def test_test_command(capsys):
    assert cli.main(["test", "two-sum", "--no-isolate"]) == 0
    assert "all passed" in capsys.readouterr().out
    assert cli.main(["test", "does-not-exist"]) == 2


def test_fuzz_command(capsys):
    assert cli.main(["fuzz", "coin-change", "--trials", "50"]) == 0


def test_log_due_next_stats(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("LEETFORGE_HOME", str(tmp_path))
    assert cli.main(["log", "two-sum", "--quality", "5"]) == 0
    assert (tmp_path / "progress.json").exists()
    assert cli.main(["next", "-n", "2"]) == 0
    assert cli.main(["stats"]) == 0
    assert "Solved 1/" in capsys.readouterr().out


def test_docs_generate_and_check(tmp_path, capsys):
    out = tmp_path / "PROBLEMS.md"
    assert cli.main(["docs", "--out", str(out), "--check"]) == 1
    assert cli.main(["docs", "--out", str(out)]) == 0
    assert cli.main(["docs", "--out", str(out), "--check"]) == 0
    out.write_text(out.read_text() + "x")
    assert cli.main(["docs", "--out", str(out), "--check"]) == 1


def test_scaffold_creates_module_and_rejects_bad_slug(tmp_path, monkeypatch):
    import types
    monkeypatch.setattr(scaffold, "solutions", types.SimpleNamespace(__path__=[str(tmp_path)]))
    path = scaffold.create("my-new-problem", "My New Problem", "Medium", ["dp"], 4242)
    text = path.read_text()
    assert path.name == "my_new_problem.py" and '"id": 4242' in text and "'dp'" in text
    compile(text, str(path), "exec")
    with pytest.raises(FileExistsError):
        scaffold.create("my-new-problem", "", "Easy", ["dp"])
    with pytest.raises(ValueError):
        scaffold.create("Bad Slug!", "", "Easy", ["dp"])
