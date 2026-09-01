# Case provenance

All 30 rows currently present in [data/cases.csv](../data/cases.csv) are starter scenarios. Their `show_outputs` field contains a replacement instruction rather than a Cisco command transcript, and `verified` remains `NO`. The authoritative evidence manifest classifies 4 cases as `VERIFIED` under the public paired-evidence rule, 21 as `REFERENCE`, and 5 as `PENDING`.

Downloaded `.pkt` and `.pka` artifacts and supporting guides are now present under `evidence/public-labs/`. No downloaded binary has been independently opened and matched to an exact case fault, so these sources remain reference material. The source/reference for each row is the official NetSage AI case specification plus the mapped public lab where applicable; Packet Tracer reproduction remains required.

| Case | Concept | Source/reference | Evidence status | Lab file | Commands required for verification |
|---|---|---|---|---|---|
| CASE001 | VLAN | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show vlan brief`; `show interfaces switchport`; `ping` |
| CASE002 | VLAN/Gateway | Public paired broken/fixed VLAN lab | VERIFIED | `evidence/public-labs/portfolio/vlan-variant1-broken-README.md` plus inspected screenshots | `show interfaces switchport`; `show ip interface brief`; `ping` |
| CASE003 | Gateway | Public paired broken/fixed gateway lab | VERIFIED | `evidence/public-labs/portfolio/vlan-variant3-broken/README.md` plus inspected screenshots | `show ip`; `ping <gateway>`; `ping <peer>` |
| CASE004 | DHCP | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show ip dhcp pool`; `show ip dhcp binding`; `ipconfig /all` |
| CASE005 | DHCP | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show ip dhcp pool`; `show ip dhcp binding`; `ipconfig /renew`; `ipconfig /all` |
| CASE006 | DHCP | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show running-config interface vlan X`; `show ip dhcp binding`; `ipconfig /renew` |
| CASE007 | DNS | Official case seed; Packet Tracer reproduction required | PENDING | None available | `ipconfig /all`; `ping <dns-server>`; `nslookup example.com` |
| CASE008 | DNS/ACL | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show access-lists`; `show ip route`; `ping <dns-server>`; `nslookup example.com` |
| CASE009 | Routing | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show ip route`; `show ip route static`; `ping <remote-host>`; `traceroute` |
| CASE010 | Gateway/Routing | Official case seed; Packet Tracer reproduction required | PENDING | None available | `ipconfig /all`; `show ip route`; `ping <gateway>`; `ping <remote-host>` |
| CASE011 | Routing | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show ip route`; `show running-config | section ip route`; `traceroute` |
| CASE012 | VLAN/Trunking | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show interfaces trunk`; `show vlan brief`; `show interfaces switchport` |
| CASE013 | VLAN/Routing | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show interfaces trunk`; `show running-config interface g0/1`; `ping` |
| CASE014 | VLAN | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show vlan brief`; `show running-config | section vlan`; `show interfaces switchport` |
| CASE015 | Interface | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show interfaces status`; `show interfaces fa0/1`; `show interfaces summary`; `ping` |
| CASE016 | Interface | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show interfaces status`; `show running-config interface fa0/1`; `ping` |
| CASE017 | NAT | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show ip nat translations`; `show ip nat statistics`; `show ip route`; `ping <outside-ip>` |
| CASE018 | NAT | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show access-lists`; `show ip nat translations`; `show ip nat statistics` |
| CASE019 | NAT | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show ip nat translations`; `show access-lists`; `show running-config | section nat` |
| CASE020 | ACL | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show access-lists`; `show running-config | section access-list`; `ping`; HTTP test |
| CASE021 | ACL | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show access-lists`; `ping`; `telnet <server> 80` or HTTP test |
| CASE022 | ACL | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show ip access-lists`; `show access-lists`; `ping`; HTTP test |
| CASE023 | Wireless/ACL | Official case seed; Packet Tracer reproduction required | PENDING | None available | WLAN/SSID status; `show ip dhcp binding`; `ping <internal-server>` |
| CASE024 | Wireless/DHCP | Official case seed; Packet Tracer reproduction required | PENDING | None available | WLAN/VLAN mapping; `show ip dhcp binding`; `show interfaces status`; `ipconfig /all` |
| CASE025 | Wireless | Official case seed; Packet Tracer reproduction required | PENDING | None available | AP wireless status; channel/client status; `show interfaces summary` |
| CASE026 | VLAN | Public paired broken/fixed VLAN lab | VERIFIED | `evidence/public-labs/portfolio/vlan-variant1-broken-README.md` plus inspected screenshots | `show interfaces switchport`; `show vlan brief`; `ping <gateway>` |
| CASE027 | Routing/DNS | Official case seed; Packet Tracer reproduction required | PENDING | None available | `show ip route`; `show access-lists`; `ping <dns-server>`; `nslookup example.com` |
| CASE028 | IP Addressing | Official case seed; Packet Tracer reproduction required | PENDING | None available | `ipconfig /all`; `arp -a`; `show ip dhcp binding`; `ping` |
| CASE029 | IP Addressing/Gateway | Official case seed; Packet Tracer reproduction required | PENDING | None available | `ipconfig /all`; `ping <peer-ip>`; `arp -a` |
| CASE030 | Routing | Public troubleshooting lab Phase 3 | VERIFIED | `evidence/public-labs/portfolio/troubleshooting-lab-1/troubleshooting-lab-1.pkt` plus inspected screenshots | `show ip route 192.168.20.0`; `show ip ospf database`; `ping <remote-host>` |

## Demo evidence boundary

The workspace has no independently inspectable lab output for the supplied router/subnet scenario. It must therefore be described as `REFERENCE LAB EVIDENCE — VERIFICATION REQUIRED` if included later. It must not be used to claim a confirmed connectivity failure or a verified case.

## Public source inventory

The following public sources were inspected on 2026-08-25 and recorded in [data/evidence.csv](../data/evidence.csv):

| Source | What was actually observed | Use in this project |
|---|---|---|
| [Cisco Networking Academy Packet Tracer](https://www.netacad.com/courses/packet-tracer) | Cisco describes Packet Tracer as a teaching simulator supporting topologies, visualization, and troubleshooting challenges. | General educational reference; not case evidence. |
| [CCNA Networking Portfolio](https://github.com/jahsonjb/CCNA-Networking-Portfolio) | Repository lists VLAN/inter-VLAN broken/fixed variants, static/OSPF routing, ACL, NAT/PAT, and troubleshooting labs. Several README files were downloaded locally. | Reference mappings for VLAN, routing, ACL, and NAT cases. |
| [LuqmanKt98/Cisco-Packet-Tracer](https://github.com/LuqmanKt98/Cisco-Packet-Tracer) | Repository tree lists Packet Tracer files named for DHCP, IP helper-address, inter-VLAN/DNS, and static routing. Two `.pkt` files were downloaded locally. | Reference mappings only; binary contents were not independently opened. |
| [PacketTracer-Troubleshooting-Challenge](https://github.com/Maro7420/PacketTracer-Troubleshooting-Challenge) | README describes a router, three switches, PCs, a web server, IPv4/IPv6, VLANs, gateways, subnetting, and a `.pka` artifact. | Reference mappings for general LAN/VLAN/gateway/subnet cases; exact fault not independently verified. |

Local collection summary:
- 4 Packet Tracer binaries: 3 `.pkt` and 1 `.pka`.
- 7 supporting README/guide files.
- 4 cases supported by explicit public fault/correction evidence and inspected screenshots; not independently rerun locally.
- 21 reference mappings and 5 pending mappings in `data/evidence.csv`.

The local files are source artifacts, not generated evidence. They must be opened and checked in Packet Tracer before any case can be upgraded to `VERIFIED`.
