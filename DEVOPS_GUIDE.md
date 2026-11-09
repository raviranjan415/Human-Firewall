# HUMAN FIREWALL — DEVOPS PRACTITIONER GUIDE
**Master Operations & Engineering Manual | INT333 DevOps Advanced Configuration Management**

---

## 1. Introduction & Engineering Objectives

The **Human Firewall** platform combines advanced configuration management with a gamified cybersecurity awareness suite. This guide serves as the primary operational handbook for DevOps Architects, Site Reliability Engineers, and System Administrators managing the platform.

### Core Architectural Mandates
1. **Terraform** provisions all infrastructure declaratively.
2. **Ansible** automates machine configuration, security baseline rollout, and application deployment.
3. **Puppet** continuously enforces desired-state compliance and heals configuration drift.
4. **Nginx** load-balances traffic across multiple Flask WSGI replicas using least-connections.
5. **Prometheus & Grafana** provide live observability and SRE telemetry.

---

## 2. Quickstart: End-to-End Pipeline in One Command

To execute the entire automated lifecycle (Terraform inventory generation &rarr; Ansible verification &rarr; Puppet drift reconciliation &rarr; SRE health check):

```bash
# Execute master orchestrator
python scripts/devops_orchestrator.py
```

Expected output:
```
================================================================================
HUMAN FIREWALL — FULL STACK DEVOPS CONTINUOUS DEPLOYMENT PIPELINE
Terraform (IaC) -> Ansible (Config) -> Puppet (State) -> Verification
================================================================================
>>> [21:01:31] STAGE 1: Terraform Infrastructure as Code...
    ✓ STAGE 1: Terraform Infrastructure as Code COMPLETED SUCCESSFULLY.
>>> [21:01:31] STAGE 2: Ansible Configuration & Deployment...
    ✓ STAGE 2: Ansible Configuration & Deployment COMPLETED SUCCESSFULLY.
>>> [21:01:31] STAGE 3: Puppet Desired-State Enforcement...
    ✓ STAGE 3: Puppet Desired-State Enforcement COMPLETED SUCCESSFULLY.
>>> [21:01:31] STAGE 4: End-to-End Application Health Check...
    ✓ STAGE 4: End-to-End Application Health Check COMPLETED SUCCESSFULLY.
================================================================================
PIPELINE RUN FINISHED — STATUS: SUCCESS
================================================================================
[+] Pipeline telemetry written to: instance/devops_reports/latest_pipeline_run.json
```

---

## 3. Individual Component Execution

### 3.1 Provisioning with Terraform
```bash
cd terraform/environments/production
terraform init -backend=false
terraform validate
terraform plan
# Generate inventory for Ansible
python ../../scripts/generate_ansible_inventory.py
```

### 3.2 Configuring with Ansible
```bash
cd ansible
# Verify syntax of all playbooks
ansible-playbook -i inventory/hosts.ini playbooks/site.yml --syntax-check
# Run deployment playbook (dry run)
ansible-playbook -i inventory/hosts.ini playbooks/deploy.yml --check
```

### 3.3 Enforcing Desired-State with Puppet
```bash
# Execute configuration drift detection and automated remediation
python puppet/scripts/drift_demo.py
```

### 3.4 Running via Docker Compose
```bash
# Start Nginx load balancer, 3 Flask replicas, PostgreSQL, and Redis
docker compose up -d

# Check cluster status
docker compose ps

# View Nginx upstream distribution logs
docker compose logs -f load_balancer
```

---

## 4. Admin DevOps Console (`/admin/devops`)

Administrators with the `admin` role can access the real-time DevOps management console:
- **URL**: `http://localhost:5000/admin/devops`
- **Features**:
  - Live inspection of Terraform provisioned VPC, subnets, and instances.
  - Ansible host task success/changed statistics.
  - Puppet continuous compliance percentage and drift event history.
  - Live button to trigger a Puppet Configuration Drift check on demand.
  - Live button to execute the full Continuous Delivery pipeline.
  - Live host CPU, RAM, and database latency telemetry.

---

## 5. Troubleshooting & Incident Runbooks

| Incident Scenario | Primary Symptom | Diagnostic Command | Remediation Action |
|---|---|---|---|
| **Replica Health Probe Failure** | HTTP 502 Bad Gateway from Nginx | `curl -f http://localhost:5000/healthz` | Inspect `/app/logs`, verify PostgreSQL connection string in `.env`, restart WSGI unit. |
| **Configuration Drift Alert** | Puppet compliance drops below 100% | `python puppet/scripts/drift_demo.py` | Trigger Puppet catalog apply; verify unauthorized operator edits in `/etc/ssh/sshd_config`. |
| **Database Pool Exhaustion** | Latency $> 500\text{ms}$ or `pool_timeout` | Query `/metrics` metric `human_firewall_database_status` | Increase PostgreSQL `max_connections` in `ansible/group_vars/dbservers.yml` and restart Postgres. |
| **Session Invalidation Across Replicas** | User logged out upon hitting different replica | Check `SECRET_KEY` environment variable across replicas | Ensure all Flask replicas share identical `SECRET_KEY` and Redis session store. |

