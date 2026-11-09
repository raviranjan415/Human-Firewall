# HUMAN FIREWALL — TERRAFORM IMPLEMENTATION MANUAL
**Technology Priority 1: Declarative Infrastructure as Code (IaC)**
**INT333 DevOps Advanced Configuration Management**

---

## 1. Architectural Role & Technology Priority

**Terraform** is the foundational **Technology Priority 1** component of the Human Firewall platform. It is responsible for declarative provisioning of all underlying cloud and network infrastructure.

The Terraform layer operates strictly before configuration management begins:
1. Provisions isolated Virtual Private Cloud (VPC) network boundaries.
2. Allocates public DMZ subnets for Edge Nginx Load Balancing.
3. Allocates private subnets for stateless Flask application replicas and datastores.
4. Enforces least-privilege security groups and network access control lists.
5. Emits structured outputs that dynamically feed the **Ansible** inventory generator.

---

## 2. Directory Layout & Modular Structure

```
terraform/
├── versions.tf                        # Terraform version & provider constraints
├── providers.tf                       # AWS / Cloud provider definition with tagging
├── main.tf                            # Root composition and local values
├── variables.tf                       # Root variables with validation rules
├── outputs.tf                         # Outputs & machine-readable Ansible inventory map
├── network.tf                         # VPC, Subnets, Gateways, Route Tables
├── security.tf                        # Edge LB, App Cluster, and Data Security Groups
├── compute.tf                         # EC2 Compute instances & Key Pairs
├── modules/
│   ├── vpc/                           # Reusable VPC module
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── security/                      # Reusable security group module
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── compute/                       # Reusable compute replica module
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── environments/
│   ├── dev/                           # 1 replica, t3.micro, small CIDR
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── terraform.tfvars
│   ├── staging/                       # 2 replicas, t3.small, staging CIDR
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── terraform.tfvars
│   └── production/                    # 3 replicas, t3.medium, multi-AZ production
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── terraform.tfvars
├── scripts/
│   └── generate_ansible_inventory.py  # Bridge script generating Ansible hosts.ini
└── reports/
    └── last_run.json                  # Telemetry read by Admin DevOps Console
```

---

## 3. Network & Security Architecture

### 3.1 Network Topology (`network.tf`)
- **VPC CIDR**: `10.0.0.0/16` (Production)
- **Public Subnets**: `10.0.1.0/24`, `10.0.2.0/24` (Multi-AZ DMZ hosting Nginx Load Balancers)
- **Private Subnets**: `10.0.10.0/24`, `10.0.11.0/24` (Isolated application replicas & databases)
- **Internet Gateway**: Attached to VPC; public route table defaults `0.0.0.0/0` to gateway.

### 3.2 Security Group Firewall Rules (`security.tf`)
1. **Edge Load Balancer (`aws_security_group.lb`)**:
   - Ingress: Port 80 (HTTP) and Port 443 (HTTPS) from `0.0.0.0/0`.
   - Egress: Full outbound to internal VPC.
2. **Application Cluster (`aws_security_group.app`)**:
   - Ingress: Port 5000 (Gunicorn WSGI) **restricted exclusively** to `aws_security_group.lb.id`.
   - Ingress: Port 22 (SSH) restricted to authorized management CIDR.
   - Egress: Outbound to database and Internet for package updates.
3. **Data Persistence Tier (`aws_security_group.data`)**:
   - Ingress: Port 5432 (PostgreSQL) and Port 6379 (Redis) **restricted exclusively** to `aws_security_group.app.id`.
   - **Zero direct Internet ingress**; completely insulated from external traffic.

---

## 4. Multi-Environment Separation

| Parameter | Development (`dev/`) | Staging (`staging/`) | Production (`production/`) |
|---|---|---|---|
| **VPC CIDR** | `10.10.0.0/16` | `10.20.0.0/16` | `10.0.0.0/16` |
| **Instance Type** | `t3.micro` | `t3.small` | `t3.medium` |
| **App Replicas** | 1 | 2 | 3 |
| **State File** | `dev/terraform.tfstate` | `staging/terraform.tfstate` | `production/terraform.tfstate` |

---

## 5. Integration with Ansible Dynamic Inventory

Terraform outputs a machine-readable data block:
```hcl
output "ansible_inventory" {
  value = {
    loadbalancers = [ { name = "...", public_ip = "...", private_ip = "..." } ]
    webservers    = [ { name = "...", private_ip = "...", replica_id = 1 } ]
    dbservers     = [ { name = "...", private_ip = "..." } ]
  }
}
```

The bridge script executes automatically:
```bash
python terraform/scripts/generate_ansible_inventory.py
```
This writes `ansible/inventory/hosts.ini` and `ansible/inventory/hosts.json`, seamlessly transferring host metadata to Ansible.

---

## 6. Execution Commands & Operational Workflow

### 6.1 Formatting & Validation
```bash
cd terraform
# Format all configuration files
terraform fmt -recursive

# Initialize providers
terraform init -backend=false

# Validate configuration syntax
terraform validate
```

### 6.2 Planning & Deployment
```bash
# Generate execution plan
terraform plan -out=tfplan.binary

# Apply infrastructure changes
terraform apply tfplan.binary

# Extract outputs to JSON
terraform output -json > reports/last_run.json
```

### 6.3 Offline Validation Mode
The provider configuration contains:
```hcl
skip_credentials_validation = true
skip_metadata_api_check     = true
skip_requesting_account_id  = true
```
This enables full static analysis, module compiling, and validation without requiring active cloud payment credentials.

