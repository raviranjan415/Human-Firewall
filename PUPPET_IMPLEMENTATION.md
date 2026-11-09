# HUMAN FIREWALL — PUPPET IMPLEMENTATION MANUAL
**Technology Priority 3: Desired-State Configuration Management & Drift Healing**
**INT333 DevOps Advanced Configuration Management**

---

## 1. Architectural Role & Technology Priority

**Puppet** is the **Technology Priority 3** component of the Human Firewall platform. Operating on a declarative desired-state model, Puppet ensures continuous compliance, drift detection, and automated remediation across the server fleet.

While Ansible handles the initial imperative installation and rolling code releases, Puppet acts as the **24/7 compliance guardian**:
1. Declares the authoritative state of system services, configuration files, and permissions.
2. Compiles node catalogs via Hiera parameter lookups.
3. Automatically detects unauthorized manual modifications ("configuration drift").
4. Heals drifted resources back to their declared state without human intervention.
5. Emits structured compliance telemetry consumed by the Admin DevOps Dashboard.

---

## 2. Directory Layout & Modular Structure

```
puppet/
├── hiera.yaml                         # Hiera 5 data lookup hierarchy
├── hieradata/
│   ├── common.yaml                    # Universal baseline parameters
│   └── environments/
│       └── production.yaml            # Production-specific parameter overrides
├── manifests/
│   └── site.pp                        # Master node classification entrypoint
├── modules/
│   ├── packages/                      # Enforces installed utility packages
│   │   └── manifests/init.pp
│   ├── users/                         # Enforces system service account & GID/UID
│   │   └── manifests/init.pp
│   ├── ssh/                           # Enforces hardened sshd_config & daemon state
│   │   ├── manifests/init.pp
│   │   └── templates/sshd_config.erb
│   ├── firewall/                      # Enforces UFW daemon execution state
│   │   └── manifests/init.pp
│   ├── nginx/                         # Enforces Nginx reverse proxy configuration
│   │   ├── manifests/init.pp
│   │   └── templates/nginx.conf.erb
│   ├── application/                   # Enforces app directory ownership & systemd unit
│   │   └── manifests/init.pp
│   ├── security_baseline/             # Primary drift target (sysctl & security limits)
│   │   └── manifests/init.pp
│   └── monitoring/                    # Enforces node-exporter daemon state
│       └── manifests/init.pp
├── environments/
│   └── production/                    # Production environment directory
│       ├── environment.conf
│       └── manifests/site.pp
├── scripts/
│   ├── drift_demo.py                  # Live configuration drift & remediation runner
│   └── drift_demo.sh                  # Shell wrapper
└── reports/
    ├── drift_report.json              # Full audit report with drift events & SHA256 hashes
    └── last_run_summary.yaml          # Standard Puppet agent run summary
```

---

## 3. Separation of Ownership: Ansible vs. Puppet

To prevent conflicting automation cycles ("configuration flapping"), responsibilities are strictly demarcated:

- **Ansible Owns**: Initial system bootstrap, Docker package installation, database migration execution (`migrate_db.py`), rolling code checkout, and container restarts.
- **Puppet Owns**: Ongoing declarative state enforcement of `/etc/ssh/sshd_config`, `/etc/sysctl.d/99-human-firewall-security.conf`, `/etc/security/limits.d/99-human-firewall-limits.conf`, permissions on `/etc/shadow`, and ensuring core services (`ssh`, `nginx`, `ufw`) remain running.

Neither tool ever writes to the other's application configuration files.

---

## 4. Node Classification (`manifests/site.pp`)

Puppet classifies hosts using regular expression pattern matching on hostnames:

```puppet
# Global Baseline for all nodes
node default {
  include packages
  include users
  include ssh
  include firewall
  include security_baseline
  include monitoring
}

# Edge Load Balancers inherit baseline + Nginx
node /^.*lb.*$/ inherits default {
  include nginx
}

# Application Replicas inherit baseline + App Service
node /^.*replica.*$/ inherits default {
  include application
}

# Database Nodes inherit baseline + Postgres Data Dir
node /^.*db.*$/ inherits default {
  file { '/var/lib/postgresql/data':
    ensure => directory,
    owner  => 'postgres',
    group  => 'postgres',
    mode   => '0700',
  }
}
```

---

## 5. Live Configuration Drift Demonstration & Remediation

A core academic requirement is proving that Puppet can detect and heal configuration drift.

### 5.1 The 6-Step Drift Reconciliation Lifecycle
The script `puppet/scripts/drift_demo.py` executes the following sequence:

```
[ Step 1: Baseline Enforcement ]
Puppet enforces declared baseline:
  - `/etc/ssh/sshd_config` (PermitRootLogin no, Mode 0600)
  - `/etc/sysctl.d/99-human-firewall-security.conf` (tcp_syncookies = 1)
  - `/etc/security/limits.d/99-human-firewall-limits.conf` (nofile = 65535)
                │
                ▼
[ Step 2: Unauthorized Drift Injected ]
An operator or attacker manually modifies `/etc/ssh/sshd_config`:
  - `PermitRootLogin yes`
  - `PasswordAuthentication yes`
  - File SHA256 changes: 653e86aa -> a653556c
                │
                ▼
[ Step 3: Puppet Inspection & Drift Detection ]
Puppet agent compiles catalog and compares target file against compiled hash:
  - Status: DRIFT DETECTED
  - Severity: HIGH
  - Resource: File['/etc/ssh/sshd_config']
                │
                ▼
[ Step 4: Automated Self-Healing Remediation ]
Puppet re-applies template from Hiera:
  - Overwrites unauthorized edit.
  - Re-asserts `PermitRootLogin no` and `0600` permissions.
  - Notifies Service['ssh'] to reload.
                │
                ▼
[ Step 5: Post-Remediation Compliance Verification ]
Puppet verifies file checksum matches desired catalog hash:
  - Compliance Restored: 100.0%
  - Corrective Changes: 1/1
                │
                ▼
[ Step 6: Telemetry Recording ]
Audit record written to `puppet/reports/drift_report.json` and `last_run_summary.yaml`.
Live metrics are reflected on `/admin/devops?tab=puppet`.
```

---

## 6. Execution Commands & Verification

### 6.1 Running the Drift Demonstration
```bash
# Execute drift simulation and self-healing
python puppet/scripts/drift_demo.py
```

### 6.2 Validating Puppet Manifest Syntax
```bash
# Validate master manifest syntax
puppet parser validate puppet/manifests/site.pp

# Validate individual module manifests
puppet parser validate puppet/modules/ssh/manifests/init.pp
puppet parser validate puppet/modules/security_baseline/manifests/init.pp
```

### 6.3 Executing Agent Run in Check Mode
```bash
puppet agent -t --noop --environment production
```

