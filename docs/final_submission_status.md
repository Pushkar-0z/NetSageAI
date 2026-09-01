# NetSage AI Final Submission Status

## Project title

NetSage AI: AI-assisted Cisco/Packet Tracer network troubleshooting assistant.

## Problem

Network troubleshooting learners need a structured way to connect symptoms, topology context, command evidence, likely faults, and review decisions across common Cisco-style scenarios.

## Solution

NetSage AI combines a 30-case CSV dataset, evidence provenance manifest, deterministic rule checks, optional Gemini diagnosis, a Streamlit interface, and a human review audit trail.

## Architecture

`app.py` loads cases and evidence, classifies evidence status, presents Diagnose/Cases/Review/Dashboard/About pages, runs deterministic checks, optionally calls Gemini, and saves review records. Supporting modules handle case loading, evidence validation, rule detection, AI response validation, and review persistence.

## Dataset

`data/cases.csv` contains exactly 30 unique case definitions covering VLAN, gateway/IP, DHCP, DNS, routing, ACL, NAT/PAT, and wireless topics. The case definitions were not changed during packaging.

`data/evidence.csv` contains exactly one mapping for each case ID from `CASE001` through `CASE030`.

Current evidence counts:

- `VERIFIED`: 4
- `REFERENCE`: 21
- `PENDING`: 5

The four verified records use explicit public fault/correction material and inspected screenshots. They were not independently rerun locally. Reference records are not treated as verified, and pending records remain visibly pending.

## Evidence methodology

Evidence status is conservative and provenance-driven:

- `VERIFIED` means the evidence manifest identifies direct public fault/correction evidence that meets the project evidence rule.
- `REFERENCE` means a legitimate external lab or guide supports the networking concept or topology but does not independently verify the exact case.
- `PENDING` means no adequate matching evidence was retained.

The UI displays status, source name, URL, evidence reference, and local artifact path. Placeholder case text is never silently promoted to verified evidence.

## AI component

Gemini is optional and configured through `GEMINI_API_KEY` and `GEMINI_MODEL`. The prompt receives the case evidence text, evidence status, source, and reference. Responses are validated as structured JSON containing root cause, confidence, evidence, next command, fix steps, OSI layer, and severity. Gemini is advisory and is prevented from making affirmative verification claims for `REFERENCE` or `PENDING` evidence.

## Rule engine

The deterministic checker provides findings with detected status, explanation, evidence basis, next command, severity, and confidence. It covers duplicate IP, subnet mask, gateway, interface state, missing/wrong VLAN, missing route, NAT, ACL, and DHCP indicators.

## Human review

The workflow supports `Accepted`, `Edited`, and `Rejected`. Reviews store the AI diagnosis, human diagnosis/correction, reason, timestamp, evidence reference, and source. The five existing records are explicitly labeled `DEMO/HUMAN REVIEW EXAMPLES`; they are not presented as independent human reviews.

## Responsible AI

The application keeps evidence provenance visible, distinguishes advisory AI output from human decisions, preserves uncertainty, rejects malformed AI responses, avoids fabricated terminal output, protects API keys, and never counts reference or pending material as verified.

## Limitations

The workspace contains public `.pkt`/`.pka` artifacts and supporting documentation, but Packet Tracer binary files were not independently rerun locally. The four verified records therefore rely on the documented public-evidence rule and inspected source screenshots. Five cases remain pending because no sufficiently matching evidence was found. The internal checklist's 30+ verified-cases item is labeled as an internal quality goal; it is not an official Cisco/EdCreate/course requirement found in the workspace.

## Test result

```text
.venv\\Scripts\\python.exe -m pytest -q
22 passed
```

Streamlit startup smoke test passed at `http://localhost:8506`.

Packaging checks passed for:
- all five Streamlit pages
- evidence counts and unique mappings
- review CSV schema
- evidence CSV schema
- valid local evidence paths
- public source URLs
- `.env` exclusion
- no real API key in `.env.example`
- documented broken/reference case -> deterministic diagnosis -> optional Gemini -> human review -> dashboard/provenance workflow

## Current status

The implementation and evidence package are ready for submission under the official requirements available in the workspace. The internal 30+ verified-cases quality goal remains incomplete, but it is clearly labeled as internal and does not alter the official requirement assessment.

SUBMISSION READY
