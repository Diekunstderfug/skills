"""One resumable retrieval: atomic snapshots, buffered records and provenance."""
from __future__ import annotations

import json
import math
import os
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from _common import Reconciliation


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Progress:
    api: str
    query: str
    next_state: Any
    records: list[dict] = field(default_factory=list)
    buffered: list[dict] = field(default_factory=list)
    reconciliation: Reconciliation = field(default_factory=Reconciliation)
    urls: list[str] = field(default_factory=list)
    exhausted: bool = False
    last_page_at: float | None = None
    started_at: str = field(default_factory=timestamp)
    status: str = "running"
    delay: float = 0.0
    retry_not_before: float | None = None
    events: list[dict] = field(default_factory=list)

    def event(self, kind: str, **details: Any) -> None:
        self.events.append({"time": timestamp(), "type": kind, **details})

    def envelope(self) -> dict:
        self.reconciliation.retrieved = len(self.records)
        counts = self.reconciliation.as_dict()
        if self.status == "running":
            counts["complete"] = False
            if "shortfall" in counts:
                counts["shortfall_reason"] = "retrieval in progress"
        return {
            "api": self.api, "query": self.query, "status": self.status,
            "started_at": self.started_at, "updated_at": timestamp(),
            "provenance": {"urls": self.urls, "delay_seconds": self.delay,
                           "requests_made": len(self.urls)},
            "reconciliation": counts, "records": self.records, "events": self.events,
            "checkpoint": {"version": 1, "next_state": self.next_state,
                           "buffered_records": self.buffered, "exhausted": self.exhausted,
                           "last_page_at": self.last_page_at, "retry_not_before": self.retry_not_before},
        }

    def save(self, destination: str | Path | None) -> None:
        if destination is None:
            return
        target = Path(destination)
        target.parent.mkdir(parents=True, exist_ok=True)
        name = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=target.parent,
                                             prefix="." + target.name + ".", delete=False) as f:
                name = f.name
                json.dump(self.envelope(), f, ensure_ascii=False, indent=2, allow_nan=False)
                f.write("\n")
                f.flush()
                os.fsync(f.fileno())
            os.replace(name, target)
        finally:
            if name and os.path.exists(name):
                os.unlink(name)

    @classmethod
    def load(cls, path: str | Path) -> Progress:
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            c = data["checkpoint"]
            r = data["reconciliation"]
            provenance = data["provenance"]
            if type(c["version"]) is not int or c["version"] != 1:
                raise ValueError("unsupported checkpoint version")
            for rows in (data["records"], c["buffered_records"]):
                if not isinstance(rows, list) or not all(isinstance(x, dict) for x in rows):
                    raise ValueError("invalid records")
            for value in (r["pages_fetched"], r["retrieved_total"]):
                if type(value) is not int or value < 0:
                    raise ValueError("invalid count")
            total = r["expected_total"]
            if total is not None and (type(total) is not int or total < 0):
                raise ValueError("invalid total")
            if r["retrieved_total"] != len(data["records"]):
                raise ValueError("record count does not match checkpoint")
            if not isinstance(provenance["urls"], list) or not all(isinstance(x, str) for x in provenance["urls"]):
                raise ValueError("invalid request history")
            if type(c["exhausted"]) is not bool or c["exhausted"] != (c["next_state"] is None):
                raise ValueError("inconsistent cursor state")
            if not isinstance(data["api"], str) or not isinstance(data["query"], str):
                raise ValueError("missing API or query")
            for key in ("last_page_at", "retry_not_before"):
                val = c.get(key)
                if val is not None and (type(val) not in (int, float) or not math.isfinite(val) or val < 0):
                    raise ValueError("invalid checkpoint timestamp")
            events = data.get("events", [])
            if not isinstance(events, list) or not all(isinstance(x, dict) for x in events):
                raise ValueError("invalid event log")
            notes = r.get("notes", [])
            if not isinstance(notes, list) or not all(isinstance(x, str) for x in notes):
                raise ValueError("invalid reconciliation notes")
            delay = provenance["delay_seconds"]
            if type(delay) not in (int, float) or not math.isfinite(delay) or delay < 0:
                raise ValueError("invalid request pacing")
            return cls(api=data["api"], query=data["query"], next_state=c["next_state"],
                       records=data["records"], buffered=c["buffered_records"],
                       reconciliation=Reconciliation(expected=total, pages=r["pages_fetched"],
                           retrieved=len(data["records"]), notes=notes),
                       urls=provenance["urls"], exhausted=c["exhausted"],
                       last_page_at=c.get("last_page_at"), started_at=data["started_at"],
                       retry_not_before=c.get("retry_not_before"), events=events, delay=delay)
        except (OSError, ValueError, KeyError, TypeError) as e:
            raise RuntimeError(f"cannot load checkpoint {path}: {e}") from e
