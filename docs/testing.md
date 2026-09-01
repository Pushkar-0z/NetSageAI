# Testing

Run tests with the project interpreter:

```powershell
.venv\Scripts\python.exe -m pytest -q
```

The suite covers:
- loading all 30 cases and validating the evidence manifest
- placeholder and evidence-status classification
- case CSV validation
- duplicate IP, gateway, interface, VLAN, route, and subnet-mask rules
- malformed Gemini JSON and missing API key behavior
- review save/load behavior
- evidence-aware case filtering/status behavior

Run the Streamlit smoke check with:

```powershell
.venv\Scripts\streamlit.exe run app.py --server.headless true --server.port 8501
```

The app must start without a traceback. The current evidence manifest should produce 30 total cases, 4 verified, 21 reference, and 5 pending. The verified count reflects the public-evidence rule documented in `data/evidence.csv`; it does not claim local Packet Tracer reproduction.

## Evidence test policy

Tests validate code behavior and schema only. They do not turn scenario text into lab evidence. A case becomes `VERIFIED` only when actual command output is added, its provenance is documented, and `verified` is set to `YES` after independent reproduction.
