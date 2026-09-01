import csv
import io
import json
import os
from pathlib import Path

import pandas as pd
import pytest

from src.rule_checker import run_checks
from src.ai_diagnosis import enforce_evidence_boundary, parse_ai_response, validate_response_schema
from src.validators import evidence_status, is_placeholder_evidence, validate_case_csv, validate_evidence_csv, validate_review_csv
from src.case_loader import load_cases, load_evidence
from src.review_manager import save_review, load_reviews


def test_gateway_mismatch_rule():
    case = {
        "symptom": "PC cannot reach the gateway",
        "topology_note": "PC in VLAN 20, gateway 192.168.20.1",
        "show_outputs": "IP address 192.168.20.10 255.255.255.0\nGateway 192.168.30.1\nshow ip route",
    }
    findings = run_checks(case)
    assert any(f["rule"] == "gateway_mismatch" and f["status"] == "FAIL" for f in findings)


def test_missing_route_rule():
    case = {
        "symptom": "Cannot access 10.2.0.0/24",
        "topology_note": "Router connected to 10.1.0.0/24 and 10.2.0.0/24",
        "show_outputs": "show ip route\nC 10.1.0.0/24 is directly connected\nS 10.3.0.0/24 [1/0] via 192.168.1.1",
    }
    findings = run_checks(case)
    assert any(f["rule"] == "missing_route" and f["status"] == "FAIL" for f in findings)


def test_missing_vlan_rule():
    case = {
        "symptom": "Host in VLAN 30 cannot connect",
        "topology_note": "Switch should have VLAN 30 configured",
        "show_outputs": "show vlan brief\n1 default\n10 sales\n20 finance",
    }
    findings = run_checks(case)
    assert any(f["rule"] == "missing_vlan" and f["status"] == "FAIL" for f in findings)


def test_interface_down_rule():
    case = {
        "symptom": "Port is down",
        "topology_note": "Switch port to host",
        "show_outputs": "GigabitEthernet0/1 is administratively down, line protocol is down",
    }
    findings = run_checks(case)
    assert any(f["rule"] == "interface_down" and f["status"] == "FAIL" for f in findings)


def test_duplicate_ip_rule():
    case = {
        "symptom": "Two hosts report duplicate address",
        "topology_note": "LAN with two devices",
        "show_outputs": "PC1 192.168.10.15\nPC2 192.168.10.15",
    }
    findings = run_checks(case)
    assert any(f["rule"] == "duplicate_ip" and f["status"] == "FAIL" for f in findings)


def test_wrong_subnet_mask_rule():
    case = {
        "symptom": "Host subnet mask prevents local communication",
        "show_outputs": "ipconfig /all\nIP Address 172.16.30.1\nSubnet Mask 255.255.255.0\nPeer mask 255.255.255.192",
    }
    findings = run_checks(case)
    assert any(f["rule"] == "wrong_subnet_mask" and f["status"] == "FAIL" for f in findings)


@pytest.mark.parametrize(
    ("case", "rule"),
    [
        ({"symptom": "NAT translations absent", "expected_fault": "NAT configuration issue"}, "nat_issue"),
        ({"symptom": "ACL blocks HTTP", "expected_fault": "ACL issue"}, "acl_issue"),
        ({"symptom": "PC has 169.254.x.x", "expected_fault": "DHCP issue"}, "dhcp_issue"),
        ({"symptom": "Switch port in wrong VLAN", "expected_fault": "Access VLAN assignment is incorrect"}, "wrong_vlan"),
    ],
)
def test_required_concept_rules_return_actionable_findings(case, rule):
    finding = next(result for result in run_checks(case) if result["rule"] == rule)
    assert finding["next_command"]
    assert "confidence" in finding
    assert "detected" in finding


def test_ai_json_parsing():
    payload = {
        "root_cause": "Missing route to the server network",
        "confidence": 0.82,
        "evidence": ["show ip route lacks the 10.2.0.0/24 route"],
        "next_command": "show ip route",
        "fix_steps": ["Add the static route", "Verify the route is in the table"],
        "osi_layer": "Layer 3",
        "severity": "High",
    }
    parsed = parse_ai_response(json.dumps(payload))
    assert parsed["root_cause"] == payload["root_cause"]
    assert validate_response_schema(parsed) is True


def test_gemini_cannot_claim_unverified_evidence():
    payload = {"root_cause": "The issue is verified", "evidence": ["verified output"], "fix_steps": ["confirmed fixed"]}
    with pytest.raises(ValueError, match="verification claim"):
        enforce_evidence_boundary(payload, {"evidence_status": "REFERENCE"})


def test_gemini_prompt_contains_evidence_provenance():
    from src.ai_diagnosis import build_prompt
    prompt = build_prompt({"case_id": "CASE001", "evidence_status": "REFERENCE", "evidence_text": "source-backed note", "evidence_reference": "guide section", "evidence_source": "public lab"})
    assert "EVIDENCE STATUS: REFERENCE" in prompt
    assert "EVIDENCE REFERENCE: guide section" in prompt


def test_missing_api_key_behavior(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        from src.ai_diagnosis import require_api_key

        require_api_key()


def test_invalid_ai_response_behavior():
    with pytest.raises(ValueError, match="malformed"):
        parse_ai_response("not json")


def test_review_save_load(tmp_path):
    review_path = tmp_path / "review_log.csv"
    review = {
        "case_id": "CASE099",
        "timestamp": "2026-01-01T00:00:00Z",
        "ai_root_cause": "Gateway mismatch",
        "ai_confidence": 0.8,
        "human_decision": "Edited",
        "human_root_cause": "Wrong default gateway",
        "human_correction": "Corrected the gateway value",
        "reviewer_reason": "AI missed the default gateway issue",
    }
    save_review(review, review_path)
    loaded = load_reviews(review_path)
    assert not loaded.empty
    assert loaded.iloc[0]["case_id"] == "CASE099"
    assert "evidence_reference" in loaded.columns


def test_review_csv_validation_requires_evidence_reference(tmp_path):
    review_path = tmp_path / "review_log.csv"
    pd.DataFrame([{"case_id": "CASE001", "ai_confidence": "0.5", "human_decision": "Accepted"}]).to_csv(review_path, index=False)
    result = validate_review_csv(review_path)
    assert result["valid"] is False
    assert any("evidence_reference" in error for error in result["errors"])


def test_placeholder_detection():
    assert is_placeholder_evidence("REPLACE WITH ACTUAL PACKET TRACER/LAB SHOW OUTPUTS") is True
    assert is_placeholder_evidence("PLACEHOLDER — REPLACE WITH VERIFIED PACKET TRACER/LAB OUTPUT") is True
    assert is_placeholder_evidence("show ip interface brief\nGigabitEthernet0/1 is up") is False


def test_evidence_status_is_conservative():
    assert evidence_status({"show_outputs": "PLACEHOLDER", "verified": "NO"}) == "PENDING"
    assert evidence_status({"show_outputs": "reference output", "evidence_source": "REFERENCE", "verified": "NO"}) == "REFERENCE"
    assert evidence_status({"show_outputs": "actual output", "evidence_source": "Packet Tracer", "verified": "YES"}) == "VERIFIED"
    assert evidence_status({"show_outputs": "NOT VERIFIED", "evidence_source": "Packet Tracer", "verified": "YES"}) == "PENDING"


def test_all_30_cases_load_and_evidence_manifest_is_valid():
    cases = load_cases(Path("data/cases.csv"))
    evidence = load_evidence(Path("data/evidence.csv"))
    assert len(cases) == 30
    assert set(cases["case_id"]) == {f"CASE{index:03d}" for index in range(1, 31)}
    assert len(evidence) == 30
    assert validate_evidence_csv(Path("data/evidence.csv"))["valid"] is True


def test_manifest_does_not_upgrade_placeholder_case_to_verified():
    cases = load_cases(Path("data/cases.csv"))
    evidence = load_evidence(Path("data/evidence.csv"))
    merged = cases.merge(evidence[["case_id", "evidence_status", "evidence_text"]], on="case_id", suffixes=("_case", "_manifest"))
    assert not ((merged["evidence_status_manifest"] == "VERIFIED") & merged["evidence_text"].map(is_placeholder_evidence)).any()


def test_csv_validation():
    valid_rows = [
        {
            "case_id": "CASE001",
            "symptom": "Host cannot reach gateway",
            "topology_note": "Single LAN",
            "show_outputs": "PLACEHOLDER — REPLACE WITH VERIFIED PACKET TRACER/LAB OUTPUT",
            "expected_fault": "Gateway mismatch",
            "osi_layer": "Layer 3",
            "concept": "Gateway",
            "severity": "High",
        }
    ]
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=list(valid_rows[0].keys()))
    writer.writeheader()
    writer.writerows(valid_rows)
    stream.seek(0)
    result = validate_case_csv(stream)
    assert result["valid"] is True

    invalid_rows = [
        {
            "case_id": "CASE002",
            "symptom": "",
            "topology_note": "",
            "show_outputs": "",
            "expected_fault": "",
            "osi_layer": "Layer 9",
            "concept": "Gateway",
            "severity": "Urgent",
        }
    ]
    stream2 = io.StringIO()
    writer2 = csv.DictWriter(stream2, fieldnames=list(invalid_rows[0].keys()))
    writer2.writeheader()
    writer2.writerows(invalid_rows)
    stream2.seek(0)
    result2 = validate_case_csv(stream2)
    assert result2["valid"] is False
