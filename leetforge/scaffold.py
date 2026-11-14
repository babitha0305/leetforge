from __future__ import annotations

import re
from pathlib import Path
from typing import List

from . import solutions
from .registry import load_all

TEMPLATE = '''"""__TITLE__"""
META = {"id": __ID__, "title": "__TITLE__", "difficulty": "__DIFF__", "tags": __TAGS__, "pattern": "TODO"}


def brute_force(*args):
    # TODO: simplest correct solution first - it becomes the reference for fuzzing
    raise NotImplementedError


APPROACHES = {"brute_force": brute_force}
COMPLEXITY = {"brute_force": ("O(?)", "O(?)")}
TESTS = [
    # ((arg1, arg2), expected),
]


def gen(n, rng):
    """Worst-case-ish input of size n for `leetforge bench`."""
    raise NotImplementedError


def rand_case(rng):
    """Small random input for `leetforge fuzz`."""
    raise NotImplementedError
'''


def create(slug: str, title: str, difficulty: str, tags: List[str], problem_id: int = 0) -> Path:
    slug = slug.strip().lower().replace("_", "-")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        raise ValueError("slug must look like 'two-sum'")
    path = Path(solutions.__path__[0]) / f"{slug.replace('-', '_')}.py"
    if path.exists():
        raise FileExistsError(path)
    pid = problem_id or (max((p.id for p in load_all()), default=0) + 1)
    text = (TEMPLATE.replace("__TITLE__", title or slug.replace("-", " ").title())
            .replace("__ID__", str(pid)).replace("__DIFF__", difficulty).replace("__TAGS__", repr(tags)))
    path.write_text(text, encoding="utf-8")
    return path
