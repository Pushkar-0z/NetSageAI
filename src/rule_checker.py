from __future__ import annotations

import ipaddress
import re
from typing import Any


VALID_RULES = {
    "gateway_mismatch",
    "missing_vlan",
    "interface_down",
    "missing_route",
    "wrong_subnet_mask",
    "duplicate_ip",
    "wrong_vlan",
    "nat_issue",
    "acl_issue",
    "dhcp_issue",
}


def extract_ips(text: str) -> list[str]:
    return re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text or "")


def _format_result(
    rule: str,
    status: str,
    finding: str,
    evidence: str,
    severity: str,
    next_command: str = "",
    confidence: float = 0.0,
) -> dict[str, str | float | bool]:
    return {
        "rule": rule,
        "status": status,
        "detected": status == "FAIL",
        "finding": finding,
        "explanation": finding,
        "evidence": evidence,
        "severity": severity,
        "next_command": next_command,
        "confidence": confidence,
    }


def _extract_gateway(text: str) -> str | None:
    match = re.search(r"gateway\s+([0-9]{1,3}(?:\.[0-9]{1,3}){3})", text, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    for line in text.splitlines():
        if "gateway" in line.lower():
            ip = re.search(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", line)
            if ip:
                return ip.group(0)
    return None


def _extract_host_ip(text: str) -> str | None:
    ips = extract_ips(text)
    if not ips:
        return None
    return ips[0]


def check_duplicate_ips(text: str) -> dict[str, str]:
    ips = extract_ips(text)
    seen = []
    duplicates = []
    for ip in ips:
        if ip in seen and ip not in duplicates:
            duplicates.append(ip)
        seen.append(ip)
    if duplicates:
        return _format_result(
            "duplicate_ip",
            "FAIL",
            f"Duplicate IP detected: {', '.join(duplicates)}.",
            "Multiple identical IP addresses found in the evidence.",
            "High",
        )
    return _format_result(
        "duplicate_ip",
        "PASS",
        "No duplicate IP addresses detected.",
        "No duplicate IPs were found in the supplied evidence.",
        "Low",
    )


def check_interface_down(text: str) -> dict[str, str]:
    lowered = (text or "").lower()
    if any(token in lowered for token in ["administratively down", "line protocol is down", "down/down", "status is down"]):
        return _format_result(
            "interface_down",
            "FAIL",
            "An interface is down or disabled.",
            "Evidence mentions a shutdown or down/down interface state.",
            "High",
        )
    return _format_result(
        "interface_down",
        "PASS",
        "No interface-down indicators found.",
        "No interface-down evidence was detected.",
        "Low",
    )


def check_missing_vlan(case_text: str, evidence_text: str = "") -> dict[str, str]:
    lowered = (case_text or "").lower()
    evidence_lower = (evidence_text or "").lower()
    expected_vlans = {match for match in re.findall(r"vlan\s+(\d+)", lowered)}
    if not expected_vlans:
        if "vlan" in lowered and "not found" in lowered:
            return _format_result(
                "missing_vlan",
                "FAIL",
                "The expected VLAN is not configured.",
                "Evidence explicitly mentions the VLAN is absent or not found.",
                "High",
            )
        return _format_result(
            "missing_vlan",
            "PASS",
            "The VLAN evidence does not show a missing VLAN.",
            "No missing-VLAN indicators were detected.",
            "Low",
        )

    if "show vlan brief" in evidence_lower:
        present_vlans = set(re.findall(r"(?m)^\s*(\d+)\s+\S+", evidence_text or ""))
        missing = sorted(expected_vlans - present_vlans)
        if missing:
            return _format_result(
                "missing_vlan",
                "FAIL",
                f"The required VLAN(s) {', '.join(missing)} are not present in the VLAN table.",
                "The switch VLAN summary does not include the expected VLAN IDs mentioned in the symptom or topology.",
                "High",
            )

    if "vlan" in lowered and "not found" in lowered:
        return _format_result(
            "missing_vlan",
            "FAIL",
            "The expected VLAN is not configured.",
            "Evidence explicitly mentions the VLAN is absent or not found.",
            "High",
        )

    return _format_result(
        "missing_vlan",
        "PASS",
        "The VLAN evidence does not show a missing VLAN.",
        "No missing-VLAN indicators were detected.",
        "Low",
    )


def check_gateway_mismatch(case: dict[str, Any]) -> dict[str, str]:
    text = str(case.get("show_outputs", "") or "")
    if not text:
        return _format_result(
            "gateway_mismatch",
            "PASS",
            "No gateway evidence provided.",
            "The case does not contain a hostname/gateway comparison.",
            "Low",
        )
    host_ip = _extract_host_ip(text)
    gateway = _extract_gateway(text)
    if host_ip and gateway:
        try:
            host = ipaddress.ip_address(host_ip)
            gateway_ip = ipaddress.ip_address(gateway)
            net = ipaddress.ip_network(f"{host_ip}/255.255.255.0", strict=False)
            if gateway_ip not in net:
                return _format_result(
                    "gateway_mismatch",
                    "FAIL",
                    "The configured gateway is outside the host subnet.",
                    "The gateway IP does not fall within the host subnet.",
                    "High",
                )
            if gateway_ip == host:
                return _format_result(
                    "gateway_mismatch",
                    "WARN",
                    "Gateway and host IP appear to be the same address.",
                    "The evidence suggests the gateway may be misconfigured or duplicated.",
                    "Medium",
                )
        except ValueError:
            pass
    return _format_result(
        "gateway_mismatch",
        "PASS",
        "Gateway and host subnet are not clearly inconsistent.",
        "No obvious gateway mismatch was detected in the evidence.",
        "Low",
    )


def check_missing_route(case_text: str, evidence_text: str = "") -> dict[str, str]:
    lowered = (case_text or "").lower()
    evidence_lower = (evidence_text or "").lower()
    route_refs = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\b", case_text or "")
    if "show ip route" in evidence_lower:
        route_table_networks = set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\b", evidence_text or ""))
        if route_refs:
            missing = [route for route in route_refs if route not in route_table_networks]
            if missing:
                return _format_result(
                    "missing_route",
                    "FAIL",
                    f"The target network {missing[0]} is absent from the routing table.",
                    "The route table does not contain the network referenced by the symptom or topology.",
                    "High",
                )
    if "show ip route" in evidence_lower and "network not in routing table" in evidence_lower:
        return _format_result(
            "missing_route",
            "FAIL",
            "The target network is missing from the routing table.",
            "The evidence specifically indicates the route is absent from the router table.",
            "High",
        )
    if "no route to host" in lowered or "network unreachable" in lowered:
        return _format_result(
            "missing_route",
            "FAIL",
            "A missing route or no-route condition is suggested by the evidence.",
            "The troubleshooting output includes a no-route/unreachable message.",
            "High",
        )
    if "show ip route" in evidence_lower and not route_table_networks:
        return _format_result(
            "missing_route",
            "WARN",
            "The route table appears sparse or incomplete.",
            "The evidence hints at a route table without the expected destination route.",
            "Medium",
        )
    return _format_result(
        "missing_route",
        "PASS",
        "No missing-route indicators were detected.",
        "No route absence symptoms were observed.",
        "Low",
    )


def check_wrong_subnet_mask(case: dict[str, Any]) -> dict[str, str]:
    text = str(case.get("show_outputs", "") or "")
    masks = re.findall(r"(?:255\.){3}\d+|/\d{1,2}", text)
    if len(set(masks)) > 1 and any(token in text.lower() for token in ["mask", "subnet", "ipconfig"]):
        return _format_result(
            "wrong_subnet_mask", "FAIL", "Different subnet masks are present in the supplied evidence.",
            "The evidence contains more than one mask/prefix in a subnet-mismatch context.", "Medium",
            "ipconfig /all", 0.86,
        )
    ips = extract_ips(text)
    if len(ips) >= 2:
        try:
            first = ipaddress.ip_address(ips[0])
            second = ipaddress.ip_address(ips[1])
            if first.version == second.version:
                return _format_result(
                    "wrong_subnet_mask",
                    "WARN",
                    "Subnet or mask mismatch may be present.",
                    "Multiple IPs in the evidence suggest a potential subnet/mask inconsistency.",
                    "Medium",
                )
        except ValueError:
            pass
    return _format_result(
        "wrong_subnet_mask",
        "PASS",
        "No clear subnet mask mismatch was detected.",
        "No definitive mask mismatch evidence was found.",
        "Low",
    )


def _concept_rule(case: dict[str, Any], rule: str, keywords: tuple[str, ...], command: str, finding: str) -> dict:
    text = " ".join(str(case.get(field, "")) for field in ("symptom", "topology_note", "show_outputs", "expected_fault")).lower()
    if any(keyword in text for keyword in keywords):
        evidence = str(case.get("show_outputs", "") or "")
        return _format_result(rule, "WARN", finding, evidence or "The case text identifies this troubleshooting area.", "Medium", command, 0.55)
    return _format_result(rule, "PASS", f"No {rule.replace('_', ' ')} indicators were detected.", "No matching indicators in supplied case text.", "Low", command, 0.2)


def check_wrong_vlan(case: dict[str, Any]) -> dict:
    text = " ".join(str(case.get(field, "")) for field in ("symptom", "expected_fault", "show_outputs")).lower()
    if "wrong vlan" in text or "access vlan assignment" in text or "assigned to wrong vlan" in text:
        return _format_result("wrong_vlan", "WARN", "The case indicates an access-port VLAN assignment issue.", str(case.get("show_outputs", "")), "Medium", "show interfaces switchport", 0.7)
    return _format_result("wrong_vlan", "PASS", "No wrong-VLAN indicator was detected.", "No wrong access-VLAN evidence was found.", "Low", "show interfaces switchport", 0.2)


def check_nat_issue(case: dict[str, Any]) -> dict:
    return _concept_rule(case, "nat_issue", ("nat", "pat", "translated addresses"), "show ip nat translations", "The case indicates a NAT/PAT configuration or translation issue.")


def check_acl_issue(case: dict[str, Any]) -> dict:
    return _concept_rule(case, "acl_issue", ("acl", "access-list", "blocked", "deny"), "show access-lists", "The case indicates traffic may be affected by an ACL.")


def check_dhcp_issue(case: dict[str, Any]) -> dict:
    return _concept_rule(case, "dhcp_issue", ("dhcp", "169.254", "helper"), "show ip dhcp binding", "The case indicates a DHCP allocation or relay issue.")


def run_checks(case: dict[str, Any]) -> list[dict[str, str]]:
    aggregated_text = "\n".join(
        [
            str(case.get("symptom", "")),
            str(case.get("topology_note", "")),
            str(case.get("show_outputs", "")),
        ]
    )
    evidence_text = str(case.get("show_outputs", ""))
    return [
        check_duplicate_ips(aggregated_text),
        check_interface_down(evidence_text),
        check_missing_vlan(aggregated_text, evidence_text),
        check_missing_route(aggregated_text, evidence_text),
        check_gateway_mismatch(case),
        check_wrong_subnet_mask(case),
        check_wrong_vlan(case),
        check_nat_issue(case),
        check_acl_issue(case),
        check_dhcp_issue(case),
    ]


if __name__ == "__main__":
    sample = {
        "symptom": "Host reports duplicate IP 192.168.1.10",
        "topology_note": "Two hosts share the LAN",
        "show_outputs": "192.168.1.10 appears twice; interface Gi0/1 is administratively down",
    }
    for result in run_checks(sample):
        print(result)
