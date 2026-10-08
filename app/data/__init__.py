from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from threading import Lock
from typing import Any


@dataclass
class AuditEvent:
    source: str
    timestamp: str
    user: str
    action: str
    result: str
    control_mark: str
    citation: str | None = None


class AuditLogger:
    _instance: "AuditLogger | None" = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.events = []
        return cls._instance

    def log_event(
        self,
        source: str,
        user: str,
        action: str,
        result: str,
        control_mark: str,
        citation: str | None = None,
    ) -> dict[str, Any]:
        event = AuditEvent(
            source=source,
            timestamp=datetime.now(timezone.utc).isoformat(),
            user=user,
            action=action,
            result=result,
            control_mark=control_mark,
            citation=citation,
        )
        self.events.append(asdict(event))
        return asdict(event)

    def get_trail(self) -> list[dict[str, Any]]:
        return list(self.events)
