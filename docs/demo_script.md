# NetSage AI demo script (5–10 minutes)

## 1. Introduce the problem (1 minute)
Explain that the system helps students troubleshoot common Cisco-style networking issues while keeping evidence provenance and a human decision visible.

## 2. Show a sample case (1 minute)
Open a case and point out the symptom, topology note, expected fault, and the evidence badge. State clearly that the current manifest contains 4 verified public-evidence mappings, 21 reference mappings, and 5 pending mappings; the verified public evidence was not independently rerun locally.

## 3. Display evidence and deterministic checks (2 minutes)
Open the Diagnose tab, run the rule checker, and explain that deterministic findings are completely transparent and based on the supplied text.

## 4. Run the Gemini diagnosis (2 minutes)
If a valid local key is configured, click Run Diagnosis and show the AI root cause, confidence, evidence, next command, and fix steps. Emphasize that the output is advisory and tied to supplied evidence. Without a key, show the graceful unavailable message and continue with deterministic findings.

## 5. Human review (2 minutes)
Open the Review tab, accept or edit the diagnosis, and save the review. Explain the required human decision before the output is treated as final.

## 6. Dashboard and final notes (1–2 minutes)
Show the Dashboard and explain total, verified, reference, and pending counts, review distribution, case coverage, and agreement. Close by emphasizing that real lab evidence must replace pending data before final academic use.

## Demo evidence boundary

Do not use the unverified subnet/configuration scenario as a confirmed connectivity failure. If it is mentioned, call it `REFERENCE LAB EVIDENCE — VERIFICATION REQUIRED` and describe only the observed inconsistency.
