# HUMAN FIREWALL — DEVOPS INTEGRATION WORKFLOW SPECIFICATION
**Advanced Configuration Management Integration: Terraform + Ansible + Puppet**

---

## 1. The Integrated DevOps Continuous Lifecycle

The Human Firewall DevOps architecture unites **Terraform**, **Ansible**, and **Puppet** into a single, cohesive, non-overlapping automation pipeline. Each tool operates within its strict architectural domain:

```
[ Developer Git Push ]
         │
         ▼
[ 1. TERRAFORM ]
  - Declares VPC, Subnets, Routing, Security Groups, and Compute Nodes.
  - Provisions AWS / Cloud infrastructure.
  - Generates structured JSON outputs and dynamic inventory data.
         │
         ▼
[ 2. INVENTORY BRIDGE ]
  - `terraform/scripts/generate_ansible_inventory.py` extracts live host IPs.
  - Generates `ansible/inventory/hosts.ini` and `hosts.json`.
         │
         ▼
[ 3. ANSIBLE ORCHESTRATION ]
  - Connects over SSH using unprivileged keypair.
  - Executes 9 modular roles (`common`, `security`, `users`, `firewall`, `docker`, `nginx`, `application`, `database`, `monitoring`).
  - Bootstraps and activates the Puppet agent service.
         │
         ▼
[ 4. PUPPET DESIRED-STATE CONTINUOUS ENFORCEMENT ]
  - Enforces baseline system compliance (`site.pp`, Hiera data).
  - Detects unauthorized manual modifications (configuration drift).
  - Automatically restores declared state without full redeployment.
         │
         ▼
[ 5. HEALTH & SRE VERIFICATION ]
  - Automated probes: Nginx `/lb-status`, Flask `/healthz`, Prometheus `/metrics`.
  - Publishes telemetry to the Admin DevOps Management Dashboard (`/admin/devops`).
```

---

## 2. Tool Boundaries & Separation of Ownership

To prevent configuration collision, ownership is strictly partitioned:

| Tool | Primary Domain | Managed Resources | Execution Pattern |
|---|---|---|---|
| **Terraform** | **Infrastructure as Code (IaC)** | VPC, Subnets, Internet Gateways, Security Groups, EC2 instances, Storage Volumes, Key Pairs | Declarative, plan-and-apply, executed during infrastructure lifecycle |
| **Ansible** | **Configuration Management & Deployment** | OS packages, user creation, Docker Engine, initial app deployment, DB migrations, Gunicorn service | Push-based orchestration over SSH, idempotent task playbooks |
| **Puppet** | **Desired-State Enforcement & Drift Control** | Service states (`nginx`, `ssh`, `ufw`), file permissions (`/etc/shadow`, `/etc/ssh/sshd_config`), kernel sysctl baseline | Continuous declarative agent loop, drift self-healing |

---

## 3. Terraform to Ansible Integration

Terraform outputs the provisioned infrastructure in structured format:
```hcl
output "ansible_inventory" {
  value = {
    loadbalancers = [ ... ]
    webservers    = [ ... ]
    dbservers     = [ ... ]
  }
}
```

The bridge script `terraform/scripts/generate_ansible_inventory.py` translates this data into:
```ini
[loadbalancers]
human-firewall-lb-01 ansible_host=198.51.100.10 private_ip=10.0.1.10

[webservers]
human-firewall-replica-01 ansible_host=10.0.10.11 private_ip=10.0.10.11 replica_id=1
human-firewall-replica-02 ansible_host=10.0.10.12 private_ip=10.0.10.12 replica_id=2
human-firewall-replica-03 ansible_host=10.0.10.13 private_ip=10.0.10.13 replica_id=3

[dbservers]
human-firewall-db-01 ansible_host=10.0.10.50 private_ip=10.0.10.50
```

---

## 4. Ansible to Puppet Activation

Ansible initializes the Puppet agent on managed nodes and compiles the node classification:
1. Ansible installs `puppet-agent` package via `roles/common`.
2. Ansible configures `/etc/puppetlabs/puppet/puppet.conf` pointing to the Puppet master.
3. Ansible triggers the initial Puppet run:
   ```bash
   puppet agent -t --environment production
   ```
4. Puppet takes over ongoing compliance enforcement and drift correction.

---

## 5. Live Configuration Drift Detection & Correction

Configuration drift occurs when an operator or attacker manually modifies files or services outside the automated pipeline (e.g. enabling root SSH login, changing firewall ports, altering file permissions).

### 5.1 Verification Script (`puppet/scripts/drift_demo.py`)
1. **Desired State**: Puppet ensures `/etc/ssh/sshd_config` contains `PermitRootLogin no` with mode `0600`.
2. **Drift Injection**: An unauthorized edit changes `PermitRootLogin yes` and file permissions.
3. **Drift Detection**: The Puppet agent runs an inspection catalog, detects hash mismatch `653e86aa` $\to$ `a653556c`, and flags a critical compliance error.
4. **Automated Remediation**: Puppet re-applies the compiled template from Hiera, restoring `PermitRootLogin no` and mode `0600`.
5. **Audit Telemetry**: The event is recorded in `puppet/reports/drift_report.json` with 100% compliance restored.

---

## 6. Rollback & Disaster Recovery Procedures

### 6.1 Application Rollback
If an application deployment fails during the rolling update:
```bash
# Roll back to the previous stable release commit
ansible-playbook -i inventory/hosts.ini playbooks/deploy.yml -e "app_version=v1.9.8"
```
Because the deployment uses `serial: 1`, at least two replicas remain online serving traffic during updates.

### 6.2 Infrastructure Rollback
To destroy and reprovision degraded infrastructure:
```bash
cd terraform/environments/production
terraform apply -target=aws_instance.app_replicas[0] -replace=aws_instance.app_replicas[0]
```

### 6.3 State File Recovery
Terraform state is versioned in `terraform.tfstate`. If corrupted:
```bash
cp terraform.tfstate.backup terraform.tfstate
terraform refresh
```

