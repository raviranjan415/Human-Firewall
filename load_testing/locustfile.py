"""Locust performance & load testing suite for Human Firewall.

Simulates 4 realistic enterprise & academic workloads:
1. Personal Learners: Browsing games, answering scenarios, checking leaderboards.
2. Organization Members: Accessing dedicated workspace, viewing assignments.
3. HR / T&P Coordinators: Querying organization metrics and members.
4. DevOps & SRE Monitors: Polling /healthz, /readyz, and Prometheus /metrics.
"""

from __future__ import annotations

import random
from locust import HttpUser, TaskSet, between, task


class PersonalLearnerBehavior(TaskSet):
    def on_start(self):
        # Authenticate learner
        self.client.post("/auth/login", data={
            "identifier": "learner1",
            "password": "Testing1pass",
        })

    @task(5)
    def browse_homepage(self):
        self.client.get("/")

    @task(4)
    def view_dashboard(self):
        self.client.get("/dashboard/")

    @task(5)
    def browse_games_hub(self):
        self.client.get("/games/")

    @task(3)
    def play_game(self):
        slugs = [
            "phishing-detective",
            "smishing-showdown",
            "password-fortress",
            "wifi-safety-mission",
            "malware-hunter",
            "data-privacy-guardian",
        ]
        chosen = random.choice(slugs)
        self.client.get(f"/games/{chosen}")

    @task(2)
    def submit_game_answer(self):
        self.client.post(
            "/api/games/phishing-detective/answer",
            json={"scenario_id": 1, "is_threat": True},
        )

    @task(3)
    def browse_labs(self):
        self.client.get("/labs/")

    @task(2)
    def check_leaderboard(self):
        self.client.get("/dashboard/leaderboard")

    @task(1)
    def check_certificates(self):
        self.client.get("/certificates/")


class OrganizationMemberBehavior(TaskSet):
    def on_start(self):
        self.client.post("/auth/login", data={
            "identifier": "learner1",
            "password": "Testing1pass",
        })

    @task(3)
    def view_workspace(self):
        self.client.get("/org/1/workspace")

    @task(2)
    def view_org_leaderboard(self):
        self.client.get("/org/1/leaderboard")


class HRCoordinatorBehavior(TaskSet):
    def on_start(self):
        self.client.post("/auth/login", data={
            "identifier": "admin",
            "password": "Admin@150305",
        })

    @task(4)
    def view_hr_dashboard(self):
        self.client.get("/org/1/dashboard")

    @task(2)
    def view_devops_console(self):
        self.client.get("/admin/devops?tab=overview")


class SREMonitorBehavior(TaskSet):
    @task(4)
    def poll_healthz(self):
        self.client.get("/healthz")

    @task(3)
    def poll_readyz(self):
        self.client.get("/readyz")

    @task(2)
    def scrape_metrics(self):
        self.client.get("/metrics")


class HumanFirewallUser(HttpUser):
    wait_time = between(0.1, 0.5)
    tasks = {
        PersonalLearnerBehavior: 6,
        OrganizationMemberBehavior: 3,
        HRCoordinatorBehavior: 1,
        SREMonitorBehavior: 2,
    }
