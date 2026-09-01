from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Any

VALID_SEVERITIES = {"Low", "Medium", "High", "Critical"}
VALID_OSI = {
    "Layer 1",
    "Layer 1/2",
    "Layer 2",
    "Layer 2/3",
    "Layer 3",
    "Layer 3/4",
    "Layer 4",
    "Layer 7",
}
VALID_DECISIONS = {"Accepted", "Edited", "Rejected"}
VALID_EVIDENCE_STATUS = {"VERIFIED", "REFERENCE", "PENDING"}
PLACEHOLDER_PATTERNS = (
    "PLACEHOLDER",
    "REPLACE WITH ACTUAL",
    "REPLACE WITH VERIFIED",
    "REPLACE THIS",
    "VERIFICATION REQUIRED",
    "NOT VERIFIED",
    "TODO",
)


def is_placeholder_evidence(value: Any) -> bool:
    text = str(value or "")
    if not text.strip():
        return False
    normalized = text.upper()
    return any(pattern in normalized for pattern in PLACEHOLDER_PATTERNS)


def evidence_status(row_or_evidence: Any) -> str:
    """Classify evidence without treating reference or pending material as verified."""
    if isinstance(row_or_evidence, dict):
        explicit_status = str(row_or_evidence.get("evidence_status", "")).upper()
        evidence = row_or_evidence.get("evidence_text") or row_or_evidence.get("show_outputs", "")
        if explicit_status in {"REFERENCE", "PENDING"}:
            return explicit_status
        if explicit_status == "VERIFIED" and str(evidence or "").strip() and not is_placeholder_evidence(evidence):
            return "VERIFIED"
        declared_source = str(row_or_evidence.get("evidence_source", "")).upper()
        declared_verified = str(row_or_evidence.get("verified", "")).upper()
    else:
        evidence = row_or_evidence
        declared_source = ""
        declared_verified = ""

    if not str(evidence or "").strip():
        return "PENDING"
    if declared_verified in {"YES", "TRUE", "VERIFIED"} and is_placeholder_evidence(evidence):
        return "PENDING"
    if declared_verified in {"YES", "TRUE", "VERIFIED"} and declared_source not in {"REFERENCE", "DEMO", "DEMO_TEST"}:
        return "VERIFIED"
    if declared_source in {"REFERENCE", "REFERENCE LAB", "REFERENCE LAB EVIDENCE"}:
        return "REFERENCE"
    if is_placeholder_evidence(evidence):
        return "PENDING"
    return "PENDING"


def validate_evidence_csv(file_or_path: Any) -> dict:
    try:
        rows = _read_csv_rows(file_or_path)
    except Exception as exc:
        return {"valid": False, "errors": [f"Could not read CSV: {exc}"], "count": 0}
    if not rows:
        return {"valid": False, "errors": ["Evidence CSV is empty."], "count": 0}
    required = ["case_id", "evidence_status", "source_type", "source_name", "source_url", "local_file", "evidence_reference", "evidence_text", "verification_notes"]
    fieldnames = rows[0].keys() if rows[0] else []
    errors = [f"Missing required evidence columns: {', '.join(name for name in required if name not in fieldnames)}"] if any(name not in fieldnames for name in required) else []
    seen = set()
    for index, row in enumerate(rows, start=2):
        case_id = (row.get("case_id") or "").strip()
        if not case_id or case_id in seen:
            errors.append(f"Row {index}: missing or duplicate case_id")
        seen.add(case_id)
        status = (row.get("evidence_status") or "").strip().upper()
        if status not in VALID_EVIDENCE_STATUS:
            errors.append(f"Row {index}: invalid evidence_status '{status}'")
    expected = {f"CASE{index:03d}" for index in range(1, 31)}
    missing_cases = sorted(expected - seen)
    extra_cases = sorted(seen - expected)
    if missing_cases:
        errors.append(f"Missing case mappings: {', '.join(missing_cases)}")
    if extra_cases:
        errors.append(f"Unexpected case mappings: {', '.join(extra_cases)}")
    return {"valid": not errors, "errors": errors, "count": len(rows)}


def _read_csv_rows(file_or_path: Any):
    if hasattr(file_or_path, "read"):
        text = file_or_path.read()
        if isinstance(text, bytes):
            text = text.decode("utf-8")
        return list(csv.DictReader(io.StringIO(text)))

    path = Path(file_or_path)
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_case_csv(file_or_path: Any) -> dict:
    try:
        rows = _read_csv_rows(file_or_path)
    except Exception as exc:
        return {"valid": False, "errors": [f"Could not read CSV: {exc}"], "warnings": [], "count": 0}

    if not rows:
        return {"valid": False, "errors": ["CSV is empty or missing data rows."], "warnings": [], "count": 0}

    required = [
        "case_id",
        "symptom",
        "topology_note",
        "show_outputs",
        "expected_fault",
        "osi_layer",
        "concept",
        "severity",
    ]
    fieldnames = rows[0].keys() if rows[0] else []
    missing = [name for name in required if name not in fieldnames]
    errors = []
    warnings = []

    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")

    seen = set()
    for index, row in enumerate(rows, start=2):
        case_id = (row.get("case_id") or "").strip()
        if not case_id:
            errors.append(f"Row {index}: missing case_id")
        elif case_id in seen:
            errors.append(f"Row {index}: duplicate case_id '{case_id}'")
        seen.add(case_id)

        for field in ["symptom", "topology_note", "show_outputs", "expected_fault"]:
            if not (row.get(field) or "").strip():
                errors.append(f"Row {index}: missing {field}")

        osi = (row.get("osi_layer") or "").strip()
        if osi and osi not in VALID_OSI:
            errors.append(f"Row {index}: invalid osi_layer '{osi}'")

        severity = (row.get("severity") or "").strip()
        if severity and severity not in VALID_SEVERITIES:
            errors.append(f"Row {index}: invalid severity '{severity}'")

        if is_placeholder_evidence(row.get("show_outputs")):
            warnings.append(f"Row {index}: placeholder evidence should be replaced with verified lab output.")

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "count": len(rows),
    }


def validate_review_csv(file_or_path: Any) -> dict:
    try:
        rows = _read_csv_rows(file_or_path)
    except Exception as exc:
        return {"valid": False, "errors": [f"Could not read CSV: {exc}"], "count": 0}

    if not rows:
        return {"valid": False, "errors": ["Review CSV is empty."], "count": 0}

    required = [
        "case_id",
        "timestamp",
        "ai_root_cause",
        "ai_confidence",
        "human_decision",
        "human_root_cause",
        "human_correction",
        "reviewer_reason",
        "evidence_reference",
    ]
    fieldnames = rows[0].keys() if rows[0] else []
    errors = []
    missing = [name for name in required if name not in fieldnames]
    if missing:
        errors.append(f"Missing required review columns: {', '.join(missing)}")

    for index, row in enumerate(rows, start=2):
        decision = (row.get("human_decision") or "").strip()
        if decision and decision not in VALID_DECISIONS:
            errors.append(f"Row {index}: invalid review decision '{decision}'")

        try:
            value = float((row.get("ai_confidence") or "0").strip())
            if not 0.0 <= value <= 1.0:
                errors.append(f"Row {index}: ai_confidence must be between 0 and 1")
        except ValueError:
            errors.append(f"Row {index}: malformed ai_confidence value")

    return {"valid": not errors, "errors": errors, "count": len(rows)}
