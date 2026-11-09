# Human Firewall — AWS Production Deployment Manual

This guide walks you through deploying the complete **Terraform + Ansible + Puppet** DevOps architecture directly onto your real **Amazon Web Services (AWS)** account.

---

## 🏗️ Architecture on AWS

When applied to AWS, Terraform provisions:
1. **Dedicated Virtual Private Cloud (VPC)**: `10.0.0.0/16` with DNS hostnames and resolution enabled.
2. **Internet Gateway (IGW)**: Direct high-speed routing to the public internet.
3. **Public DMZ Subnets**: `10.0.1.0/24` and `10.0.2.0/24` across multiple Availability Zones.
4. **Security Groups**:
   - `lb-sg`: Ingress HTTP (80) and HTTPS (443) from `0.0.0.0/0`.
   - `app-sg`: Ingress Port 5000 strictly from the Load Balancer security group.
   - `db-sg`: Ingress PostgreSQL (5432) and Redis (6379) strictly from Application Replicas.
   - `ssh-sg`: Ingress SSH (22) for Ansible automation and administration.
5. **EC2 Instances (AWS Free Tier Eligible - `t3.micro` / `t2.micro`)**:
   - **Nginx Edge Load Balancer**: Forwarding traffic to replicas using `least_conn`.
   - **Flask Application Replicas**: 2 active application nodes.
   - **Database Host**: PostgreSQL 16 & Redis datastore.

---

## 🚀 Option 1: 1-Click Deployment Wizard from Windows (Easiest)

We built an automated deployment engine directly into your repository:

### Step 1: Run the Deployer Script
In **Command Prompt (`cmd`)** or **PowerShell**:
```cmd
deploy_aws
```
*(or run `.venv\Scripts\python scripts/aws_deployer.py`)*

### Step 2: Enter Your AWS IAM Credentials
The wizard will ask for:
1. **AWS Access Key ID**: e.g., `AKIA...`
2. **AWS Secret Access Key**: e.g., `wJalrXUtnFEMI...`
3. **Target Region**: e.g., `ap-south-1` (Mumbai) or `us-east-1` (N. Virginia)

*(If you don't have an Access Key yet, log in to **AWS Console** $\to$ **IAM** $\to$ **Users** $\to$ **Security Credentials** $\to$ **Create Access Key**).*

### Step 3: Automated Execution
The script automatically:
* Checks for `terraform.exe` (downloads the official standalone binary to `bin/` if not present).
* Generates an SSH keypair for EC2 access.
* Runs `terraform init` and `terraform apply`.
* Prints your **Live AWS Public Application URL** (e.g. `http://13.233.xx.xx`).
* Generates the live Ansible inventory at [`ansible/inventory/hosts.ini`](file:///d:/human-firewall/ansible/inventory/hosts.ini).

---

## ☁️ Option 2: Using AWS CloudShell (Zero Setup / No Download Needed)

If you prefer not to enter keys on your local computer, you can run directly inside AWS:

1. Open **[https://console.aws.com](https://console.aws.com)** in your browser and log in.
2. Click the **CloudShell** icon `>_` at the top right of the navigation bar.
3. In the CloudShell terminal, clone or upload your project files:
   ```bash
   git clone <your-repo-url>
   cd human-firewall/terraform
   ```
4. Run Terraform directly (CloudShell is already authenticated with your AWS account!):
   ```bash
   terraform init
   terraform apply \
     -var="skip_credentials_validation=false" \
     -var="skip_metadata_api_check=false" \
     -var="skip_requesting_account_id=false"
   ```
5. Terraform will output:
   ```hcl
   app_url = "http://13.233.x.x"
   load_balancer_public_ip = "13.233.x.x"
   ```
6. Open the `app_url` in your browser to view your live platform on AWS!

---

## 🧹 Cost Management & Teardown (Avoid AWS Billing)

Once your academic viva or project demonstration is complete, destroy the AWS resources to avoid ongoing cloud costs:

### From Windows:
Run:
```cmd
deploy_aws
```
Select **Option 2: Teardown / Destroy**.

### From CloudShell / Terminal:
```bash
cd terraform
terraform destroy -auto-approve \
  -var="skip_credentials_validation=false" \
  -var="skip_metadata_api_check=false" \
  -var="skip_requesting_account_id=false"
```
All VPCs, Subnets, and EC2 instances will be immediately terminated.

