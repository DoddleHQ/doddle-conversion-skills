"""The evidence envelope: the single JSON shape every command emits."""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

CURRENT = "CURRENT"
PARTIAL = "PARTIAL"
STALE = "STALE"

DETERMINISTIC = "deterministic"
HEURISTIC = "heuristic"
LIVE = "live"
ADVISORY = "advisory"

TIERS = [(85, "Excellent"), (70, "Good"), (55, "Fair"), (40, "Weak"), (0, "Critical")]


def tier_for(score: Optional[float]) -> str:
    if score is None:
        return "Not scored"
    for floor, label in TIERS:
        if score >= floor:
            return label
    return "Critical"


def utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class Signal:
    id: str
    value: Optional[float]
    max: float
    klass: str = DETERMINISTIC
    detail: Dict[str, Any] = field(default_factory=dict)
    skipped_reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "value": self.value, "max": self.max, "class": self.klass,
                "detail": self.detail, "skipped_reason": self.skipped_reason}


@dataclass
class Finding:
    id: str
    priority: int
    severity: str
    effort: str
    points_lost: float
    title: str
    detail: str
    pages: List[str] = field(default_factory=list)
    excerpt: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def make_envelope(command: str, target: str, *, toolkit_version: str, scoring_version: str,
                  data_version: str, evidence_stamp: str = CURRENT, pages_ok: int = 1,
                  pages_failed: Optional[List[Dict[str, Any]]] = None,
                  notes: Optional[List[str]] = None, categories: Optional[Dict[str, float]] = None,
                  missing: Optional[List[str]] = None, signal_count: int = 0,
                  signal_total: int = 0, scores: Optional[Dict[str, Any]] = None,
                  signals: Optional[List[Signal]] = None, findings: Optional[List[Finding]] = None,
                  error: Optional[Dict[str, str]] = None, **kw: Any) -> Dict[str, Any]:
    findings = sorted(findings or [], key=lambda f: (f.priority, -f.points_lost))
    for i, f in enumerate(findings, start=1):
        f.priority = i
    out = {
        "ok": error is None,
        "command": command,
        "target": target,
        "generated_at": utc_now(),
        "toolkit_version": toolkit_version,
        "scoring_version": scoring_version,
        "data_version": data_version,
        "evidence": {"stamp": evidence_stamp, "pages_ok": pages_ok,
                     "pages_failed": pages_failed or [], "notes": notes or []},
        "completeness": {"signals": f"{signal_count}/{signal_total}" if signal_total else "0/0",
                         "categories": categories or {}, "missing": missing or []},
        "scores": scores,
        "signals": [s.to_dict() for s in (signals or [])],
        "findings": [f.to_dict() for f in findings],
        "error": error,
    }
    out.update(kw)
    return out
