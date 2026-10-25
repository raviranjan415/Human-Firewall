# -*- coding: utf-8 -*-
"""Synchronized Learning Defense Room Content Engine
===================================================
Provides 100% topic-synchronized learning assets for every lesson opened by the user:
1. 30-Second Synced Video Animation & Dual-Language Audio Narration
2. Topic-Matched Incident Dialogue & Comic Debrief with 3 Human Takeaways
3. Merged Practical Lab Sandbox with Forensics Artifact & Interactive Verification
4. In-Depth Study Guide, 4 Topic Red Flags, & 4 Government Threat Regulations
5. 3 Practical Scenario MCQs (Q1 Indicator Detection, Q2 Defense Protocol [ID 9001],
   Q3 Legal & Regulatory Recourse [ID 9002]) with Instant Coaching Explanations.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from app.services.i18n import current_locale

_JSON_FILE = Path(__file__).parent / "curated_lessons.json"
with open(_JSON_FILE, "r", encoding="utf-8") as _f:
    _RAW_LESSONS = json.load(_f)

# Curated synchronized lesson repository (50 comprehensive topics)
CURATED_LESSONS: Dict[int, Dict[str, Any]] = {int(k): v for k, v in _RAW_LESSONS.items()}


def get_lesson_by_id_or_slug(lesson_id: Optional[int], slug: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Retrieve curated lesson data by numerical ID or slug."""
    if lesson_id and lesson_id in CURATED_LESSONS:
        return CURATED_LESSONS[lesson_id]
    if slug:
        for l in CURATED_LESSONS.values():
            if l.get("slug") == slug:
                return l
    return None


def get_synchronized_room_content(video: Any, lesson: Any) -> Dict[str, Any]:
    """Assemble all 5 synchronized components for the Defense Room."""
    try:
        locale = current_locale()
    except Exception:
        locale = "en"
    
    # 1. Resolve matching lesson definition
    lesson_id = getattr(lesson, "id", None) or getattr(video, "order_index", None) or getattr(video, "id", 1)
    if isinstance(lesson_id, int):
        mapped_id = ((lesson_id - 1) % 50) + 1
    else:
        mapped_id = 1
        
    slug = getattr(lesson, "slug", "")
    data = get_lesson_by_id_or_slug(mapped_id, slug) or CURATED_LESSONS.get(1)

    # 2. Build 30-Second Video Animation & Narration Scenes
    # 4 synchronized intervals: [0-7s], [7-15s], [15-23s], [23-30s]
    def make_scenes(lang: str) -> List[Dict[str, Any]]:
        is_hi = (lang == "hi")
        title_key = "title_hi" if is_hi else "title_en"
        lesson_title = data.get(title_key, data.get("title_en", "Cyber Defense"))
        
        s1_b = data["s1_badge"][1] if is_hi else data["s1_badge"][0]
        s1_l = [data["s1_lines"][1], data["s1_lines"][0]] if is_hi else [data["s1_lines"][0], data["s1_lines"][1]]
        s1_n = data["s1_narr"][1] if is_hi else data["s1_narr"][0]

        s2_b = data["s2_badge"][1] if is_hi else data["s2_badge"][0]
        s2_l = [data["s2_lines"][1], data["s2_lines"][0]] if is_hi else [data["s2_lines"][0], data["s2_lines"][1]]
        s2_n = data["s2_narr"][1] if is_hi else data["s2_narr"][0]

        s3_b = data["s3_badge"][1] if is_hi else data["s3_badge"][0]
        s3_l = [data["s3_lines"][1], data["s3_lines"][0]] if is_hi else [data["s3_lines"][0], data["s3_lines"][1]]
        s3_n = data["s3_narr"][1] if is_hi else data["s3_narr"][0]

        s4_b = data["s4_badge"][1] if is_hi else data["s4_badge"][0]
        s4_l = [data["s4_lines"][1], data["s4_lines"][0]] if is_hi else [data["s4_lines"][0], data["s4_lines"][1]]
        s4_n = data["s4_narr"][1] if is_hi else data["s4_narr"][0]

        return [
            {
                "idx": 0, "start_s": 0, "end_s": 7,
                "badge": s1_b,
                "title": f"{lesson_title} - {'चरण 1: हमला परिदृश्य' if is_hi else 'Phase 1: Real Attack Scenario'}",
                "line1": s1_l[0],
                "line2": s1_l[1] if len(s1_l) > 1 else "",
                "narration": s1_n,
                "kind": "threat"
            },
            {
                "idx": 1, "start_s": 7, "end_s": 15,
                "badge": s2_b,
                "title": f"{lesson_title} - {'चरण 2: मनोवैज्ञानिक दबाव व संकेत' if is_hi else 'Phase 2: Tactical Red Flags'}",
                "line1": s2_l[0],
                "line2": s2_l[1] if len(s2_l) > 1 else "",
                "narration": s2_n,
                "kind": "alert"
            },
            {
                "idx": 2, "start_s": 15, "end_s": 23,
                "badge": s3_b,
                "title": f"{lesson_title} - {'चरण 3: मानवीय सुरक्षा कदम' if is_hi else 'Phase 3: Human Firewall Defense'}",
                "line1": s3_l[0],
                "line2": s3_l[1] if len(s3_l) > 1 else "",
                "narration": s3_n,
                "kind": "defense"
            },
            {
                "idx": 3, "start_s": 23, "end_s": 30,
                "badge": s4_b,
                "title": f"{lesson_title} - {'चरण 4: कानूनी अधिकार व सरकारी नियम' if is_hi else 'Phase 4: Statutory Rights & Laws'}",
                "line1": s4_l[0],
                "line2": s4_l[1] if len(s4_l) > 1 else "",
                "narration": s4_n,
                "kind": "legal"
            }
        ]

    video_scenes = {
        "en": make_scenes("en"),
        "hi": make_scenes("hi")
    }

    # 3. Build Topic-Matched Incident Dialogue & Comic
    raw_c = data["comic"]
    comic = {
        "target_persona": raw_c["target_persona_hi"] if locale == "hi" else raw_c["target_persona_en"],
        "target_persona_en": raw_c["target_persona_en"],
        "target_persona_hi": raw_c["target_persona_hi"],
        "situation": raw_c["situation_hi"] if locale == "hi" else raw_c["situation_en"],
        "situation_en": raw_c["situation_en"],
        "situation_hi": raw_c["situation_hi"],
        "attacker_role": raw_c["attacker_role_hi"] if locale == "hi" else raw_c["attacker_role_en"],
        "attacker_role_en": raw_c["attacker_role_en"],
        "attacker_role_hi": raw_c["attacker_role_hi"],
        "problem": raw_c["problem_hi"] if locale == "hi" else raw_c["problem_en"],
        "problem_en": raw_c["problem_en"],
        "problem_hi": raw_c["problem_hi"],
        "resolution": raw_c["resolution_hi"] if locale == "hi" else raw_c["resolution_en"],
        "resolution_en": raw_c["resolution_en"],
        "resolution_hi": raw_c["resolution_hi"],
        "takeaways": raw_c["takeaways_hi"] if locale == "hi" else raw_c["takeaways_en"],
        "takeaways_en": raw_c["takeaways_en"],
        "takeaways_hi": raw_c["takeaways_hi"],
    }

    # 4. Build Merged Practical Lab Sandbox
    raw_l = data["lab"]
    lab_opts = []
    for opt in raw_l["options"]:
        lab_opts.append({
            "id": opt["id"],
            "text": opt["text_hi"] if locale == "hi" else opt["text_en"],
            "text_en": opt["text_en"],
            "text_hi": opt["text_hi"],
            "is_correct": opt.get("is_correct", False)
        })
    lab = {
        "title": raw_l["title_hi"] if locale == "hi" else raw_l["title_en"],
        "title_en": raw_l["title_en"],
        "title_hi": raw_l["title_hi"],
        "task": raw_l["task_hi"] if locale == "hi" else raw_l["task_en"],
        "task_en": raw_l["task_en"],
        "task_hi": raw_l["task_hi"],
        "payload": raw_l["payload"],
        "options": lab_opts,
        "hint": raw_l["hint_hi"] if locale == "hi" else raw_l["hint_en"],
        "hint_en": raw_l["hint_en"],
        "hint_hi": raw_l["hint_hi"],
        "feedback": raw_l["feedback_hi"] if locale == "hi" else raw_l["feedback_en"],
        "feedback_en": raw_l["feedback_en"],
        "feedback_hi": raw_l["feedback_hi"],
    }

    # 5. Build Study Guide & Threat Laws
    raw_r = data["reading"]
    reading = {
        "overview": raw_r["overview_hi"] if locale == "hi" else raw_r["overview_en"],
        "overview_en": raw_r["overview_en"],
        "overview_hi": raw_r["overview_hi"],
        "red_flags": raw_r["red_flags_hi"] if locale == "hi" else raw_r["red_flags_en"],
        "red_flags_en": raw_r["red_flags_en"],
        "red_flags_hi": raw_r["red_flags_hi"],
        "regulations": raw_r["regulations"]
    }

    # 6. Build 3 Practical Scenario MCQs
    # Q1: Topic Threat Indicator Detection (from curated data)
    q1_raw = data["q1"]
    q1 = {
        "id": (mapped_id * 10) + 1,
        "text": q1_raw["text_hi"] if locale == "hi" else q1_raw["text_en"],
        "text_en": q1_raw["text_en"],
        "text_hi": q1_raw["text_hi"],
        "options": q1_raw["options_hi"] if locale == "hi" else q1_raw["options_en"],
        "options_en": q1_raw["options_en"],
        "options_hi": q1_raw["options_hi"],
        "correct_index": q1_raw["correct_index"],
        "explanation": q1_raw["explanation_hi"] if locale == "hi" else q1_raw["explanation_en"],
        "explanation_en": q1_raw["explanation_en"],
        "explanation_hi": q1_raw["explanation_hi"],
    }

    # Q2 (ID 9001): RBI Zero Liability & Standard Banking/Operational Verification Defense
    q2 = {
        "id": 9001,
        "text": "भारतीय रिजर्व बैंक (RBI) के सुरक्षा सर्कुलर के अनुसार, अनधिकृत डिजिटल लेनदेन की सूचना तुरंत बैंक को देने पर ग्राहक की देयता क्या होती है?" if locale == "hi" else "Under Reserve Bank of India (RBI) customer protection directives, what is your liability if an unauthorized digital transaction is reported to the bank within 3 working days?",
        "text_en": "Under Reserve Bank of India (RBI) customer protection directives, what is your liability if an unauthorized digital transaction is reported to the bank within 3 working days?",
        "text_hi": "भारतीय रिजर्व बैंक (RBI) के सुरक्षा सर्कुलर के अनुसार, अनधिकृत डिजिटल लेनदेन की सूचना तुरंत बैंक को देने पर ग्राहक की देयता क्या होती है?",
        "options": [
            "आपको चुराई गई राशि का 50% वहन करना होगा",
            "शून्य देयता (Zero Liability) — ग्राहक को कोई वित्तीय नुकसान नहीं उठाना पड़ता",
            "पूरी जिम्मेदारी खाताधारक पर होती है",
            "जिम्मेदारी आपके क्रेडिट स्कोर पर निर्भर करती है"
        ] if locale == "hi" else [
            "You must pay 50% of the stolen amount",
            "Zero Liability — the customer bears no financial loss",
            "Full liability rests with the account holder",
            "Liability depends on your credit score"
        ],
        "options_en": [
            "You must pay 50% of the stolen amount",
            "Zero Liability — the customer bears no financial loss",
            "Full liability rests with the account holder",
            "Liability depends on your credit score"
        ],
        "options_hi": [
            "आपको चुराई गई राशि का 50% वहन करना होगा",
            "शून्य देयता (Zero Liability) — ग्राहक को कोई वित्तीय नुकसान नहीं उठाना पड़ता",
            "पूरी जिम्मेदारी खाताधारक पर होती है",
            "जिम्मेदारी आपके क्रेडिट स्कोर पर निर्भर करती है"
        ],
        "correct_index": 1,
        "explanation": "RBI के सर्कुलर DBR.No.Leg.BC.78/09.07.005/2017-18 के अनुसार, अनधिकृत लेनदेन की सूचना 3 कार्य दिवसों के भीतर देने पर ग्राहक की देयता शून्य होती है।" if locale == "hi" else "Under RBI Circular DBR.No.Leg.BC.78/09.07.005/2017-18, customers have ZERO liability if an unauthorized transaction is reported within 3 working days.",
        "explanation_en": "Under RBI Circular DBR.No.Leg.BC.78/09.07.005/2017-18, customers have ZERO liability if an unauthorized transaction is reported within 3 working days.",
        "explanation_hi": "RBI के सर्कुलर DBR.No.Leg.BC.78/09.07.005/2017-18 के अनुसार, अनधिकृत लेनदेन की सूचना 3 कार्य दिवसों के भीतर देने पर ग्राहक की देयता शून्य होती है।",
    }

    # Q3 (ID 9002): IT Act Section 66D Cheating by Impersonation & Digital Fraud Legal Recourse
    q3 = {
        "id": 9002,
        "text": "सूचना प्रौद्योगिकी (IT) अधिनियम 2000 की धारा 66D के तहत, कंप्यूटर या मोबाइल के माध्यम से पहचान बदलकर धोखाधड़ी करने पर क्या कानूनी सजा है?" if locale == "hi" else "Under Section 66D of the Information Technology (IT) Act 2000, what is the legal penalty for cheating by impersonation using a computer or mobile device?",
        "text_en": "Under Section 66D of the Information Technology (IT) Act 2000, what is the legal penalty for cheating by impersonation using a computer or mobile device?",
        "text_hi": "सूचना प्रौद्योगिकी (IT) अधिनियम 2000 की धारा 66D के तहत, कंप्यूटर या मोबाइल के माध्यम से पहचान बदलकर धोखाधड़ी करने पर क्या कानूनी सजा है?",
        "options": [
            "बिना आपराधिक रिकॉर्ड के केवल चेतावनी",
            "3 वर्ष तक का कारावास और ₹1,00,000 तक का जुर्माना",
            "केवल जमानत जब्त होना",
            "30 दिनों की सामुदायिक सेवा"
        ] if locale == "hi" else [
            "Warning letter with no criminal record",
            "Imprisonment up to 3 years and a fine up to ₹1,00,000",
            "Bail forfeiture only",
            "Community service for 30 days"
        ],
        "options_en": [
            "Warning letter with no criminal record",
            "Imprisonment up to 3 years and a fine up to ₹1,00,000",
            "Bail forfeiture only",
            "Community service for 30 days"
        ],
        "options_hi": [
            "बिना आपराधिक रिकॉर्ड के केवल चेतावनी",
            "3 वर्ष तक का कारावास और ₹1,00,000 तक का जुर्माना",
            "केवल जमानत जब्त होना",
            "30 दिनों की सामुदायिक सेवा"
        ],
        "correct_index": 1,
        "explanation": "IT एक्ट 2000 की धारा 66D के तहत कंप्यूटर या फोन से फर्जी प्रतिरूप बनाकर धोखाधड़ी करने पर 3 साल तक की जेल और ₹1 लाख तक का जुर्माना हो सकता है।" if locale == "hi" else "Section 66D of the IT Act penalizes cheating by personation by using any communication device or computer resource with imprisonment up to 3 years and fine up to ₹1 Lakh.",
        "explanation_en": "Section 66D of the IT Act penalizes cheating by personation by using any communication device or computer resource with imprisonment up to 3 years and fine up to ₹1 Lakh.",
        "explanation_hi": "IT एक्ट 2000 की धारा 66D के तहत कंप्यूटर या फोन से फर्जी प्रतिरूप बनाकर धोखाधड़ी करने पर 3 साल तक की जेल और ₹1 लाख तक का जुर्माना हो सकता है।",
    }

    questions = [q1, q2, q3]

    return {
        "lesson_id": mapped_id,
        "title_en": data["title_en"],
        "title_hi": data["title_hi"],
        "video_scenes": video_scenes,
        "comic": comic,
        "lab": lab,
        "reading": reading,
        "questions": questions,
    }
