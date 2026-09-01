# Case-to-Lab Mapping for Packet Tracer Evidence Collection

This document maps each of the 30 cases in [data/cases.csv](../data/cases.csv) to the most practical Packet Tracer topology and evidence plan without modifying the case data or claiming any case is verified.

Scope and constraints:
- No case output is fabricated.
- No case is marked as verified.
- No case is changed in [data/cases.csv](../data/cases.csv).
- The mapping minimizes Packet Tracer work by reusing a small number of topologies.
- We do not assume that a downloaded lab matches a case unless the topology and fault are actually compatible.

## Workspace lab inventory check

Public Packet Tracer artifacts have since been collected under `evidence/public-labs/`, including 3 `.pkt` files and 1 `.pka` file plus supporting guides. Four cases are mapped as `VERIFIED` under the public paired-evidence rule; the remaining mappings are `REFERENCE` or `PENDING`.

The `Downloaded lab support in workspace?` values in the original planning table describe the workspace before public collection. The current authoritative source/artifact mapping is [data/evidence.csv](../data/evidence.csv), which records the 25 reference mappings and 5 pending cases.

## Minimal reusable topology set

The 30 cases can be covered efficiently with 8 reusable Packet Tracer topologies:

1. Access-switch VLAN + gateway topology
2. DHCP client + gateway topology
3. Router-on-a-stick / trunk + inter-VLAN routing
4. Two-router routed LAN topology
5. Interface down / shutdown topology
6. NAT/PAT edge topology
7. ACL filtering topology
8. Wireless AP + guest VLAN + DHCP topology

This keeps the lab count low while still supporting each case with realistic evidence collection.

---

## Detailed case mapping

| Case ID | Exact expected fault | Required networking concept | Required evidence | Best matching Packet Tracer topology | Downloaded lab support in workspace? | Show / verification commands | Clarification needed? |
|---|---|---|---|---|---|---|---|
| CASE001 | VLAN 10 missing or port assigned to wrong VLAN | VLAN | Show VLAN membership, interface assignment, host connectivity | Access-switch VLAN + gateway topology | No matching lab file found in workspace | `show vlan brief`, `show interfaces switchport`, `show ip interface brief`, `ping` | No |
| CASE002 | Access-port VLAN mismatch or gateway/SVI VLAN issue | VLAN / gateway | Interface VLAN, SVI, gateway, reachability test | Access-switch VLAN + gateway topology | No matching lab file found in workspace | `show interfaces switchport`, `show ip interface brief`, `show running-config interface vlan X`, `ping <gateway>` | Minor: confirm whether VLAN mismatch or SVI not created is the intended root cause |
| CASE003 | Wrong default gateway configuration | DHCP / gateway | DHCP lease, gateway value, ping to default gateway | DHCP client + gateway topology | No matching lab file found in workspace | `ipconfig /all`, `show ip dhcp binding`, `show ip interface brief`, `ping <gateway>` | No |
| CASE004 | DHCP pool/network mismatch | DHCP | DHCP pool subnet, lease, host IP and mask | DHCP client + gateway topology | No matching lab file found in workspace | `show ip dhcp pool`, `show ip dhcp binding`, `ipconfig /all`, `ping <gateway>` | No |
| CASE005 | DHCP server/pool unavailable or relay path broken | DHCP | DHCP process status, lease table, APIPA result | DHCP client + gateway topology | No matching lab file found in workspace | `show ip dhcp binding`, `show ip dhcp pool`, `show running-config | section dhcp`, `ipconfig /renew`, `ipconfig /all` | Minor: confirm whether the issue is server outage vs relay path failure |
| CASE006 | Missing DHCP relay/helper on affected VLAN interface | DHCP / relay | Helper address, VLAN interface, DHCP request success/failure | DHCP client + gateway topology | No matching lab file found in workspace | `show ip dhcp pool`, `show running-config interface vlan X`, `show ip interface brief`, `ipconfig /renew` | No |
| CASE007 | DNS server address or DNS service configuration problem | DNS | DNS server IP, nslookup/dig/host test, reachability to DNS server | DNS + client topology | No matching lab file found in workspace | `ipconfig /all`, `ping <dns-server>`, `nslookup example.com`, `show running-config | section dns` | No |
| CASE008 | ACL or routing prevents DNS traffic | DNS / ACL / routing | ACL entries, route table, name resolution failure | DNS + client topology with ACL path | No matching lab file found in workspace | `show access-lists`, `show ip route`, `ping <dns-server>`, `nslookup example.com` | Minor: confirm whether the blocking element is an ACL or a route issue |
| CASE009 | Missing route to remote network | Routing | Route table, remote subnet, ping failure | Two-router routed LAN topology | No matching lab file found in workspace | `show ip route`, `show ip route static`, `ping <remote-host>`, `traceroute` | No |
| CASE010 | Incorrect default gateway on clients | Gateway / routing | Client gateway, route table, ping from PC to gateway and remote host | Two-router routed LAN topology | No matching lab file found in workspace | `ipconfig /all`, `show ip route`, `ping <gateway>`, `ping <remote-host>` | No |
| CASE011 | Incorrect next-hop or exit interface in static route | Routing | Static route entries, route lookup, ping failure | Two-router routed LAN topology | No matching lab file found in workspace | `show ip route`, `show running-config | section ip route`, `ping <remote-host>`, `traceroute` | No |
| CASE012 | VLAN not allowed on trunk | VLAN / trunking | Trunk allowed VLAN list, port states, VLAN reachability | Router-on-a-stick / trunk + inter-VLAN routing | No matching lab file found in workspace | `show interfaces trunk`, `show vlan brief`, `show interfaces switchport`, `ping` | No |
| CASE013 | Trunk encapsulation/native VLAN/subinterface mismatch | VLAN / routing | Dot1Q config, subinterface config, ping between VLANs | Router-on-a-stick / trunk + inter-VLAN routing | No matching lab file found in workspace | `show interfaces trunk`, `show running-config interface g0/1`, `show running-config interface vlan X`, `ping` | No |
| CASE014 | VLAN was not created or configuration was not saved/applied | VLAN | Switch VLAN table, SVI config if used, switch show output | Access-switch VLAN + gateway topology | No matching lab file found in workspace | `show vlan brief`, `show running-config | section vlan`, `show interfaces switchport` | No |
| CASE015 | Interface administratively disabled or physical link problem | Interface / layer 1-2 | Port status and counters, link lights, host connectivity | Interface down / shutdown topology | No matching lab file found in workspace | `show interfaces status`, `show interfaces fa0/1`, `show interfaces summary`, `ping` | No |
| CASE016 | Port is shutdown | Interface / layer 1-2 | Port state, shutdown status, connectivity | Interface down / shutdown topology | No matching lab file found in workspace | `show interfaces status`, `show running-config interface fa0/1`, `ping` | No |
| CASE017 | Missing or incorrect NAT/PAT configuration | NAT | NAT translations, PAT rules, outside reachability | NAT/PAT edge topology | No matching lab file found in workspace | `show ip nat translations`, `show ip nat statistics`, `show ip route`, `ping <outside-ip>` | No |
| CASE018 | NAT rule/ACL does not include affected subnet | NAT / ACL | NAT access list, translated addresses, connectivity per subnet | NAT/PAT edge topology | No matching lab file found in workspace | `show access-lists`, `show ip nat translations`, `show ip nat statistics`, `ping <outside-ip>` | No |
| CASE019 | NAT configuration or matching ACL is missing | NAT / ACL | NAT statement, ACL match, translation table | NAT/PAT edge topology | No matching lab file found in workspace | `show ip nat translations`, `show access-lists`, `show running-config | section nat`, `ping` | No |
| CASE020 | ACL denies required traffic | ACL | ACL entries on interface, ping/HTTP test failure, permit/deny result | ACL filtering topology | No matching lab file found in workspace | `show access-lists`, `show running-config | section access-list`, `ping`, `telnet` or HTTP test | No |
| CASE021 | ACL blocks TCP/80 or equivalent web traffic | ACL / application traffic | ACL applied to interface, TCP port service test, ping may still succeed | ACL filtering topology | No matching lab file found in workspace | `show access-lists`, `show running-config | section access-list`, `ping`, `telnet <server> 80` or browser HTTP check | No |
| CASE022 | ACL rule matches the affected source address | ACL | Source IP range, ACL order, affected host test | ACL filtering topology | No matching lab file found in workspace | `show access-lists`, `show ip access-lists`, `ping`, `telnet` | No |
| CASE023 | Guest isolation ACL/VLAN policy is missing | Wireless / ACL | Guest WLAN mapping, VLAN policy, guest to internal server reachability | Wireless AP + guest VLAN + DHCP topology | No matching lab file found in workspace | `show wlan summary`, `show running-config | section wlan`, `show ip dhcp binding`, `ping <internal-server>` | No |
| CASE024 | Wireless VLAN/DHCP path is misconfigured | Wireless / DHCP | AP to VLAN mapping, DHCP pool, client lease | Wireless AP + guest VLAN + DHCP topology | No matching lab file found in workspace | `show running-config | section wlan`, `show ip dhcp binding`, `show interfaces status`, `ipconfig /all` | No |
| CASE025 | Channel/interference or unstable AP/link configuration | Wireless / layer 1-2 | AP channel, signal quality, connectivity stability | Wireless AP + guest VLAN + DHCP topology | No matching lab file found in workspace | `show running-config | section wlan`, `show ap config 802.11a`, `show interfaces summary`, wireless client status | Minor: clarify whether this is RF interference, AP channel issue, or port issue |
| CASE026 | Access VLAN assignment is incorrect | VLAN | Switch port access VLAN, host subnet/VLAN match | Access-switch VLAN + gateway topology | No matching lab file found in workspace | `show interfaces switchport`, `show vlan brief`, `ping <gateway>`, `ipconfig /all` | No |
| CASE027 | Routing/ACL prevents traffic to DNS server | Routing / DNS / ACL | Route table, ACL, DNS server reachability | Two-router routed LAN topology with DNS server path | No matching lab file found in workspace | `show ip route`, `show access-lists`, `ping <dns-server>`, `nslookup example.com` | Minor: specify whether DNS failure is from routing or ACL path issue |
| CASE028 | Duplicate IP address configuration | IP addressing | Duplicate address conflict warning, same IP on two hosts | Access-switch VLAN + gateway topology | No matching lab file found in workspace | `show ip dhcp binding`, `ipconfig /all`, `arp -a`, `ping` | No |
| CASE029 | Incorrect subnet mask on host | IP addressing / gateway | Host IP, mask, and local peer reachability | Access-switch VLAN + gateway topology | No matching lab file found in workspace | `ipconfig /all`, `ping <peer-ip>`, `arp -a`, `show ip interface brief` | No |
| CASE030 | Remote network route is missing | Routing | Route table on both routers, expected remote network, ping failure | Two-router routed LAN topology | No matching lab file found in workspace | `show ip route`, `show running-config | section ip route`, `ping <remote-host>`, `traceroute` | No |

---

## Topology grouping for fastest completion

### 1) Access-switch VLAN + gateway topology
Best for:
- CASE001
- CASE002
- CASE014
- CASE026
- CASE028
- CASE029

Why this grouping works:
- Same switch + access VLAN + PC + gateway structure
- Minimal device churn
- Easy to reuse same base topology for multiple VLAN and IP faults

### 2) DHCP client + gateway topology
Best for:
- CASE003
- CASE004
- CASE005
- CASE006

Why this grouping works:
- Same DHCP server, pool, switch, client segment
- Reuse same base build and vary only DHCP scope or relay configuration

### 3) DNS + ACL + service path topology
Best for:
- CASE007
- CASE008
- CASE027

Why this grouping works:
- DNS server is the service under test
- Same client-server path can be used with either ACL or route issue

### 4) Two-router routed LAN topology
Best for:
- CASE009
- CASE010
- CASE011
- CASE030

Why this grouping works:
- Same remote-network design with different route or gateway problems
- Efficient to recreate and validate with `show ip route`

### 5) Router-on-a-stick / trunk + inter-VLAN routing topology
Best for:
- CASE012
- CASE013

Why this grouping works:
- Same trunk and subinterface design
- Good reuse for trunk VLAN permit and encapsulation problems

### 6) Interface down / shutdown topology
Best for:
- CASE015
- CASE016

Why this grouping works:
- Same physical switch port + host connection
- Only port state differs

### 7) NAT/PAT edge topology
Best for:
- CASE017
- CASE018
- CASE019

Why this grouping works:
- Same edge router and inside/outside network layout
- Different NAT and ACL issues can be injected without rebuilding from scratch

### 8) ACL filtering topology
Best for:
- CASE020
- CASE021
- CASE022

Why this grouping works:
- Same client-to-server traffic path
- Targeted ACL changes produce each failure pattern

### 9) Wireless AP + guest VLAN + DHCP topology
Best for:
- CASE023
- CASE024
- CASE025

Why this grouping works:
- Same AP, switch, WLAN, and guest VLAN design
- Faults vary between guest policy, VLAN/DHCP mapping, and RF/channel instability

---

## Practical completion order

To minimize Packet Tracer work, the best order is:

1. Build the VLAN + gateway topology and complete CASE001, 002, 014, 026, 028, 029
2. Build the DHCP topology and complete CASE003, 004, 005, 006
3. Build the two-router routing topology and complete CASE009, 010, 011, 030
4. Build the NAT topology and complete CASE017, 018, 019
5. Build the ACL topology and complete CASE020, 021, 022
6. Build the wireless topology and complete CASE023, 024, 025
7. Build the trunk/inter-VLAN topology and complete CASE012, 013
8. Build the interface-failure topology and complete CASE015, 016
9. Use the DNS-focused topology for CASE007, 008, 027 if needed, or fold it into the routed service topology as a shared path

This produces the lowest total lab build count while preserving realistic evidence collection for all 30 cases.

---

## Final conclusion

The current workspace includes downloaded public Packet Tracer artifacts, but they are reference material rather than verified reproductions. The practical path is to inspect/reproduce the mapped scenarios and attach actual command output before upgrading any case to `VERIFIED`.

The key design principle is reuse: most cases are not unique network designs; they are the same topology with different faults applied. That gives the lowest Packet Tracer effort and the strongest evidence quality for the final project.
