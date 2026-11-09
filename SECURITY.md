# HUMAN FIREWALL — APPLICATION & INFRASTRUCTURE SECURITY SPECIFICATION
**Defense-in-Depth, Cryptography, Access Control & Threat Modeling**

---

## 1. Security Architecture Principles

Human Firewall embodies the principle that **cybersecurity begins at home**. The platform enforces strict defense-in-depth across the web application, APIs, database, containers, and infrastructure.

```
[ Edge Perimeter ]       --> TLS 1.3, Strict CSP, HSTS, X-Frame-Options: DENY, Rate Limiting
[ Identity Tier ]        --> Salted Argon2id Hashing, Session Fixation Defense, RBAC
[ Application Logic ]    --> Server-Side Answer Grading, Idempotent XP Ledger Savepoints
[ Data Persistence ]     --> Isolated Subnets, Parameterized SQL Queries, No Plain Secrets
[ Container Runtime ]    --> Unprivileged User (UID 10001), Read-Only Root, Non-Root WSGI
[ DevOps Core ]          --> Restricted Endpoints, No Arbitrary Shell Execution
```

---

## 2. Authentication & Credential Storage

### 2.1 Argon2id Password Hashing
- Passwords are hashed using the state-of-the-art **Argon2id** algorithm via `argon2-cffi`.
- Resistant to GPU/ASIC brute-force cracking.
- Transparent re-hashing: If parameters are tuned or legacy hashes are verified, the user's hash is re-encoded automatically upon successful login.

### 2.2 Session Security
- Cookies configured with:
  - `HttpOnly = True`: Prevents client-side JavaScript access and XSS theft.
  - `SameSite = 'Lax'`: Mitigates Cross-Site Request Forgery (CSRF).
  - `Secure = True`: Enforces transmission exclusively over HTTPS in production.
  - `PERMANENT_SESSION_LIFETIME = 120 minutes`: Enforces automatic timeout on idle sessions.

---

## 3. Role-Based Access Control (RBAC)

Four distinct roles are enforced via decorators (`@login_required`, `@admin_required`, `@org_admin_required`):

1. **Learner (`ROLE_LEARNER`)**: Can browse published courses, play awareness games, submit practical labs, and earn digital certificates.
2. **Instructor (`ROLE_INSTRUCTOR`)**: Can review learner cohort progress, assign learning paths, and view class statistics.
3. **Organization Administrator (`ROLE_ORG_ADMIN`)**: Manages enterprise seat licenses, white-lists eligible employee email domains, and tracks departmental completion rates.
4. **Platform Administrator (`ROLE_ADMIN`)**: Accesses system user records, content publishing queues, append-only audit logs, and the **DevOps Management Console**.

---

## 4. Anti-Cheat & Gamification Security

1. **Server-Side Answer Grading**:
   - Correct scenario choices, threat flags, and lab answer keys are **never sent to the client browser** before a commitment is submitted.
   - The client sends only `{"scenario_id": X, "choice_id": Y}` or `{"scenario_id": X, "is_threat": bool}`. The server evaluates against the database.
2. **Idempotent XP Ledger**:
   - XP is tracked in the immutable `xp_transactions` table with composite unique constraint `(user_id, reason, reference_type, reference_id)`.
   - If a malicious client replays `/api/games/<slug>/complete` multiple times, the transaction fails gracefully inside a nested database savepoint, awarding **0 duplicate XP**.
3. **Distributed Rate Limiting**:
   - Sensitive endpoints (`/auth/login`, `/api/games/<slug>/complete`, `/api/labs/<lab_id>/submit`) are protected by `Flask-Limiter` with a Redis backend to block credential stuffing and brute-forcing.

---

## 5. Network & Container Security

1. **Least-Privilege Docker Execution**:
   - The production container executes as non-root user `appuser` (UID 10001, GID 10001).
   - Shell access is set to `/sbin/nologin`.
2. **Zero-Trust Network Segmentation**:
   - Database (Port 5432) and Redis (Port 6379) reside on internal Docker / VPC subnets with zero internet-facing gateways.
   - Traffic between Nginx and Flask travels over internal container bridge networks.

---

## 6. DevOps Security: Safe Management Dashboard

The Admin DevOps Console (`/admin/devops`):
- **Never exposes raw bash / shell execution** to web administrators.
- Operates strictly through pre-compiled, sanitized backend service calls (`devops_telemetry.py`).
- Every administrative invocation (such as triggering a Puppet drift check) is permanently recorded in the immutable `audit_logs` table with actor ID, timestamp, and client IP.

