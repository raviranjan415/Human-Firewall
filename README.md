# HUMAN FIREWALL — IMMERSIVE CYBERSECURITY CAREER SIMULATOR & ENTERPRISE DEVOPS PLATFORM

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue.svg)](.github/workflows/ci-cd.yml)
[![Tests Passing](https://img.shields.io/badge/Tests-172%20Passed-brightgreen.svg)](#-testing--validation)
[![Terraform](https://img.shields.io/badge/IaC-Terraform%201.7-844FBA.svg)](TERRAFORM_IMPLEMENTATION.md)
[![Ansible](https://img.shields.io/badge/Automation-Ansible%202.16-EE0000.svg)](ANSIBLE_IMPLEMENTATION.md)
[![Puppet](https://img.shields.io/badge/Desired--State-Puppet%208.4-FFAE1A.svg)](PUPPET_IMPLEMENTATION.md)
[![Docker](https://img.shields.io/badge/Container-Docker%20Compose-2496ED.svg)](docker-compose.yml)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **"Enjoy with Safety — Play Smart, Stay Cyber Safe!"**  
> **Human Firewall** is an enterprise-grade, realistic cybersecurity simulation and awareness training platform. It transforms passive security training into an engaging **corporate job simulator, interactive animated study classroom, and hands-on defense lab arena** powered by an enterprise **Tripartite DevOps Configuration Management Engine**: **Terraform** (IaC), **Ansible** (Automation), and **Puppet** (Desired-State Compliance).

---

## 🌟 Key Platform Innovations

### 1. 🎬 Interactive Animated Cyber Classrooms & Study Videos
- **Natural Instructor Narration**: Engaging teaching delivery by animated faculty instructors (**Prof. Alex** & **Prof. Maya**), explaining real-world pretexts, threat anatomy, and operational defense rules.
- **Visual Classroom Dynamics**: Digital smartboard diagrams, animated laser pointer highlights, animated student desks, and interactive question-and-answer interactions.
- **Pure Bilingual Separation**: 100% Hindi in Hindi mode, 100% English in English mode — zero bilingual mixing.
- **Accurate Progress Tracking**: Automated progress sync via `/api/videos/<id>/progress`, marking completed lessons with a verified green checkmark (`✓`).

### 2. 🛡️ TryHackMe-Style Compact Defense Rooms
Every lesson features a structured 8-task compact theory room designed for beginner-to-advanced learners:
- **Task A (Learning Objectives)**: 3 clear, actionable competency goals.
- **Task B (Concept Deep Dive & Attack Mechanics)**: Progressive theoretical foundation explaining attack pretexts and mechanics.
- **Task C (Enterprise Incident Scenario)**: Realistic corporate breach case studies and adversary timelines.
- **Task D (Technical Deep Dive)**: Terminology (RFC specs), network protocols/ports table, SOC CLI tools (`dig`, `curl`, `MXToolbox`), and interactive Forensic IOC Matrix.
- **Task E (Practical Investigation Drill)**: 4-step triage drill with exact terminal commands and expected verification outputs.
- **Task F (SOC Analyst Operational Guidelines)**: Tier-1 triage rules, Tier-2 escalation thresholds, and chain of custody standards.
- **Task G (Common Beginner Traps & Mitigations)**: 3 common beginner pitfalls and operational fixes.
- **Task H (Interactive Knowledge Check)**: 3 interactive scenario checks with instant click-to-verify feedback and technical explanations.
- **Statutory Legal Framework**: Full integration of **IT Act 2000 (§66D & §43)**, **RBI Master Circular Zero Liability Protection**, **DPDP Act 2023 (§8)**, and the **Citizen Financial Cyber Fraud Reporting System (1930 Helpline)**.

### 3. 🎮 Dual-Engine Gameplay Across 35 Games
Every game supports two distinct playable modes:
1. **🌐 3D Cyber Simulator**: Immersive 3D corporate office, employee workstations, server rooms, and live CyberWork OS incident response console.
2. **🕹️ 2D Field Patrol**: Retro 2D keyboard-controlled campus patrol and device inspection simulator.

---

## 🎮 35 Interactive Cybersecurity Awareness Games

Spanning 6 core threat vectors with server-side grading, debriefs, and full bilingual support:

### Category A — Social Engineering
1. **Phishing Detective** (`phishing-detective`): Inspect deceptive emails, spoofed sender domains, and concealed links.
2. **Smishing Showdown** (`smishing-showdown`): Detect fake delivery failures, bank suspensions, and shortened URLs.
3. **Vishing Challenge** (`vishing-challenge`): Handle high-pressure voice scams impersonating corporate IT or law enforcement.
4. **Impersonation Trap** (`impersonation-trap`): Identify Business Email Compromise (BEC) and unauthorized bank change requests.
5. **Bait or Truth** (`bait-or-truth`): Differentiate between legitimate open-source tools and trojanized bait.
6. **Deepfake Detective** (`deepfake-detective`): Spot AI voice synthesis, audio anomalies, and emergency wire transfer traps.

### Category B — Identity and Password Security
7. **Password Fortress** (`password-fortress`): Evaluate passphrase entropy against dictionary attacks and credential stuffing.
8. **MFA Guardian** (`mfa-guardian`): Defend against MFA fatigue push-bombing and SIM swapping indicators.
9. **Account Recovery Rescue** (`account-recovery-rescue`): Prevent OSINT reconnaissance from compromising security questions.
10. **Credential Leak Detective** (`credential-leak-detective`): Formulate rapid breach responses to leaked combo dumps.
11. **Access Control Master** (`access-control-master`): Enforce the Principle of Least Privilege (PoLP) and prevent privilege creep.

### Category C — Network and Web Security
12. **Wi-Fi Safety Mission** (`wifi-safety-mission`): Spot Evil Twin rogue access points and captive portal manipulation.
13. **URL Inspector** (`url-inspector`): Detect IDN homograph attacks, lookalike subdomains, and misleading paths.
14. **Browser Security Quest** (`browser-security-quest`): Audit malicious extension permissions and invalid SSL certs.
15. **SQL Injection Shield** (`sql-injection-shield`): Identify SQL syntax tampering and parameterized query defenses.
16. **XSS Defender** (`xss-defender`): Recognize stored and reflected Cross-Site Scripting (XSS) in user inputs.
17. **Network Guardian** (`network-guardian`): Analyze TCP SYN sweeps, port probes, and lateral movement attempts.

### Category D — Malware and Incident Response
18. **Malware Hunter** (`malware-hunter`): Spot double extensions (`.pdf.exe`) and weaponized Office macros.
19. **Ransomware Rescue** (`ransomware-rescue`): Execute physical network isolation to halt encryptor lateral spread.
20. **USB Danger Zone** (`usb-danger-zone`): Defend against BadUSB keystroke injection bait drops in parking lots.
21. **Incident Commander** (`incident-commander`): Master the NIST Incident Response lifecycle (Containment &rarr; Eradication &rarr; Recovery).
22. **Digital Evidence Detective** (`digital-evidence-detective`): Capture live volatile RAM and preserve forensic chain of custody.
23. **SOC Alert Triage** (`soc-alert-triage`): Correlate SIEM telemetry and prioritize critical data exfiltration alerts.

### Category E — Privacy, Cloud and Security Operations
24. **Data Privacy Guardian** (`data-privacy-guardian`): Uphold data minimization and PII protection (GDPR / DPDP).
25. **Backup and Recovery Mission** (`backup-recovery-mission`): Implement the 3-2-1 backup strategy with immutable snapshots.
26. **Cloud Misconfiguration Hunt** (`cloud-misconfiguration-hunt`): Detect open S3 buckets and exposed 0.0.0.0/0 database ports.
27. **Insider Threat Investigation** (`insider-threat-investigation`): Spot off-hours mass repository downloads by departing staff.
28. **Secure Coding Challenge** (`secure-coding-challenge`): Remove hardcoded secrets and disable interactive production debuggers.
29. **Cybersecurity Escape Room** (`cybersecurity-escape-room`): Multi-stage puzzle decoding Base64 wipers and closing backdoors.
30. **Ultimate Human Firewall** (`ultimate-human-firewall`): Grand Capstone: Defeat a coordinated multi-vector APT attack.

### Category F — Executive Honeytraps & C-Suite Fraud (New)
31. **Executive Whaling Incident** (`c-suite-honeytrap-whaling`): Detect urgent C-suite impersonation, acquisition pretexting, and hostile takeover wire requests.
32. **Boardroom Wire Fraud Honeytrap** (`boardroom-wire-fraud-honeytrap`): Defend against out-of-band banking rerouting, dual-custody authorization bypass, and escrow divert fraud.
33. **Field Patrol Security Guard** (`patrol-guard`): Physical access badge auditing and tailgating inspection.
34. **Badge Inspection Challenge** (`badge-inspection`): Physical RFID clone detection and security checkpoint validation.
35. **Tailgating Lockdown** (`tailgate-lockdown`): Turnstile enforcement and unauthorized visitor containment.

---

## ⚙️ DevOps Tripartite Architecture & Workflow

```
[ Developer Git Push ]
         │
         ▼
[ 1. TERRAFORM ]  --> Provisions VPC, Multi-Tier Subnets, Security Groups, EC2 Compute & Emits JSON Outputs
         │
         ▼
[ INVENTORY BRIDGE ] --> `generate_ansible_inventory.py` bridges Terraform outputs to `ansible/inventory/hosts.ini`
         │
         ▼
[ 2. ANSIBLE ]    --> Executes 9 Modular Roles, Hardens OS Baselines, Configures Nginx & Deploys Flask Cluster
         │
         ▼
[ 3. PUPPET ]     --> Continuously Enforces Baseline State & Heals Configuration Drift (Hiera 5)
         │
         ▼
[ VERIFICATION ]  --> Automated SRE Health Checks, Telemetry & Management at `/admin/devops`
```

---

## 🚀 Quickstart & Installation

### Option 1: Native Local Development
```bash
# 1. Clone repository
git clone https://github.com/raviranjan415/Human-Firewall.git
cd Human-Firewall

# 2. Set up virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database and seed all 35 games
flask init-db
flask seed

# 5. Launch application
python run.py
# Navigate to http://127.0.0.1:5000
```

### Option 2: Production Multi-Replica Docker Compose
```bash
# Launch Nginx load balancer + 3 Flask replicas + PostgreSQL 16 + Redis 7
docker compose up -d --build

# Inspect running cluster
docker compose ps

# Test load balancer upstream routing
curl http://localhost/lb-status
```

### Option 3: Continuous DevOps Pipeline Orchestrator
```bash
# Executes Terraform inventory bridge, Ansible checks, Puppet drift demonstration, and SRE health check
python scripts/devops_orchestrator.py
```

### Option 4: Puppet Configuration Drift Demonstration
```bash
# Proves Puppet detects manual unauthorized edits and restores desired state
python puppet/scripts/drift_demo.py
```

---

## 📊 Administrator DevOps Management Console

Accessible at `http://localhost:5000/admin/devops` for authenticated users with the `admin` role:
- **Architecture Overview**: Unified health telemetry across Terraform, Ansible, and Puppet.
- **Terraform Tab**: Live VPC, subnets, and instance inventory telemetry.
- **Ansible Tab**: Host task stats (`ok`, `changed`, `failed`) and role-by-role execution breakdowns.
- **Puppet Tab**: Compliance percentage, drift event history, and one-click drift check trigger.
- **Application & SRE Tab**: Real-time database latency (ms), host CPU/RAM utilization, and WSGI replica states.

---

## 🧪 Testing & Validation

```bash
# Run full automated test suite (172 passed, 4 skipped)
pytest

# Test room experience, human UI, and legal frameworks
pytest tests/test_room_human_ui.py

# Test all games and dual 3D/2D engines
pytest tests/test_30_games.py tests/test_games.py

# Run Locust load benchmark
locust -f load_testing/locustfile.py --headless -u 100 -r 20 --run-time 1m --host http://127.0.0.1:5000
```

---

## 📚 Complete Project Documentation Index

- **[PROJECT_AUDIT.md](PROJECT_AUDIT.md)**: Architectural and security baseline audit.
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Complete system design, topology diagrams, and data flows.
- **[IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md)**: Detailed phase milestones and acceptance criteria.
- **[TERRAFORM_IMPLEMENTATION.md](TERRAFORM_IMPLEMENTATION.md)**: Technology Priority 1 implementation manual.
- **[ANSIBLE_IMPLEMENTATION.md](ANSIBLE_IMPLEMENTATION.md)**: Technology Priority 2 implementation manual.
- **[PUPPET_IMPLEMENTATION.md](PUPPET_IMPLEMENTATION.md)**: Technology Priority 3 implementation manual.
- **[DEVOPS_INTEGRATION.md](DEVOPS_INTEGRATION.md)**: End-to-end integration workflow specification.
- **[DEVOPS_GUIDE.md](DEVOPS_GUIDE.md)**: Practitioner operations and troubleshooting runbooks.
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**: Production deployment and multi-replica clustering guide.
- **[SECURITY.md](SECURITY.md)**: Defense-in-depth, cryptography, and access control specification.
- **[PERFORMANCE_REPORT.md](PERFORMANCE_REPORT.md)**: Algorithmic complexity analysis and query optimizations.
- **[TESTING_REPORT.md](TESTING_REPORT.md)**: Pytest verification, 35 games matrix, and load testing benchmarks.

---

## 👨‍💻 Lead Architect & Developer

**Ravi Ranjan**  
Lead Architect & Security Developer  
- **LinkedIn**: [linkedin.com/in/ravi6745](https://www.linkedin.com/in/ravi6745)  
- **GitHub**: [github.com/raviranjan415](https://github.com/raviranjan415)  

---

## 📄 License & Academic Attribution
Developed for **INT333 DevOps Advanced Configuration Management**.  
Released under the MIT License.
