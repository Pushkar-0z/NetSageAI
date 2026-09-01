# 🛜 NetSage AI

**AI-Assisted Network Troubleshooting Assistant with Deterministic Checks and Human Review**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.62.0-FF4B4B.svg)](https://streamlit.io/)
[![Google GenAI](https://img.shields.io/badge/Google%20GenAI-Gemini%202.5%20Flash-4285F4.svg)](https://ai.google.dev/)
[![Pytest Passed](https://img.shields.io/badge/tests-22%20passed-brightgreen.svg)](tests/test_core.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Repository Structure](#-repository-structure)
- [Case Library & Lab Topologies](#-case-library--lab-topologies)
- [Evidence Provenance & Classification](#-evidence-provenance--classification)
- [Deterministic Rule Engine](#-deterministic-rule-engine)
- [AI Diagnosis with Gemini](#-ai-diagnosis-with-gemini)
- [Human Review & Responsible AI](#-human-review--responsible-ai)
- [Interactive Dashboard](#-interactive-dashboard)
- [Getting Started & Installation](#-getting-started--installation)
  - [Prerequisites](#prerequisites)
  - [Automated Windows Setup](#automated-windows-setup)
  - [Manual Setup (Windows / macOS / Linux)](#manual-setup-windows--macos--linux)
  - [Environment Configuration](#environment-configuration)
- [Running the Application](#-running-the-application)
- [Testing & Quality Assurance](#-testing--quality-assurance)
- [Documentation Guide](#-documentation-guide)
- [Limitations & Ethical Boundaries](#-limitations--ethical-boundaries)

---

## 📖 Overview

**NetSage AI** is an educational, AI-assisted network troubleshooting platform designed for Cisco CCNA and Cisco Packet Tracer environments. It bridges the gap between chaotic network symptoms, raw terminal CLI outputs, transparent deterministic rule checks, structured Google Gemini AI reasoning, and accountable human oversight.

### The Problem
During lab experiments and network troubleshooting, learners frequently encounter scattered CLI show commands, misconfigured routing tables, subnet mismatches, and ambiguous link failures. Students either guess randomly or rely on generic AI chatbots that hallucinate non-existent commands or claim unverified fixes.

### The NetSage AI Solution
1. **Case Normalization**: Structures symptoms, topology notes, and CLI show command outputs into standardized case schemas.
2. **Transparent Deterministic Analysis**: 10 purpose-built rule checkers instantly inspect outputs for fundamental L1–L7 network defects.
3. **Evidence-Grounded AI Advisory**: Google Gemini provides root cause hypotheses, confidence scores, next diagnostic commands, and remediation steps—grounded strictly in the provided evidence.
4. **Mandatory Human-in-the-Loop Review**: Decisions (*Accepted*, *Edited*, *Rejected*) and audit trails are captured before any diagnosis is finalized.

```
+-----------------------------------------------------------------------------------+
|                                   NetSage AI                                      |
+-----------------------------------------------------------------------------------+
|  [Case / Symptom / CLI Evidence]                                                  |
|                |                                                                  |
|                +---> [Deterministic Rule Engine]  ---> [Transparent Findings]     |
|                |                                                                  |
|                +---> [Google Gemini 2.5 Flash]    ---> [AI Advisory Diagnosis]    |
|                                                                  |                |
|  [Human Engineer Review (Accept / Edit / Reject)] <--------------+                |
|                |                                                                  |
|                v                                                                  |
|  [Immutable CSV Audit Log & Performance Dashboard]                                |
+-----------------------------------------------------------------------------------+
```

---

## ✨ Key Features

- **30 Structured CCNA Troubleshooting Cases**: Comprehensive test library spanning 8 core networking domains (VLANs, Gateway/IP Addressing, DHCP, DNS, Static/Dynamic Routing, Physical/Logical Interfaces, ACLs, NAT/PAT, and Wireless).
- **Hybrid Diagnostic Engine**: Combines transparent deterministic regex/subnet parsing with probabilistic Large Language Model reasoning.
- **Strict Evidence Boundaries**: Strict 3-tier evidence tracking (`VERIFIED`, `REFERENCE`, `PENDING`) to prevent fabricated outputs or synthetic hallucinated claims.
- **Audited Human Review Workflow**: Reviewers can approve, edit, or reject AI diagnoses with mandatory rationale logging to evaluate AI-human agreement.
- **Live Streamlit Control Center**: Five rich tabs: *Diagnose*, *Cases*, *Review*, *Dashboard*, and *About*.
- **Offline & Graceful Fallback**: The deterministic rule engine and complete UI operate 100% locally without requiring an active internet connection or Gemini API key.

---

## 🏗️ System Architecture

NetSage AI is built with a modular, maintainable Python architecture:

```
+--------------------------------------------------------------------------------+
|                             Streamlit UI (app.py)                              |
+--------------------------------------------------------------------------------+
     |                    |                     |                     |
     v                    v                     v                     v
[case_loader.py]   [rule_checker.py]    [ai_diagnosis.py]     [review_manager.py]
  - load_cases()     - 10 core checks     - build_prompt()      - load_reviews()
  - load_evidence()  - subnet/IP logic    - Gemini 2.5 Flash    - save_review()
  - normalize df     - confidence rating  - schema validator    - make_demo_reviews()
     |                    |                     |                     |
     +--------------------+---------------------+---------------------+
                                  |
                                  v
                          [validators.py]
                            - validate_case_csv()
                            - validate_evidence_csv()
                            - validate_review_csv()
                            - evidence_status()
```

### Module Breakdown

| Module | Purpose |
|---|---|
| [`app.py`](file:///c:/Users/MD%20FAIYAZ%20KHAN/OneDrive/Documents/Desktop/NetSageAI/app.py) | Streamlit application entry point, custom UI styles, tabs, reactive state, and presentation layer. |
| [`src/case_loader.py`](file:///c:/Users/MD%20FAIYAZ%20KHAN/OneDrive/Documents/Desktop/NetSageAI/src/case_loader.py) | Loads and normalizes cases and evidence manifests into strongly typed Pandas DataFrames. |
| [`src/rule_checker.py`](file:///c:/Users/MD%20FAIYAZ%20KHAN/OneDrive/Documents/Desktop/NetSageAI/src/rule_checker.py) | Pure deterministic Python network rule engine evaluating IP, VLAN, subnet, gateway, route, interface, ACL, NAT, and DHCP patterns. |
| [`src/ai_diagnosis.py`](file:///c:/Users/MD%20FAIYAZ%20KHAN/OneDrive/Documents/Desktop/NetSageAI/src/ai_diagnosis.py) | Interacts with Google GenAI SDK (`google-genai`), builds structured prompts, validates strict JSON schemas, and enforces evidence boundaries. |
| [`src/review_manager.py`](file:///c:/Users/MD%20FAIYAZ%20KHAN/OneDrive/Documents/Desktop/NetSageAI/src/review_manager.py) | Handles human review lifecycle, demo review initialization, and append-only CSV persistence. |
| [`src/validators.py`](file:///c:/Users/MD%20FAIYAZ%20KHAN/OneDrive/Documents/Desktop/NetSageAI/src/validators.py) | Validates CSV data schemas, checks placeholder patterns, and enforces conservative evidence classification. |

---

## 📂 Repository Structure

```
NetSageAI/
├── .env.example                # Template for environment configuration
├── .gitignore                  # Git exclusion rules (virtual environments, keys, cache)
├── app.py                      # Main Streamlit web application
├── pytest.ini                  # Pytest configuration (pythonpath root)
├── README.md                   # Complete project documentation
├── requirements.txt            # Python package dependencies
├── run_windows.bat             # 1-click Windows execution launcher
├── setup_windows.bat           # 1-click Windows environment installer
├── data/
│   ├── cases.csv               # 30 structured CCNA network troubleshooting cases
│   ├── evidence.csv            # Manifest mapping cases to source provenance
│   └── review_log.csv          # Human review audit trail and decisions
├── docs/
│   ├── architecture.md         # Detailed technical design & component architecture
│   ├── case-to-lab-mapping.md  # Packet Tracer topology mapping for all 30 cases
│   ├── case_provenance.md      # Public source attribution & verification records
│   ├── demo_readiness.md       # Audit checklist for demonstration readiness
│   ├── demo_script.md          # Step-by-step 5-10 minute presentation guide
│   ├── final_package_audit.md  # Comprehensive codebase and file integrity audit
│   ├── final_presentation_script.md # Script for live presentations & walkthroughs
│   ├── final_submission_status.md   # Project completion metrics & validation log
│   ├── responsible_ai.md       # Responsible AI guidelines, safety, and ethics
│   ├── submission_checklist.md # Verification checklist for academic submission
│   └── testing.md              # Unit test guidelines and test execution notes
├── evidence/
│   └── public-labs/            # Downloaded public Packet Tracer lab files (.pkt, .pka)
├── outputs/
│   └── ai_responses/           # Sample captured AI diagnosis payloads
├── prompts/
│   └── diagnose_prompt.md      # Grounded prompt template for Gemini diagnosis
├── src/
│   ├── __init__.py             # Python package identifier
│   ├── ai_diagnosis.py         # Google GenAI integration and response validation
│   ├── case_loader.py          # Data ingestion and case normalization
│   ├── review_manager.py       # Review logging and persistence
│   ├── rule_checker.py         # 10 deterministic network rule checkers
│   └── validators.py           # Data schema and evidence boundary validators
└── tests/
    └── test_core.py            # Complete unit test suite (22 tests)
```

---

## 🗂️ Case Library & Lab Topologies

NetSage AI includes **30 structured cases** mapped to **8 minimal reusable Packet Tracer topologies**:

### The 8 Core Lab Topologies

1. **Access-Switch VLAN + Gateway Topology**: Covers single/multi-VLAN access ports, default gateway reachability, and trunk access errors.
2. **DHCP Client + Gateway Topology**: Covers pool configuration, APIPA (169.254.x.x) address exhaustion, and IP helper relay issues.
3. **Router-on-a-Stick / Trunk Inter-VLAN Routing**: Covers 802.1Q subinterfaces, native VLAN mismatch, and trunk allowed lists.
4. **Two-Router Routed LAN Topology**: Covers static routes, next-hop unreachable errors, and inter-network routing table gaps.
5. **Interface Down / Physical Layer Topology**: Covers administratively shutdown interfaces and line protocol errors.
6. **NAT/PAT Edge Topology**: Covers inside/outside NAT interface assignment, overload pools, and translation ACL matching.
7. **ACL Traffic Filtering Topology**: Covers standard/extended ACLs blocking HTTP, DNS, or specific client IP ranges.
8. **Wireless AP + Guest VLAN Topology**: Covers SSID VLAN mapping, guest isolation policies, and wireless DHCP lease paths.

### Case Summary Matrix

| Domain | Cases Covered | Key Troubleshooting Scenarios |
|---|---|---|
| **VLAN & Trunking** | CASE001, CASE002, CASE012, CASE013, CASE014, CASE026 | Missing VLAN in database, incorrect access port assignment, trunk allowed list mismatch, encapsulation dot1q errors. |
| **DHCP & Addressing** | CASE003, CASE004, CASE005, CASE006, CASE028, CASE029 | Default gateway in pool mismatch, wrong DHCP pool subnet, APIPA fallback, missing `ip helper-address`, duplicate IPs, subnet mask mismatch. |
| **Routing & Gateway** | CASE009, CASE010, CASE011, CASE030 | Missing static route, wrong default gateway on host, incorrect next-hop IP/exit interface, OSPF neighbor down. |
| **Interface Status** | CASE015, CASE016 | Interface administratively shutdown (`shutdown`), speed/duplex mismatch, cable disconnect. |
| **DNS Resolution** | CASE007, CASE008, CASE027 | Wrong DNS server IP configured on client, UDP 53 blocked by router ACL, DNS server unreachable. |
| **ACL Filtering** | CASE020, CASE021, CASE022 | Implicit deny blocking host, TCP port 80 blocked while ICMP allowed, ACL applied in wrong direction/interface. |
| **NAT / PAT** | CASE017, CASE018, CASE019 | Missing `ip nat inside/outside`, ACL not permitting LAN subnet, overload keyword missing. |
| **Wireless LAN** | CASE023, CASE024, CASE025 | Guest VLAN leaking into internal network, AP DHCP relay broken, wireless channel interference. |

---

## 🛡️ Evidence Provenance & Classification

To ensure academic and professional integrity, NetSage AI rejects simulated or hallucinated confirmation. Every case is classified under a strict 3-tier hierarchy:

- `VERIFIED`: Direct public fault/correction evidence is attached and inspected under strict project verification rules.
- `REFERENCE`: A legitimate public lab topology exists and corresponds to the scenario, but requires independent local re-execution.
- `PENDING`: Starter scenario where verified lab show command outputs have not yet been attached.

```
+-------------------------------------------------------------------------+
|                      Evidence Classification Rules                      |
+-------------------------------------------------------------------------+
|                                                                         |
|  [Evidence Text]                                                        |
|         |                                                               |
|         +---> Contains "PLACEHOLDER" or empty? ---> PENDING             |
|         |                                                               |
|         +---> Verified="YES" & Valid Lab Provenance? ---> VERIFIED      |
|         |                                                               |
|         +---> Verified="NO" & Valid External Lab? ---> REFERENCE        |
|                                                                         |
+-------------------------------------------------------------------------+
```

---

## ⚙️ Deterministic Rule Engine

The deterministic engine ([`src/rule_checker.py`](file:///c:/Users/MD%20FAIYAZ%20KHAN/OneDrive/Documents/Desktop/NetSageAI/src/rule_checker.py)) provides transparent, auditable analysis without calling external APIs:

1. **`duplicate_ip`**: Parses all IPv4 addresses in the evidence and alerts if identical IPs appear across multiple endpoints.
2. **`interface_down`**: Detects `administratively down`, `line protocol is down`, or `down/down` interface states.
3. **`missing_vlan`**: Compares VLAN IDs referenced in symptoms against `show vlan brief` tables.
4. **`missing_route`**: Validates whether target subnets (e.g. `10.2.0.0/24`) appear in `show ip route` tables.
5. **`gateway_mismatch`**: Uses Python's `ipaddress` library to calculate subnet masks and detect when a default gateway is outside the host's subnet.
6. **`wrong_subnet_mask`**: Identifies conflicting subnet masks (e.g. `/24` vs `/26`) within the same broadcast domain.
7. **`wrong_vlan`**: Flags access-port VLAN assignment discrepancies from switchport output.
8. **`nat_issue`**: Examines `show ip nat translations` and NAT configuration statements.
9. **`acl_issue`**: Evaluates access-list deny statements and traffic matching.
10. **`dhcp_issue`**: Identifies APIPA `169.254.x.x` addresses and missing DHCP relay configurations.

---

## 🤖 AI Diagnosis with Gemini

When a Google Gemini API key is configured, NetSage AI can generate structured diagnostic advisories using **Gemini 2.5 Flash**:

- **Structured Output Schema**: Enforces strict JSON return types matching `root_cause`, `confidence`, `evidence`, `next_command`, `fix_steps`, `osi_layer`, and `severity`.
- **Anti-Hallucination Guardrails**: If a case is classified as `REFERENCE` or `PENDING`, the system automatically verifies that the AI does not falsely claim the issue has been "verified" or "proven".
- **Graceful Degradation**: If the API key is absent, quota is exceeded (`429`), or network is unavailable, NetSage AI displays an informative status notice while keeping all deterministic findings fully available.

---

## 👥 Human Review & Responsible AI

NetSage AI enforces **Human-in-the-Loop (HITL)** accountability:

1. **Advisory Role**: AI suggestions are recommendations, never automated network modifications.
2. **Review Options**: The reviewer selects:
   - **`Accepted`**: Agree with the AI root cause and recommended remediation.
   - **`Edited`**: AI was partially correct or incomplete; reviewer inputs corrected diagnosis.
   - **`Rejected`**: AI was incorrect; reviewer provides the accurate root cause.
3. **Audit Trail**: Every decision is persisted to [`data/review_log.csv`](file:///c:/Users/MD%20FAIYAZ%20KHAN/OneDrive/Documents/Desktop/NetSageAI/data/review_log.csv) with timestamps, confidence scores, human rationale, and provenance references.
4. **Agreement Analytics**: Calculates real-time AI-vs-human agreement percentages on the dashboard.

---

## 📊 Interactive Dashboard

The Streamlit dashboard gives real-time operational insights into your troubleshooting dataset:

- **Case Portfolio Metrics**: Total cases, Verified cases, Reference cases, and Pending cases.
- **Review Statistics**: Breakdown of Accepted, Edited, and Rejected human decisions.
- **AI-Human Agreement Rate**: Real-time percentage of AI diagnoses accepted by human engineers.
- **Distribution Charts**: Case coverage by OSI Layer (Layer 1 to Layer 7), Severity (Low, Medium, High, Critical), and Concept (VLAN, DHCP, Routing, ACL, etc.).

---

## 🚀 Getting Started & Installation

### Prerequisites

- **Python 3.10 to 3.14** installed on your system.
- **Git** installed.

### Automated Windows Setup

NetSage AI includes automated batch scripts for quick Windows deployment:

1. Run the setup script:
   ```cmd
   setup_windows.bat
   ```
2. Run the application:
   ```cmd
   run_windows.bat
   ```

---

### Manual Setup (Windows / macOS / Linux)

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/NetSageAI.git
   cd NetSageAI
   ```

2. **Create and Activate a Virtual Environment**:
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

### Environment Configuration

1. Copy the example environment file:
   - **Windows (PowerShell)**:
     ```powershell
     Copy-Item .env.example .env
     ```
   - **macOS / Linux**:
     ```bash
     cp .env.example .env
     ```

2. Edit `.env` to configure your settings:
   ```env
   # Optional: Add your Google Gemini API Key for AI Diagnosis
   GEMINI_API_KEY=your_gemini_api_key_here

   # Optional: Configure Gemini Model (defaults to gemini-2.5-flash)
   GEMINI_MODEL=gemini-2.5-flash
   ```

> [!NOTE]
> NetSage AI operates completely fine without a Gemini API key. All deterministic rule checks, case libraries, review manager, and dashboard metrics work offline.

---

## 🖥️ Running the Application

Launch the Streamlit web interface:

```bash
streamlit run app.py
```

Once launched, open your web browser to:
👉 **[http://localhost:8501](http://localhost:8501)**

### Navigating the Application Tabs

- **🛜 Diagnose**: Select any case from the dropdown, review case details and CLI evidence, inspect deterministic findings, run Gemini AI diagnosis, and submit human reviews.
- **📚 Cases**: Filter the 30-case repository by concept, OSI layer, severity level, or evidence status.
- **📝 Review**: Inspect all logged human reviews, review audit details, or seed demo review records.
- **📊 Dashboard**: View case distribution graphs, evidence status metrics, and AI-human agreement statistics.
- **ℹ️ About**: Read about the project architecture, evidence philosophy, and responsible AI principles.

---

## 🧪 Testing & Quality Assurance

NetSage AI includes a comprehensive test suite in [`tests/test_core.py`](file:///c:/Users/MD%20FAIYAZ%20KHAN/OneDrive/Documents/Desktop/NetSageAI/tests/test_core.py) covering rule engines, CSV validators, schema boundaries, evidence classification, and review persistence.

To run all unit tests:

```powershell
.venv\Scripts\pytest -v
```

Or using `python -m pytest`:

```bash
python -m pytest -v
```

### Test Coverage Summary

- ✅ **Gateway mismatch checks** (outside subnet calculations)
- ✅ **Missing route detection** (missing network prefixes)
- ✅ **Missing VLAN detection** (`show vlan brief` parsing)
- ✅ **Interface down detection** (administratively down states)
- ✅ **Duplicate IP detection** (multi-host IP collisions)
- ✅ **Subnet mask mismatch detection** (conflicting prefix lengths)
- ✅ **NAT, ACL, DHCP, and Wrong VLAN checks**
- ✅ **Gemini AI JSON parsing & schema validation**
- ✅ **Evidence boundary enforcement** (rejection of unverified claims)
- ✅ **Prompt construction with evidence provenance**
- ✅ **API key failure handling & graceful error paths**
- ✅ **Review save, load, and CSV validation**
- ✅ **Placeholder evidence detection**
- ✅ **Integrity of all 30 cases and evidence manifests**

---

## 📚 Documentation Guide

Detailed design and audit documentation is available in the [`docs/`](file:///c:/Users/MD%20FAIYAZ%20KHAN/OneDrive/Documents/Desktop/NetSageAI/docs) directory:

- 📐 [**Architecture Guide** (`docs/architecture.md`)](file:///c:/Users/MD%20FAIYAZ%20KHAN/OneDrive/Documents/Desktop/NetSageAI/docs/architecture.md): Technical components, data pipeline, and system flow.
- 🗺️ [**Case-to-Lab Mapping** (`docs/case-to-lab-mapping.md`)](file:///c:/Users/MD%20FAIYAZ%20KHAN/OneDrive/Documents/Desktop/NetSageAI/docs/case-to-lab-mapping.md): Detailed Packet Tracer topology blueprints for all 30 cases.
- 🔍 [**Case Provenance** (`docs/case_provenance.md`)](file:///c:/Users/MD%20FAIYAZ%20KHAN/OneDrive/Documents/Desktop/NetSageAI/docs/case_provenance.md): Public source attribution, audit findings, and verification criteria.
- ⚖️ [**Responsible AI Policy** (`docs/responsible_ai.md`)](file:///c:/Users/MD%20FAIYAZ%20KHAN/OneDrive/Documents/Desktop/NetSageAI/docs/responsible_ai.md): Ethics, uncertainty communication, and human oversight.
- 🎬 [**Demo Presentation Script** (`docs/demo_script.md`)](file:///c:/Users/MD%20FAIYAZ%20KHAN/OneDrive/Documents/Desktop/NetSageAI/docs/demo_script.md): 5–10 minute live demonstration walkthrough guide.
- 📋 [**Testing Guide** (`docs/testing.md`)](file:///c:/Users/MD%20FAIYAZ%20KHAN/OneDrive/Documents/Desktop/NetSageAI/docs/testing.md): Test execution instructions and smoke-check commands.

---

## ⚠️ Limitations & Ethical Boundaries

1. **Advisory Nature**: NetSage AI is an educational troubleshooting aid. It does not automatically execute configuration commands on live network hardware.
2. **Deterministic Precedence**: Probabilistic AI suggestions should never supersede deterministic subnet math or physical link states.
3. **Reproduction Required**: Starter cases marked as `REFERENCE` or `PENDING` must be reproduced in Cisco Packet Tracer or a physical lab before being considered verified.
4. **Secrets Protection**: API keys are isolated in local `.env` files and never committed to source control or logged in review files.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
