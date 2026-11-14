from __future__ import annotations

from types import ModuleType
from typing import Callable, Dict, List, Tuple

DIFFICULTY_ORDER = {"Easy": 0, "Medium": 1, "Hard": 2}


class Problem:
    """Wraps a solution module. A module declares:

    META        dict: id, title, difficulty, tags, pattern
    APPROACHES  dict name -> function (first one should be the simplest/brute-force reference)
    COMPLEXITY  dict name -> (time, space) declared Big-O strings
    TESTS       list of (args_tuple, expected)
    optional:   CHECK(args, out) validator, NORMALIZE(out), gen(n, rng) worst-case input of size n,
                rand_case(rng) small random input for fuzzing, BENCH_SIZES list of n for `bench`
    """

    def __init__(self, module: ModuleType):
        self.module = module

    @property
    def module_name(self) -> str:
        return self.module.__name__

    @property
    def slug(self) -> str:
        return self.module_name.rsplit(".", 1)[-1].replace("_", "-")

    @property
    def meta(self) -> dict:
        return getattr(self.module, "META", {})

    id = property(lambda self: self.meta.get("id", 0))
    title = property(lambda self: self.meta.get("title", self.slug))
    difficulty = property(lambda self: self.meta.get("difficulty", "?"))
    tags = property(lambda self: list(self.meta.get("tags", [])))
    pattern = property(lambda self: self.meta.get("pattern", ""))

    @property
    def approaches(self) -> Dict[str, Callable]:
        return getattr(self.module, "APPROACHES", {})

    @property
    def complexity(self) -> Dict[str, Tuple[str, str]]:
        return getattr(self.module, "COMPLEXITY", {})

    @property
    def tests(self) -> list:
        return getattr(self.module, "TESTS", [])

    def validate(self) -> List[str]:
        errs: List[str] = []
        m = self.meta
        for key in ("id", "title", "difficulty", "tags", "pattern"):
            if key not in m:
                errs.append(f"META missing '{key}'")
        if m.get("difficulty") not in DIFFICULTY_ORDER:
            errs.append(f"difficulty must be one of {list(DIFFICULTY_ORDER)}")
        if not isinstance(m.get("tags", []), list) or not m.get("tags"):
            errs.append("tags must be a non-empty list")
        if not self.approaches or not all(callable(f) for f in self.approaches.values()):
            errs.append("APPROACHES must map names to callables")
        if set(self.complexity) != set(self.approaches):
            errs.append("COMPLEXITY keys must match APPROACHES keys")
        if not self.tests:
            errs.append("TESTS is empty")
        return errs
