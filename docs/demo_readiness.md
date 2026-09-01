# NetSage AI Demo Readiness

## 1. Recommended primary demo case

Use **CASE002: PC in VLAN 20 cannot reach its default gateway**.

This is the strongest primary demonstration because its evidence manifest maps to a public broken/fixed VLAN-assignment lab. The source documents the wrong access VLAN, failed gateway reachability, the corrected switchport assignment, and successful connectivity screenshots. The evidence is marked `VERIFIED` under the project's public-evidence rule, but it was not locally rerun in Packet Tracer.

## 2. Exact case-selection sequence

1. Start the app with `streamlit run app.py`.
2. Open the **Diagnose** page, which is the first tab.
3. In **Choose a case**, select `CASE002`.
4. Keep the selected case visible while discussing its symptom, topology, evidence status, and deterministic findings.
5. If Gemini is available, click **Run Diagnosis** after reviewing the evidence.
6. Use the displayed human-review controls to demonstrate an `Accepted`, `Edited`, or `Rejected` decision.
7. Open **Review** to show the audit records.
8. Open **Dashboard** to show current evidence and review metrics.

## 3. What should be visible on the Diagnose page

The evaluator should see:

- Case ID `CASE002` selected.
- Symptom: the PC in VLAN 20 cannot reach its default gateway.
- Topology: the PC is connected to an access switch and the gateway is a router SVI.
- Concept: VLAN/Gateway.
- OSI layer: Layer 2/3.
- Severity: High.
- Evidence status: `VERIFIED LAB EVIDENCE`.
- The public source name, source URL, evidence reference, and local artifact path.
- The evidence limitation that the public material was not independently rerun locally.
- Deterministic findings below the case and evidence sections.

The status label must be read together with its provenance. `VERIFIED` here means verified under the documented public-evidence rule, not locally reproduced by this project.

## 4. Deterministic finding to notice

The evaluator should focus on the VLAN-related finding: the supplied evidence indicates an access-port VLAN assignment problem. The recommended investigation is:

```text
show interfaces switchport
show vlan brief
ping 192.168.20.1
```

Explain that the rule engine is transparent and evidence-oriented. It identifies the likely wrong VLAN condition and recommends the smallest useful verification commands; it does not change the switch configuration.

## 5. Demonstrating evidence and provenance

On the Diagnose page, point to:

- The `VERIFIED LAB EVIDENCE` status label.
- The public source name and clickable source URL.
- The evidence reference describing the broken and fixed lab material.
- The local evidence artifact path.
- The evidence text and the note that the source was not rerun locally.

Explain the three project statuses:

- `VERIFIED`: direct public fault/correction evidence is attached under the project rule.
- `REFERENCE`: a legitimate external lab supports the scenario but does not verify the exact case.
- `PENDING`: adequate evidence was not found.

Make clear that the separate `data/evidence.csv` manifest supplies provenance and that the original case definitions remain in `data/cases.csv`.

## 6. Demonstrating Gemini when the API is available

1. Confirm the sidebar says Gemini is configured without displaying the API key.
2. With `CASE002` selected, click **Run Diagnosis**.
3. Show the structured response fields:
   - `root_cause`
   - `confidence`
   - `evidence`
   - `next_command`
   - `fix_steps`
   - `osi_layer`
   - `severity`
4. Explain that the prompt includes the case evidence text, evidence status, source, and evidence reference.
5. Emphasize that Gemini is advisory and that its response is not the final decision.
6. Continue to the human-review controls rather than treating the AI response as approved automatically.

Do not imply that a successful API response proves the network fix. The AI reasons from supplied material; it does not operate Packet Tracer.

## 7. What to do when Gemini quota is unavailable

If Gemini returns a 429, `RESOURCE_EXHAUSTED`, quota, or rate-limit error, show the concise message:

> AI diagnosis is temporarily unavailable because the Gemini API quota has been reached. Deterministic findings remain available.

Continue the demonstration using the deterministic findings for CASE002. Explain that this is an expected graceful-degradation path. Do not retry repeatedly, display the raw Google API payload, or pretend that Gemini produced a diagnosis.

For any other Gemini failure, show the short unavailable message and continue with deterministic findings. The technical exception is kept in the developer logger.

## 8. Demonstrating the Review page

Open **Review** and point out:

- The visible `DEMO/HUMAN REVIEW EXAMPLES` notice.
- The five existing records.
- The `Accepted`, `Edited`, and `Rejected` decisions.
- The AI diagnosis and confidence.
- The human diagnosis, correction, reviewer reason, evidence reference, and review source.

Explain that these records demonstrate the review workflow only. They are not independent human evaluations. During a live diagnosis, the reviewer must choose a decision; an edited or rejected decision requires a correction or reason.

## 9. Demonstrating the Dashboard

Open **Dashboard** and show the metric row:

- Total cases: `30`
- Verified: `4`
- Reference: `21`
- Pending: `5`

Then show:

- Accepted: `2`
- Edited: `2`
- Rejected: `1`
- AI-human agreement: `40%`
- Evidence-status chart.
- Concept, severity, and OSI-layer charts.

Explain that the Dashboard counts come from the evidence manifest and review log. Reference and pending cases are not counted as verified.

## 10. Exact 5-7 minute demo timeline

| Time | Demonstration |
|---|---|
| 0:00-0:40 | Introduce the problem: structured, evidence-aware troubleshooting for Cisco-style network cases. |
| 0:40-1:20 | Explain why NetSage AI combines deterministic rules, optional Gemini, provenance, and human review. |
| 1:20-2:00 | Select `CASE002` and explain the symptom, topology, concept, OSI layer, severity, and expected VLAN fault. |
| 2:00-2:45 | Show the evidence status, source, URL, evidence reference, local artifact, and public-evidence limitation. |
| 2:45-3:30 | Show deterministic findings and the recommended `show interfaces switchport`, `show vlan brief`, and ping checks. |
| 3:30-4:20 | Run Gemini if available; show the structured advisory response. If quota is unavailable, show the concise fallback and continue. |
| 4:20-5:10 | Demonstrate human review, including how an Accepted, Edited, or Rejected decision is recorded. |
| 5:10-6:00 | Open Review and show the labeled demo examples and audit fields. |
| 6:00-6:45 | Open Dashboard and explain the evidence counts, review counts, agreement rate, and charts. |
| 6:45-7:00 | Close with limitations and the distinction between public evidence, reference material, pending cases, and local reproduction. |

## 11. Expected current metrics

```text
Total cases: 30
VERIFIED: 4
REFERENCE: 21
PENDING: 5
Review records: 5
AI-human agreement: 40%
```

These are the expected current values. They must not be altered for the presentation.

## 12. Claims that must NOT be made

Do not claim:

- That all 30 cases are verified.
- That the public evidence was locally rerun in Packet Tracer.
- That Gemini is deterministic.
- That Gemini output is final without human review.
- That demo review records are independent human evaluations.
- That a source URL or `.pkt`/`.pka` file alone proves the exact case fault.
- That a reference or pending case is verified.
- That the application automatically changes router or switch configuration.
- That a successful AI response proves a network fix.

The accurate closing statement is: NetSage AI provides a transparent troubleshooting workflow for 30 structured cases, with `4 VERIFIED`, `21 REFERENCE`, and `5 PENDING` evidence records, optional Gemini assistance, and human review before final decisions.
