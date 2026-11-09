# HUMAN FIREWALL — COMPLETE DEPLOYMENT GUIDE
**Production Rollout, Multi-Replica Clustering & Cloud Infrastructure**

---

## 1. Prerequisites

### 1.1 Local Development Environment
- Python 3.12 or 3.13
- Git
- Virtual environment (`venv`)

### 1.2 Production Server & Container Prerequisites
- Docker Engine 24+ and Docker Compose 2.20+
- Linux (Ubuntu 22.04 LTS recommended)
- 4 vCPU, 8 GB RAM minimum for multi-replica cluster
- Open incoming ports: 80 (HTTP), 443 (HTTPS), 22 (SSH)

---

## 2. Option A: Local Development Setup

```bash
# 1. Clone repository
git clone https://github.com/human-firewall/platform.git
cd platform

# 2. Create and activate Python virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database and seed all 30 games and content
flask init-db
flask seed

# 5. Launch local server
python run.py
# Server will be live at http://127.0.0.1:5000
```

---

## 3. Option B: High-Availability Docker Multi-Replica Deployment

This deployment spins up:
- 1x Nginx Edge Load Balancer (`least_conn` upstream balancing)
- 3x Flask WSGI Application Replicas (Gunicorn)
- 1x PostgreSQL 16 Database Server
- 1x Redis 7 Distributed Session & Rate-Limiting Cache

```bash
# 1. Configure production environment
cp .env.example .env
# Edit SECRET_KEY and ADMIN_PASSWORD in .env

# 2. Build and launch the containerized stack
docker compose up -d --build

# 3. Verify container health
docker compose ps

# 4. Probe load balancer status
curl http://localhost/lb-status
# Expected response:
# {"status":"healthy","load_balancer":"nginx","algorithm":"least_conn","upstream_replicas":3}

# 5. Probe application metrics
curl http://localhost/metrics
```

---

## 4. Option C: Cloud Infrastructure Provisioning (Terraform & Ansible)

```bash
# 1. Provision Cloud Infrastructure with Terraform
cd terraform/environments/production
terraform init
terraform plan -out=tfplan
terraform apply tfplan

# 2. Export dynamic inventory to Ansible
python ../../scripts/generate_ansible_inventory.py

# 3. Execute Ansible configuration management
cd ../../../ansible
ansible-playbook -i inventory/hosts.ini playbooks/site.yml

# 4. Activate Puppet desired-state enforcement
python ../puppet/scripts/drift_demo.py
```

---

## 5. Verifying High Availability & Session Distribution

1. **Session Persistence Test**:
   - Log in at `http://localhost/auth/login` as `learner1` / `Testing1pass`.
   - Refresh the page multiple times. Inspect Nginx access logs:
     ```bash
     docker compose logs load_balancer
     ```
   - Notice that requests are distributed across `app_replica_1`, `app_replica_2`, and `app_replica_3`, while your session remains completely valid and authenticated.
2. **Graceful Failover Test**:
   - Terminate one replica:
     ```bash
     docker stop human_firewall_replica_1
     ```
   - Navigate to `/games/`. Nginx automatically routes traffic to the surviving replicas within milliseconds, with zero downtime or error pages.

