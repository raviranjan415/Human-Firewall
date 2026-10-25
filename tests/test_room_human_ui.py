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
    assert "30s Synced Video" in html
    assert "Incident Chat" in html
    assert "Practical Lab" in html
    assert "Study &amp; Laws" in html or "Study & Laws" in html
    assert "3 MCQs Quiz" in html

    # 2. Reading Material & Government Regulations
    assert "IT Act" in html or "66D" in html
    assert "Zero Liability" in html or "RBI" in html
    assert "1930" in html
    assert "DPDP Act" in html

    # 3. 3 Scenario MCQs rendered in json payload
    assert "9001" in html
    assert "9002" in html

    # 4. 30-Second Synced Video Player tokens
    assert "30-Second Synced Video" in html
    assert "0:30" in html


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
    from app.services.lesson_sync import CURATED_LESSONS, get_synchronized_room_content
    from app.models import VideoAsset

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
                assert "start_s" in s and "title" in s and "badge" in s and "narration" in s

            # 2. Incident Chat Comic & 3 Takeaways
            comic = data.get("comic", {})
            assert "situation_en" in comic and "problem_en" in comic and "resolution_en" in comic
            assert len(comic.get("takeaways_en", [])) == 3

            # 3. Practical Lab Artifact & Options
            lab = data.get("lab", {})
            assert "task" in lab and "payload" in lab and "hint" in lab
            assert len(lab.get("options", [])) >= 3
            assert any(opt.get("is_correct") for opt in lab.get("options", []))

            # 4. Reading Material: 4 Red Flags & 4 Laws
            reading = data.get("reading", {})
            assert "overview" in reading
            assert len(reading.get("red_flags", [])) == 4
            assert len(reading.get("regulations", [])) == 4

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
        (22, ["Voice", "Deepfake", "Cloning"])
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


