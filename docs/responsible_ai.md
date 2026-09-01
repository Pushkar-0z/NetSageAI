# Responsible AI and review policy

## 1. Human oversight
The diagnosis is advisory, not final. A reviewer must explicitly accept, edit, or reject the AI output before it is treated as a final decision.

## 2. Confidence and uncertainty
AI confidence is reported as a numeric value between 0 and 1. Low-confidence results show a warning in the UI and the model is asked to explain uncertainty.

## 3. Evidence-based reasoning
The model reasons only from the symptom, topology note, and supplied evidence. It must not invent missing commands, topology details, or verified states.

## 4. No fabricated evidence
All placeholder, reference, and missing lab outputs are clearly labeled. The app uses `VERIFIED`, `REFERENCE`, and `PENDING` statuses and never counts reference or pending evidence as verified. No synthetic terminal transcript or screenshot is generated.

## 5. Safe troubleshooting recommendations
The system prefers narrow diagnostic commands before destructive configuration changes. It recommends human review for uncertain or high-risk cases.

## 6. Auditability
The review log records case ID, timestamp, AI output, decision, and review reason. This supports AI-human agreement analysis and accountability.

## 7. Privacy and secrets handling
API keys are stored only in the local .env file and never committed to the repository. Screenshots, logs, source code, and git history must not contain secrets.

## 8. AI-vs-human agreement
The dashboard reports accepted, edited, and rejected decisions. Agreement is calculated as accepted decisions divided by all recorded decisions. Demo/test review records are labeled `demo_test` and are examples, not independent reviews.

## 9. Correction examples

The five rows in `data/review_log.csv` are `DEMO/HUMAN REVIEW EXAMPLES`. They demonstrate accepted, edited, and rejected outcomes, but do not prove that another person reviewed the cases.
