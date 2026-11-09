# HUMAN FIREWALL — ADVANCED DEVOPS CONFIGURATION MANAGEMENT & CYBERSECURITY AWARENESS PLATFORM

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue.svg)](.github/workflows/ci-cd.yml)
[![Terraform](https://img.shields.io/badge/IaC-Terraform%201.7-844FBA.svg)](TERRAFORM_IMPLEMENTATION.md)
[![Ansible](https://img.shields.io/badge/Automation-Ansible%202.16-EE0000.svg)](ANSIBLE_IMPLEMENTATION.md)
[![Puppet](https://img.shields.io/badge/Desired--State-Puppet%208.4-FFAE1A.svg)](PUPPET_IMPLEMENTATION.md)
[![Docker](https://img.shields.io/badge/Container-Docker%20Compose-2496ED.svg)](docker-compose.yml)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/Course-INT333%20DevOps-green.svg)](#)

> **"Enjoy with Safety — Play Smart, Stay Cyber Safe!"**  
> An enterprise-grade, scalable cybersecurity awareness and training platform engineered with a strict **Tripartite DevOps Configuration Management Engine**: **Terraform** (IaC), **Ansible** (Automation), and **Puppet** (Desired-State Enforcement).

---

## 🌟 Technology Hierarchy & Core Priorities

The core architecture prioritizes three foundational DevOps technologies:

1. **[TERRAFORM (Primary 1)](TERRAFORM_IMPLEMENTATION.md)**: Declarative Infrastructure as Code (IaC) provisioning isolated VPCs, multi-tier subnets, zero-trust security groups, and compute instances with dynamic Ansible inventory emission.
2. **[ANSIBLE (Primary 2)](ANSIBLE_IMPLEMENTATION.md)**: Agentless configuration automation, security baseline hardening, and zero-downtime rolling deployment of the Flask application across replicas (`serial: 1`) across 9 modular roles.
3. **[PUPPET (Primary 3)](PUPPET_IMPLEMENTATION.md)**: Continuous desired-state compliance management, catalog compilation via Hiera 5, and automated **configuration drift detection & self-healing remediation**.

### Supporting Enterprise Stack
- **Ingress & Load Balancing**: Nginx Reverse Proxy (`least_conn` algorithm with health probes).
- **Application Server**: Python 3.13 Flask WSGI with Gunicorn (4 workers, unprivileged UID 10001).
- **Datastores**: PostgreSQL 16 (ACID relational persistence) + Redis 7 (distributed rate limiting & session cache).
- **Observability**: Prometheus metrics exporter (`/metrics`) + Grafana telemetry dashboards.
- **Performance Benchmarking**: Locust load testing suite.

---

## 🎮 30 Interactive Cybersecurity Awareness Games

Human Firewall features **30 genuinely playable games** spanning 5 core threat vectors. Each game includes beginner/intermediate/advanced levels, server-side grading, debriefs, and full bilingual English/Hindi support:

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

### Category E — Privacy and Security Operations
24. **Data Privacy Guardian** (`data-privacy-guardian`): Uphold data minimization and PII protection (GDPR / DPDP).
25. **Backup and Recovery Mission** (`backup-recovery-mission`): Implement the 3-2-1 backup strategy with immutable snapshots.
26. **Cloud Misconfiguration Hunt** (`cloud-misconfiguration-hunt`): Detect open S3 buckets and exposed 0.0.0.0/0 database ports.
27. **Insider Threat Investigation** (`insider-threat-investigation`): Spot off-hours mass repository downloads by departing staff.
28. **Secure Coding Challenge** (`secure-coding-challenge`): Remove hardcoded secrets and disable interactive production debuggers.
29. **Cybersecurity Escape Room** (`cybersecurity-escape-room`): Multi-stage puzzle decoding Base64 wipers and closing backdoors.
30. **Ultimate Human Firewall** (`ultimate-human-firewall`): Grand Capstone: Defeat a coordinated multi-vector APT attack.

---

## ⚙️ DevOps Tripartite Architecture & Workflow

```
[ Developer Git Push ]
         │
         ▼
[ 1. TERRAFORM ]  --> Provisions VPC, Subnets, SG, EC2 Compute & Emits JSON Outputs
         │
         ▼
[ INVENTORY BRIDGE ] --> `generate_ansible_inventory.py` creates `ansible/inventory/hosts.ini`
         │
         ▼
[ 2. ANSIBLE ]    --> Runs 9 Roles, Hardens OS, Configures Nginx & Deploys Flask Cluster
         │
         ▼
[ 3. PUPPET ]     --> Continuously Enforces Baseline State & Heals Configuration Drift
         │
         ▼
[ VERIFICATION ]  --> Automated SRE Health Checks & Telemetry to `/admin/devops`
```

---

## 🚀 Quickstart & Installation

### Option 1: Native Local Development
```bash
# 1. Clone repository
git clone https://github.com/human-firewall/platform.git
cd platform

# 2. Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database and seed all 30 games
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

Accessible at `http://localhost:5000/admin/devops` for users with the `admin` role:
- **Architecture Overview**: Unified health cards for all 3 technologies.
- **Terraform Tab**: Live VPC, subnets, and instance inventory telemetry.
- **Ansible Tab**: Host task stats (`ok`, `changed`, `failed`) and role breakdown.
- **Puppet Tab**: Compliance percentage, drift event history, and one-click drift check trigger.
- **Application & SRE Tab**: Real-time database latency (ms), host CPU/RAM utilization, and WSGI replica states.

---

## 🧪 Testing & Validation

```bash
# Run full automated test suite (157 passed, 4 skipped)
pytest

# Test 30 games and DevOps dashboard specifically
pytest tests/test_30_games.py tests/test_devops_dashboard.py

# Run Locust load benchmark
locust -f load_testing/locustfile.py --headless -u 100 -r 20 --run-time 1m --host http://127.0.0.1:5000
```

---

## 📚 Complete Project Documentation Index

- **[PROJECT_AUDIT.md](PROJECT_AUDIT.md)**: Comprehensive architectural and security baseline audit.
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
- **[TESTING_REPORT.md](TESTING_REPORT.md)**: Pytest verification, 30 games matrix, and load testing benchmarks.

---

## 📄 License & Academic Attribution
Developed for **INT333 DevOps Advanced Configuration Management**.  
Released under the MIT License.
