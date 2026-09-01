from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

DEFAULT_REVIEW_PATH = Path(__file__).resolve().parents[1] / "data" / "review_log.csv"

REQUIRED_COLUMNS = [
    "case_id",
    "timestamp",
    "ai_root_cause",
    "ai_confidence",
    "human_decision",
    "human_root_cause",
    "human_correction",
    "reviewer_reason",
    "evidence_reference",
    "review_source",
]


def load_reviews(path: str | Path | None = None) -> pd.DataFrame:
    review_path = Path(path) if path else DEFAULT_REVIEW_PATH
    if not review_path.exists():
        return pd.DataFrame(columns=REQUIRED_COLUMNS)
    try:
        df = pd.read_csv(review_path)
    except Exception:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df


def save_review(record: dict[str, Any], path: str | Path | None = None) -> pd.DataFrame:
    review_path = Path(path) if path else DEFAULT_REVIEW_PATH
    review_path.parent.mkdir(parents=True, exist_ok=True)

    normalized = {
        "case_id": str(record.get("case_id", "")).strip(),
        "timestamp": record.get("timestamp") or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ai_root_cause": str(record.get("ai_root_cause", "")).strip(),
        "ai_confidence": record.get("ai_confidence", 0.0),
        "human_decision": str(record.get("human_decision", "")).strip(),
        "human_root_cause": str(record.get("human_root_cause", "")).strip(),
        "human_correction": str(record.get("human_correction", "")).strip(),
        "reviewer_reason": str(record.get("reviewer_reason", "")).strip(),
        "evidence_reference": str(record.get("evidence_reference", "")).strip(),
        "review_source": str(record.get("review_source", "real")).strip() or "real",
    }

    if review_path.exists():
        df = pd.read_csv(review_path)
    else:
        df = pd.DataFrame(columns=REQUIRED_COLUMNS)

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df = pd.concat([df, pd.DataFrame([normalized])], ignore_index=True)
    df = df[REQUIRED_COLUMNS]
    df.to_csv(review_path, index=False)
    return df


def make_demo_reviews(path: str | Path | None = None) -> pd.DataFrame:
    demo_rows = [
        {
            "case_id": "CASE003",
            "timestamp": "2026-08-25T09:00:00Z",
            "ai_root_cause": "Wrong default gateway configuration",
            "ai_confidence": 0.81,
            "human_decision": "Edited",
            "human_root_cause": "Default gateway missing on DHCP scope",
            "human_correction": "AI missed the DHCP scope default gateway issue",
            "reviewer_reason": "The DHCP pool used the wrong gateway address.",
            "review_source": "demo_test",
        },
        {
            "case_id": "CASE009",
            "timestamp": "2026-08-25T09:05:00Z",
            "ai_root_cause": "Missing route to remote network",
            "ai_confidence": 0.86,
            "human_decision": "Accepted",
            "human_root_cause": "Missing route to remote network",
            "human_correction": "No change",
            "reviewer_reason": "Route absence matched the observed evidence.",
            "review_source": "demo_test",
        },
        {
            "case_id": "CASE012",
            "timestamp": "2026-08-25T09:10:00Z",
            "ai_root_cause": "Trunk VLAN mismatch",
            "ai_confidence": 0.72,
            "human_decision": "Rejected",
            "human_root_cause": "Allowed VLAN list missing on trunk",
            "human_correction": "AI over-attributed the issue to a trunk encapsulation mismatch.",
            "reviewer_reason": "The actual evidence showed the missing VLAN in trunk allowed list.",
            "review_source": "demo_test",
        },
        {
            "case_id": "CASE020",
            "timestamp": "2026-08-25T09:15:00Z",
            "ai_root_cause": "Access-list denies HTTP",
            "ai_confidence": 0.75,
            "human_decision": "Edited",
            "human_root_cause": "ACL blocks TCP 80 to the web server",
            "human_correction": "AI did not specify that the deny rule matched HTTP traffic.",
            "reviewer_reason": "Evidence showed the ACL sequence had a deny for TCP 80.",
            "review_source": "demo_test",
        },
        {
            "case_id": "CASE024",
            "timestamp": "2026-08-25T09:20:00Z",
            "ai_root_cause": "Wireless VLAN DHCP path is misconfigured",
            "ai_confidence": 0.79,
            "human_decision": "Accepted",
            "human_root_cause": "Wireless VLAN DHCP path is misconfigured",
            "human_correction": "No change",
            "reviewer_reason": "The DHCP scope and wireless access VLAN matched the diagnosis.",
            "review_source": "demo_test",
        },
    ]

    for row in demo_rows:
        row["evidence_reference"] = f"{row['case_id']}: PENDING case evidence"
        row["review_source"] = "DEMO/HUMAN REVIEW EXAMPLES"

    review_path = Path(path) if path else DEFAULT_REVIEW_PATH
    review_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(demo_rows, columns=REQUIRED_COLUMNS)
    df.to_csv(review_path, index=False)
    return df
