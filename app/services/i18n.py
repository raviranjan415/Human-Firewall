"""Bilingual (English / Hindi) translation service.

Pages are not duplicated per language: every string in a template goes through
``t()`` and every content record stores ``*_en`` / ``*_hi`` columns that are
resolved by :func:`t_content`. Hindi strings use natural, everyday language.
"""

from __future__ import annotations

from flask import current_app, has_request_context, session

DEFAULT_LOCALE = "en"

LOCALE_LABELS = {
    "en": {"en": "English", "hi": "अंग्रेज़ी"},
    "hi": {"en": "Hindi", "hi": "हिन्दी"},
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        # Brand
        "brand.name": "Human Firewall",
        "brand.tagline": "Professional Cybersecurity Awareness Platform",
        "brand.secondary": "Empowering Every Individual and Organization as an Impenetrable Human Firewall.",
        "brand.motto": "Train Smart, Stay Secure, Defend Together!",
        "brand.hero_title": "Turn Your People Into Your Strongest Defense.",
        "brand.hero_subtitle": (
            "Interactive social engineering labs, educational comics, video lessons, "
            "and enterprise training management that transform employees and students into an active Human Firewall."
        ),
        "nav.enterprise": "Enterprise & Orgs",
        "nav.workspace": "Org Workspace",
        "nav.hr_dashboard": "HR / T&P Dashboard",

        # Navigation
        "nav.home": "Home",
        "nav.dashboard": "Dashboard",
        "nav.learn": "Learn",
        "nav.videos": "Video Lessons",
        "nav.comics": "Comic Library",
        "nav.games": "Games",
        "nav.labs": "Practical Labs",
        "nav.challenges": "Daily Challenges",
        "nav.leaderboard": "Leaderboard",
        "nav.achievements": "Achievements",
        "nav.certificates": "Certificates",
        "nav.incidents": "What Happened?",
        "nav.news": "Cyber News Today",
        "nav.analytics": "My Analytics",
        "nav.profile": "Profile",
        "nav.settings": "Settings",
        "nav.instructor": "Instructor",
        "nav.admin": "Admin",
        "nav.login": "Log in",
        "nav.register": "Create account",
        "nav.logout": "Log out",
        "nav.menu": "Menu",
        "nav.language": "Language",
        "nav.help": "Help & Support",
        # Auth
        "auth.login_title": "Welcome back, defender",
        "auth.register_title": "Start your Cyber Quest",
        "auth.username": "Username",
        "auth.email": "Email address",
        "auth.password": "Password",
        "auth.confirm_password": "Confirm password",
        "auth.display_name": "Display name (optional)",
        "auth.remember": "Keep me signed in",
        "auth.forgot": "Forgot your password?",
        "auth.no_account": "New to CyberQuest?",
        "auth.have_account": "Already have an account?",
        "auth.reset_request": "Reset your password",
        "auth.reset_send": "Send reset instructions",
        "auth.reset_new": "Choose a new password",
        "auth.success": "Success",
        "auth.logged_out": "You have been signed out.",
        "auth.account_created": "Your account is ready. Welcome to CyberQuest!",
        # Dashboard
        "dash.welcome": "Welcome back",
        "dash.level": "Level",
        "dash.total_xp": "Total XP",
        "dash.streak": "Day streak",
        "dash.longest_streak": "Longest streak",
        "dash.completion": "Overall completion",
        "dash.daily_challenge": "Daily challenge",
        "dash.weekly_challenge": "Weekly challenge",
        "dash.next_certificate": "Next certificate milestone",
        "dash.leaderboard_position": "Leaderboard position",
        "dash.continue": "CONTINUE YOUR CYBER QUEST",
        "dash.recommended": "Recommended next activity",
        "dash.recent_mistakes": "Recent mistakes to revise",
        "dash.completed_lessons": "Completed lessons",
        "dash.completed_labs": "Completed labs",
        "dash.achievements": "Achievements earned",
        "dash.current_path": "Current learning path",
        "dash.no_mistakes": "No recent mistakes — excellent work.",
        "dash.latest_incidents": "Recently published incidents",
        # Tracks
        "get.started": "Get started",
        "get.explore_quest": "Explore the quest",
        "get.browse_labs": "Browse labs",
        "get.play_games": "Play a game",
        "get.read_comics": "Read a comic",
        "get.watch_videos": "Watch a lesson",
        "get.view_all": "View all",
        "get.optional": "optional",
        "get.required": "required",
        "get.difficulty": "Difficulty",
        "get.duration": "Duration",
        "get.minutes": "min",
        "get.level": "Level",
        "get.score": "Score",
        "get.points": "points",
        "get.hint": "Need a hint?",
        "get.show_hint": "Show hint",
        "get.submit": "Submit answer",
        "get.next": "Next",
        "get.previous": "Previous",
        "get.back": "Back",
        "get.close": "Close",
        "get.retry": "Try again",
        "get.try_again": "Try again",
        "get.start": "Start",
        "get.start_lab": "Start lab",
        "get.continue": "Continue",
        "get.download": "Download",
        "get.locked": "Locked",
        "get.completed": "Completed",
        "get.in_progress": "In progress",
        "get.not_started": "Not started",
        "get.search": "Search",
        "get.filter": "Filter",
        "get.all": "All",
        "get.clear_filters": "Clear filters",
        "get.no_results": "Nothing matches your filters yet.",
        "get.prerequisites": "Prerequisites",
        "get.objectives": "Learning objectives",
        "get.scenario": "Scenario",
        "get.your_task": "Your task",
        "get.explanation": "Step-by-step explanation",
        "get.remediation": "Recommended revision",
        "get.feedback": "Feedback",
        "get.correct": "Correct",
        "get.incorrect": "Not quite",
        "get.perfect": "Perfect score!",
        "earned": "earned",
        "of": "of",
        "total": "Total",
        # Labs
        "lab.title": "Practical Labs",
        "lab.subtitle": "One hundred connected investigations, from hygiene basics to expert capstones.",
        "lab.number": "Lab",
        "lab.pass_score": "Passing score",
        "lab.hints_used": "Hints used",
        "lab.attempts": "Attempts",
        "lab.basic": "Basic",
        "lab.intermediate": "Intermediate",
        "lab.advanced": "Advanced",
        "lab.capstone": "Expert capstone",
        "lab.certificate_after": "Certificate unlocked after",
        "lab.complete_prev": "Complete the previous labs to unlock this one.",
        "lab.validated": "Completion is verified on the server before XP is awarded.",
        # Games
        "game.title": "Games",
        "game.instructions": "How to play",
        "game.start": "Start the challenge",
        "game.debrief": "Debrief",
        "game.warning_signs": "Warning signs",
        "game.is_threat": "This is a scam or attack",
        "game.is_safe": "This looks legitimate",
        "game.report_it": "Report it",
        "game.result": "Result",
        "game.replay": "Play again",
        # Certificate
        "cert.title": "Certificates",
        "cert.verify": "Verify a certificate",
        "cert.verification_code": "Verification code",
        "cert.issue_date": "Issued on",
        "cert.tier": "Tier",
        "cert.eligible": "You are eligible",
        "cert.not_eligible": "Not eligible yet",
        "cert.generate": "Generate certificate",
        "cert.note": (
            "Certificates issued here are platform training records. They are not "
            "accredited professional certifications."
        ),
        # Misc
        "msg.access_denied": "You do not have permission to view that page.",
        "msg.not_found": "We could not find that page.",
        "msg.rate_limited": "Too many requests. Please slow down and try again shortly.",
        "footer.about": "About",
        "footer.privacy": "Privacy policy",
        "footer.terms": "Terms of use",
        "footer.accessibility": "Accessibility",
        "footer.help": "Help & Support",
        "footer.note": "A defensive, educational awareness platform. All simulations are fictional.",
    },
    "hi": {
        "brand.name": "ह्यूमन फ़ायरवॉल (Human Firewall)",
        "brand.tagline": "सुरक्षा के साथ मज़ा",
        "brand.secondary": "प्रत्येक व्यक्ति और संगठन को एक अभेद्य ह्यूमन फ़ायरवॉल बनाना।",
        "brand.motto": "होशियार बनें, सुरक्षित रहें, मिलकर बचाव करें!",
        "brand.hero_title": "अपने लोगों को अपनी सबसे मजबूत सुरक्षा दीवार बनाएं।",
        "brand.hero_subtitle": (
            "प्रैक्टिकल सोशल इंजीनियरिंग लैब, इंटरैक्टिव कॉमिक्स और वीडियो पाठ जो साइबर खतरों के सामने आपको तैयार करते हैं।"
        ),
        "nav.enterprise": "संस्थान एवं कंपनियाँ",
        "nav.workspace": "वर्कस्पेस",
        "nav.hr_dashboard": "एचआर डैशबोर्ड",

        "nav.home": "होम",
        "nav.dashboard": "डैशबोर्ड",
        "nav.learn": "सीखें",
        "nav.videos": "वीडियो पाठ",
        "nav.comics": "कॉमिक लाइब्रेरी",
        "nav.games": "गेम्स",
        "nav.labs": "प्रैक्टिकल लैब",
        "nav.challenges": "रोज़ की चुनौती",
        "nav.leaderboard": "लीडरबोर्ड",
        "nav.achievements": "उपलब्धियाँ",
        "nav.certificates": "प्रमाणपत्र",
        "nav.incidents": "क्या हुआ था?",
        "nav.news": "आज की साइबर खबरें",
        "nav.analytics": "मेरा विश्लेषण",
        "nav.profile": "प्रोफ़ाइल",
        "nav.settings": "सेटिंग्स",
        "nav.instructor": "प्रशिक्षक",
        "nav.admin": "एडमिन",
        "nav.login": "लॉग इन",
        "nav.register": "खाता बनाएँ",
        "nav.logout": "लॉग आउट",
        "nav.menu": "मेन्यू",
        "nav.language": "भाषा",
        "nav.help": "सहायता",
        "auth.login_title": "फिर से स्वागत है",
        "auth.register_title": "अपनी साइबर यात्रा शुरू करें",
        "auth.username": "उपयोगकर्ता नाम",
        "auth.email": "ईमेल पता",
        "auth.password": "पासवर्ड",
        "auth.confirm_password": "पासवर्ड दोबारा लिखें",
        "auth.display_name": "प्रदर्शित नाम (वैकल्पिक)",
        "auth.remember": "मुझे लॉग इन रखें",
        "auth.forgot": "पासवर्ड भूल गए?",
        "auth.no_account": "साइबरक्वेस्ट पर नए हैं?",
        "auth.have_account": "पहले से खाता है?",
        "auth.reset_request": "पासवर्ड रीसेट करें",
        "auth.reset_send": "रीसेट निर्देश भेजें",
        "auth.reset_new": "नया पासवर्ड चुनें",
        "auth.success": "सफल",
        "auth.logged_out": "आप लॉग आउट हो गए हैं।",
        "auth.account_created": "आपका खाता तैयार है। साइबरक्वेस्ट में स्वागत है!",
        "dash.welcome": "वापसी पर स्वागत",
        "dash.level": "स्तर",
        "dash.total_xp": "कुल XP",
        "dash.streak": "दिन की लय",
        "dash.longest_streak": "सबसे लंबी लय",
        "dash.completion": "कुल पूर्णता",
        "dash.daily_challenge": "आज की चुनौती",
        "dash.weekly_challenge": "इस सप्ताह की चुनौती",
        "dash.next_certificate": "अगला प्रमाणपत्र",
        "dash.leaderboard_position": "लीडरबोर्ड पर स्थान",
        "dash.continue": "अपनी साइबर यात्रा जारी रखें",
        "dash.recommended": "अगला सुझाया गया कार्य",
        "dash.recent_mistakes": "दोहराने योग्य हाल की गलतियाँ",
        "dash.completed_lessons": "पूरे किए पाठ",
        "dash.completed_labs": "पूरी की गई लैब",
        "dash.achievements": "मिली उपलब्धियाँ",
        "dash.current_path": "वर्तमान लर्निंग पथ",
        "dash.no_mistakes": "कोई हाल की गलती नहीं — बहुत बढ़िया।",
        "dash.latest_incidents": "हाल प्रकाशित घटनाएँ",
        "get.started": "शुरू करें",
        "get.explore_quest": "यात्रा देखें",
        "get.browse_labs": "लैब देखें",
        "get.play_games": "गेम खेलें",
        "get.read_comics": "कॉमिक पढ़ें",
        "get.watch_videos": "पाठ देखें",
        "get.view_all": "सभी देखें",
        "get.optional": "वैकल्पिक",
        "get.required": "आवश्यक",
        "get.difficulty": "कठिनाई",
        "get.duration": "अवधि",
        "get.minutes": "मिनट",
        "get.level": "स्तर",
        "get.score": "अंक",
        "get.points": "अंक",
        "get.hint": "संकेत चाहिए?",
        "get.show_hint": "संकेत दिखाएँ",
        "get.submit": "उत्तर भेजें",
        "get.next": "आगे",
        "get.previous": "पीछे",
        "get.back": "वापस",
        "get.close": "बंद करें",
        "get.retry": "फिर कोशिश करें",
        "get.try_again": "फिर कोशिश करें",
        "get.start": "शुरू",
        "get.start_lab": "लैब शुरू करें",
        "get.continue": "जारी रखें",
        "get.download": "डाउनलोड",
        "get.locked": "बंद",
        "get.completed": "पूरा हुआ",
        "get.in_progress": "चल रहा है",
        "get.not_started": "शुरू नहीं हुआ",
        "get.search": "खोजें",
        "get.filter": "छाँटें",
        "get.all": "सभी",
        "get.clear_filters": "फ़िल्टर हटाएँ",
        "get.no_results": "आपके फ़िल्टर से कुछ मेल नहीं खाता।",
        "get.prerequisites": "पहले पूरा करें",
        "get.objectives": "सीखने के लक्ष्य",
        "get.scenario": "स्थिति",
        "get.your_task": "आपका काम",
        "get.explanation": "चरण-दर-चरण समझ",
        "get.remediation": "दोहराने की सलाह",
        "get.feedback": "प्रतिक्रिया",
        "get.correct": "सही",
        "get.incorrect": "पूरा सही नहीं",
        "get.perfect": "पूरे अंक!",
        "earned": "मिले",
        "of": "में से",
        "total": "कुल",
        "lab.title": "प्रैक्टिकल लैब",
        "lab.subtitle": "साफ़-सुथरी आदतों से लेकर विशेषज्ञ स्तर तक — सौ जुड़ी हुई जाँचें।",
        "lab.number": "लैब",
        "lab.pass_score": "पास होने के अंक",
        "lab.hints_used": "इस्तेमाल किए संकेत",
        "lab.attempts": "कोशिशें",
        "lab.basic": "बुनियादी",
        "lab.intermediate": "मध्यम",
        "lab.advanced": "उच्च",
        "lab.capstone": "विशेषज्ञ कैपस्टोन",
        "lab.certificate_after": "प्रमाणपत्र मिलेगा पूरा करने पर",
        "lab.complete_prev": "इसे खोलने के लिए पहले वाले लैब पूरे करें।",
        "lab.validated": "XP मिलने से पहले सर्वर पर पूर्णता की जाँच होती है।",
        "game.title": "गेम्स",
        "game.instructions": "कैसे खेलें",
        "game.start": "चुनौती शुरू करें",
        "game.debrief": "सारांश",
        "game.warning_signs": "चेतावनी के संकेत",
        "game.is_threat": "यह ठगी या हमला है",
        "game.is_safe": "यह असली लगता है",
        "game.report_it": "रिपोर्ट करें",
        "game.result": "नतीजा",
        "game.replay": "फिर खेलें",
        "cert.title": "प्रमाणपत्र",
        "cert.verify": "प्रमाणपत्र जाँचें",
        "cert.verification_code": "सत्यापन कोड",
        "cert.issue_date": "जारी दिनांक",
        "cert.tier": "श्रेणी",
        "cert.eligible": "आप पात्र हैं",
        "cert.not_eligible": "अभी पात्र नहीं",
        "cert.generate": "प्रमाणपत्र बनाएँ",
        "cert.note": (
            "यहाँ जारी प्रमाणपत्र प्लेटफ़ॉर्म के प्रशिक्षण रिकॉर्ड हैं। ये मान्यता प्राप्त "
            "पेशेवर प्रमाणपत्र नहीं हैं।"
        ),
        "msg.access_denied": "इस पेज को देखने की आपको अनुमति नहीं है।",
        "msg.not_found": "यह पेज नहीं मिला।",
        "msg.rate_limited": "बहुत ज़्यादा अनुरोध। कृपया थोड़ी देर बाद कोशिश करें।",
        "footer.about": "परिचय",
        "footer.privacy": "गोपनीयता नीति",
        "footer.terms": "उपयोग की शर्तें",
        "footer.accessibility": "सुगम्यता",
        "footer.help": "सहायता",
        "footer.note": "यह एक शैक्षिक, रक्षात्मक जागरूकता प्लेटफ़ॉर्म है। सभी अभ्यास काल्पनिक हैं।",
    },
}


def init_i18n(app) -> None:
    """Register locale persistence hooks (kept intentionally simple)."""

    @app.before_request
    def _apply_requested_locale():  # pragma: no cover - thin wrapper
        from flask import request, session as flask_session

        lang = request.args.get("lang")
        if lang in current_app.config["SUPPORTED_LOCALES"]:
            flask_session["locale"] = lang


def current_locale() -> str:
    """Resolve the active locale: session -> user preference -> default."""
    supported = current_app.config.get("SUPPORTED_LOCALES", ("en", "hi"))
    if has_request_context():
        lang = session.get("locale")
        if lang in supported:
            return lang
        try:
            from flask_login import current_user

            if current_user.is_authenticated:
                pref = getattr(current_user, "preference", None)
                if pref and pref.language in supported:
                    return pref.language
                if current_user.locale in supported:
                    return current_user.locale
        except Exception:  # pragma: no cover - defensive
            pass
    return current_app.config.get("DEFAULT_LOCALE", DEFAULT_LOCALE)


def available_locales() -> list[dict]:
    return [
        {"code": code, "label": LOCALE_LABELS[code][current_locale()]}
        for code in current_app.config.get("SUPPORTED_LOCALES", ("en", "hi"))
    ]


def t(key: str, **kwargs) -> str:
    """Translate a UI string, falling back to English then to the key itself."""
    locale = current_locale()
    text = TRANSLATIONS.get(locale, {}).get(key)
    if text is None:
        text = TRANSLATIONS["en"].get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text


def t_content(obj, field: str, locale: str | None = None) -> str:
    """Return ``field`` in the active locale from a bilingual model column.

    Falls back to the English value and finally to an empty string, so a
    missing translation is never shown as another language's text.
    """
    if obj is None:
        return ""
    locale = locale or current_locale()
    if locale == "hi":
        value = getattr(obj, f"{field}_hi", None)
        if value:
            return value
    return getattr(obj, f"{field}_en", None) or getattr(obj, field, "") or ""


def get_theme_classes() -> str:
    """Body classes derived from the user's accessibility preferences."""
    classes = []
    if has_request_context():
        try:
            from flask_login import current_user

            if current_user.is_authenticated and current_user.preference:
                pref = current_user.preference
                if pref.text_size != "normal":
                    classes.append(f"text-{pref.text_size}")
                if pref.reduce_motion:
                    classes.append("reduce-motion")
                if pref.high_contrast:
                    classes.append("high-contrast")
        except Exception:  # pragma: no cover - defensive
            pass
    return " ".join(classes)
