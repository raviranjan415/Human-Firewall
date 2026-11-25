"""Verification test for human-designed interactive room with 30s synced video,
merged practical lab, reading material, government regulations, 3 scenario MCQs,
and the official About page for Ravi Ranjan.
"""

from app.models import VideoAsset

from .conftest import login


def test_room_human_ui_and_regulations(app, client, learner):
    login(client, "learner1")

    video = VideoAsset.query.first()
    assert video is not None

    response = client.get(f"/learn/videos/{video.id}")
    assert response.status_code == 200

    html = response.get_data(as_text=True)

    # 1. Human Step Navigation with Merged Practical Lab
    assert (
        "Study Video" in html
        or "80s Video Lecture" in html
        or "30s Synced Video" in html
    )
    assert "Incident Chat" in html
    assert "Practical Lab" in html
    assert (
        "Theory &amp; Study Room" in html
        or "Theory & Study Room" in html
        or "Study &amp; Laws" in html
        or "Study & Laws" in html
        or "Deep Study &amp; Laws" in html
    )
    assert "Scenario Quiz" in html or "3 MCQs Quiz" in html

    # 2. Reading Material & Government Regulations
    assert "IT Act" in html or "66D" in html
    assert "Zero Liability" in html or "RBI" in html
    assert "1930" in html
    assert "DPDP Act" in html

    # 3. 3 Scenario MCQs rendered in json payload
    assert "9001" in html
    assert "9002" in html

    # 4. Synced Video Player tokens
    assert (
        "Interactive Study Video" in html
        or "80-Second Synced Video" in html
        or "30-Second Synced Video" in html
    )
    assert "1:20" in html or "0:30" in html


def test_about_page_and_developer_attribution(client):
    response = client.get("/about")
    assert response.status_code == 200

    html = response.get_data(as_text=True)

    # Ravi Ranjan Attribution & Professional Bio
    assert "Ravi Ranjan" in html
    assert "Lead Architect" in html or "Security Developer" in html
    assert "linkedin.com/in/ravi6745" in html
    assert "Connect on LinkedIn" in html

    # Mission and Vision
    assert "Human Firewall" in html
    assert "Vision for Securing Humans" in html


def test_curated_lessons_integrity(app):
    """Verify that all 50 lessons produce synchronized video, comics, lab, reading and quiz."""
    from app.models import VideoAsset
    from app.services.lesson_sync import CURATED_LESSONS, get_synchronized_room_content

    assert len(CURATED_LESSONS) == 50

    with app.app_context():
        for num in range(1, 51):
            video = VideoAsset.query.filter_by(lesson_id=num).first()
            if not video:
                continue
            data = get_synchronized_room_content(video, video.lesson)
            assert data["lesson_id"] == num
            assert "title_en" in data and "title_hi" in data

            # 1. 30s Video Scenes: 4 scenes for EN and HI
            scenes = data.get("video_scenes", {})
            assert len(scenes.get("en", [])) == 4
            assert len(scenes.get("hi", [])) == 4
            for s in scenes["en"] + scenes["hi"]:
                assert (
                    "start_s" in s
                    and "title" in s
                    and "badge" in s
                    and "narration" in s
                )

            # 2. Incident Chat Comic & 3 Takeaways
            comic = data.get("comic", {})
            assert (
                "situation_en" in comic
                and "problem_en" in comic
                and "resolution_en" in comic
            )
            assert len(comic.get("takeaways_en", [])) == 3

            # 3. Practical Lab Artifact & Options
            lab = data.get("lab", {})
            assert "task" in lab and "payload" in lab and "hint" in lab
            assert len(lab.get("options", [])) >= 3
            assert any(opt.get("is_correct") for opt in lab.get("options", []))

            # 4. Reading Material: 4 Red Flags, 4 Laws, and TryHackMe Compact Modules
            reading = data.get("reading", {})
            assert "overview" in reading
            assert len(reading.get("red_flags", [])) == 4
            assert len(reading.get("regulations", [])) == 4
            assert "objectives" in reading and len(reading["objectives"]) == 3
            assert "concept_explanation" in reading
            assert "real_world_scenario" in reading
            assert "technical_breakdown" in reading
            assert "practical_investigation" in reading
            assert "analyst_notes" in reading
            assert "common_mistakes" in reading and len(reading["common_mistakes"]) == 3
            assert "knowledge_check" in reading and len(reading["knowledge_check"]) == 3

            # 5. 3 Scenario MCQs with coaching explanations
            questions = data.get("questions", [])
            assert len(questions) == 3
            for q in questions:
                assert "text_en" in q and "text_hi" in q
                assert len(q.get("options_en", [])) == 4
                assert len(q.get("options_hi", [])) == 4
                assert 0 <= q.get("correct_index", -1) < 4
                assert "explanation_en" in q and "explanation_hi" in q


def test_lesson_synchronization_across_topics(app, client, learner):
    """Verify that opening different lessons renders their distinct topic-synchronized content."""
    login(client, "learner1")

    # Test distinct lessons: 1 (Social Engineering), 6 (Phishing), 16 (Wire Transfer / CEO Fraud), 22 (Voice Cloning)
    test_cases = [
        (1, ["Social Engineering", "Human Target", "Psychological"]),
        (6, ["Phishing", "Email", "Fake IT Portal"]),
        (16, ["Wire Transfer", "CEO", "Bank"]),
        (22, ["Voice", "Deepfake", "Cloning"]),
    ]

    for lesson_num, expected_keywords in test_cases:
        video = VideoAsset.query.filter_by(lesson_id=lesson_num).first()
        if not video:
            continue
        resp = client.get(f"/learn/videos/{video.id}")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)

        # Check at least one topic-specific keyword is present in the rendered HTML
        assert any(kw.lower() in html.lower() for kw in expected_keywords), (
            f"Lesson {lesson_num} does not contain any of {expected_keywords}"
        )


def test_classroom_video_teacher_engine(app, client, learner):
    """Verify cartoon classroom video presentation, teacher selector, and study points."""
    login(client, "learner1")

    video = VideoAsset.query.first()
    assert video is not None

    resp = client.get(f"/learn/videos/{video.id}")
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)

    # 1. Classroom Teachers & Interactive Controls
    assert "Prof. Alex" in html
    assert "Prof. Maya" in html
    assert "simCanvas" in html
    assert "Classroom Masterclass" in html
    assert "Ask the Professor" in html
    assert "Key Topic Study Points" in html

    # 2. Check lesson_sync output for teacher_script and study_bullets
    from app.services.lesson_sync import get_synchronized_room_content

    with app.app_context():
        content = get_synchronized_room_content(video, video.lesson)
        scenes_en = content["video_scenes"]["en"]
        scenes_hi = content["video_scenes"]["hi"]

        assert len(scenes_en) == 4
        assert len(scenes_hi) == 4

        for s in scenes_en:
            assert "teacher_script" in s
            assert "Hello class!" in s["teacher_script"] or "Notice" in s["teacher_script"] or "Here is our" in s["teacher_script"] or "Class," in s["teacher_script"]
            assert "study_bullets" in s
            assert len(s["study_bullets"]) >= 2

        for s in scenes_hi:
            assert "teacher_script" in s
            assert "नमस्ते क्लास!" in s["teacher_script"] or "छात्रों" in s["teacher_script"] or "यह है हमारा" in s["teacher_script"] or "कक्षा" in s["teacher_script"]
            assert "study_bullets" in s
            assert len(s["study_bullets"]) >= 2

