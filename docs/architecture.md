# NetSage AI architecture

## Overview
NetSage AI is a Python-first troubleshooting assistant for Cisco-style networking labs. It combines deterministic checks with Gemini-assisted reasoning and human review.

## Pipeline
1. User enters a symptom, topology note, and evidence.
2. The deterministic rule checker scans the evidence for common issues.
3. The AI diagnosis module calls Gemini only when a key is configured.
4. The UI presents AI and rule findings side by side.
5. Human reviewers accept, reject, or edit the final output.
6. Review results are saved to the CSV audit log.

## Modules
- app.py: Streamlit entry point and UI.
- src/case_loader.py: dataset loading and normalization.
- src/rule_checker.py: deterministic networking checks.
- src/ai_diagnosis.py: prompt construction, JSON parsing, and Gemini integration.
- src/review_manager.py: review save/load helpers.
- src/validators.py: CSV validation and guard checks.

## Evidence status

`src/validators.py` owns the shared evidence classification used by loading and the UI:

- `VERIFIED` requires explicit verification and non-reference provenance.
- `REFERENCE` identifies reference-lab material that still needs reproduction.
- `PENDING` covers placeholders, missing evidence, and unverified scenarios.

## Data and safety

- Demonstrations use pending or explicitly labeled demo material until Packet Tracer output is verified.
- The app never claims a fix is confirmed without human review and evidence.
- The default workflow keeps AI advisory and preserves deterministic findings if Gemini is unavailable.
- Secrets are read from the local ignored `.env` file and are not stored in case data or documentation.
