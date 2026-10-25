"""Seeding service — creates roles, bootstrap accounts and sample content.

Running ``flask seed`` is idempotent: existing records are left alone, so it is
safe to run after every deployment.
"""

from __future__ import annotations

import json
from datetime import date

from flask import current_app

from app.extensions import db
from app.models import (
    Achievement,
    Comic,
    ComicPanel,
    Game,
    GameScenario,
    HistoricalIncident,
    IncidentSource,
    Lab,
    LabPrerequisite,
    LearningPath,
    Lesson,
    Module,
    NewsSource,
    Question,
    ScenarioChoice,
    User,
    UserPreference,
    VideoAsset,
    VideoLanguageTrack,
)
from app.models.user import ROLE_ADMIN, ROLE_INSTRUCTOR, ROLE_LEARNER, ROLE_ORG_ADMIN, Role


from app.services.news_ingest import ensure_default_sources
from app.services.seed_data import ACHIEVEMENTS
from app.services.catalog_labs import CATALOG_LABS as LABS_AUTHORED
from app.services.catalog_videos import CATALOG_VIDEOS as VIDEO_LESSONS
from app.services.catalog_comics import COMICS
from app.services.catalog_incidents import CATALOG_INCIDENTS as INCIDENTS
from app.services.seed_data_ext import (
    COMIC_PLACEHOLDER,
    GAMES,
    LABS_ROADMAP,
    LEARNING_PATH,
)

ROLE_SPECS = [
    (ROLE_LEARNER, "Learns, plays games, completes labs and earns certificates"),
    (ROLE_INSTRUCTOR, "Reviews learner progress, assigns paths and reports"),
    (ROLE_ADMIN, "Manages users, content, analytics and platform configuration"),
    (ROLE_ORG_ADMIN, "Manages organization workspace, eligible members, seats, and reports"),
]


def run_seed(with_demo: bool | None = None) -> list[str]:
    """Create everything the application needs to run. Returns log lines."""
    if with_demo is None:
        with_demo = current_app.config.get("CREATE_DEMO_ACCOUNTS", True)

    lines: list[str] = []
    lines += ensure_roles()
    lines += ensure_achievements()
    lines += ensure_learning_path()
    lines += ensure_labs()
    lines += ensure_games()
    lines += ensure_videos()
    lines += ensure_comics()
    lines += ensure_incidents()
    lines += ensure_news_sources()
    lines += ensure_admin_account()
    if with_demo:
        lines += ensure_demo_accounts()
        lines += ensure_sample_organizations()
    else:
        lines.append("Demo accounts: skipped")
    db.session.commit()
    return lines


def _get_or_create(model, defaults: dict | None = None, **filters):
    instance = model.query.filter_by(**filters).first()
    if instance is not None:
        return instance, False
    instance = model(**{**filters, **(defaults or {})})
    db.session.add(instance)
    db.session.flush()
    return instance, True


# ---------------------------------------------------------------------------

def ensure_roles() -> list[str]:
    created = 0
    for name, description in ROLE_SPECS:
        _, is_new = _get_or_create(Role, {"description": description}, name=name)
        created += int(is_new)
    db.session.commit()
    return [f"Roles: {created} created, {len(ROLE_SPECS) - created} already present"]


def ensure_achievements() -> list[str]:
    created = 0
    for code, name_en, name_hi, desc_en, desc_hi, icon, ctype, cvalue, extra, bonus in ACHIEVEMENTS:
        _, is_new = _get_or_create(
            Achievement,
            {
                "name_en": name_en,
                "name_hi": name_hi,
                "description_en": desc_en,
                "description_hi": desc_hi,
                "icon": icon,
                "criteria_type": ctype,
                "criteria_value": cvalue,
                "criteria_extra": extra,
                "xp_bonus": bonus,
            },
            code=code,
        )
        created += int(is_new)
    db.session.commit()
    return [f"Achievements: {created} created"]


def ensure_learning_path() -> list[str]:
    path, is_new = _get_or_create(
        LearningPath,
        {
            "title_en": LEARNING_PATH["title_en"],
            "title_hi": LEARNING_PATH["title_hi"],
            "description_en": LEARNING_PATH["description_en"],
            "description_hi": LEARNING_PATH["description_hi"],
            "level": "beginner",
            "state": "published",
        },
        slug=LEARNING_PATH["slug"],
    )
    created_modules = 0
    for index, (slug, title_en, title_hi) in enumerate(LEARNING_PATH["modules"]):
        _, is_new_module = _get_or_create(
            Module,
            {
                "title_en": title_en,
                "title_hi": title_hi,
                "summary_en": None,
                "summary_hi": None,
                "order_index": index,
                "state": "published",
            },
            path_id=path.id,
            slug=slug,
        )
        created_modules += int(is_new_module)
    db.session.commit()
    return [
        f"Learning path: {'created' if is_new else 'present'}, {created_modules} new modules"
    ]


def _lab_level_for_number(number: int) -> str:
    if number <= 30:
        return "basic"
    if number <= 60:
        return "intermediate"
    if number <= 90:
        return "advanced"
    return "capstone"


def _difficulty_for_level(level: str) -> str:
    return {
        "basic": "beginner",
        "intermediate": "intermediate",
        "advanced": "advanced",
        "capstone": "expert",
    }[level]


def ensure_labs() -> list[str]:
    from app.services.gamification import xp_reward_for

    created_authored = 0
    created_roadmap = 0

    # Labs 1–10 — fully authored and published.
    for spec in LABS_AUTHORED:
        level = spec["level"]
        existing = Lab.query.filter_by(number=spec["number"]).first()
        if existing is None:
            lab = Lab(
                number=spec["number"],
                slug=spec["slug"],
                title_en=spec["title_en"],
                title_hi=spec.get("title_hi"),
                level=level,
                difficulty=spec["difficulty"],
                estimated_minutes=spec["estimated_minutes"],
                objectives_en=spec["objectives_en"],
                objectives_hi=spec.get("objectives_hi"),
                scenario_en=spec["scenario_en"],
                scenario_hi=spec.get("scenario_hi"),
                task_en=spec["task_en"],
                task_hi=spec.get("task_hi"),
                step_by_step_en=spec["step_by_step_en"],
                step_by_step_hi=spec.get("step_by_step_hi"),
                remediation_en=spec["remediation_en"],
                remediation_hi=spec.get("remediation_hi"),
                task_type=spec["task_type"],
                options_json=json.dumps(spec["options"]),
                validation_json=json.dumps(
                    {"correct": spec["correct"], "min_score": 70}
                ),
                hints_json=json.dumps(spec["hints"]),
                payload_json=json.dumps(spec["payload"]),
                xp_reward=xp_reward_for(level),
                pass_score=70,
                order_index=spec["number"],
                state="published",
            )
            db.session.add(lab)
            db.session.flush()
            created_authored += 1
        elif existing.state != "published":
            existing.slug = spec["slug"]
            existing.title_en = spec["title_en"]
            existing.title_hi = spec.get("title_hi")
            existing.level = level
            existing.difficulty = spec["difficulty"]
            existing.estimated_minutes = spec["estimated_minutes"]
            existing.objectives_en = spec["objectives_en"]
            existing.objectives_hi = spec.get("objectives_hi")
            existing.scenario_en = spec["scenario_en"]
            existing.scenario_hi = spec.get("scenario_hi")
            existing.task_en = spec["task_en"]
            existing.task_hi = spec.get("task_hi")
            existing.step_by_step_en = spec["step_by_step_en"]
            existing.step_by_step_hi = spec.get("step_by_step_hi")
            existing.remediation_en = spec["remediation_en"]
            existing.remediation_hi = spec.get("remediation_hi")
            existing.task_type = spec["task_type"]
            existing.options_json = json.dumps(spec["options"])
            existing.validation_json = json.dumps(
                {"correct": spec["correct"], "min_score": 70}
            )
            existing.hints_json = json.dumps(spec["hints"])
            existing.payload_json = json.dumps(spec["payload"])
            existing.xp_reward = xp_reward_for(level)
            existing.state = "published"
            created_authored += 1

    # Labs 11–100 — planned catalogue entries, deliberately kept in draft.
    for number, title, level in LABS_ROADMAP:
        existing = Lab.query.filter_by(number=number).first()
        if existing is None:
            db.session.add(
                Lab(
                    number=number,
                    slug=f"lab-{number}-{title.lower().replace(' ', '-').replace(',', '')[:60]}",
                    title_en=title,
                    level=level,
                    difficulty=_difficulty_for_level(level),
                    estimated_minutes=10,
                    objectives_en="Objectives to be authored in the lab build phase.",
                    task_en=None,
                    task_type="single_choice",
                    xp_reward=xp_reward_for(level),
                    pass_score=70,
                    order_index=number,
                    state="draft",
                )
            )
            db.session.flush()
            created_roadmap += 1

    db.session.commit()

    # Prerequisite chain: each lab requires the previous lab.
    created_prereqs = 0
    numbers = [n for (n,) in db.session.query(Lab.number).order_by(Lab.number).all()]
    for number in numbers:
        if number == 1:
            continue
        lab = Lab.query.filter_by(number=number).first()
        previous = Lab.query.filter_by(number=number - 1).first()
        if lab is None or previous is None:
            continue
        _, is_new = _get_or_create(
            LabPrerequisite, {}, lab_id=lab.id, requires_lab_id=previous.id
        )
        created_prereqs += int(is_new)
    db.session.commit()

    return [
        f"Labs: {created_authored} authored (published), "
        f"{created_roadmap} roadmap entries (draft), {created_prereqs} prerequisites linked"
    ]


def ensure_games() -> list[str]:
    created_games = created_scenarios = 0
    for spec in GAMES:
        game, is_new = _get_or_create(
            Game,
            {
                "title_en": spec["title_en"],
                "title_hi": spec.get("title_hi"),
                "instructions_en": spec["instructions_en"],
                "instructions_hi": spec.get("instructions_hi"),
                "debrief_en": spec["debrief_en"],
                "debrief_hi": spec.get("debrief_hi"),
                "difficulty": spec["difficulty"],
                "timed": spec["timed"],
                "xp_reward": spec["xp"],
                "state": "published",
            },
            slug=spec["slug"],
        )
        created_games += int(is_new)
        if not is_new and GameScenario.query.filter_by(game_id=game.id).count():
            continue

        for index, scenario in enumerate(spec["scenarios"]):
            if spec["slug"] == "scam-or-legit":
                body, is_threat, explanation, explanation_hi = scenario
                db.session.add(
                    GameScenario(
                        game_id=game.id,
                        order_index=index,
                        scenario_type="notification",
                        sender=None,
                        subject_en=None,
                        body_en=body,
                        is_threat=is_threat,
                        explanation_en=explanation,
                        explanation_hi=explanation_hi,
                        warning_signs_en=None,
                        xp_value=10,
                    )
                )
                created_scenarios += 1
                continue

            db.session.add(
                GameScenario(
                    game_id=game.id,
                    order_index=index,
                    scenario_type=scenario["type"],
                    sender=scenario.get("sender"),
                    subject_en=scenario.get("subject"),
                    body_en=scenario["body"],
                    meta_json=json.dumps(scenario.get("meta") or {}),
                    is_threat=scenario["is_threat"],
                    difficulty=spec["difficulty"],
                    explanation_en=scenario["explanation_en"],
                    explanation_hi=scenario.get("explanation_hi"),
                    warning_signs_en=scenario.get("warning_signs_en"),
                    warning_signs_hi=scenario.get("warning_signs_hi"),
                    xp_value=10,
                )
            )
            db.session.flush()
            created_scenarios += 1
            scenario_row = (
                GameScenario.query.filter_by(game_id=game.id)
                .order_by(GameScenario.order_index.desc())
                .first()
            )
            for choice_index, choice in enumerate(scenario["choices"]):
                text_en, is_correct, feedback_en, feedback_hi = choice
                db.session.add(
                    ScenarioChoice(
                        scenario_id=scenario_row.id,
                        order_index=choice_index,
                        text_en=text_en,
                        is_correct=is_correct,
                        feedback_en=feedback_en,
                        feedback_hi=feedback_hi,
                    )
                )
    db.session.commit()
    return [f"Games: {created_games} created, {created_scenarios} scenarios added"]


def ensure_videos() -> list[str]:
    path = LearningPath.query.filter_by(slug=LEARNING_PATH["slug"]).first()
    if path is None:
        return ["Videos: skipped (learning path missing)"]

    created_lessons = created_videos = created_questions = 0
    for index, spec in enumerate(VIDEO_LESSONS):
        module = Module.query.filter_by(path_id=path.id, slug=spec["module"]).first()
        if module is None:
            continue
        lesson, is_new = _get_or_create(
            Lesson,
            {
                "title_en": spec["title_en"],
                "title_hi": spec.get("title_hi"),
                "summary_en": spec["summary_en"],
                "summary_hi": spec.get("summary_hi"),
                "category": spec["module"],
                "difficulty": spec["difficulty"],
                "duration_minutes": spec["duration"],
                "order_index": index,
                "state": "published",
            },
            module_id=module.id,
            slug=spec["slug"],
        )
        created_lessons += int(is_new)

        existing_video = VideoAsset.query.filter_by(lesson_id=lesson.id).first()
        if existing_video is None:
            video = VideoAsset(
                lesson_id=lesson.id,
                title_en=spec["title_en"],
                title_hi=spec.get("title_hi"),
                script_en=spec["script_en"],
                script_hi=spec.get("script_hi"),
                narration_en=spec["narration_en"],
                narration_hi=spec.get("narration_hi"),
                transcript_en=spec["transcript_en"],
                transcript_hi=spec.get("transcript_hi"),
                duration_seconds=spec["duration"] * 60,
                # Honest flag: rendered media is not produced yet.
                is_prototype=True,
                available_languages="en,hi",
                order_index=0,
            )
            db.session.add(video)
            db.session.flush()
            created_videos += 1
            db.session.add(
                VideoLanguageTrack(
                    video_id=video.id,
                    language="en",
                    media_url=None,
                    captions_url=None,
                    is_available=True,
                )
            )
            db.session.add(
                VideoLanguageTrack(
                    video_id=video.id,
                    language="hi",
                    media_url=None,
                    captions_url=None,
                    is_available=True,
                )
            )
        else:
            existing_video.title_hi = spec.get("title_hi")
            existing_video.script_hi = spec.get("script_hi")
            existing_video.narration_hi = spec.get("narration_hi")
            existing_video.transcript_hi = spec.get("transcript_hi")
            existing_video.available_languages = "en,hi"

        if Question.query.filter_by(lesson_id=lesson.id).count() == 0:
            for q_index, (text, options, correct, explanation) in enumerate(
                spec.get("questions", [])
            ):
                db.session.add(
                    Question(
                        lesson_id=lesson.id,
                        topic=spec["module"],
                        phase="knowledge_check",
                        text_en=text,
                        options_json=json.dumps([{"en": option} for option in options]),
                        correct_index=correct,
                        explanation_en=explanation,
                        order_index=q_index,
                    )
                )
                created_questions += 1

    db.session.commit()
    return [
        f"Video lessons: {created_lessons} lessons, {created_videos} prototype assets, "
        f"{created_questions} knowledge-check questions"
    ]


def ensure_comics() -> list[str]:
    created_comics = created_panels = 0
    for index, spec in enumerate(COMICS):
        lab = None
        if spec.get("related_lab_number"):
            lab = Lab.query.filter_by(number=spec["related_lab_number"]).first()

        comic, is_new = _get_or_create(
            Comic,
            {
                "collection": spec["collection"],
                "title_en": spec["title_en"],
                "title_hi": spec.get("title_hi"),
                "character": spec["character"],
                "situation_en": spec["situation_en"],
                "situation_hi": spec.get("situation_hi"),
                "problem_en": spec["problem_en"],
                "problem_hi": spec.get("problem_hi"),
                "decision_en": spec["decision_en"],
                "decision_hi": spec.get("decision_hi"),
                "resolution_en": spec["resolution_en"],
                "resolution_hi": spec.get("resolution_hi"),
                "lesson_1_en": spec["lessons_en"][0],
                "lesson_2_en": spec["lessons_en"][1],
                "lesson_3_en": spec["lessons_en"][2],
                "lesson_1_hi": (spec.get("lessons_hi") or [None, None, None])[0],
                "lesson_2_hi": (spec.get("lessons_hi") or [None, None, None])[1],
                "lesson_3_hi": (spec.get("lessons_hi") or [None, None, None])[2],
                "related_lab_id": lab.id if lab else None,
                "badge_name": spec["collection"],
                "difficulty": spec["difficulty"],
                "order_index": index,
                "state": "published",
            },
            slug=spec["slug"],
        )
        created_comics += int(is_new)
        if not is_new and ComicPanel.query.filter_by(comic_id=comic.id).count():
            continue
        for panel_index, (caption_en, caption_hi) in enumerate(spec["panels"]):
            db.session.add(
                ComicPanel(
                    comic_id=comic.id,
                    order_index=panel_index,
                    image_url=COMIC_PLACEHOLDER,
                    caption_en=caption_en,
                    caption_hi=caption_hi or None,
                    dialogue_en=None,
                    alt_text_en=caption_en,
                    alt_text_hi=caption_hi or None,
                )
            )
            created_panels += 1
    db.session.commit()
    return [f"Comics: {created_comics} created, {created_panels} panels"]


def ensure_incidents() -> list[str]:
    from datetime import datetime

    created_incidents = created_sources = 0
    for index, spec in enumerate(INCIDENTS):
        published = None
        if spec.get("source_published_on"):
            try:
                published = datetime.strptime(spec["source_published_on"], "%Y-%m-%d").date()
            except ValueError:
                published = None

        incident, is_new = _get_or_create(
            HistoricalIncident,
            {
                "title_en": spec["title_en"],
                "year": spec["year"],
                "organization": spec.get("organization"),
                "sector": spec.get("sector"),
                "category": spec.get("category"),
                "attack_type": spec.get("attack_type"),
                "human_factor": True,
                "summary_en": spec.get("summary_en"),
                "summary_hi": spec.get("summary_hi"),
                "what_happened_en": spec.get("what_happened_en"),
                "what_happened_hi": spec.get("what_happened_hi"),
                "how_it_worked_en": spec.get("how_it_worked_en"),
                "how_it_worked_hi": spec.get("how_it_worked_hi"),
                "weaknesses_en": spec.get("weaknesses_en"),
                "weaknesses_hi": spec.get("weaknesses_hi"),
                "consequences_en": spec.get("consequences_en"),
                "consequences_hi": spec.get("consequences_hi"),
                "discovery_en": spec.get("discovery_en"),
                "discovery_hi": spec.get("discovery_hi"),
                "response_en": spec.get("response_en"),
                "response_hi": spec.get("response_hi"),
                "remediation_en": spec.get("remediation_en"),
                "remediation_hi": spec.get("remediation_hi"),
                "precautions_en": spec.get("precautions_en"),
                "precautions_hi": spec.get("precautions_hi"),
                "lessons_en": spec.get("lessons_en"),
                "lessons_hi": spec.get("lessons_hi"),
                "technical_detail_en": spec.get("technical_detail_en"),
                "confidence": spec.get("confidence", "confirmed"),
                "uncertainty_note_en": spec.get("uncertainty_note_en"),
                "uncertainty_note_hi": spec.get("uncertainty_note_hi"),
                "source_published_on": published,
                "last_reviewed_on": date.today(),
                "state": "published",
                "order_index": index,
            },
            slug=spec["slug"],
        )
        created_incidents += int(is_new)
        if is_new:
            for label, url, publisher in spec.get("sources", []):
                db.session.add(
                    IncidentSource(
                        incident_id=incident.id,
                        label=label,
                        url=url,
                        publisher=publisher,
                        published_on=published,
                    )
                )
                created_sources += 1
    db.session.commit()
    return [
        f"Historical incidents: {created_incidents} created, {created_sources} sources linked "
        f"(starter set — the roadmap expands this to 30 fully researched cases)"
    ]


def ensure_news_sources() -> list[str]:
    created = ensure_default_sources()
    total = NewsSource.query.count()
    return [f"News sources: {created} created, {total} configured"]


# ---------------------------------------------------------------------------
# Accounts
# ---------------------------------------------------------------------------

def _create_user(username: str, email: str, password: str, role_name: str,
                 display_name: str | None = None, locale: str = "en") -> User | None:
    role = Role.query.filter_by(name=role_name).first()
    if role is None:
        return None
    existing = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing is not None:
        return None
    user = User(
        username=username,
        email=email.lower(),
        display_name=display_name or username,
        role_id=role.id,
        locale=locale,
        email_verified=True,
    )
    user.set_password(password)
    db.session.add(user)
    db.session.flush()
    db.session.add(UserPreference(user_id=user.id, language=locale))
    return user


def ensure_admin_account() -> list[str]:
    username = current_app.config.get("ADMIN_USERNAME", "admin")
    email = current_app.config.get("ADMIN_EMAIL", "admin@cyberquest.example")
    password = current_app.config.get("ADMIN_PASSWORD", "")

    if not password:
        return [
            "Admin account: skipped — set ADMIN_USERNAME / ADMIN_EMAIL / ADMIN_PASSWORD "
            "in .env (or run `flask create-admin`)."
        ]

    existing = User.query.filter(
        (User.username == username) | (User.email == email.lower())
    ).first()
    if existing is not None:
        # Keep the role correct without ever logging or resetting the password.
        role = Role.query.filter_by(name=ROLE_ADMIN).first()
        if role and existing.role_id != role.id:
            existing.role_id = role.id
            db.session.commit()
            return [f"Admin account '{username}': existing user promoted to administrator"]
        return [f"Admin account '{username}': already present"]

    user = _create_user(username, email, password, ROLE_ADMIN, display_name="Platform Administrator")
    db.session.commit()
    if user is None:
        return ["Admin account: failed (administrator role missing)"]
    return [f"Admin account '{username}' created with role administrator"]


def ensure_demo_accounts() -> list[str]:
    password = current_app.config.get("DEMO_PASSWORD", "Demo@12345")
    created = []
    if _create_user("learner", "learner@cyberquest.example", password, ROLE_LEARNER,
                    display_name="Demo Learner", locale="en"):
        created.append("learner")
    if _create_user("learner_hi", "learner.hi@cyberquest.example", password, ROLE_LEARNER,
                    display_name="डेमो विद्यार्थी", locale="hi"):
        created.append("learner_hi")
    if _create_user("instructor", "instructor@cyberquest.example", password, ROLE_INSTRUCTOR,
                    display_name="Demo Instructor"):
        created.append("instructor")
    db.session.commit()
    if not created:
        return ["Demo accounts: already present"]
    return [
        "Demo accounts created (development only): " + ", ".join(created)
        + f" — password from DEMO_PASSWORD"
    ]


def ensure_sample_organizations() -> list[str]:
    from app.models import EligibleMember, Organization, OrganizationMembership
    from app.services.organizations import add_eligible_member, create_organization

    password = current_app.config.get("DEMO_PASSWORD", "Demo@12345")
    # 1. Create HR Coordinator / Org Admin account
    hr_user = _create_user(
        "tp_coordinator",
        "coordinator@cybershield.example",
        password,
        ROLE_ORG_ADMIN,
        display_name="T&P Coordinator (CyberShield)",
    )

    # 2. Create sample organization CyberShield University
    org = Organization.query.filter_by(slug="cybershield-university").first()
    if not org:
        admin_actor = hr_user or User.query.filter_by(username="tp_coordinator").first()
        org = create_organization(
            name="CyberShield University",
            slug="cybershield-university",
            plan_code="professional",
            seats=150,
            domain="cybershield.example",
            contact_email="coordinator@cybershield.example",
            contact_name="Prof. Rajesh Verma",
            admin_user=admin_actor,
        )
        org.org_code = "HF-ORG-UNIV1"
        org.set_passcode("Campus@2026")
        db.session.commit()

        # Seed eligible members
        add_eligible_member(org, "REG-2026-001", "Aarav Sharma", "aarav@cybershield.example", "Computer Science", "Batch 2026")
        add_eligible_member(org, "REG-2026-002", "Diya Patel", "diya@cybershield.example", "Cybersecurity", "Batch 2026")
        add_eligible_member(org, "REG-2026-003", "Rohan Mehta", "rohan@cybershield.example", "Information Technology", "Batch 2026")
        add_eligible_member(org, "REG-2026-004", "Ananya Sen", "ananya@cybershield.example", "Computer Science", "Batch 2026")
        return [f"Sample organization 'CyberShield University' created (Code: {org.org_code}) with 4 eligible registry members"]

    return [f"Sample organization '{org.name}': already present (Code: {org.org_code})"]

