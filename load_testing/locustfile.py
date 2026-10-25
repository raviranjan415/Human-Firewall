"""Locust performance & load testing suite for Human Firewall.

Simulates three realistic user workflows:
1. Personal Learners: Anonymous and authenticated browsing, lab access, gamification sync.
2. Organization Members: Accessing dedicated workspace, viewing assignments, checking org leaderboard.
3. HR / T&P Coordinators: Querying organization dashboard metrics, searching eligible registry, inspecting assignments.
"""

from __future__ import annotations

import random
from locust import HttpUser, TaskSet, task, between


class PersonalLearnerBehavior(TaskSet):
    def on_start(self):
        self.username = f"bench_user_{random.randint(1, 1000)}"
        # Authenticate learner
        self.client.post("/auth/login", data={
            "identifier": "learner1",
            "password": "Testing1pass",
        })

    @task(4)
    def browse_homepage(self):
        self.client.get("/")

    @task(3)
    def view_dashboard(self):
        self.client.get("/dashboard/")

    @task(3)
    def browse_labs(self):
        self.client.get("/labs/")

    @task(2)
    def view_lab_detail(self):
        lab_num = random.choice([1, 2, 3, 4, 5])
        self.client.get(f"/labs/{lab_num}")

    @task(1)
    def check_certificates(self):
        self.client.get("/certificates/")

    @task(1)
    def view_educational_news(self):
        self.client.get("/cyber-news/")


class OrganizationMemberBehavior(TaskSet):
    def on_start(self):
        # Authenticate learner belonging to workspace
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

    @task(2)
    def check_assigned_labs(self):
        self.client.get("/labs/1")


class HRCoordinatorBehavior(TaskSet):
    def on_start(self):
        # Authenticate HR Administrator
        self.client.post("/auth/login", data={
            "identifier": "admin",
            "password": "Admin@150305",
        })

    @task(4)
    def view_hr_dashboard(self):
        self.client.get("/org/1/dashboard")

    @task(2)
    def search_eligible_members(self):
        self.client.get("/org/1/eligible?q=EMP")

    @task(2)
    def inspect_active_members(self):
        self.client.get("/org/1/members")

    @task(1)
    def view_assignments(self):
        self.client.get("/org/1/assignments")


class HumanFirewallUser(HttpUser):
    wait_time = between(0.1, 0.5)  # rapid requests for load benchmarking
    tasks = {
        PersonalLearnerBehavior: 6,
        OrganizationMemberBehavior: 3,
        HRCoordinatorBehavior: 1,
    }
