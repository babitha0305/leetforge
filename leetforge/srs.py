"""SM-2 spaced repetition (the SuperMemo-2 algorithm) for problem review scheduling."""
from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Optional


class Scheduler:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.data: Dict[str, dict] = {}
        if self.path.exists():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2, sort_keys=True), encoding="utf-8")

    def log(self, slug: str, quality: int, today: Optional[date] = None) -> dict:
        """Record a review. quality: 0-5 (0 blackout ... 3 correct with effort ... 5 perfect recall)."""
        if not 0 <= quality <= 5:
            raise ValueError("quality must be between 0 and 5")
        today = today or date.today()
        card = self.data.setdefault(slug, {"ease": 2.5, "interval": 0, "reps": 0, "due": today.isoformat(), "history": []})
        if quality < 3:                      # failed recall: restart the ladder, keep ease
            card["reps"], card["interval"] = 0, 1
        else:
            if card["reps"] == 0:
                card["interval"] = 1
            elif card["reps"] == 1:
                card["interval"] = 6
            else:
                card["interval"] = round(card["interval"] * card["ease"])
            card["reps"] += 1
            card["ease"] = round(max(1.3, card["ease"] + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)), 4)
        card["due"] = (today + timedelta(days=card["interval"])).isoformat()
        card["history"].append([today.isoformat(), quality])
        return card

    def due(self, today: Optional[date] = None) -> List[str]:
        today = today or date.today()
        return [s for s, _ in sorted(((s, c["due"]) for s, c in self.data.items() if c["due"] <= today.isoformat()),
                                     key=lambda x: x[1])]

    def streak(self, today: Optional[date] = None) -> int:
        """Consecutive days (ending today, or yesterday if nothing logged yet today) with at least one review."""
        today = today or date.today()
        days = {d for c in self.data.values() for d, _ in c["history"]}
        cur = today if today.isoformat() in days else today - timedelta(days=1)
        n = 0
        while cur.isoformat() in days:
            n += 1
            cur -= timedelta(days=1)
        return n
