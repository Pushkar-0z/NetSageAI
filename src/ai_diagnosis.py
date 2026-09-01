from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "diagnose_prompt.md"

REQUIRED_FIELDS = {
    "root_cause",
    "confidence",
    "evidence",
    "next_command",
    "fix_steps",
    "osi_layer",
    "severity",
}
UNVERIFIED_CLAIM_PATTERNS = ("is verified", "was verified", "verified as", "confirmed", "successfully fixed", "proven")


def require_api_key() -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or not api_key.strip():
        raise ValueError("GEMINI_API_KEY is missing. Add it to your .env file before running Gemini diagnosis.")
    return api_key.strip()


def parse_ai_response(raw: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(raw, dict):
        payload = raw
    else:
        text = (raw or "").strip()
        if not text:
            raise ValueError("AI response was empty.")
        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"AI response was malformed JSON: {exc}") from exc

    missing = sorted(REQUIRED_FIELDS - set(payload.keys()))
    if missing:
        raise ValueError(f"AI response missing required keys: {', '.join(missing)}")

    confidence = float(payload.get("confidence", -1))
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("AI response confidence must be between 0 and 1.")

    if not isinstance(payload.get("evidence", []), list) or not payload["evidence"]:
        raise ValueError("AI response evidence must be a non-empty list.")
    if not isinstance(payload.get("fix_steps", []), list) or not payload["fix_steps"]:
        raise ValueError("AI response fix_steps must be a non-empty list.")

    return payload


def validate_response_schema(payload: dict[str, Any]) -> bool:
    required = ["root_cause", "confidence", "evidence", "next_command", "fix_steps", "osi_layer", "severity"]
    if not isinstance(payload, dict):
        return False
    if any(key not in payload for key in required):
        return False
    if not isinstance(payload["evidence"], list):
        return False
    if not isinstance(payload["fix_steps"], list):
        return False
    try:
        conf = float(payload["confidence"])
    except (TypeError, ValueError):
        return False
    return 0.0 <= conf <= 1.0


def enforce_evidence_boundary(payload: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    status = str(case.get("evidence_status", "PENDING")).upper()
    if status == "VERIFIED":
        return payload
    fields = [payload.get("root_cause", ""), *payload.get("evidence", []), *payload.get("fix_steps", [])]
    claims = [str(value).lower() for value in fields]
    if any(pattern in value for value in claims for pattern in UNVERIFIED_CLAIM_PATTERNS):
        raise ValueError(f"AI response made a verification claim for {status} evidence.")
    return payload


def build_prompt(case: dict[str, Any]) -> str:
    prompt_text = PROMPT_PATH.read_text(encoding="utf-8")
    details = f"""
CASE ID: {case.get('case_id', '')}
SYMPTOM: {case.get('symptom', '')}
TOPOLOGY: {case.get('topology_note', '')}
SHOW OUTPUTS: {case.get('evidence_text') or case.get('show_outputs', '')}
EVIDENCE STATUS: {case.get('evidence_status', 'PENDING')}
EVIDENCE SOURCE: {case.get('evidence_source', '')}
EVIDENCE REFERENCE: {case.get('evidence_reference', '')}
CONCEPT: {case.get('concept', '')}
SEVERITY: {case.get('severity', '')}
"""
    return prompt_text + "\n\nReturn JSON only with the required fields.\n" + details


def diagnose_with_gemini(case: dict[str, Any]) -> dict[str, Any]:
    require_api_key()

    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise RuntimeError("google-genai is not installed. Install the project requirements first.") from exc

    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    client = genai.Client(api_key=require_api_key())
    response = client.models.generate_content(
        model=model_name,
        contents=build_prompt(case),
        config=types.GenerateContentConfig(temperature=0.2, response_mime_type="application/json"),
    )
    try:
        text = getattr(response, "text", None) or ""
        parsed = parse_ai_response(text)
        if not validate_response_schema(parsed):
            raise ValueError("AI response shape is invalid.")
        return enforce_evidence_boundary(parsed, case)
    except Exception as exc:
        raise ValueError(f"The model returned an unusable diagnosis: {exc}") from exc


if __name__ == "__main__":
    print("Use diagnose_with_gemini(case) from the Streamlit app.")
