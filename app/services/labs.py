"""Practical lab service: prerequisite enforcement and server-side validation.

A lab is never marked complete because a learner merely opened it. Answers are
scored here, on the server, from the lab's stored validation configuration.
"""

from __future__ import annotations

import json
from datetime import datetime

from app.extensions import db
from app.models import Lab, LabAttempt, LabPrerequisite, User
from app.models.user import utcnow
from app.services import gamification, progress as progress_service

LEVEL_THRESHOLDS = {
    # level -> minimum number of passed labs required to unlock the level
    "basic": 0,
    "intermediate": 30,
    "advanced": 60,
    "capstone": 90,
}

LEVEL_LABELS = {
    "basic": "Basic",
    "intermediate": "Intermediate",
    "advanced": "Advanced",
    "capstone": "Expert capstone",
}


def _load(raw: str | None, default):
    if not raw:
        return default
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        return default


def passed_lab_ids(user: User) -> set[int]:
    rows = (
        db.session.query(LabAttempt.lab_id)
        .filter(LabAttempt.user_id == user.id, LabAttempt.passed.is_(True))
        .distinct()
        .all()
    )
    return {row[0] for row in rows}


def best_attempt(user: User, lab_id: int) -> LabAttempt | None:
    return (
        LabAttempt.query.filter_by(user_id=user.id, lab_id=lab_id)
        .order_by(LabAttempt.percentage.desc(), LabAttempt.completed_at.desc())
        .first()
    )


def attempts_for(user: User, lab_id: int) -> list[LabAttempt]:
    return (
        LabAttempt.query.filter_by(user_id=user.id, lab_id=lab_id)
        .order_by(LabAttempt.created_at.desc())
        .all()
    )


def unlock_status(user: User, lab: Lab, passed: set[int] | None = None) -> dict:
    """Return whether a lab is unlocked and, if not, exactly why."""
    passed = passed if passed is not None else passed_lab_ids(user)

    missing_level = LEVEL_THRESHOLDS.get(lab.level, 0)
    if len(passed) < missing_level:
        return {
            "unlocked": False,
            "reason": "level",
            "missing_labs": missing_level - len(passed),
            "message_key": "lab.need_level",
        }

    for prerequisite in lab.prerequisites:
        if prerequisite.requires_lab_id not in passed:
            return {
                "unlocked": False,
                "reason": "prerequisite",
                "prerequisite_id": prerequisite.requires_lab_id,
                "message_key": "lab.complete_prev",
            }

    return {"unlocked": True, "reason": None, "missing_labs": 0, "message_key": None}


def lab_path(user: User) -> list[dict]:
    """The whole lab pathway with unlock state — rendered as a quest map."""
    labs = Lab.query.filter_by(state="published").order_by(Lab.number).all()
    passed = passed_lab_ids(user)
    result = []
    for lab in labs:
        status = unlock_status(user, lab, passed)
        attempt = best_attempt(user, lab.id)
        result.append(
            {
                "lab": lab,
                "unlocked": status["unlocked"],
                "lock_reason": status,
                "completed": lab.id in passed,
                "best_score": attempt.percentage if attempt else None,
                "attempts": attempt.retry_count if attempt else 0,
            }
        )
    return result


def level_summary(user: User) -> list[dict]:
    passed = passed_lab_ids(user)
    summary = []
    for level in ("basic", "intermediate", "advanced", "capstone"):
        labs = Lab.query.filter_by(level=level, state="published").all()
        total = len(labs)
        done = sum(1 for lab in labs if lab.id in passed)
        summary.append(
            {
                "level": level,
                "label": LEVEL_LABELS[level],
                "total": total,
                "completed": done,
                "percent": int(done / total * 100) if total else 0,
                "unlocked": len(passed) >= LEVEL_THRESHOLDS.get(level, 0),
            }
        )
    return summary


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def evaluate_submission(lab: Lab, submitted) -> tuple[int, str, str, dict]:
    """Score a submission.

    Returns ``(percentage, feedback_en, feedback_hi, detail)``.
    """
    config = _load(lab.validation_json, {})
    correct = config.get("correct", [])
    benchmark = max(1, int(config.get("min_score", lab.pass_score or 70)))

    if lab.task_type == "single_choice":
        expected = correct[0] if isinstance(correct, list) and correct else correct
        given = str(submitted or "")
        percentage = 100 if given == str(expected) else 0
        detail = {"expected": expected, "given": given}
        if percentage >= benchmark:
            return percentage, "Correct — you identified the key risk.", "सही — आपने मुख्य जोखिम पहचान लिया।", detail
        return (
            percentage,
            "Not quite. Re-read the warning signs and try again — mistakes are part of learning here.",
            "पूरा सही नहीं। चेतावनी के संकेत फिर पढ़ें और कोशिश करें — गलती से ही सीखते हैं।",
            detail,
        )

    if lab.task_type == "multi_select":
        expected_set = {str(item) for item in correct}
        given_list = submitted if isinstance(submitted, list) else ([submitted] if submitted else [])
        given_set = {str(item) for item in given_list}

        hits = len(expected_set & given_set)
        misses = len(expected_set - given_set)
        false_positives = len(given_set - expected_set)

        raw = (hits - false_positives * 0.5) / max(1, len(expected_set)) * 100
        percentage = int(max(0, min(100, round(raw))))
        detail = {
            "correct_selected": sorted(expected_set & given_set),
            "missed": sorted(expected_set - given_set),
            "incorrect_selected": sorted(given_set - expected_set),
        }
        if percentage >= benchmark and misses == 0 and false_positives == 0:
            return (
                100,
                "Perfect — every warning sign identified, nothing over-flagged.",
                "बिल्कुल सही — सभी चेतावनी संकेत पहचाने, कुछ गलत नहीं चुना।",
                detail,
            )
        if percentage >= benchmark:
            return (
                percentage,
                f"Good work. You found {hits} of {len(expected_set)} warning signs"
                + (". Some were still missed." if misses else "."),
                f"अच्छा काम। आपने {len(expected_set)} में से {hits} संकेत पकड़े।",
                detail,
            )
        return (
            percentage,
            "Keep going. Focus on the signs you missed and try the lab again.",
            "जारी रखें। छूटे हुए संकेतों पर ध्यान दें और फिर कोशिश करें।",
            detail,
        )

    if lab.task_type == "order":
        expected_order = [str(item) for item in correct]
        given_order = [str(item) for item in (submitted or [])]
        positional = sum(
            1 for i, item in enumerate(given_order) if i < len(expected_order) and item == expected_order[i]
        )
        percentage = int(round(positional / max(1, len(expected_order)) * 100))
        detail = {"expected": expected_order, "given": given_order}
        if percentage >= benchmark:
            return percentage, "Correct sequence.", "क्रम सही है।", detail
        return (
            percentage,
            "The order is not right yet. Think about what protects you first.",
            "क्रम अभी सही नहीं है। सोचें कि सबसे पहले आपकी सुरक्षा कैसे होगी।",
            detail,
        )

    if lab.task_type == "text_judgement":
        # Free-text defence is validated against keyword coverage, never as a
        # pass/fail on exact wording.
        keywords = [str(word).lower() for word in config.get("keywords", [])]
        text = str(submitted or "").lower()
        hits = [word for word in keywords if word in text]
        percentage = int(round(len(hits) / max(1, len(keywords)) * 100)) if keywords else 0
        detail = {"matched": hits, "expected_keywords": keywords}
        if percentage >= benchmark:
            return percentage, "Good reasoning — you covered the essential steps.", "अच्छी सोच — ज़रूरी कदम शामिल हैं।", detail
        return (
            percentage,
            "Mention the verification and reporting steps to complete your answer.",
            "उत्तर पूरा करने के लिए सत्यापन और रिपोर्टिंग के कदम लिखें।",
            detail,
        )

    return 0, "Unsupported task type.", "असमर्थित कार्य प्रकार।", {}


def submit_lab(
    user: User,
    lab: Lab,
    submitted,
    hints_used: int = 0,
    started_at: datetime | None = None,
) -> dict:
    """Validate, score and record a lab submission."""
    status = unlock_status(user, lab)
    if not status["unlocked"]:
        return {"ok": False, "error": "locked", "detail": status}

    percentage, feedback_en, feedback_hi, detail = evaluate_submission(lab, submitted)
    passed = percentage >= (lab.pass_score or 70)

    attempt = LabAttempt.query.filter_by(user_id=user.id, lab_id=lab.id).order_by(
        LabAttempt.created_at.desc()
    ).first()
    if attempt is None:
        attempt = LabAttempt(user_id=user.id, lab_id=lab.id, started_at=started_at or utcnow())
        db.session.add(attempt)
        attempt.retry_count = 0
    else:
        attempt.retry_count = (attempt.retry_count or 0) + 1
        attempt.started_at = attempt.started_at or started_at or utcnow()

    attempt.score = percentage
    attempt.max_score = 100
    attempt.percentage = percentage
    attempt.passed = passed or attempt.passed
    attempt.status = "passed" if (passed or attempt.passed) else "failed"
    attempt.hints_used = max(attempt.hints_used or 0, int(hints_used or 0))
    if passed:
        attempt.completed_at = utcnow()
    attempt.feedback_en = feedback_en
    attempt.feedback_hi = feedback_hi
    attempt.submitted_json = json.dumps({"detail": detail})
    db.session.commit()

    result = {
        "ok": True,
        "passed": passed,
        "already_passed": not passed and attempt.passed,
        "percentage": percentage,
        "feedback_en": feedback_en,
        "feedback_hi": feedback_hi,
        "detail": detail,
        "xp_awarded": 0,
        "achievements": [],
        "next_lab_id": None,
    }

    if passed:
        from flask import current_app

        reward = lab.xp_reward or gamification.xp_reward_for(lab.level)
        settlement = progress_service.complete_activity(
            user,
            "lab",
            lab.id,
            score=percentage,
            hints_used=hints_used,
            xp_amount=reward,
            xp_reason=f"lab_{lab.level}",
            reference_id=f"lab:{lab.id}",
            event_type="lab_passed",
        )
        result["xp_awarded"] = settlement["xp_awarded"]
        result["achievements"] = settlement["achievements"]
        result["next_lab_id"] = _next_lab_id(lab)
    else:
        progress_service.record_failure(user, "lab", lab.id, score=percentage, hints_used=hints_used)

    return result


def _next_lab_id(lab: Lab) -> int | None:
    nxt = (
        Lab.query.filter(Lab.number > lab.number, Lab.state == "published")
        .order_by(Lab.number)
        .first()
    )
    return nxt.id if nxt else None


def recommendations(user: User, limit: int = 3) -> list[Lab]:
    """Next labs worth attempting: unlocked and not yet passed."""
    passed = passed_lab_ids(user)
    labs = Lab.query.filter_by(state="published").order_by(Lab.number).all()
    ready = []
    for lab in labs:
        if lab.id in passed:
            continue
        if unlock_status(user, lab, passed)["unlocked"]:
            ready.append(lab)
        if len(ready) >= limit:
            break
    return ready
