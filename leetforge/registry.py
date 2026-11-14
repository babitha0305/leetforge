from __future__ import annotations

import importlib
import pkgutil
from typing import List, Optional

from . import solutions
from .problem import Problem


def load_all() -> List[Problem]:
    probs = []
    for info in pkgutil.iter_modules(solutions.__path__):
        if info.name.startswith("_"):
            continue
        probs.append(Problem(importlib.import_module(f"{solutions.__name__}.{info.name}")))
    return sorted(probs, key=lambda p: p.id)


def get(slug: str) -> Optional[Problem]:
    slug = slug.strip().lower().replace("_", "-")
    for p in load_all():
        if p.slug == slug or str(p.id) == slug:
            return p
    return None
