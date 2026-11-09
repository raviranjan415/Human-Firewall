"""Tests for public endpoints, health checks, metrics, and route aliases."""

import pytest


def test_public_health_and_metrics(client):
    """Verify /healthz, /readyz, and /metrics return 200 OK."""
    res_healthz = client.get("/healthz")
    assert res_healthz.status_code == 200
    assert res_healthz.get_json()["status"] == "ok"

    res_readyz = client.get("/readyz")
    assert res_readyz.status_code == 200
    assert res_readyz.get_json()["status"] == "ready"

    res_metrics = client.get("/metrics")
    assert res_metrics.status_code == 200
    assert b"human_firewall_database_status 1" in res_metrics.data
    assert b"human_firewall_games_published" in res_metrics.data


def test_route_aliases_redirect(client):
    """Verify convenience aliases redirect to canonical dashboard and auth routes."""
    aliases = [
        ("/leaderboard", "/dashboard/leaderboard"),
        ("/achievements", "/dashboard/achievements"),
        ("/profile", "/auth/profile"),
        ("/org", "/org/enterprise"),
    ]
    for src, dst in aliases:
        res = client.get(src, follow_redirects=False)
        assert res.status_code in (301, 302)
        assert dst in res.headers["Location"]

