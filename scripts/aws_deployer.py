#!/usr/bin/env python3
"""Human Firewall — Interactive AWS Real-Cloud Deployment Engine.

Automates end-to-end real cloud provisioning on Amazon Web Services:
1. Validates AWS IAM Access Credentials.
2. Ensures Terraform binary is present (downloads official binary to bin/ if needed).
3. Configures SSH Keypair for Ansible management.
4. Executes `terraform init` and `terraform apply` against real AWS infrastructure.
5. Synthesizes live Ansible inventory (`ansible/inventory/hosts.ini`) from AWS EC2 instances.
6. Displays the live public URL and offers 1-click teardown (`terraform destroy`).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TF_DIR = BASE_DIR / "terraform"
BIN_DIR = BASE_DIR / "bin"
ANSIBLE_DIR = BASE_DIR / "ansible"

TERRAFORM_VERSION = "1.8.5"
TERRAFORM_ZIP_URL = f"https://releases.hashicorp.com/terraform/{TERRAFORM_VERSION}/terraform_{TERRAFORM_VERSION}_windows_amd64.zip"


def print_banner(msg: str):
    print("\n" + "=" * 70)
    print(f"  {msg}")
    print("=" * 70)


def ensure_terraform_binary() -> Path:
    """Finds terraform in PATH or downloads standalone terraform.exe into bin/."""
    # 1. Check system PATH
    found = shutil.which("terraform")
    if found:
        print(f"✓ Using system Terraform: {found}")
        return Path(found)

    # 2. Check local bin/ folder
    BIN_DIR.mkdir(parents=True, exist_ok=True)
    local_tf = BIN_DIR / "terraform.exe"
    if local_tf.exists():
        print(f"✓ Using local Terraform binary: {local_tf}")
        return local_tf

    # 3. Download standalone zip from HashiCorp
    print(f"➜ Terraform not found in PATH. Downloading official standalone v{TERRAFORM_VERSION}...")
    zip_path = BIN_DIR / "terraform.zip"
    try:
        urllib.request.urlretrieve(TERRAFORM_ZIP_URL, zip_path)
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extract("terraform.exe", BIN_DIR)
        if zip_path.exists():
            zip_path.unlink()
        print(f"✓ Downloaded and extracted: {local_tf}")
        return local_tf
    except Exception as exc:
        print(f"⚠️ Could not automatically download Terraform: {exc}")
        print("Please install Terraform manually or install via: winget install HashiCorp.Terraform")
        sys.exit(1)


def get_or_generate_ssh_key() -> tuple[str, Path]:
    """Retrieves an existing SSH public key or generates one for AWS EC2 access."""
    ssh_dir = Path.home() / ".ssh"
    ssh_dir.mkdir(parents=True, exist_ok=True)

    for key_name in ["id_ed25519.pub", "id_rsa.pub"]:
        candidate = ssh_dir / key_name
        if candidate.exists():
            pub_content = candidate.read_text().strip()
            print(f"✓ Using existing SSH key: {candidate}")
            return pub_content, candidate.with_suffix("")

    # Generate new ed25519 keypair
    priv_key = ssh_dir / "human_firewall_aws_ed25519"
    pub_key = ssh_dir / "human_firewall_aws_ed25519.pub"
    print("➜ Generating new dedicated SSH keypair for AWS EC2 instances...")
    try:
        subprocess.run(
            ["ssh-keygen", "-t", "ed25519", "-f", str(priv_key), "-N", "", "-C", "human-firewall-aws"],
            check=True,
            capture_output=True,
        )
        print(f"✓ Created new SSH key: {pub_key}")
        return pub_key.read_text().strip(), priv_key
    except Exception:
        # Fallback dummy key for plan validation
        fallback = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIExampleDevOpsKeyHumanFirewall2026 devops@aws"
        return fallback, priv_key


def prompt_aws_credentials() -> dict[str, str]:
    """Prompts or reads AWS credentials from environment or user input."""
    print_banner("AWS ACCOUNT CREDENTIALS CONFIGURATION")

    access_key = os.environ.get("AWS_ACCESS_KEY_ID", "").strip()
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "").strip()
    region = os.environ.get("AWS_DEFAULT_REGION", "ap-south-1").strip()

    if access_key and secret_key:
        print(f"✓ Found existing AWS credentials in environment for region: {region}")
        use_env = input("Use these credentials? (Y/n): ").strip().lower()
        if use_env in ("", "y", "yes"):
            return {"access_key": access_key, "secret_key": secret_key, "region": region}

    print("\nPlease enter your AWS IAM Access Keys (Free-tier eligible):")
    print("If you don't have them yet:")
    print("1. Log in to https://console.aws.com")
    print("2. Go to IAM -> Users -> Your User -> Security Credentials -> Create Access Key")
    print("-" * 70)

    while not access_key:
        access_key = input("Enter AWS Access Key ID (e.g. AKIA...): ").strip()
    while not secret_key:
        secret_key = input("Enter AWS Secret Access Key: ").strip()

    custom_region = input(f"Enter AWS Region [default: {region}]: ").strip()
    if custom_region:
        region = custom_region

    return {"access_key": access_key, "secret_key": secret_key, "region": region}


def deploy_infrastructure(tf_bin: Path, creds: dict[str, str], pub_key: str):
    """Executes Terraform init, plan, and apply to provision real AWS resources."""
    print_banner("PROVISIONING REAL INFRASTRUCTURE ON AWS (TERRAFORM)")

    env = os.environ.copy()
    env["AWS_ACCESS_KEY_ID"] = creds["access_key"]
    env["AWS_SECRET_ACCESS_KEY"] = creds["secret_key"]
    env["AWS_DEFAULT_REGION"] = creds["region"]

    # 1. Terraform Init
    print("➜ Running: terraform init...")
    res = subprocess.run([str(tf_bin), "init"], cwd=TF_DIR, env=env)
    if res.returncode != 0:
        print("❌ terraform init failed. Check network connectivity.")
        return False

    # 2. Terraform Plan
    tf_vars = [
        "-var", f"aws_region={creds['region']}",
        "-var", "skip_credentials_validation=false",
        "-var", "skip_metadata_api_check=false",
        "-var", "skip_requesting_account_id=false",
        "-var", "deploy_in_public_subnets=true",
        "-var", f"ssh_public_key={pub_key}",
    ]

    print("\n➜ Running: terraform plan on real AWS...")
    subprocess.run([str(tf_bin), "plan"] + tf_vars, cwd=TF_DIR, env=env, check=True)

    confirm = input("\nDo you want to proceed and APPLY these real resources on AWS? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deployment aborted by user. No resources created.")
        return False

    # 3. Terraform Apply
    print("\n➜ Applying configuration on AWS (creating VPC, Subnets, Security Groups, EC2)...")
    subprocess.run([str(tf_bin), "apply", "-auto-approve"] + tf_vars, cwd=TF_DIR, env=env, check=True)

    # 4. Extract Outputs
    print("\n➜ Querying Terraform outputs...")
    out_res = subprocess.run([str(tf_bin), "output", "-json"], cwd=TF_DIR, env=env, capture_output=True, text=True)
    if out_res.returncode == 0:
        outputs = json.loads(out_res.stdout)
        app_url = outputs.get("app_url", {}).get("value", "N/A")
        lb_ip = outputs.get("load_balancer_public_ip", {}).get("value", "N/A")
        replicas = outputs.get("app_replica_public_ips", {}).get("value", [])

        print_banner("🎉 REAL AWS INFRASTRUCTURE DEPLOYED SUCCESSFULLY!")
        print(f"  Public App URL : {app_url}")
        print(f"  Nginx Load Balancer IP : {lb_ip}")
        print(f"  Application Replicas   : {', '.join(replicas) if replicas else 'Provisioned'}")
        print("=" * 70)

        # 5. Generate Real Ansible Inventory
        print("\n➜ Generating production Ansible inventory with live AWS IPs...")
        inv_script = TF_DIR / "scripts" / "generate_ansible_inventory.py"
        subprocess.run([sys.executable, str(inv_script)], cwd=BASE_DIR, check=True)
        print(f"✓ Live inventory generated at: {ANSIBLE_DIR / 'inventory' / 'hosts.ini'}")

        print("\nTo tear down all resources when your presentation is complete:")
        print(f"  cd terraform && {tf_bin} destroy -auto-approve")
        return True

    return False


def teardown_infrastructure(tf_bin: Path, creds: dict[str, str]):
    """Destroys all provisioned AWS resources to eliminate any cloud billing."""
    print_banner("TEARING DOWN REAL AWS INFRASTRUCTURE (TERRAFORM DESTROY)")
    confirm = input("Are you SURE you want to destroy all AWS resources? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Teardown cancelled.")
        return

    env = os.environ.copy()
    env["AWS_ACCESS_KEY_ID"] = creds["access_key"]
    env["AWS_SECRET_ACCESS_KEY"] = creds["secret_key"]
    env["AWS_DEFAULT_REGION"] = creds["region"]

    tf_vars = [
        "-var", f"aws_region={creds['region']}",
        "-var", "skip_credentials_validation=false",
        "-var", "skip_metadata_api_check=false",
        "-var", "skip_requesting_account_id=false",
        "-var", "deploy_in_public_subnets=true",
    ]

    subprocess.run([str(tf_bin), "destroy", "-auto-approve"] + tf_vars, cwd=TF_DIR, env=env, check=True)
    print("✓ All AWS resources destroyed successfully. Zero ongoing cloud costs.")


def main():
    print_banner("HUMAN FIREWALL — AWS DEVOPS PRODUCTION DEPLOYER")
    print("This tool deploys Terraform, Ansible, and Puppet infrastructure directly to your AWS Account.\n")
    print("Options:")
    print("1. Deploy fresh infrastructure to AWS (Terraform Apply)")
    print("2. Teardown / Destroy existing infrastructure on AWS (Terraform Destroy)")
    print("3. Exit")

    choice = input("\nSelect option (1-3) [default: 1]: ").strip() or "1"
    if choice == "3":
        print("Exiting.")
        return

    tf_bin = ensure_terraform_binary()
    creds = prompt_aws_credentials()
    pub_key, _ = get_or_generate_ssh_key()

    if choice == "1":
        deploy_infrastructure(tf_bin, creds, pub_key)
    elif choice == "2":
        teardown_infrastructure(tf_bin, creds)


if __name__ == "__main__":
    main()

