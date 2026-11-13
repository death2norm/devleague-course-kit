{{REWRITE: this is the Network+ example. Keep the shape (one page per domain: header line, the habit, 3–5 short sections with tables, 8 Top Traps from traps.tsv) and write every line from this course's handouts. Delete this line.}}

# Domain 1 Cheat Sheet: Networking Concepts

*23% of the exam · Objectives 1.1–1.8 · Taught in Sessions 1–6 and 10 · One section per domain, built from the session handouts and the Trap Atlas*

**On every question:** read the last sentence first · find the restriction (first, best, most likely, not) · follow the clue to its layer, not the symptom · eliminate answers that are true but don't do the job asked.

## OSI and Appliances (1.1, 1.2)

**OSI, bottom up** (Please Do Not Throw Sausage Pizza Away): 1 Physical, bits (cables, hub) · 2 Data Link, frames (MAC, switch, AP) · 3 Network, packets (IP, router) · 4 Transport, segments/datagrams (ports, TCP/UDP) · 5 Session · 6 Presentation · 7 Application, data (HTTP, DNS, NGFW, proxy).

Router joins networks · switch joins devices · firewall decides what's allowed · **IDS** watches a copy (SPAN, tap), **IPS** sits inline and blocks · **forward proxy** fronts users, **reverse proxy** fronts servers · **NAS** = files (SMB, NFS), **SAN** = blocks (FC, iSCSI) · **CDN** = content near users · **QoS** = priority on a busy link.

## Ports and Traffic (1.4)

| Port | Service | Port | Service |
|---|---|---|---|
| 20/21 | FTP | 161 / 162 | SNMP poll / traps (UDP) |
| 22 | SSH, SFTP | 389 / 636 | LDAP / LDAPS |
| 23 | Telnet | 80 / 443 | HTTP / HTTPS |
| 25 / 587 | SMTP / SMTPS | 445 | SMB |
| 53 | DNS (UDP lookups, TCP transfers) | 514 | Syslog (UDP) |
| 67/68 | DHCP (UDP) | 1433 | SQL Server |
| 69 | TFTP (UDP) | 3389 | RDP |
| 123 | NTP (UDP) | 5060/5061 | SIP / SIP over TLS |

**Unicast** one · **multicast** a group (IPv6 uses it instead of broadcast) · **broadcast** everyone local · **anycast** the nearest of several. **GRE** tunnels without encryption · IPsec **ESP** encrypts, **AH** doesn't.

## Media, Topologies, Cloud (1.3, 1.5, 1.6)

- **Copper:** no category goes past 100 m (Cat 8 only 30 m) · Cat 6 = 10 Gb only to about 55 m · Cat 6a = 10 Gb at 100 m · PoE 15.4 W (af), PoE+ 30 W (at), 60/90 W (bt). **Fiber:** SMF yellow, km, LR · MMF orange/aqua, hundreds of m, SR. Plenum = fire; shielded = EMI. DAC for in-rack.
- **Topology:** star has one center · full mesh most redundant · hub-and-spoke cheapest for branches · spine-leaf for data centers (every leaf to every spine) · three-tier: access, distribution (policy), core (speed) · east-west = server to server.
- **Cloud:** IaaS you patch the OS · PaaS your code · SaaS the finished app · hybrid = private or on-premises joined to a public cloud · elasticity grows **and shrinks** · NAT gateway lets private subnets out only · security group stateful, NACL stateless.

## Addressing and Modern Networks (1.7, 1.8)

Private: **10/8, 172.16–31, 192.168** · **169.254** = no DHCP answer · 127 = loopback · block size = 256 − mask octet · usable = 2^host bits − 2 · IPv6: fe80 link-local (always there), fd unique local, 2000::/3 global, one `::` · SDN centralizes the **control** plane · SD-WAN: app-aware, transport-agnostic, zero-touch · VXLAN = 16 M segments, not encryption · SASE = SD-WAN + SSE.

## Top Traps

- "Clear the browser cache" when the link light is off. Answer at the clue's layer.
- "TCP for live voice." Real-time is UDP.
- "A /26 fits 64 hosts." 62 usable.
- "172.32.x.x is private." Only 172.16–172.31.
- "Cat 6a fixes a 120 m run." Nothing copper does.
- "An IDS on a SPAN port can block." Only inline IPS blocks.
- "SFTP and FTPS are the same." SFTP is SSH on 22.
- "Scalability" for automatic grow-and-shrink. That's elasticity.

---

# Domain 2 Cheat Sheet: Network Implementation

*20% of the exam · Objectives 2.1–2.4 · Taught in Sessions 5, 7, 8 and 9*

**The habit:** find the one setting that differs, the one route that's missing, or the one channel that overlaps. Most implementation questions are a single mismatch.

## Routing (2.1)

| Step | Rule |
|---|---|
| 1. Longest prefix | /24 beats /16 beats /0, always first |
| 2. Administrative distance | Same prefix: connected 0 · static 1 · eBGP 20 · EIGRP 90 · OSPF 110 · iBGP 200 |
| 3. Metric | Same protocol only |

**OSPF** link state, cost, multivendor · **EIGRP** advanced distance vector, Cisco, feasible successor · **BGP** path vector, between AS numbers, TCP 179 · **PAT** = many to one · **inside local** = private, **inside global** = public · **port forwarding** lets the outside in · **FHRP**: hosts use the virtual IP; VRRP master/backup (open), HSRP active/standby (Cisco) · **router-on-a-stick** needs a trunk and one subinterface per VLAN.

## Switching (2.2)

- **VLAN** = one broadcast domain; crossing VLANs needs routing (SVIs on a Layer 3 switch).
- **Access port** untagged · **voice VLAN** tags the phone, not the PC · **trunk** 802.1Q tags all but the **native** VLAN, which must match both ends · missing from the **allowed list** = that VLAN fails across.
- **STP:** lowest bridge ID is root (priority 32768, then MAC) · blocking → listening → learning → forwarding · PortFast and BPDU guard on edge ports.
- **LACP** bundles links (match speed, duplex, VLANs) · **duplex mismatch** = CRCs and runts on full, late collisions on half · **MTU** 1500, jumbo ≈ 9000, every hop matches.

## Wireless (2.3)

| Standard | Band |
|---|---|
| a / ac (Wi-Fi 5) | 5 GHz only |
| b / g | 2.4 GHz only |
| n (Wi-Fi 4) · ax (Wi-Fi 6) | 2.4 and 5 · **6E** adds 6 GHz |

2.4 GHz: **1, 6, 11**, 20 MHz, best range · dense rooms: narrower channels · **DFS** moves off radar, **TPC** lowers power · SSID = name, **BSSID** = one radio's MAC · directional antenna (patch, Yagi, parabolic) for halls and buildings · **WPA3 SAE** stops offline guessing · Enterprise = 802.1X + RADIUS · **captive portal** = terms · **client isolation** = guests apart · lightweight APs + WLC over **CAPWAP**.

## Installation (2.4)

**MDF** = core and provider · **IDF** = floor closet within 90 m · 1U = 1.75 in · port-side intake/exhaust matches the aisle · **UPS** rides through; **PDU** distributes (managed = remote outlet) · clean-agent or pre-action suppression · humidity 40–60%.

## Top Traps

- "The lowest AD wins." Longest prefix first.
- "Static or dynamic NAT" for many-to-one. That's PAT.
- "The cable is bad" when one VLAN fails across a trunk. Check the allowed list.
- "Highest priority becomes root." Lowest.
- "More power" for strong signal and slow Wi-Fi. Fix the channels.
- "Channels 1, 5, 9." Use 1, 6, 11.
- "Hide the SSID" for security. Use 802.1X.
- "A PDU keeps it running in an outage." A UPS does.

---

# Domain 3 Cheat Sheet: Network Operations

*19% of the exam · Objectives 3.1–3.5 · Taught in Sessions 4, 11 and 12*

**The habit:** match the document, metric or tool to the exact question. "Data lost" is not "time down," "up" is not "fast," and a backup is not the standard.

## Documentation and Life Cycle (3.1)

| Need | Answer |
|---|---|
| Which port is this jack on? | Physical / Layer 1 diagram, cable map |
| Subnets, VLANs, routing | Logical / Layer 2–3 diagram |
| What's in each rack unit | Rack diagram |
| Track every subnet and address | **IPAM** (DHCP only knows its scopes) |
| Signal across a floor | **Heat map** from a site survey |
| Find unauthorized changes | Compare with the **golden / baseline** config |
| Restore service after a bad change | **Rollback (backout) plan** |

**EOL** = no longer sold · **EOS** = no more patches · every change: request, scope, risk, test, rollback, approval, window. **SLA** defines level and remedy; it doesn't prevent outages · 99.9% ≈ 8.8 hours down a year.

## Disaster Recovery (3.3)

**RPO** = max data lost · **RTO** = max time down · **MTBF** higher is better · **MTTR** lower is better · **hot** = minutes, **warm** = hours to a day, **cold** = days to weeks · active-active survivors must carry the full load · **tabletop** talks, **validation test** proves.

## Monitoring (3.2)

| Question | Tool |
|---|---|
| What's unusual? | Baseline first, then anomaly alerts |
| Top talkers, who talked to whom | **Flow data** (NetFlow, IPFIX) |
| What was actually said | **Packet capture** (needs port mirroring or a tap) |
| Device health on a schedule | **SNMP** polling 161, traps 162 · **v3** = authentication + encryption |
| Central logs | **Syslog** UDP 514 · severity 0 Emergency → 7 Debug · level 4 sends 0–4 |
| Correlate across sources | **SIEM** |

Availability = up · **performance** = latency, jitter, loss · discovery: **ad hoc** once, **scheduled** regularly.

## Network Services (3.4)

**DHCP** DORA, UDP 67/68 · a reservation gives a fixed address and still delivers options · new devices on 169.254 = **scope exhausted** · one VLAN on 169.254 = **relay** · **DNS** A/AAAA, CNAME, MX, PTR, TXT · stale answers = cache/TTL · **DNSSEC** = integrity, **DoH/DoT** = privacy · **NTP** 123 (ms) · **PTP** (µs) · **NTS** (trusted time) · SLAAC: router gives prefix, host builds address.

## Access and Management (3.5)

Site-to-site = networks · client-to-site = users · clientless = browser · **full tunnel** = all traffic inspected · **split** = internet direct · **console** for new or broken devices · **SSH** 22 · **jump box** = one hardened, logged hop · **out-of-band** = separate path (a management VLAN is still in-band).

## Top Traps

- "RTO" for "one hour of data lost." That's RPO.
- "A tabletop proves the backup restores." Only a validation test does.
- "Compare against the last backup." Use the golden config.
- "Packet capture for a month of top talkers." Use flow data.
- "Promiscuous mode" on a switch port. Configure mirroring.
- "Split tunnel" when all traffic must be inspected. Full tunnel.
- "Decrease MTBF." Raise it.
- "SSH into the brand-new switch." Use the console.

---

# Domain 4 Cheat Sheet: Network Security

*14% of the exam · Objectives 4.1–4.3 · Taught in Sessions 13 and 14*

**The habit:** name the attack from its one defining clue, then pick the control that touches that exact spot. One more layer beats one stronger layer.

## Concepts (4.1)

- **Vulnerability** = weakness · **threat** = who or what · **exploit** = the method · **risk** = likelihood × impact · **CIA**: confidentiality, integrity, availability.
- **Self-signed** certificate still encrypts; the warning is about identity. Fix: trusted CA, or install the internal root.
- **MFA** = two different categories (know, have, are). Password + PIN = one factor.
- **RADIUS** UDP 1812/1813, network access, encrypts the password only · **TACACS+** TCP 49, device admin, per-command, encrypts everything.
- **Least privilege** = the principle · **RBAC** = permissions on roles · honeypot (one decoy) vs. honeynet (many).
- **PCI DSS** = card data anywhere · **GDPR** = EU personal data · **data locality** = where it may be stored · can't patch it (IoT, ICS) = **isolate it**.

## Attacks (4.2)

| Attack | Defining Clue | Stopped By |
|---|---|---|
| DoS vs. DDoS | One source vs. thousands, link full | Rate limits vs. upstream scrubbing |
| MAC flooding | CAM table full, traffic on every port | Port security |
| ARP spoofing | Gateway IP shows the wrong MAC | Dynamic ARP inspection (DAI)* |
| Rogue DHCP | Wrong subnet or gateway from DHCP | DHCP snooping* |
| Switch spoofing | Port negotiates a trunk (DTP) | Access mode + nonegotiate* |
| Double tagging | Two tags, native VLAN, one-way | Unused native VLAN* |
| Rogue AP vs. evil twin | Plugged into your LAN vs. your SSID on their network | 802.1X, wireless intrusion prevention vs. WPA3-Enterprise |
| DNS poisoning | Right name, wrong IP | DNSSEC |
| Worm vs. virus | Spreads itself vs. needs a user | Patch, segment vs. endpoint protection |

*\* Taught in Session 14 beyond the objectives: know the attack, and the defense name if it's offered.*

## Defenses (4.3)

- **Harden:** change defaults · **shut unused ports** (beats port security for an empty jack) · SSH only · SNMPv3 · patch.
- **Port security:** default max 1, violation shutdown · **protect** silent · **restrict** logs · **shutdown** err-disables.
- **802.1X:** supplicant (device) → authenticator (switch, AP) → authentication server (RADIUS) · **NAC** quarantines unhealthy devices.
- **Keys:** someone who knew a shared key left → **rotate** it.
- **ACLs:** first match wins, implicit deny · standard near destination, extended near source · wildcard = inverse mask.
- **URL filtering** for sites and categories · **content filtering** for file types and data · public servers in the **screened subnet (DMZ)**.

## Top Traps

- "Threat" for a missing patch. It's a vulnerability.
- "Self-signed means unencrypted." It's an identity warning.
- "RADIUS for per-command admin." TACACS+.
- "ARP poisoning" for a full MAC table. MAC flooding.
- "Rogue AP" for a fake SSID outside. Evil twin.
- "The RADIUS server is the authenticator." The switch is.
- "Disable the leaver's account" for a shared key. Rotate the key.
- "An ACL to block a website category." URL filtering.

---

# Domain 5 Cheat Sheet: Network Troubleshooting

*24% of the exam, the biggest domain · Objectives 5.1–5.5 · Taught in Sessions 1, 15 and 16*

**The habit:** place the technician in the seven steps before you read the choices, then read the clue's layer. What changed? Start there.

## The Method (5.1)

1 **Identify** (gather information, question users, what changed, one problem at a time) → 2 **Theory** (question the obvious; top-to-bottom, bottom-to-top, divide and conquer) → 3 **Test** (not confirmed: new theory or escalate) → 4 **Plan** and potential effects → 5 **Implement** or escalate → 6 **Verify full system functionality**, preventive measures → 7 **Document** findings, actions, outcomes, lessons.

## Cables and Interfaces (5.2)

| Clue | Cause |
|---|---|
| Lower speed than expected | Wrong cable category or fiber type |
| Errors on a schedule or near a machine | Interference (EMI) |
| Passes continuity, fails under load | Split pair; use a certifier |
| CRC + runts (full side), late collisions (half side) | Duplex mismatch |
| Giants | MTU mismatch |
| Output drops | Congestion |
| Administratively down / err-disabled | Someone typed shutdown / switch shut it (remove the cause) |
| PoE fails after adding devices | Power budget exceeded |
| New fiber link dark | Transceiver mismatch or TX/RX transposed |

## Network Issues (5.3)

Loop = network down, MAC flapping · slow after a new switch = **root bridge** · wrong VLAN = link up, no gateway · one traffic type fails = **ACL** · route choice = longest prefix, then AD · trace stops after hop 1 = **return route** · **169.254** = no DHCP (pool, server, VLAN), not DNS · local OK, remote fails = gateway · works by IP, not name = **DNS** · comes and goes = **duplicate IP**.

## Performance (5.4)

**Bottleneck** = slowest link; upgrade only it · **latency** = delay · **jitter** = variation in delay (pings jumping from 20 to 200 ms) · **loss** = missing replies · voice: < 150 ms, < 30 ms jitter, < 1% loss → QoS · strong signal + slow = **channel overlap** · weak signal = coverage · drops only while moving = **roaming settings** (SSID, security, VLAN).

## Tools (5.5)

| Question | Tool |
|---|---|
| Which cable / is it wired right / meets the category? | Toner / cable tester / certifier |
| Fiber break: short run / long run | Visual fault locator / OTDR |
| My IP settings | ipconfig /all (Windows) · ip addr (Linux) |
| Path / DNS answer / IP to MAC | tracert, traceroute / nslookup, dig / arp -a |
| Which program owns the port | netstat -ano |
| Traffic contents / open ports | Protocol analyzer, tcpdump / Nmap (filtered = firewall) |
| MAC → port · neighbors | show mac-address-table · LLDP (CDP is Cisco only) |

## Top Traps

- "Document" before verifying. Verify comes first.
- "Implement the fix" on an unconfirmed theory. New theory or escalate.
- "Replace the cable" for every counter. Read which counter.
- "DNS is down" for 169.254. It's DHCP.
- "Latency" for ping times that jump around. Jitter.
- "The service is stopped" when Nmap says filtered. A firewall.
- "ipconfig" on Linux. ip addr.
- "CDP" in a mixed-vendor network. LLDP.
