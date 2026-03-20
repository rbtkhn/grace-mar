#!/usr/bin/env python3
"""
Enforced workflow state for the work-politics territory (WORK lane).

Persists clients, engagements, an operator review queue, and funnel events in SQLite.
Does not write SELF, EVIDENCE, or prompt — companion still uses RECURSION-GATE and
process_approved_candidates for Record updates. Optional approved_candidate_id on
review rows links to a CANDIDATE-* id after a gate merge.

No external deps beyond stdlib.
"""

from __future__ import annotations

import json
import re
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple

UTC = timezone.utc

TERRITORY = "work-politics"

# Align with docs/skill-work/work-politics/README.md channel_key table + generic artifact slugs.
CHANNEL_PATTERNS = [
    re.compile(r"^operator:wap:us-[a-z0-9-]+$"),
    re.compile(r"^operator:wap:us-state-[a-z0-9-]+-[a-z0-9-]+$"),
    re.compile(r"^operator:wap:us-local-[a-z0-9-]+-[a-z0-9-]+-[a-z0-9-]+$"),
    re.compile(r"^operator:wap:intl-[a-z0-9-]+-[a-z0-9-]+$"),
    re.compile(r"^operator:wap:[a-z0-9]+(?:-[a-z0-9]+)*$"),  # generic slug / artifact (e.g. iran-brief)
]


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _slug(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def validate_channel_key(channel_key: str) -> bool:
    return any(p.match(channel_key) for p in CHANNEL_PATTERNS)


def classify_jurisdiction(channel_key: str) -> str:
    if channel_key.startswith("operator:wap:intl-"):
        return "international"
    if channel_key.startswith("operator:wap:us-local-"):
        return "us_local"
    if channel_key.startswith("operator:wap:us-state-"):
        return "us_state"
    return "us_federal"


@dataclass
class PolicyDecision:
    allowed: bool
    reason: str
    requires_review: bool = False


class WorkPoliticsError(Exception):
    pass


class PolicyViolation(WorkPoliticsError):
    pass


class NotFound(WorkPoliticsError):
    pass


def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {k: row[k] for k in row.keys()}


class WorkPoliticsEngine:
    def __init__(self, user_id: str = "grace-mar", repo_root: Optional[Path] = None) -> None:
        self.user_id = (user_id or "grace-mar").strip() or "grace-mar"
        self.repo_root = Path(repo_root or Path(__file__).resolve().parents[1])
        self.base_dir = self.repo_root / "users" / self.user_id / "work-politics"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.base_dir / "work-politics.db"

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def init_db(self) -> None:
        with self.connect() as conn:
            conn.executescript(
                """
                PRAGMA foreign_keys = ON;

                CREATE TABLE IF NOT EXISTS wp_clients (
                    client_id TEXT PRIMARY KEY,
                    client_slug TEXT NOT NULL UNIQUE,
                    display_name TEXT NOT NULL,
                    channel_key TEXT NOT NULL UNIQUE,
                    jurisdiction TEXT NOT NULL,
                    territory TEXT NOT NULL DEFAULT 'work-politics',
                    principal_type TEXT NOT NULL,
                    active INTEGER NOT NULL DEFAULT 1,
                    compliance_status TEXT NOT NULL DEFAULT 'pending',
                    compliance_reviewed_at TEXT,
                    compliance_reviewer TEXT,
                    notes_json TEXT NOT NULL DEFAULT '{}',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS wp_engagements (
                    engagement_id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    work_type TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'draft',
                    public_attribution INTEGER NOT NULL DEFAULT 0,
                    record_touch INTEGER NOT NULL DEFAULT 0,
                    candidate_id TEXT,
                    created_by TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    metadata_json TEXT NOT NULL DEFAULT '{}',
                    FOREIGN KEY (client_id) REFERENCES wp_clients(client_id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS wp_review_queue (
                    review_id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL,
                    engagement_id TEXT,
                    queue_type TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    surface TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    created_by TEXT NOT NULL,
                    reviewed_by TEXT,
                    review_note TEXT,
                    approved_candidate_id TEXT,
                    created_at TEXT NOT NULL,
                    reviewed_at TEXT,
                    FOREIGN KEY (client_id) REFERENCES wp_clients(client_id) ON DELETE CASCADE,
                    FOREIGN KEY (engagement_id) REFERENCES wp_engagements(engagement_id) ON DELETE SET NULL
                );

                CREATE TABLE IF NOT EXISTS wp_funnel_events (
                    event_id TEXT PRIMARY KEY,
                    client_id TEXT,
                    engagement_id TEXT,
                    stage TEXT NOT NULL,
                    outcome TEXT,
                    source TEXT,
                    amount_usd REAL,
                    event_ts TEXT NOT NULL,
                    notes_json TEXT NOT NULL DEFAULT '{}',
                    FOREIGN KEY (client_id) REFERENCES wp_clients(client_id) ON DELETE SET NULL,
                    FOREIGN KEY (engagement_id) REFERENCES wp_engagements(engagement_id) ON DELETE SET NULL
                );

                CREATE INDEX IF NOT EXISTS idx_wp_clients_channel_key ON wp_clients(channel_key);
                CREATE INDEX IF NOT EXISTS idx_wp_clients_compliance_status ON wp_clients(compliance_status);
                CREATE INDEX IF NOT EXISTS idx_wp_engagements_client_status ON wp_engagements(client_id, status);
                CREATE INDEX IF NOT EXISTS idx_wp_review_queue_status ON wp_review_queue(status, surface);
                CREATE INDEX IF NOT EXISTS idx_wp_funnel_stage_ts ON wp_funnel_events(stage, event_ts);
                """
            )

    def _new_id(self, prefix: str) -> str:
        return f"{prefix}-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"

    def create_or_update_client(
        self,
        *,
        client_slug: str,
        display_name: str,
        channel_key: str,
        principal_type: str,
        compliance_status: str = "pending",
        reviewed_by: Optional[str] = None,
        notes: Optional[Dict[str, Any]] = None,
        active: bool = True,
    ) -> str:
        if not validate_channel_key(channel_key):
            raise PolicyViolation(f"invalid work-politics channel_key: {channel_key}")

        jurisdiction = classify_jurisdiction(channel_key)
        client_slug = _slug(client_slug)
        now = utc_now_iso()
        notes_json = json.dumps(notes or {}, sort_keys=True)

        with self.connect() as conn:
            existing = conn.execute(
                "SELECT client_id FROM wp_clients WHERE client_slug = ?",
                (client_slug,),
            ).fetchone()

            if existing:
                client_id = existing["client_id"]
                conn.execute(
                    """
                    UPDATE wp_clients
                    SET display_name = ?, channel_key = ?, jurisdiction = ?, principal_type = ?,
                        active = ?, compliance_status = ?, compliance_reviewed_at = ?,
                        compliance_reviewer = ?, notes_json = ?, updated_at = ?
                    WHERE client_id = ?
                    """,
                    (
                        display_name.strip(),
                        channel_key,
                        jurisdiction,
                        principal_type.strip(),
                        1 if active else 0,
                        compliance_status,
                        now if reviewed_by else None,
                        reviewed_by,
                        notes_json,
                        now,
                        client_id,
                    ),
                )
                return client_id

            client_id = self._new_id("WPC")
            conn.execute(
                """
                INSERT INTO wp_clients (
                    client_id, client_slug, display_name, channel_key, jurisdiction,
                    principal_type, active, compliance_status, compliance_reviewed_at,
                    compliance_reviewer, notes_json, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    client_id,
                    client_slug,
                    display_name.strip(),
                    channel_key,
                    jurisdiction,
                    principal_type.strip(),
                    1 if active else 0,
                    compliance_status,
                    now if reviewed_by else None,
                    reviewed_by,
                    notes_json,
                    now,
                    now,
                ),
            )
            return client_id

    def _get_client(self, client_id: str) -> sqlite3.Row:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM wp_clients WHERE client_id = ?",
                (client_id,),
            ).fetchone()
        if not row:
            raise NotFound(f"client not found: {client_id}")
        return row

    def _policy_for_engagement(
        self,
        *,
        client: sqlite3.Row,
        public_attribution: bool,
        record_touch: bool,
    ) -> PolicyDecision:
        if client["territory"] != TERRITORY:
            return PolicyDecision(False, "client territory mismatch")

        if not client["active"]:
            return PolicyDecision(False, "client is inactive")

        compliance_status = client["compliance_status"]

        if compliance_status != "cleared":
            return PolicyDecision(
                False,
                f"client compliance_status={compliance_status}; clear compliance before engagement",
            )

        if record_touch:
            return PolicyDecision(
                True,
                "allowed, but any Record-touching work must go through review queue",
                requires_review=True,
            )

        if public_attribution:
            return PolicyDecision(
                True,
                "allowed, but public-facing work must go through review queue",
                requires_review=True,
            )

        return PolicyDecision(True, "allowed")

    def submit_engagement(
        self,
        *,
        client_id: str,
        title: str,
        work_type: str,
        created_by: str,
        public_attribution: bool = False,
        record_touch: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Tuple[str, PolicyDecision]:
        client = self._get_client(client_id)
        decision = self._policy_for_engagement(
            client=client,
            public_attribution=public_attribution,
            record_touch=record_touch,
        )
        if not decision.allowed:
            raise PolicyViolation(decision.reason)

        now = utc_now_iso()
        engagement_id = self._new_id("WPE")

        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO wp_engagements (
                    engagement_id, client_id, title, work_type, status,
                    public_attribution, record_touch, candidate_id,
                    created_by, created_at, updated_at, metadata_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    engagement_id,
                    client_id,
                    title.strip(),
                    work_type.strip(),
                    "pending_review" if decision.requires_review else "active",
                    1 if public_attribution else 0,
                    1 if record_touch else 0,
                    None,
                    created_by.strip(),
                    now,
                    now,
                    json.dumps(metadata or {}, sort_keys=True),
                ),
            )

        if decision.requires_review:
            queue_type = "public_ship" if public_attribution else "record_touch"
            surface = "ACT" if record_touch else "PUBLIC_OUTPUT"
            self.enqueue_review(
                client_id=client_id,
                engagement_id=engagement_id,
                queue_type=queue_type,
                surface=surface,
                summary=f"{title.strip()} [{work_type.strip()}]",
                payload={
                    "title": title.strip(),
                    "work_type": work_type.strip(),
                    "public_attribution": public_attribution,
                    "record_touch": record_touch,
                    "metadata": metadata or {},
                },
                created_by=created_by,
            )

        return engagement_id, decision

    def enqueue_review(
        self,
        *,
        client_id: str,
        engagement_id: Optional[str],
        queue_type: str,
        surface: str,
        summary: str,
        payload: Dict[str, Any],
        created_by: str,
    ) -> str:
        self._get_client(client_id)
        now = utc_now_iso()
        review_id = self._new_id("WPR")

        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO wp_review_queue (
                    review_id, client_id, engagement_id, queue_type, status, surface,
                    summary, payload_json, created_by, created_at
                )
                VALUES (?, ?, ?, ?, 'pending', ?, ?, ?, ?, ?)
                """,
                (
                    review_id,
                    client_id,
                    engagement_id,
                    queue_type.strip(),
                    surface.strip(),
                    summary.strip(),
                    json.dumps(payload, sort_keys=True),
                    created_by.strip(),
                    now,
                ),
            )
        return review_id

    def list_review_queue(
        self,
        *,
        status: str = "pending",
        client_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        sql = """
            SELECT q.*, c.display_name, c.channel_key, c.jurisdiction
            FROM wp_review_queue q
            JOIN wp_clients c ON c.client_id = q.client_id
            WHERE q.status = ?
        """
        params: List[Any] = [status]
        if client_id:
            sql += " AND q.client_id = ?"
            params.append(client_id)
        sql += " ORDER BY q.created_at ASC"

        with self.connect() as conn:
            rows = conn.execute(sql, tuple(params)).fetchall()

        out: List[Dict[str, Any]] = []
        for r in rows:
            d = _row_to_dict(r)
            payload_raw = d.pop("payload_json")
            d["payload"] = json.loads(payload_raw)
            out.append(d)
        return out

    def approve_review(
        self,
        *,
        review_id: str,
        reviewed_by: str,
        approved_candidate_id: Optional[str] = None,
        review_note: Optional[str] = None,
    ) -> None:
        now = utc_now_iso()
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM wp_review_queue WHERE review_id = ?",
                (review_id,),
            ).fetchone()
            if not row:
                raise NotFound(f"review item not found: {review_id}")
            if row["status"] != "pending":
                raise PolicyViolation(f"review item already {row['status']}")

            conn.execute(
                """
                UPDATE wp_review_queue
                SET status = 'approved',
                    reviewed_by = ?, review_note = ?, approved_candidate_id = ?,
                    reviewed_at = ?
                WHERE review_id = ?
                """,
                (
                    reviewed_by.strip(),
                    review_note,
                    approved_candidate_id,
                    now,
                    review_id,
                ),
            )

            if row["engagement_id"]:
                conn.execute(
                    """
                    UPDATE wp_engagements
                    SET status = 'approved', candidate_id = ?, updated_at = ?
                    WHERE engagement_id = ?
                    """,
                    (approved_candidate_id, now, row["engagement_id"]),
                )

    def reject_review(
        self,
        *,
        review_id: str,
        reviewed_by: str,
        review_note: str,
    ) -> None:
        if not review_note.strip():
            raise PolicyViolation("rejection requires review_note")

        now = utc_now_iso()
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM wp_review_queue WHERE review_id = ?",
                (review_id,),
            ).fetchone()
            if not row:
                raise NotFound(f"review item not found: {review_id}")
            if row["status"] != "pending":
                raise PolicyViolation(f"review item already {row['status']}")

            conn.execute(
                """
                UPDATE wp_review_queue
                SET status = 'rejected',
                    reviewed_by = ?, review_note = ?, reviewed_at = ?
                WHERE review_id = ?
                """,
                (reviewed_by.strip(), review_note.strip(), now, review_id),
            )

            if row["engagement_id"]:
                conn.execute(
                    """
                    UPDATE wp_engagements
                    SET status = 'rejected', updated_at = ?
                    WHERE engagement_id = ?
                    """,
                    (now, row["engagement_id"]),
                )

    def log_funnel_event(
        self,
        *,
        stage: str,
        outcome: Optional[str] = None,
        source: Optional[str] = None,
        client_id: Optional[str] = None,
        engagement_id: Optional[str] = None,
        amount_usd: Optional[float] = None,
        notes: Optional[Dict[str, Any]] = None,
        event_ts: Optional[str] = None,
    ) -> str:
        if client_id:
            self._get_client(client_id)

        event_id = self._new_id("WPF")
        ts = event_ts or utc_now_iso()

        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO wp_funnel_events (
                    event_id, client_id, engagement_id, stage, outcome, source,
                    amount_usd, event_ts, notes_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event_id,
                    client_id,
                    engagement_id,
                    stage.strip(),
                    (outcome or "").strip() or None,
                    (source or "").strip() or None,
                    amount_usd,
                    ts,
                    json.dumps(notes or {}, sort_keys=True),
                ),
            )
        return event_id

    def funnel_metrics(self, *, days: int = 30) -> Dict[str, Any]:
        cutoff_dt = datetime.now(UTC) - timedelta(days=int(days))
        cutoff = cutoff_dt.replace(microsecond=0).isoformat()

        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT stage, outcome, COUNT(*) AS n, COALESCE(SUM(amount_usd), 0) AS revenue
                FROM wp_funnel_events
                WHERE event_ts >= ?
                GROUP BY stage, outcome
                ORDER BY stage, outcome
                """,
                (cutoff,),
            ).fetchall()

        by_stage: Dict[str, Dict[str, Any]] = {}
        total_revenue = 0.0
        for row in rows:
            stage = row["stage"]
            outcome = row["outcome"] or "_none"
            by_stage.setdefault(stage, {"total": 0, "outcomes": {}, "revenue": 0.0})
            by_stage[stage]["total"] += int(row["n"])
            by_stage[stage]["outcomes"][outcome] = int(row["n"])
            rev = float(row["revenue"] or 0.0)
            by_stage[stage]["revenue"] += rev
            total_revenue += rev

        return {
            "window_days": days,
            "stages": by_stage,
            "total_revenue_usd": round(total_revenue, 2),
        }


if __name__ == "__main__":
    import os
    import sys

    uid = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"
    engine = WorkPoliticsEngine(user_id=uid)
    engine.init_db()
    print(f"initialized {engine.db_path}", file=sys.stderr)
