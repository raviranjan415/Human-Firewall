#!/usr/bin/env python3
"""Terraform to Ansible Dynamic Inventory Integration Bridge.

Extracts infrastructure topology provisioned by Terraform and generates
production-ready Ansible inventory files (`hosts.ini` and `hosts.json`).
"""

import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TF_DIR = BASE_DIR / "terraform"
ANSIBLE_DIR = BASE_DIR / "ansible" / "inventory"


def generate_inventory(tf_output: dict | None = None) -> tuple[Path, Path]:
    ANSIBLE_DIR.mkdir(parents=True, exist_ok=True)
    ini_path = ANSIBLE_DIR / "hosts.ini"
    json_path = ANSIBLE_DIR / "hosts.json"

    # Default topology if state is fresh or offline
    topology = {
        "loadbalancers": [
            {"name": "human-firewall-lb-01", "ansible_host": "198.51.100.10", "private_ip": "10.0.1.10"}
        ],
        "webservers": [
            {"name": "human-firewall-replica-01", "ansible_host": "10.0.10.11", "private_ip": "10.0.10.11", "replica_id": 1},
            {"name": "human-firewall-replica-02", "ansible_host": "10.0.10.12", "private_ip": "10.0.10.12", "replica_id": 2},
            {"name": "human-firewall-replica-03", "ansible_host": "10.0.10.13", "private_ip": "10.0.10.13", "replica_id": 3},
        ],
        "dbservers": [
            {"name": "human-firewall-db-01", "ansible_host": "10.0.10.50", "private_ip": "10.0.10.50"}
        ],
    }

    if tf_output and "ansible_inventory" in tf_output:
        inv = tf_output["ansible_inventory"].get("value", {})
        if "loadbalancers" in inv:
            topology["loadbalancers"] = [
                {"name": lb["name"], "ansible_host": lb.get("public_ip") or lb.get("private_ip"), "private_ip": lb["private_ip"]}
                for lb in inv["loadbalancers"]
            ]
        if "webservers" in inv:
            topology["webservers"] = [
                {"name": ws["name"], "ansible_host": ws.get("public_ip") or ws.get("private_ip"), "private_ip": ws["private_ip"], "replica_id": ws.get("replica_id", idx + 1)}
                for idx, ws in enumerate(inv["webservers"])
            ]
        if "dbservers" in inv:
            topology["dbservers"] = [
                {"name": db["name"], "ansible_host": db.get("public_ip") or db.get("private_ip"), "private_ip": db["private_ip"]}
                for db in inv["dbservers"]
            ]

    # Write hosts.ini
    ini_lines = [
        "# ==============================================================================",
        "# Human Firewall — Auto-Generated Ansible Inventory from Terraform",
        "# ==============================================================================",
        "",
        "[loadbalancers]",
    ]
    for lb in topology["loadbalancers"]:
        ini_lines.append(f"{lb['name']} ansible_host={lb['ansible_host']} private_ip={lb['private_ip']}")

    ini_lines.extend(["", "[webservers]"])
    for ws in topology["webservers"]:
        ini_lines.append(f"{ws['name']} ansible_host={ws['ansible_host']} private_ip={ws['private_ip']} replica_id={ws['replica_id']}")

    ini_lines.extend(["", "[dbservers]"])
    for db in topology["dbservers"]:
        ini_lines.append(f"{db['name']} ansible_host={db['ansible_host']} private_ip={db['private_ip']}")

    ini_lines.extend([
        "",
        "[all:vars]",
        "ansible_user=ubuntu",
        "ansible_ssh_common_args='-o StrictHostKeyChecking=no'",
        "ansible_python_interpreter=/usr/bin/python3",
        "app_environment=production",
        "http_port=80",
        "app_port=5000",
        "db_port=5432",
        "redis_port=6379",
        "",
    ])

    ini_content = "\n".join(ini_lines)
    ini_path.write_text(ini_content, encoding="utf-8")

    # Write hosts.json
    json_path.write_text(json.dumps(topology, indent=2), encoding="utf-8")

    print(f"[+] Ansible inventory generated at: {ini_path}")
    print(f"[+] JSON inventory generated at: {json_path}")
    return ini_path, json_path


if __name__ == "__main__":
    tf_data = None
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            tf_data = json.load(f)
    generate_inventory(tf_data)

