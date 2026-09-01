from __future__ import annotations

import pandas as pd
from pathlib import Path

try:
    from .validators import evidence_status
except ImportError:
    from validators import evidence_status


def load_cases(csv_path: str | Path | None = None) -> pd.DataFrame:
    """Load and normalize the case dataset, returning a dataframe even for partial/corrupt data."""
    if csv_path is None:
        csv_path = Path(__file__).resolve().parents[1] / "data" / "cases.csv"
    path = Path(csv_path)
    if not path.exists():
        return pd.DataFrame()

    try:
        df = pd.read_csv(path)
    except Exception:
        return pd.DataFrame()

    if df.empty:
        return df

    required = {
        "case_id",
        "symptom",
        "topology_note",
        "show_outputs",
        "expected_fault",
        "osi_layer",
        "concept",
        "severity",
    }
    for col in required:
        if col not in df.columns:
            df[col] = ""

    df["case_id"] = df["case_id"].fillna("").astype(str)
    df["symptom"] = df["symptom"].fillna("").astype(str)
    df["topology_note"] = df["topology_note"].fillna("").astype(str)
    df["show_outputs"] = df["show_outputs"].fillna("").astype(str)
    df["expected_fault"] = df["expected_fault"].fillna("").astype(str)
    df["osi_layer"] = df["osi_layer"].fillna("").astype(str)
    df["concept"] = df["concept"].fillna("").astype(str)
    df["severity"] = df["severity"].fillna("").astype(str)
    if "verified" not in df.columns:
        df["verified"] = "NO"
    if "evidence_source" not in df.columns:
        df["evidence_source"] = "Demo"
    if "review_status" not in df.columns:
        df["review_status"] = "Pending"
    df["evidence_status"] = df.apply(lambda row: evidence_status(row.to_dict()), axis=1)
    return df


def load_evidence(csv_path: str | Path | None = None) -> pd.DataFrame:
    if csv_path is None:
        csv_path = Path(__file__).resolve().parents[1] / "data" / "evidence.csv"
    path = Path(csv_path)
    if not path.exists():
        return pd.DataFrame()
    try:
        df = pd.read_csv(path).fillna("")
    except Exception:
        return pd.DataFrame()
    if "case_id" in df.columns:
        df["case_id"] = df["case_id"].astype(str)
    return df


def get_case_by_id(df: pd.DataFrame, case_id: str) -> dict | None:
    if df.empty:
        return None
    match = df[df["case_id"].astype(str).str.lower() == str(case_id).lower()]
    if match.empty:
        return None
    return match.iloc[0].to_dict()
