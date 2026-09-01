# NetSage AI Final Presentation and Demo Script

**Target duration:** 5-7 minutes

**Demo case:** CASE002, the public wrong-VLAN-assignment scenario. The case is marked `VERIFIED` in the evidence manifest under the project's public-evidence rule because the source provides the broken fault, correction, and inspected failure/success screenshots. It was not independently rerun locally in Packet Tracer.

## 1. Problem Statement - 0:00-0:40

"NetSage AI addresses a common networking-learning problem: a student has a connectivity symptom, a topology description, and Cisco-style diagnostic evidence, but needs a structured way to connect those facts to a likely fault and a safe next step.

The project focuses on troubleshooting scenarios across VLAN, gateway/IP, DHCP, DNS, routing, ACL, NAT/PAT, and wireless networking. The goal is not to replace a network engineer or a human reviewer. The goal is to make troubleshooting evidence easier to organize, interpret, and review."

## 2. Why NetSage AI Is Needed - 0:40-1:10

"A symptom such as 'the PC cannot reach its gateway' can have several causes. It may be an access-port VLAN error, a wrong gateway, a missing SVI, a DHCP problem, or an ACL or routing issue.

NetSage AI brings three useful layers together:

1. Transparent deterministic checks for recognizable network indicators.
2. Optional Gemini reasoning grounded in the supplied case evidence.
3. Mandatory human review before an AI diagnosis is treated as final.

This makes the reasoning auditable instead of presenting an unexplained AI answer."

## 3. System Architecture - 1:10-1:45

[Show the application and briefly point to the tabs.]

"The Streamlit application is `app.py`. It loads the 30 case definitions from `data/cases.csv` and joins them with the evidence and provenance manifest in `data/evidence.csv`.

The supporting modules are:

- `case_loader.py` for normalized case and evidence loading.
- `validators.py` for CSV validation and the shared `VERIFIED`, `REFERENCE`, and `PENDING` status logic.
- `rule_checker.py` for deterministic findings.
- `ai_diagnosis.py` for the optional Gemini call and response validation.
- `review_manager.py` for the human-review audit log.

The five UI areas are Diagnose, Cases, Review, Dashboard, and About."

## 4. Dataset and Evidence Provenance - 1:45-2:20

[Open the Cases or Diagnose tab and show the status/source information.]

"The dataset contains exactly 30 unique cases. Evidence status is deliberately conservative:

- **4 VERIFIED:** supported by explicit public fault/correction evidence and inspected screenshots under the project's evidence rule. These were not independently rerun locally.
- **21 REFERENCE:** legitimate public labs or guides support the networking concept or topology, but do not independently verify the exact case.
- **5 PENDING:** no sufficiently matching evidence was retained.

The case definitions remain separate from the evidence manifest. This prevents an external reference, a placeholder, or a review example from silently becoming verified evidence.

The UI displays the evidence status, source type, source name, URL, evidence reference, and local artifact path when available."

## 5. Deterministic Rule Engine - 2:20-2:55

[Select CASE002 in Diagnose and show Deterministic findings.]

"The deterministic engine analyzes the case input and supplied evidence text. It reports a rule name, status, detected flag, explanation, evidence basis, severity, confidence, and a recommended next command.

The implemented checks cover duplicate IP, wrong subnet mask, gateway mismatch, interface down, missing VLAN, wrong VLAN assignment, missing route, NAT, ACL, and DHCP indicators.

For CASE002, the relevant networking concept is VLAN and gateway reachability. The evidence identifies a switchport assigned to the wrong VLAN and a failed gateway ping. The next diagnostic command is `show interfaces switchport`, alongside `show vlan brief` and a gateway ping when working in the lab."

## 6. Gemini AI Diagnosis - 2:55-3:35

[Click Run Diagnosis only if `GEMINI_API_KEY` is configured.]

"Gemini is optional. Its configuration uses `GEMINI_API_KEY` and `GEMINI_MODEL`; no API key is stored in the project.

The prompt includes the case symptom, topology, evidence text, evidence status, evidence source, and evidence reference. The required response is structured JSON containing `root_cause`, `confidence`, `evidence`, `next_command`, `fix_steps`, `osi_layer`, and `severity`.

If Gemini is unavailable, the application keeps the deterministic findings and displays a graceful unavailable message. If Gemini responds with malformed JSON, missing fields, or a verification claim for `REFERENCE` or `PENDING` evidence, the response is rejected.

For this demo, I will describe any Gemini result as advisory. It is not the final decision and it does not create Packet Tracer evidence."

**No-key fallback:** "Gemini is unavailable in this environment, so I will continue with the deterministic diagnosis. This is an expected supported mode, not an application failure."

## 7. Human Review Workflow - 3:35-4:15

[Show the Review area and the review columns.]

"After diagnosis, the reviewer must choose `Accepted`, `Edited`, or `Rejected`.

A review record preserves:

- case ID and timestamp
- AI root cause and confidence
- human decision
- human root cause and correction
- reviewer reason
- evidence reference
- review source

The project includes five records labeled `DEMO/HUMAN REVIEW EXAMPLES`. They demonstrate accepted, edited, and rejected outcomes, but they are not presented as independent reviews.

For CASE002, a reviewer could accept the VLAN diagnosis if it matches the public evidence, or edit it to clarify the exact switchport and VLAN correction. The saved human decision is the accountable outcome."

## 8. Dashboard - 4:15-4:50

[Open Dashboard.]

"The Dashboard provides the project-level view:

- Total cases: 30
- Verified: 4
- Reference: 21
- Pending: 5
- Review decisions: Accepted, Edited, and Rejected
- AI-human agreement rate
- Case coverage by concept, severity, and OSI layer
- Evidence-status distribution

Reference and pending cases are not counted as verified. This distinction is important for academic integrity and for interpreting the project results."

## 9. Responsible AI Safeguards - 4:50-5:25

[Optionally open About or refer to `docs/responsible_ai.md`.]

"NetSage AI uses several safeguards:

- AI is advisory, not autonomous or final.
- Evidence provenance remains visible.
- Placeholder and missing evidence remain pending.
- Reference material is not silently converted into verified evidence.
- Gemini responses are schema-validated.
- Unverified cases cannot receive an affirmative AI verification claim.
- Human review is mandatory.
- API keys are kept in the ignored local `.env` file.
- The project does not generate synthetic Cisco terminal output or screenshots."

## 10. Complete Case Demonstration: CASE002 - 5:25-6:25

### Input

[In Diagnose, select CASE002.]

"The input is CASE002: a PC in VLAN 20 cannot reach its default gateway. The case topology says the PC is connected to an access switch and the gateway is a router SVI. The expected fault is an access-port VLAN mismatch or gateway/SVI VLAN issue.

The evidence panel identifies this as `VERIFIED LAB EVIDENCE` under the public-evidence rule and shows the public source and local evidence reference. I will also state the limitation: this evidence was inspected from paired public documentation and screenshots, not rerun in this workspace."

### Rules

"The deterministic findings now run from the case and manifest evidence. I use the relevant VLAN checks and the recommended commands, especially `show interfaces switchport`, `show vlan brief`, and `ping 192.168.20.1`.

The evidence supports the narrower diagnosis: the PC's switchport was assigned to the wrong VLAN."

### AI

"If Gemini is available, I click Run Diagnosis. I verify that its evidence references the supplied source material and that it returns the required JSON fields. I do not call it proof of a fix. If Gemini is unavailable, the deterministic result remains available and the workflow continues."

### Human review

"The reviewer compares the AI output with the evidence and chooses a decision. For this demonstration, I show the review interface and explain an `Accepted` decision: the documented correction assigns Gi0/2 to VLAN 20 and the public evidence includes the corrected configuration and successful connectivity screenshots.

If the reviewer needs to narrow or correct the wording, choosing `Edited` stores the human diagnosis separately from the AI diagnosis. `Rejected` is also available when the evidence does not support the AI conclusion."

### Final decision

"The final decision is the human-reviewed result, not the raw AI response. The review record keeps the case ID, decision, correction or reason, evidence reference, and source for auditability."

## 11. Current Limitations - 6:25-6:50

"The project currently has 30 cases, but not all are independently reproduced in Packet Tracer. The honest evidence state is 4 verified public-evidence mappings, 21 reference mappings, and 5 pending mappings.

The four verified mappings meet the project's public-evidence rule through explicit fault/correction documentation and inspected screenshots; they were not locally rerun. The five pending cases remain pending because no sufficiently matching evidence was retained. The rule engine is conservative text analysis, and Gemini depends on API availability and model quota."

## 12. Conclusion - 6:50-7:00

"NetSage AI provides a practical troubleshooting workflow that connects structured cases, evidence provenance, deterministic rules, optional AI assistance, and human accountability.

Its key result is not an inflated verification number. It is a transparent system that clearly distinguishes what is verified, what is reference material, and what still needs evidence."

## Evaluator takeaway

- 30 structured cases are present.
- Coverage includes VLAN, gateway/IP, DHCP, DNS, routing, ACL, NAT/PAT, and wireless.
- Current evidence counts are exactly `4 VERIFIED`, `21 REFERENCE`, and `5 PENDING`.
- The application supports Diagnose, Cases, Review, Dashboard, and About views.
- Gemini is optional and evidence-grounded.
- Human review is mandatory for final decisions.
- No claim is made that all 30 cases are verified.
