"""Tests for the DevOps Management Dashboard and Observability Endpoints."""

from __future__ import annotations

import pytest
from app.models import AuditLog
from .conftest import login, logout, ADMIN_USERNAME, ADMIN_PASSWORD, LEARNER_PASSWORD


def test_devops_dashboard_rbac(client, learner, admin_user):
    """Verify that only platform administrators can access /admin/devops."""
    # 1. Unauthenticated -> Redirect to login
    res = client.get("/admin/devops")
    assert res.status_code in (302, 401)

    # 2. Regular Learner -> 403 Forbidden
    login(client, "learner1", LEARNER_PASSWORD)
    res_learner = client.get("/admin/devops")
    assert res_learner.status_code == 403

    # 3. Platform Admin -> 200 OK
    logout(client)
    login(client, ADMIN_USERNAME, ADMIN_PASSWORD)
    res_admin = client.get("/admin/devops")
    assert res_admin.status_code == 200
    assert b"DevOps Management Console" in res_admin.data
    assert b"Terraform" in res_admin.data
    assert b"Ansible" in res_admin.data
    assert b"Puppet" in res_admin.data


def test_devops_tabs_rendering(client, admin_user):
    """Verify that all 5 DevOps tabs render successfully."""
    login(client, ADMIN_USERNAME, ADMIN_PASSWORD)

    tabs = ["overview", "terraform", "ansible", "puppet", "application"]
    for tab in tabs:
        res = client.get(f"/admin/devops?tab={tab}")
        assert res.status_code == 200
        assert b"DevOps Management Console" in res.data


def test_devops_drift_check_action(client, admin_user, app):
    """Test triggering a Puppet configuration drift check from the admin console."""
    login(client, ADMIN_USERNAME, ADMIN_PASSWORD)

    res = client.post("/admin/devops/drift-check", follow_redirects=True)
    assert res.status_code == 200
    assert b"Puppet configuration drift check executed successfully" in res.data

    # Verify audit log was created
    with app.app_context():
        log = AuditLog.query.filter_by(action="puppet_drift_check_triggered").first()
        assert log is not None
        assert log.actor_id == admin_user.id


def test_health_ready_and_metrics_endpoints(client):
    """Test /healthz, /readyz, and Prometheus /metrics."""
    # 1. Healthz
    res_health = client.get("/healthz")
    assert res_health.status_code == 200
    d_health = res_health.get_json()
    assert d_health["status"] == "ok"
    assert d_health["database"] is True

    # 2. Readyz
    res_ready = client.get("/readyz")
    assert res_ready.status_code == 200
    d_ready = res_ready.get_json()
    assert d_ready["status"] == "ready"

    # 3. Metrics (Prometheus exposition format)
    res_metrics = client.get("/metrics")
    assert res_metrics.status_code == 200
    assert "text/plain" in res_metrics.content_type
    assert b"human_firewall_database_status 1" in res_metrics.data
    assert b"human_firewall_system_cpu_percent" in res_metrics.data
