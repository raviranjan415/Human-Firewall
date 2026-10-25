"""Seed catalogues, part two: lab roadmap, games, video lessons, comics and
researched historical incidents.

Content status is stated plainly so nothing is over-claimed:

* ``LABS_ROADMAP`` — labs 11–100 as planned catalogue entries (title, level,
  ordered prerequisites). They are seeded in ``draft`` state and are not
  visible to learners until their scenario, task and validation rules are
  authored.
* ``VIDEO_LESSONS`` — prototype video lessons. Scripts and narration are
  original and complete enough to produce the media; the rendered video files
  do not ship with the project, and every record is flagged
  ``is_prototype=True``.
* ``COMICS`` — prototype comic stories with original panel captions. Panel
  artwork is a clearly labelled placeholder illustration.
* ``INCIDENTS`` — a starter set of historical incidents. Each entry carries a
  confidence label and points to the publishing organisation rather than
  invented deep links.
"""

# ---------------------------------------------------------------------------
# Labs 11–100 — planned catalogue (draft state, not learner-visible)
# ---------------------------------------------------------------------------

LABS_ROADMAP = [
    # Level 2? No — Labs 11–30 remain Level 1 (Basic track).
    (11, "Identify a fake customer-support message", "basic"),
    (12, "Recognize a password-reset scam", "basic"),
    (13, "Detect a suspicious social media account", "basic"),
    (14, "Identify an impersonation attempt", "basic"),
    (15, "Recognize a fake refund notification", "basic"),
    (16, "Identify a suspicious payment request", "basic"),
    (17, "Detect a fake login page", "basic"),
    (18, "Recognize an unexpected MFA request", "basic"),
    (19, "Identify unsafe public Wi-Fi behaviour", "basic"),
    (20, "Choose a strong password strategy", "basic"),
    (21, "Select appropriate MFA options", "basic"),
    (22, "Configure privacy settings in a simulator", "basic"),
    (23, "Verify a job opportunity independently", "basic"),
    (24, "Verify a banking notification safely", "basic"),
    (25, "Recognize suspicious online shopping messages", "basic"),
    (26, "Identify warning signs in a phone transcript", "basic"),
    (27, "Recognize shoulder-surfing risks", "basic"),
    (28, "Identify a tailgating attempt", "basic"),
    (29, "Choose a safe response to an unknown USB device", "basic"),
    (30, "Complete the Basic Cyber Safety Challenge", "basic"),
    (31, "Analyze a suspicious email header", "intermediate"),
    (32, "Compare sender and reply-to addresses", "intermediate"),
    (33, "Examine URL characteristics safely", "intermediate"),
    (34, "Analyze a simulated phishing landing page", "intermediate"),
    (35, "Investigate a fake recruitment campaign", "intermediate"),
    (36, "Identify business email compromise indicators", "intermediate"),
    (37, "Investigate a suspicious invoice", "intermediate"),
    (38, "Analyze a suspicious WhatsApp conversation", "intermediate"),
    (39, "Respond to a simulated vishing call", "intermediate"),
    (40, "Investigate an MFA fatigue scenario", "intermediate"),
    (41, "Investigate a suspicious account-recovery request", "intermediate"),
    (42, "Identify manipulation techniques in a pretext", "intermediate"),
    (43, "Investigate a fake executive request", "intermediate"),
    (44, "Build an incident timeline", "intermediate"),
    (45, "Classify collected evidence", "intermediate"),
    (46, "Preserve a simulated email artefact", "intermediate"),
    (47, "Prioritize security alerts", "intermediate"),
    (48, "Determine the scope of a simulated compromise", "intermediate"),
    (49, "Recommend account-containment steps", "intermediate"),
    (50, "Create an incident-report draft", "intermediate"),
    (51, "Investigate a suspicious QR-code campaign", "intermediate"),
    (52, "Examine a fake social media profile", "intermediate"),
    (53, "Identify risks in a simulated payment workflow", "intermediate"),
    (54, "Investigate a malicious attachment scenario without executing it", "intermediate"),
    (55, "Verify a vendor's identity", "intermediate"),
    (56, "Identify physical-access control failures", "intermediate"),
    (57, "Analyze a simulated data-disclosure incident", "intermediate"),
    (58, "Build a user-awareness improvement plan", "intermediate"),
    (59, "Complete an incident-response tabletop exercise", "intermediate"),
    (60, "Complete the Intermediate Security Investigation Challenge", "intermediate"),
    (61, "Investigate a multi-channel phishing campaign", "advanced"),
    (62, "Correlate suspicious email and login events", "advanced"),
    (63, "Investigate a simulated account takeover", "advanced"),
    (64, "Analyze a business email compromise incident", "advanced"),
    (65, "Investigate a vendor impersonation scenario", "advanced"),
    (66, "Respond to a synthetic deepfake voice request", "advanced"),
    (67, "Analyze a multi-stage recruitment scam", "advanced"),
    (68, "Investigate suspicious password-reset activity", "advanced"),
    (69, "Build a complete incident timeline", "advanced"),
    (70, "Prioritize containment decisions", "advanced"),
    (71, "Distinguish malicious indicators from benign activity", "advanced"),
    (72, "Investigate simulated identity-verification failures", "advanced"),
    (73, "Analyze a physical and digital attack chain", "advanced"),
    (74, "Review a fictional organization's security controls", "advanced"),
    (75, "Develop a phishing-reporting workflow", "advanced"),
    (76, "Analyze a simulated executive impersonation incident", "advanced"),
    (77, "Investigate a suspicious OAuth-consent scenario", "advanced"),
    (78, "Review identity and access-management weaknesses", "advanced"),
    (79, "Analyze an insider-assisted social engineering scenario", "advanced"),
    (80, "Develop a targeted awareness intervention", "advanced"),
    (81, "Design a safe phishing-awareness exercise", "advanced"),
    (82, "Evaluate user-reported security alerts", "advanced"),
    (83, "Investigate a synthetic payment-diversion incident", "advanced"),
    (84, "Correlate endpoint and authentication alerts", "advanced"),
    (85, "Develop a containment and recovery plan", "advanced"),
    (86, "Evaluate incident-response decisions", "advanced"),
    (87, "Conduct a security-awareness risk assessment", "advanced"),
    (88, "Create a measurable training-improvement plan", "advanced"),
    (89, "Complete an advanced incident simulation", "advanced"),
    (90, "Complete the Advanced Cyber Defense Challenge", "advanced"),
    (91, "Investigate a complete simulated phishing incident", "capstone"),
    (92, "Analyze a complex identity-impersonation scenario", "capstone"),
    (93, "Investigate a synthetic executive fraud incident", "capstone"),
    (94, "Correlate email, identity and endpoint evidence", "capstone"),
    (95, "Develop a defensive playbook", "capstone"),
    (96, "Design an awareness program for a fictional organization", "capstone"),
    (97, "Evaluate a simulated incident-response team", "capstone"),
    (98, "Conduct a tabletop exercise", "capstone"),
    (99, "Complete a multi-stage cyber-awareness investigation", "capstone"),
    (100, "Complete the CyberQuest Master Capstone", "capstone"),
]


# ---------------------------------------------------------------------------
# Learning path / modules for the video curriculum
# ---------------------------------------------------------------------------

LEARNING_PATH = {
    "slug": "social-engineering-awareness",
    "title_en": "Social Engineering Awareness",
    "title_hi": "सोशल इंजीनियरिंग जागरूकता",
    "description_en": (
        "A guided path from cyber-safety basics to expert incident investigation, "
        "built from video lessons, comics, games and 100 connected practical labs."
    ),
    "description_hi": (
        "साइबर सुरक्षा की बुनियाद से विशेषज्ञ स्तर की जाँच तक — वीडियो पाठ, कॉमिक, "
        "गेम और 100 जुड़ी प्रैक्टिकल लैब से बना मार्ग।"
    ),
    "modules": [
        ("foundations", "Cybersecurity Foundations", "साइबर सुरक्षा की बुनियाद"),
        ("phishing", "Phishing", "फ़िशिंग"),
        ("messaging", "Messaging and Social Media", "मैसेजिंग और सोशल मीडिया"),
        ("financial", "Financial Scams", "वित्तीय ठगी"),
        ("voice", "Voice and Identity", "आवाज़ और पहचान"),
        ("physical", "Physical Security", "भौतिक सुरक्षा"),
        ("workplace", "Workplace Security", "कार्यस्थल सुरक्षा"),
        ("personal", "Personal Digital Safety", "व्यक्तिगत डिजिटल सुरक्षा"),
        ("incident", "Incident Response", "घटना पर प्रतिक्रिया"),
        ("advanced", "Advanced Awareness", "उच्च जागरूकता"),
    ],
}


# ---------------------------------------------------------------------------
# Video lessons — prototype assets with original scripts
# ---------------------------------------------------------------------------

VIDEO_LESSONS = [
    {
        "module": "foundations",
        "slug": "what-is-social-engineering",
        "title_en": "What Is Social Engineering?",
        "title_hi": "सोशल इंजीनियरिंग क्या है?",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Scams target people, not machines. Learn why the human being is the first door.",
        "summary_hi": "ठगी लोगों को निशाना बनाती है, मशीनों को नहीं। जानें कि इंसान ही पहला दरवाज़ा क्यों है।",
        "script_en": (
            "Open on a locked office building at night. Narration: 'This building has cameras, "
            "locks and alarms. So why do attackers keep getting in?'\n"
            "Cut to a morning scene: a delivery person in uniform holds two heavy boxes at the "
            "door. The receptionist smiles and holds the door open.\n"
            "Narration: 'Because the easiest way past every control is a polite request.'\n"
            "Definition card: Social engineering is the use of psychological pressure — trust, "
            "authority, fear, curiosity — to make a person do something that helps the attacker.\n"
            "Three-step diagram: (1) The attacker studies you. (2) The attacker builds a believable "
            "story. (3) The attacker asks for one small action.\n"
            "Callback: 'A real delivery driver used the front door. So did the fake one. The door "
            "never asks for ID — you do.'\n"
            "Interactive question: Which control stopped neither the real nor the fake visitor?"
        ),
        "narration_en": (
            "Every lock on that building was working. The weakness was a person trying to be helpful. "
            "Social engineering is not hacking a computer. It is hacking a decision."
        ),
        "transcript_en": "[00:00] Locked office building at night. [00:08] Delivery scene. [00:20] Definition card. [00:35] Three-step diagram. [00:55] Callback and question.",
        "questions": [
            ("Social engineering mainly targets…", ["Weak software", "People and their decisions",
                                                    "Network cables", "Printer firmware"], 1,
             "It manipulates people into making an unsafe decision."),
        ],
    },
    {
        "module": "foundations",
        "slug": "why-humans-become-targets",
        "title_en": "Why Humans Become Targets",
        "title_hi": "इंसान ही निशाना क्यों बनते हैं",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Helpfulness, habit and authority are normal traits an attacker can borrow.",
        "summary_hi": "मदद करने की आदत, रोज़ की आदत और अधिकार का डर — ठग इन्हीं का फ़ायदा उठाता है।",
        "script_en": (
            "Four short scenes. One: a guard opens a door for a person carrying coffee. Two: an "
            "employee clicks 'OK' without reading a pop-up. Three: a junior answers a call from "
            "'the CEO'. Four: a student accepts a friend request from a look-alike profile.\n"
            "Narration: 'None of these people were careless. They were human.'\n"
            "Diagram of the six levers: authority, urgency, helpfulness, familiarity, curiosity, "
            "fear of consequences.\n"
            "Close: 'Attackers do not need you to be foolish. They only need you to be normal, "
            "at a moment when you are busy.'"
        ),
        "narration_en": "The traits that make a good colleague make a good target: you help, you trust, you do not want to be rude, and you are usually in a hurry.",
        "transcript_en": "[00:00] Guard scene. [00:15] Pop-up scene. [00:30] CEO call scene. [00:45] Friend request scene. [01:05] Six levers diagram.",
        "questions": [
            ("Which trait do attackers most often borrow?", ["Rudeness", "Helpfulness", "Laziness", "Anger"], 1,
             "Willingness to help is the most frequently exploited trait."),
        ],
    },
    {
        "module": "foundations",
        "slug": "how-scammers-build-trust",
        "title_en": "How Scammers Build Trust",
        "title_hi": "ठग भरोसा कैसे बनाते हैं",
        "difficulty": "beginner",
        "duration": 6,
        "summary_en": "Logos, familiar language, correct order details — all cheap to copy.",
        "summary_hi": "लोगो, जानी-पहचानी भाषा, सही ऑर्डर विवरण — ये सब कॉपी करना आसान है।",
        "script_en": (
            "Show a message with a perfect logo, correct order number and polite tone.\n"
            "Narration: 'This looks real. It should. Everything you can see is free to copy.'\n"
            "Reveal a spreadsheet of a leaked database with names and order IDs; highlight that "
            "small details come from breaches, not from the company.\n"
            "Rule card: Trust must come from an independent channel, not from the message itself."
        ),
        "narration_en": "Never verify a message using the contact details inside that same message.",
        "transcript_en": "[00:00] Perfect-looking message. [00:20] Data-breach reveal. [00:50] Rule card.",
        "questions": [
            ("What proves a message is genuine?", ["A correct logo", "Your real order number",
                                                   "Independent verification", "Polite tone"], 2,
             "Only verification through a channel you already trust proves anything."),
        ],
    },
    {
        "module": "foundations",
        "slug": "recognizing-manipulation",
        "title_en": "Recognizing Manipulation and Urgency",
        "title_hi": "हेर-फेर और जल्दबाज़ी पहचानना",
        "difficulty": "beginner",
        "duration": 6,
        "summary_en": "A countdown clock is a tactic, not a fact.",
        "summary_hi": "उलटी गिनती एक चाल है, सच्चाई नहीं।",
        "script_en": (
            "Split screen: left, a normal bank notice with a 30-day window; right, a fake alert "
            "with 'act in 10 minutes'.\n"
            "Narration: 'One of these wants a decision. The other wants a reaction.'\n"
            "Technique cards: urgency, scarcity, authority, social proof, fear, guilt.\n"
            "Two-second rule: 'Say it out loud: why is this urgent? Real processes are patient.'"
        ),
        "narration_en": "Urgency is the single most reliable warning sign, because no legitimate organisation needs your password in ten minutes.",
        "transcript_en": "[00:00] Split screen. [00:25] Six technique cards. [01:00] Two-second rule.",
        "questions": [
            ("The strongest general warning sign is…", ["Bad grammar", "Manufactured urgency",
                                                        "Missing logo", "Long email"], 1,
             "Urgency is engineered to stop you from checking."),
        ],
    },
    {
        "module": "foundations",
        "slug": "first-cyber-safety-mission",
        "title_en": "Your First Cyber Safety Mission",
        "title_hi": "आपका पहला साइबर सुरक्षा अभियान",
        "difficulty": "beginner",
        "duration": 4,
        "summary_en": "One habit: pause, verify, report.",
        "summary_hi": "एक आदत: रुकें, पुष्टि करें, रिपोर्ट करें।",
        "script_en": (
            "A learner receives a suspicious message. An on-screen prompt appears: PAUSE.\n"
            "Then: VERIFY — open the official app, not the link.\n"
            "Then: REPORT — send it to the security team or platform.\n"
            "Narration: 'Three steps. Ten seconds. That is the whole mission.'\n"
            "End card: 'Your brain is your best firewall.'"
        ),
        "narration_en": "Pause, verify, report. Practise it until it is automatic.",
        "transcript_en": "[00:00] Suspicious message. [00:10] PAUSE prompt. [00:25] VERIFY step. [00:40] REPORT step. [00:55] End card.",
        "questions": [
            ("After receiving a suspicious request you should…", ["Delete it silently",
                                                                  "Reply asking who they are",
                                                                  "Pause, verify independently, then report",
                                                                  "Forward it to friends"], 2,
             "Pause, verify through a trusted channel, then report."),
        ],
    },
    {
        "module": "phishing",
        "slug": "anatomy-of-a-phishing-email",
        "title_en": "Anatomy of a Phishing Email",
        "title_hi": "फ़िशिंग ईमेल की बनावट",
        "difficulty": "beginner",
        "duration": 7,
        "summary_en": "Five parts: sender, subject, greeting, body, link or attachment.",
        "summary_hi": "पाँच हिस्से: प्रेषक, विषय, संबोधन, सामग्री, लिंक या अटैचमेंट।",
        "script_en": (
            "An X-ray effect reveals the hidden layers of an email: real sender address, reply-to, "
            "link destination, attachment type.\n"
            "Narration: 'What you see is a name. What matters is the address behind it.'\n"
            "Each layer is labelled with a check question.\n"
            "Close: hover before you click; expand before you trust."
        ),
        "narration_en": "Check the address, not the name. Hover the link, do not click it.",
        "transcript_en": "[00:00] X-ray reveal. [00:30] Sender layer. [00:50] Reply-to layer. [01:10] Link layer. [01:30] Attachment layer.",
        "questions": [
            ("The part of a sender address that matters is…", ["The display name", "The part after @",
                                                               "The signature", "The subject"], 1,
             "The domain after @ is the only part an attacker cannot fake at will."),
        ],
    },
    {
        "module": "phishing",
        "slug": "spotting-suspicious-links",
        "title_en": "Spotting Suspicious Links",
        "title_hi": "संदिग्ध लिंक पहचानना",
        "difficulty": "beginner",
        "duration": 6,
        "summary_en": "Read right to left, stop at the first single slash.",
        "summary_hi": "दाएँ से बाएँ पढ़ें, पहले अकेले स्लैश पर रुकें।",
        "script_en": (
            "A giant URL is shown on screen. A marker moves along it.\n"
            "Narration: 'Start at the right. Find the first single slash. The word just before it is "
            "the real destination.'\n"
            "Four examples are dissected: subdomain trap, hyphen trick, homoglyph, shortener.\n"
            "Rule: if the destination is not the company's own domain, stop."
        ),
        "narration_en": "Reading a link properly takes five seconds and prevents most credential theft.",
        "transcript_en": "[00:00] URL anatomy. [00:30] Four traps. [01:10] Rule card.",
        "questions": [
            ("In http://bank.com.secure-login.net/pay, the real domain is…",
             ["bank.com", "secure-login.net", "pay", "com.secure"], 1,
             "The domain immediately before the first single slash is the real destination."),
        ],
    },
    {
        "module": "phishing",
        "slug": "fake-login-pages",
        "title_en": "Fake Login Pages",
        "title_hi": "नकली लॉगिन पेज",
        "difficulty": "beginner",
        "duration": 6,
        "summary_en": "A copied page cannot copy your browser's memory of the real site.",
        "summary_hi": "नकली पेज आपके ब्राउज़र की असली साइट की पहचान नहीं बदल सकता।",
        "script_en": (
            "Two login pages side by side, visually identical.\n"
            "Zoom into the address bar of each: one shows the bank's domain, the other a look-alike.\n"
            "Narration: 'A criminal can copy every pixel. They cannot copy the address bar.'\n"
            "Warning: never enter credentials on a page reached from a message link — open the app "
            "or type the address yourself."
        ),
        "narration_en": "Always arrive at a login page from a bookmark or by typing the address, never from a message.",
        "transcript_en": "[00:00] Two pages. [00:25] Address bar zoom. [00:50] Rule card.",
        "questions": [
            ("The safest way to reach a login page is…", ["From an email link",
                                                           "From a search ad",
                                                           "By typing the address or using a bookmark",
                                                           "From a QR code"], 2,
             "Type the address yourself or use a saved bookmark."),
        ],
    },
    {
        "module": "phishing",
        "slug": "spear-phishing",
        "title_en": "Spear Phishing and Targeted Attacks",
        "title_hi": "स्पियर फ़िशिंग और लक्षित हमले",
        "difficulty": "intermediate",
        "duration": 7,
        "summary_en": "When the message knows your project, your manager and your deadline.",
        "summary_hi": "जब संदेश को आपका प्रोजेक्ट, आपका मैनेजर और डेडलाइन पता हो।",
        "script_en": (
            "A message references a real project, a real manager and an internal file name.\n"
            "Narration: 'This one is hard, because the attacker did their homework.'\n"
            "Where the details come from: social media, job posts, a previous breach, an "
            "auto-reply with your out-of-office message.\n"
            "Defence: verify unusual requests by calling a number you already have."
        ),
        "narration_en": "Personalisation is not proof. It is research.",
        "transcript_en": "[00:00] Targeted message. [00:30] Research sources. [01:00] Defence: call a known number.",
        "questions": [
            ("A message that mentions your real project proves…", ["It is genuine",
                                                                   "The sender researched you",
                                                                   "You were hacked", "Nothing at all"], 1,
             "Personal details show research, not authenticity."),
        ],
    },
    {
        "module": "phishing",
        "slug": "qr-code-phishing",
        "title_en": "QR-Code Phishing",
        "title_hi": "QR कोड फ़िशिंग",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "A QR code hides its destination — and stickers can be pasted over real ones.",
        "summary_hi": "QR कोड अपना गंतव्य छिपाता है — और असली कोड पर स्टिकर चिपके हो सकते हैं।",
        "script_en": (
            "A payment counter is shown. A sticker QR code is lifted slightly, revealing the shop's "
            "real code underneath.\n"
            "Narration: 'A QR code is just a link in a disguise.'\n"
            "Rules: preview the URL before opening, never enter a UPI PIN to receive money, and "
            "check for peeling stickers and pasted panels."
        ),
        "narration_en": "Preview the link, never pay to receive money, and look for covered codes.",
        "transcript_en": "[00:00] Sticker peel reveal. [00:25] Preview rule. [00:45] UPI PIN rule.",
        "questions": [
            ("You need a UPI PIN to…", ["Receive money", "Authorise a payment",
                                        "Check your balance", "Block a card"], 1,
             "A PIN authorises money leaving your account."),
        ],
    },
]


# ---------------------------------------------------------------------------
# Comics — prototype stories with original captions
# ---------------------------------------------------------------------------

COMIC_PLACEHOLDER = "/static/images/panel-placeholder.svg"

COMICS = [
    {
        "slug": "the-internship-that-never-existed",
        "collection": "Fake Job Offer Investigations",
        "title_en": "The Internship That Never Existed",
        "title_hi": "जो इंटर्नशिप कभी थी ही नहीं",
        "character": "Aarav, a final-year college student",
        "difficulty": "beginner",
        "panel_bilingual": True,
        "situation_en": "Aarav receives a high-salary internship offer on WhatsApp.",
        "situation_hi": "आरव को WhatsApp पर मोटी सैलरी वाली इंटर्नशिप का ऑफ़र मिलता है।",
        "problem_en": "The recruiter asks for a registration fee before joining.",
        "problem_hi": "भर्तीकर्ता जॉइनिंग से पहले रजिस्ट्रेशन फ़ीस माँगता है।",
        "decision_en": "Aarav notices the email domain is not the company's official domain.",
        "decision_hi": "आरव देखता है कि ईमेल डोमेन कंपनी का आधिकारिक डोमेन नहीं है।",
        "resolution_en": "He checks the official careers page, finds no such opening, and reports it.",
        "resolution_hi": "वह आधिकारिक करियर पेज देखता है, ऐसी कोई भर्ती नहीं मिलती, और रिपोर्ट कर देता है।",
        "lessons_en": ["Legitimate employers never charge you a fee.",
                       "Verify the recruiter's domain, not their logo.",
                       "Always confirm openings on the official careers page."],
        "lessons_hi": ["असली नियोक्ता कभी फ़ीस नहीं लेते।",
                       "लोगो नहीं, भर्तीकर्ता का डोमेन जाँचें।",
                       "भर्ती की पुष्टि कंपनी के आधिकारिक करियर पेज पर करें।"],
        "panels": [
            ("Aarav's phone lights up: 'Selected for internship — ₹45,000/month!'",
             "आरव का फ़ोन बजता है: 'इंटर्नशिप के लिए चयनित — ₹45,000 प्रति माह!'"),
            ("The recruiter adds: 'Pay ₹1,999 registration fee today to confirm your seat.'",
             "भर्तीकर्ता कहता है: 'सीट पक्की करने के लिए आज ₹1,999 रजिस्ट्रेशन फ़ीस भरें।'"),
            ("Aarav zooms in on the sender: hr@techmahindra-careers.online — that is not the company's domain.",
             "आरव प्रेषक को ज़ूम करता है: hr@techmahindra-careers.online — यह कंपनी का डोमेन नहीं है।"),
            ("He opens the company's official careers page. No such internship exists.",
             "वह कंपनी का आधिकारिक करियर पेज खोलता है। ऐसी कोई इंटर्नशिप नहीं है।"),
            ("Aarav blocks the number and reports the message. His friend is warned in time.",
             "आरव नंबर ब्लॉक कर संदेश की रिपोर्ट करता है। उसका दोस्त समय रहते बच जाता है।"),
        ],
        "related_lab_number": 9,
    },
    {
        "slug": "the-parcel-that-was-never-sent",
        "collection": "WhatsApp Scam Survivors",
        "title_en": "The Parcel That Was Never Sent",
        "character": "Meera, a working mother",
        "difficulty": "beginner",
        "situation_en": "Meera gets a WhatsApp message about a held parcel needing a ₹25 fee.",
        "problem_en": "The payment page asks for full card details.",
        "decision_en": "She checks the tracking number on the official courier site instead.",
        "resolution_en": "No such parcel exists; she reports and blocks the number.",
        "lessons_en": ["Tiny fees are bait for card details.",
                       "Verify on the official app or website.",
                       "Never reply to confirm your number is active."],
        "panels": [
            ("Meera is cooking when her phone buzzes with a delivery message.",
             ""),
            ("It says: 'Parcel held. Pay ₹25 within 12 hours.'", ""),
            ("She opens the official courier app and searches the tracking number.", ""),
            ("'No shipment found.' The message was fake all along.", ""),
            ("She blocks the sender and tells her family group what to watch for.", ""),
        ],
        "related_lab_number": 7,
    },
    {
        "slug": "the-refund-that-reversed",
        "collection": "Digital Banking Safety",
        "title_en": "The Refund That Reversed",
        "character": "Rahul, a small business owner",
        "difficulty": "intermediate",
        "situation_en": "A 'customer care' agent offers an instant refund for a failed transaction.",
        "problem_en": "The agent sends a 'receive money' request instead of a refund.",
        "decision_en": "Rahul spots that receiving money never needs a PIN.",
        "resolution_en": "He declines, hangs up, and calls the bank's official number.",
        "lessons_en": ["A refund never requires your PIN.",
                       "Requests marked 'collect' take money out.",
                       "Call the number printed on your card, not the one in the message."],
        "panels": [
            ("Rahul's payment failed and he searches for customer care online.", ""),
            ("He calls a number from an advertisement and reaches a 'support agent'.", ""),
            ("The agent sends a UPI request: 'Approve this to receive your refund.'", ""),
            ("Rahul notices the request is a collect request. Approving it would pay the scammer.", ""),
            ("He hangs up and calls the bank's official helpline instead.", ""),
        ],
        "related_lab_number": 15,
    },
    {
        "slug": "the-manager-who-was-not-there",
        "collection": "Workplace Cyber Heroes",
        "title_en": "The Manager Who Was Not There",
        "character": "Priya, an accounts executive",
        "difficulty": "intermediate",
        "situation_en": "An email appears to come from the CFO asking for an urgent vendor payment.",
        "problem_en": "The reply-to address is different from the sender address.",
        "decision_en": "Priya calls the CFO's known number to confirm.",
        "resolution_en": "It was business email compromise; the payment is stopped in time.",
        "lessons_en": ["Urgent payment requests must be verified by voice.",
                       "Compare sender and reply-to addresses.",
                       "Follow the two-person approval rule, even for executives."],
        "panels": [
            ("Priya receives an urgent email from the 'CFO' about a confidential payment.", ""),
            ("The amount is large and the deadline is 'within the hour'.", ""),
            ("She expands the reply-to address. It is a free webmail account.", ""),
            ("She calls the CFO on the number saved in her phone. He never sent it.", ""),
            ("The finance team files the incident report. The fraud is contained.", ""),
        ],
        "related_lab_number": 36,
    },
    {
        "slug": "the-usb-in-the-car-park",
        "collection": "Physical Security Adventures",
        "title_en": "The USB in the Car Park",
        "character": "Sameer, an office intern",
        "difficulty": "beginner",
        "situation_en": "Sameer finds an unlabelled USB drive near the office gate.",
        "problem_en": "Curiosity says plug it in; policy says otherwise.",
        "decision_en": "He hands it to the security desk without plugging it in.",
        "resolution_en": "The security team examines it in an isolated lab and finds it malicious.",
        "lessons_en": ["Never plug in an unknown device.",
                       "Hand found media to security.",
                       "Curiosity is the attack vector here."],
        "panels": [
            ("Sameer spots a shiny USB drive on the pavement near the entrance.", ""),
            ("A colleague says: 'Just check whose it is on your laptop.'", ""),
            ("Sameer remembers the awareness poster: unknown drives can carry malware.", ""),
            ("He drops it in the security box without touching his computer.", ""),
            ("Security later confirms the drive was a simulation of a real attack.", ""),
        ],
        "related_lab_number": 29,
    },
    {
        "slug": "the-voice-that-sounded-like-dad",
        "collection": "Deepfake Detectives",
        "title_en": "The Voice That Sounded Like Dad",
        "character": "Nisha, a first-year student",
        "difficulty": "advanced",
        "situation_en": "Nisha gets a call in her father's voice asking for an urgent transfer.",
        "problem_en": "The voice is convincing but the request is unusual and rushed.",
        "decision_en": "She hangs up and calls her father directly.",
        "resolution_en": "It was a synthetic voice. Her father is fine and no money is sent.",
        "lessons_en": ["A familiar voice is not proof of identity.",
                       "Agree on a family verification phrase.",
                       "Urgency plus money equals pause."],
        "panels": [
            ("Nisha answers a call. It is her father's voice, but he sounds panicked.", ""),
            ("'I am in trouble, send money to this account right now.'", ""),
            ("Nisha notices the line quality and the strange urgency.", ""),
            ("She hangs up and dials her father's number directly.", ""),
            ("He answers calmly at home. The voice was a synthetic copy.", ""),
        ],
        "related_lab_number": 23,
    },
    {
        "slug": "the-friend-who-was-a-copy",
        "collection": "Social Media Mysteries",
        "title_en": "The Friend Who Was a Copy",
        "character": "Kabir, a college student",
        "difficulty": "beginner",
        "situation_en": "A duplicate profile of Kabir's friend sends a loan request.",
        "problem_en": "The profile uses the same photos but a slightly altered username.",
        "decision_en": "Kabir calls his friend offline to confirm.",
        "resolution_en": "The copy is reported and removed; a second classmate was almost caught.",
        "lessons_en": ["Compare usernames letter by letter.",
                       "Verify off-platform before sending money.",
                       "Report cloned profiles to the platform."],
        "panels": [
            ("A friend request arrives from someone who looks exactly like Kabir's friend.", ""),
            ("The account messages: 'I need ₹8,000 urgently, sending my QR code.'", ""),
            ("Kabir notices the username has an extra underscore.", ""),
            ("He calls his friend. The real friend never messaged him.", ""),
            ("They report the cloned profile together and warn the class group.", ""),
        ],
        "related_lab_number": 13,
    },
    {
        "slug": "grandmother-and-the-lottery",
        "collection": "Family Cyber Safety",
        "title_en": "Grandmother and the Lottery",
        "character": "Kamla, a retired teacher",
        "difficulty": "beginner",
        "situation_en": "Kamla receives a message saying she won a lottery.",
        "problem_en": "She is asked to pay a processing fee to release the prize.",
        "decision_en": "She shares the message with her granddaughter instead of paying.",
        "resolution_en": "The family confirms the fraud and reports the number.",
        "lessons_en": ["You cannot win a draw you never entered.",
                       "Never pay to receive a prize.",
                       "Talk to family before acting on surprising news."],
        "panels": [
            ("Kamla's phone shows a message: 'You have won ₹25,00,000!'", ""),
            ("A caller explains that a ₹6,500 fee will release the prize.", ""),
            ("Kamla feels excited but calls her granddaughter first.", ""),
            ("Her granddaughter explains that this is a well-known prize scam.", ""),
            ("Kamla blocks the number and shares the story in the family group.", ""),
        ],
        "related_lab_number": 8,
    },
    {
        "slug": "the-invitation-that-was-a-trap",
        "collection": "Phishing Detectives",
        "title_en": "The Invitation That Was a Trap",
        "character": "Riya, an event coordinator",
        "difficulty": "beginner",
        "situation_en": "Riya receives a wedding invitation attachment from an unknown sender.",
        "problem_en": "The attachment asks her to enable macros and sign in with her work email.",
        "decision_en": "She checks the domain, hovers over the link and refuses to sign in.",
        "resolution_en": "She reports the message and the mail gateway blocks the sender.",
        "lessons_en": ["Hover before you click.",
                       "No document needs your email password.",
                       "Report, do not delete quietly."],
        "panels": [
            ("An invitation email arrives with a colourful attachment.", ""),
            ("Opening it shows a fake sign-in screen asking for work credentials.", ""),
            ("Riya hovers the link: the destination is not the company domain.", ""),
            ("She closes the file without entering anything.", ""),
            ("She reports it to IT and warns her team.", ""),
        ],
        "related_lab_number": 5,
    },
    {
        "slug": "the-airport-wifi",
        "collection": "Real-World Cyber Incident Stories",
        "title_en": "The Airport Wi-Fi",
        "character": "Arjun, a travelling consultant",
        "difficulty": "intermediate",
        "situation_en": "Arjun logs into a free airport Wi-Fi that looks official.",
        "problem_en": "The network mimics the airport's real network and intercepts his logins.",
        "decision_en": "He uses his phone hotspot for anything sensitive.",
        "resolution_en": "The fake network is reported; his company enables VPN-only access.",
        "lessons_en": ["Confirm the exact network name with staff.",
                       "Avoid logins on public Wi-Fi without a VPN.",
                       "Use mobile data for sensitive work."],
        "panels": [
            ("Arjun settles at the gate and sees two networks: 'Airport_Free' and 'Airport Free WiFi'.", ""),
            ("He picks the one with the strongest signal and a login page.", ""),
            ("The page asks for his email password to 'activate' the internet.", ""),
            ("He disconnects and turns on his phone hotspot instead.", ""),
            ("At the office, IT confirms the twin network was an evil-twin hotspot.", ""),
        ],
        "related_lab_number": 19,
    },
]


# ---------------------------------------------------------------------------
# Games
# ---------------------------------------------------------------------------

GAMES = [
    {
        "slug": "spot-the-phish",
        "title_en": "Spot the Phish",
        "title_hi": "फ़िशिंग पहचानें",
        "instructions_en": (
            "You will see ten simulated messages and notifications. For each one decide what a "
            "careful person should do. There is no timer — read carefully. Every decision comes "
            "with an explanation, so a wrong answer is a lesson, not a penalty."
        ),
        "instructions_hi": (
            "आप दस नकली संदेश देखेंगे। हर संदेश पर तय करें कि सावधान व्यक्ति क्या करेगा। कोई समय "
            "सीमा नहीं है — ध्यान से पढ़ें। हर उत्तर के साथ समझ भी मिलेगी, इसलिए गलती सज़ा नहीं, पाठ है।"
        ),
        "debrief_en": (
            "Phishing survives because it exploits routine. The reliable defence is a habit: pause, "
            "verify through a channel you already trust, then report. Never verify a message using "
            "the contact details inside it."
        ),
        "debrief_hi": (
            "फ़िशिंग इसलिए चलती है क्योंकि वह हमारी आदतों का फ़ायदा उठाती है। सुरक्षा एक आदत से आती है: "
            "रुकें, अपने भरोसेमंद माध्यम से पुष्टि करें, फिर रिपोर्ट करें। संदेश में दिए नंबर या लिंक से "
            "कभी पुष्टि न करें।"
        ),
        "difficulty": "beginner",
        "timed": False,
        "xp": 40,
        "scenarios": [
            {
                "type": "email",
                "sender": "security@paypa1-alerts.com",
                "subject": "Your account has been limited",
                "body": "We detected unusual activity. Verify your identity within 24 hours or your funds will be frozen and your account closed.",
                "meta": {"links": ["http://paypa1-alerts.com/verify"], "attachments": []},
                "is_threat": True,
                "warning_signs_en": "Look-alike domain with a digit (paypa1), a threat of frozen funds, 24-hour deadline, and a link that is unencrypted (http).",
                "warning_signs_hi": "डिजिट वाला मिलता-जुलता डोमेन (paypa1), पैसे रुकने की धमकी, 24 घंटे की सीमा, और असुरक्षित (http) लिंक।",
                "explanation_en": "Payment platforms do not warn you to verify through a link in an email. Open the official app instead.",
                "explanation_hi": "भुगतान कंपनियाँ ईमेल के लिंक से पुष्टि नहीं करातीं। आधिकारिक ऐप खोलें।",
                "choices": [
                    ("Click the link and verify quickly", False,
                     "You would have handed your credentials to the attacker.", "आपने ठग को अपनी जानकारी दे दी होती।"),
                    ("Report the message and open the official app instead", True,
                     "Correct. Verify in a channel you already trust.", "सही। अपने भरोसेमंद माध्यम में पुष्टि करें।"),
                    ("Reply asking them to confirm the account number", False,
                     "Replying only confirms your address is live.", "जवाब देने से पता चल जाता है कि आपका पता चालू है।"),
                ],
            },
            {
                "type": "sms",
                "sender": "VM-AMZNIN",
                "subject": "Delivery update",
                "body": "Your Amazon order will be returned to sender. Update your address: http://amaz0n-in.redeliver.top/addr",
                "meta": {"links": ["http://amaz0n-in.redeliver.top/addr"]},
                "is_threat": True,
                "warning_signs_en": "Digit-swapped brand (amaz0n), unrelated domain (redeliver.top), unencrypted link, and pressure about a return.",
                "warning_signs_hi": "बदला हुआ ब्रांड नाम (amaz0n), असंबंधित डोमेन (redeliver.top), असुरक्षित लिंक और वापसी का दबाव।",
                "explanation_en": "Check delivery status inside the shopping app you already use.",
                "explanation_hi": "डिलीवरी की स्थिति पहले से इस्तेमाल किए जा रहे शॉपिंग ऐप में देखें।",
                "choices": [
                    ("Open the link to save the delivery", False,
                     "The page exists only to capture your details.", "वह पेज सिर्फ़ आपकी जानकारी लेने के लिए है।"),
                    ("Open the shopping app and check the order there", True,
                     "Correct — the app is a trusted channel.", "सही — ऐप भरोसेमंद माध्यम है।"),
                    ("Forward it to family as a warning", False,
                     "Forwarding spreads the link. Report it instead.", "फ़ॉरवर्ड करने से लिंक फैलता है। रिपोर्ट करें।"),
                ],
            },
            {
                "type": "chat",
                "sender": "+91 90XXXXXX21 (unknown)",
                "subject": "Work from home opportunity",
                "body": "Earn ₹3,000 per day liking videos. Pay ₹500 joining deposit, refundable after 3 days.",
                "meta": {},
                "is_threat": True,
                "warning_signs_en": "A deposit to start work, unrealistic daily earnings, unknown number, and a refund promise used as bait.",
                "warning_signs_hi": "काम शुरू करने के लिए जमा राशि, अवास्तविक कमाई, अनजान नंबर और वापसी का लालच।",
                "explanation_en": "Legitimate work never requires you to pay first.",
                "explanation_hi": "असली काम में पहले पैसे देने नहीं पड़ते।",
                "choices": [
                    ("Pay ₹500 — it is refundable after all", False,
                     "The refund never arrives; the first payment is the attack.", "वापसी कभी नहीं आती; पहली राशि ही ठगी है।"),
                    ("Ignore, block and report the number", True,
                     "Correct. Unrealistic earnings plus an entry fee is a scam pattern.", "सही। बड़ी कमाई और पहले फ़ीस — यह ठगी का पैटर्न है।"),
                    ("Ask for the company's website first", False,
                     "Engaging keeps the conversation alive and the pressure building.", "जवाब देने से ठग को और मौका मिलता है।"),
                ],
            },
            {
                "type": "email",
                "sender": "no-reply@github.com",
                "subject": "A new SSH key was added to your account",
                "body": "A new SSH key was added to your account. If you did not make this change, review your security settings at https://github.com/settings/keys",
                "meta": {"links": ["https://github.com/settings/keys"]},
                "is_threat": False,
                "warning_signs_en": "None. Sender domain matches, the link points to the official domain over HTTPS, and it asks you to check the official settings page rather than click a login link.",
                "warning_signs_hi": "कोई नहीं। डोमेन सही है, लिंक आधिकारिक HTTPS पते पर है और लॉगिन लिंक नहीं माँगता।",
                "explanation_en": "Even legitimate notices should be verified by opening the site yourself. If the change is not yours, rotate the key immediately.",
                "explanation_hi": "असली सूचना भी खुद साइट खोलकर जाँचें। अगर बदलाव आपने नहीं किया, तुरंत बदलें।",
                "choices": [
                    ("Report it as phishing immediately", False,
                     "Over-reporting genuine alerts tires your security team.", "असली सूचना को गलत रिपोर्ट करने से टीम थक जाती है।"),
                    ("Ignore it — GitHub emails are never important", False,
                     "Ignoring it wastes the early warning you just received.", "नज़रअंदाज़ करने से चेतावनी बेकार जाती है।"),
                    ("Open the site yourself and check your security settings", True,
                     "Correct — verify from the site, not from the email.", "सही — ईमेल से नहीं, साइट से जाँचें।"),
                ],
            },
            {
                "type": "email",
                "sender": "hr@naukri-careers.online",
                "subject": "Interview scheduled — pay registration",
                "body": "Congratulations, you are shortlisted. Pay ₹1,299 registration to confirm your interview slot. No interview round is required.",
                "meta": {},
                "is_threat": True,
                "warning_signs_en": "Payment for a job, no interview process, and a domain that is not the job portal's real domain.",
                "warning_signs_hi": "नौकरी के लिए भुगतान, कोई इंटरव्यू नहीं, और पोर्टल का असली डोमेन न होना।",
                "explanation_en": "Employers pay employees. A fee is the whole point of the scam.",
                "explanation_hi": "नियोक्ता कर्मचारियों को पैसे देते हैं। फ़ीस लेना ही ठगी का उद्देश्य है।",
                "choices": [
                    ("Pay and confirm the slot", False,
                     "The interview never happens.", "इंटरव्यू कभी नहीं होगा।"),
                    ("Verify the opening on the official careers page", True,
                     "Correct. Apply only through the company's own portal.", "सही। आवेदन कंपनी के अपने पोर्टल से करें।"),
                    ("Share Aadhaar to speed up the process", False,
                     "Identity documents enable fraud in your name.", "पहचान दस्तावेज़ आपके नाम पर ठगी का रास्ता खोलते हैं।"),
                ],
            },
            {
                "type": "call",
                "sender": "Unknown number, claims to be bank fraud team",
                "subject": "Suspicious transaction",
                "body": "Sir, a fraudulent transaction is in progress. To block it, install this remote support app and share the code I send you.",
                "meta": {},
                "is_threat": True,
                "warning_signs_en": "Remote-access software, a one-time code requested over the phone, and urgency. No bank ever asks for this.",
                "warning_signs_hi": "रिमोट-एक्सेस ऐप, फ़ोन पर OTP माँगना और जल्दबाज़ी। कोई बैंक ऐसा नहीं करता।",
                "explanation_en": "Hang up and call the number printed on your card.",
                "explanation_hi": "कॉल काटें और अपने कार्ड पर छपे नंबर पर बात करें।",
                "choices": [
                    ("Install the app to stop the fraud", False,
                     "That gives the caller full control of your device.", "इससे कॉल करने वाले को आपके फ़ोन पर पूरा नियंत्रण मिल जाता है।"),
                    ("Hang up and call the bank's official number", True,
                     "Correct — verify on a channel you chose.", "सही — अपने चुने हुए माध्यम से पुष्टि करें।"),
                    ("Share the code but not the password", False,
                     "The code alone can complete the fraud.", "सिर्फ़ कोड से भी ठगी पूरी हो सकती है।"),
                ],
            },
            {
                "type": "page",
                "sender": "Shared link: yourcompany-portal.com/login",
                "subject": "Document shared with you",
                "body": "A colleague shared a document. Sign in with your work email to view it. The page looks exactly like your company portal.",
                "meta": {},
                "is_threat": True,
                "warning_signs_en": "A look-alike login page outside your company domain asking for work credentials.",
                "warning_signs_hi": "कंपनी के डोमेन के बाहर मिलता-जुलता लॉगिन पेज जो कार्य ईमेल माँगता है।",
                "explanation_en": "Open your real portal from a bookmark and check whether the document exists there.",
                "explanation_hi": "अपना असली पोर्टल बुकमार्क से खोलें और देखें कि दस्तावेज़ वहाँ है या नहीं।",
                "choices": [
                    ("Sign in — the page looks identical", False,
                     "Copying a page is trivial; the domain is not.", "पेज कॉपी करना आसान है; डोमेन नहीं।"),
                    ("Sign in but change the password afterwards", False,
                     "The credentials are stolen at the moment you type them.", "पासवर्ड लिखते ही वह चोरी हो जाता है।"),
                    ("Close it and open the portal from your own bookmark", True,
                     "Correct.", "सही।"),
                ],
            },
            {
                "type": "sms",
                "sender": "VM-HDFCBK",
                "subject": "Transaction alert",
                "body": "Rs.450.00 debited from A/c XX1234 at CHAI POINT on 12-06-26. Balance Rs.12,340.00. Not you? Call 18002586161.",
                "meta": {},
                "is_threat": False,
                "warning_signs_en": "None. The amount, merchant, account and a verifiable helpline are all present, with no link and no request for information.",
                "warning_signs_hi": "कोई नहीं। राशि, दुकान, खाता और असली हेल्पलाइन दी गई है; कोई लिंक या जानकारी की माँग नहीं।",
                "explanation_en": "A transaction alert that states facts and gives no link is normal. Keep it, and check your statement.",
                "explanation_hi": "तथ्य बताने वाली और लिंक रहित सूचना सामान्य है। इसे रखें और स्टेटमेंट जाँचें।",
                "choices": [
                    ("Report it as fraud", False,
                     "This is a normal alert with verifiable details.", "यह सामान्य सूचना है जिसकी जाँच हो सकती है।"),
                    ("Keep it and confirm against your statement", True,
                     "Correct — routine, low-risk handling.", "सही — सामान्य और सुरक्षित तरीका।"),
                    ("Call the number in the message immediately", False,
                     "Only call if you do not recognise the transaction — and use the number on your card.", "सिर्फ़ तब कॉल करें जब लेन-देन पहचान न हो — और कार्ड पर छपे नंबर पर।"),
                ],
            },
            {
                "type": "chat",
                "sender": "Priya (your friend's real account)",
                "subject": "Photo request",
                "body": "Hey, I lost my contacts. Send me your number and the code you just received, I am resetting my account.",
                "meta": {},
                "is_threat": True,
                "warning_signs_en": "Anyone asking for a one-time code is taking over an account — including a real contact whose account may already be compromised.",
                "warning_signs_hi": "जो कोई OTP माँगे, वह खाता हड़पने की कोशिश कर रहा है — भले ही वह जान-पहचान का खाता हो जो पहले ही हैक हो चुका हो।",
                "explanation_en": "Verify by voice. Never forward a code.",
                "explanation_hi": "आवाज़ में पुष्टि करें। कोड कभी न भेजें।",
                "choices": [
                    ("Send the code — it is my friend", False,
                     "Compromised accounts impersonate real friends.", "हैक किए खाते असली दोस्तों का रूप लेते हैं।"),
                    ("Call the friend directly and ask about it", True,
                     "Correct — verify out of band.", "सही — दूसरे माध्यम से पुष्टि करें।"),
                    ("Send only the number, not the code", False,
                     "Contact lists are also sold to scammers.", "संपर्क सूची भी ठगों को बेची जाती है।"),
                ],
            },
            {
                "type": "email",
                "sender": "accounts@vendor-invoices.co",
                "subject": "Updated bank details — please use from now",
                "body": "Our bank details have changed. Please make all future payments to the new account below. Attached is the revised invoice.",
                "meta": {"attachments": ["invoice_revised.pdf"]},
                "is_threat": True,
                "warning_signs_en": "A payment-redirection request, new bank details in an email, and a change of process sent only by message.",
                "warning_signs_hi": "भुगतान का पता बदलने का अनुरोध, ईमेल में नई बैंक जानकारी, और सिर्फ़ संदेश से प्रक्रिया बदलना।",
                "explanation_en": "Call the vendor on a number you already have and confirm before changing payment details.",
                "explanation_hi": "भुगतान जानकारी बदलने से पहले अपने पास मौजूद पुराने नंबर पर सप्लायर से पुष्टि करें।",
                "choices": [
                    ("Update the payment details right away", False,
                     "This is the classic invoice-redirection fraud.", "यह इनवॉइस डायवर्जन की प्रसिद्ध ठगी है।"),
                    ("Call the vendor on a known number to confirm", True,
                     "Correct. Any change of payment details needs voice verification.", "सही। भुगतान जानकारी में बदलाव पर आवाज़ से पुष्टि ज़रूरी है।"),
                    ("Reply to the email and ask for confirmation", False,
                     "You would be confirming with the attacker.", "आप ठग से ही पुष्टि कर रहे होंगे।"),
                ],
            },
        ],
    },
    {
        "slug": "scam-or-legit",
        "title_en": "Scam or Legit?",
        "title_hi": "ठगी या असली?",
        "instructions_en": (
            "Classify eight realistic situations as a scam or a legitimate message, then read the "
            "reasoning. Accuracy matters more than speed, and the challenge is untimed."
        ),
        "instructions_hi": (
            "आठ स्थितियों को ठगी या असली बताएँ, फिर कारण पढ़ें। सही पहचान ज़रूरी है, रफ़्तार नहीं; "
            "कोई समय सीमा नहीं है।"
        ),
        "debrief_en": (
            "Legitimate organisations are patient, provide verifiable details and never need your "
            "password. Scams are urgent, vague about how to verify, and always need one small "
            "action from you right now."
        ),
        "debrief_hi": (
            "असली संस्थाएँ धैर्य रखती हैं, जाँचने लायक जानकारी देती हैं और पासवर्ड नहीं माँगती। ठगी "
            "जल्दबाज़ी कराती है, पुष्टि का रास्ता नहीं देती और हमेशा एक छोटा-सा काम तुरंत कराती है।"
        ),
        "difficulty": "beginner",
        "timed": False,
        "xp": 30,
        "scenarios": [
            ("Your card is blocked. Call this number to reactivate and share the OTP.",
             True, "Banks never ask for an OTP. This is vishing.", "बैंक OTP नहीं माँगते। यह वॉइस ठगी है।"),
            ("A courier app notification shows your parcel is out for delivery today.",
             False, "A notification inside the official app with no request for action is normal.",
             "आधिकारिक ऐप की सूचना और किसी जानकारी की माँग नहीं — यह सामान्य है।"),
            ("Your electricity bill is overdue; pay on this link in 30 minutes or power is cut.",
             True, "Urgency plus a link, with no account number, is a scam pattern.",
             "जल्दबाज़ी के साथ लिंक और खाता संख्या का अभाव — यह ठगी का पैटर्न है।"),
            ("Your bank sends a monthly e-statement to your registered email, with no links.",
             False, "An informational statement with no action request is legitimate.",
             "बिना किसी कार्रवाई की माँग वाला सूचना संदेश असली होता है।"),
            ("A customer-care agent asks you to install AnyDesk to process a refund.",
             True, "Remote-access tools on a support call are a standard fraud.",
             "सपोर्ट कॉल पर रिमोट-एक्सेस ऐप ठगी का आम तरीका है।"),
            ("An order confirmation from the shopping app you just used, sent to your registered email.",
             False, "You initiated the action yourself; the message matches your own transaction.",
             "आपने खुद ऑर्डर किया है; संदेश आपके लेन-देन से मेल खाता है।"),
            ("A recruiter offers double salary and asks for your bank passbook photo before joining.",
             True, "Salary promises plus document requests before an offer is a fraud pattern.",
             "ऑफ़र से पहले दस्तावेज़ माँगना और दोगुनी सैलरी का वादा ठगी है।"),
            ("Your workplace IT team emails from the company domain asking you to change your password at the portal you already use.",
             False, "The domain matches and the action happens in your own portal — verify the domain anyway before acting.",
             "डोमेन सही है और काम अपने ही पोर्टल पर है — फिर भी डोमेन जाँच लें।"),
        ],
    },
]


# ---------------------------------------------------------------------------
# Historical incidents — starter set with confidence labels
#
# Facts here are limited to well-established public reporting. Deep links are
# deliberately not invented: sources point to the publishing organisation.
# Phase 5 of the roadmap expands this set to 30 fully researched cases.
# ---------------------------------------------------------------------------

INCIDENTS = [
    {
        "slug": "rsa-securid-2011",
        "title_en": "The RSA SecurID phishing breach (2011)",
        "year": 2011,
        "organization": "RSA Security (EMC)",
        "sector": "Security technology",
        "category": "Phishing / spear phishing",
        "attack_type": "Spear phishing with a malicious spreadsheet attachment",
        "confidence": "confirmed",
        "summary_en": "A small, well-written email to a handful of employees led to the theft of information related to RSA's SecurID two-factor authentication products.",
        "summary_hi": "कुछ कर्मचारियों को भेजे गए छोटे, भरोसेमंद लगने वाले ईमेल ने RSA के SecurID टू-फैक्टर उत्पादों से जुड़ी जानकारी की चोरी का रास्ता खोला।",
        "what_happened_en": "Employees received a phishing email with a spreadsheet attachment titled to look like a recruitment plan. Opening it installed malware that gave attackers a foothold inside RSA's network, from which information relating to SecurID was taken.",
        "what_happened_hi": "कर्मचारियों को एक स्प्रेडशीट अटैचमेंट वाला फ़िशिंग ईमेल मिला, जिसका नाम भर्ती योजना जैसा लगता था। उसे खोलने पर मैलवेयर आ गया और हमलावरों को नेटवर्क में जगह मिल गई।",
        "how_it_worked_en": "The attachment used a known software vulnerability to execute code. The attackers then moved carefully, escalating access until they reached the systems holding SecurID-related information.",
        "how_it_worked_hi": "अटैचमेंट ने पुरानी सॉफ़्टवेयर कमज़ोरी का फ़ायदा उठाकर कोड चलाया, फिर हमलावर धीरे-धीरे और अधिकार लेते हुए SecurID से जुड़ी जानकारी तक पहुँचे।",
        "weaknesses_en": "A single user opening one attachment was enough; the payload exploited an unpatched application.",
        "weaknesses_hi": "एक उपयोगकर्ता द्वारा एक अटैचमेंट खोलना ही काफी था; कोड पुराने, अपडेट न किए सॉफ़्टवेयर का फ़ायदा उठा रहा था।",
        "consequences_en": "RSA replaced a large number of SecurID tokens for customers. The wider consequence was that a compromise of an authentication vendor weakened the assurance of a second factor for many organisations.",
        "consequences_hi": "RSA को बड़ी संख्या में ग्राहकों के SecurID टोकन बदलने पड़े। व्यापक असर यह हुआ कि प्रमाणीकरण देने वाली कंपनी के हैक होने से कई संस्थाओं के दूसरे कारक पर भरोसा कमज़ोर पड़ा।",
        "discovery_en": "RSA detected the intrusion through its own monitoring and publicly disclosed it in an open letter.",
        "discovery_hi": "RSA ने अपनी निगरानी से घुसपैठ पकड़ी और एक खुले पत्र में सार्वजनिक रूप से बताया।",
        "response_en": "Forensic investigation, notification of customers, token replacement programme and increased monitoring.",
        "response_hi": "जाँच, ग्राहकों को सूचना, टोकन बदलने का कार्यक्रम और बढ़ी हुई निगरानी।",
        "remediation_en": "Patch management for document viewers, email filtering, and monitoring for outbound connections from office applications.",
        "remediation_hi": "दस्तावेज़ व्यूअर के अपडेट, ईमेल फ़िल्टरिंग और ऑफ़िस ऐप्स के बाहरी कनेक्शन पर निगरानी।",
        "precautions_en": "Treat unexpected attachments as untrusted even when the message looks personal; report rather than open.",
        "precautions_hi": "अनजान अटैचमेंट को संदिग्ध मानें, भले ही संदेश निजी लगे; खोलें नहीं, रिपोर्ट करें।",
        "lessons_en": "Authentication suppliers are high-value targets; one attachment can start a large breach; patching document readers matters as much as patching servers; a well-written email beats a poorly configured filter; incident disclosure builds trust.",
        "lessons_hi": "प्रमाणीकरण देने वाली कंपनियाँ बड़ा निशाना होती हैं; एक अटैचमेंट बड़ी घटना शुरू कर सकता है; दस्तावेज़ पढ़ने वाले सॉफ़्टवेयर का अपडेट भी ज़रूरी है; अच्छी भाषा वाला ईमेल कमज़ोर फ़िल्टर को पार कर जाता है; सही जानकारी साझा करने से भरोसा बनता है।",
        "technical_detail_en": "Public reporting described the email subject as an attractive recruitment-themed lure and the payload as a zero-day exploit in a spreadsheet component. RSA's letter confirmed that information related to SecurID was extracted.",
        "sources": [
            ("RSA open letter to customers (2011)", "https://www.rsa.com", "RSA / EMC"),
            ("CISA — guidance on mitigating social engineering", "https://www.cisa.gov", "CISA"),
        ],
        "source_published_on": "2011-04-01",
    },
    {
        "slug": "bangladesh-bank-2016",
        "title_en": "The Bangladesh Bank SWIFT heist (2016)",
        "year": 2016,
        "organization": "Bangladesh Bank",
        "sector": "Banking / central bank",
        "category": "Financial fraud / network intrusion",
        "attack_type": "Compromised operator credentials and SWIFT payment instructions",
        "confidence": "confirmed",
        "summary_en": "Attackers used stolen credentials to send fraudulent international payment instructions, moving tens of millions of dollars out of the central bank's account at the New York Federal Reserve.",
        "summary_hi": "हमलावरों ने चोरी की जानकारी से जाली अंतरराष्ट्रीय भुगतान संदेश भेजे और न्यूयॉर्क फेडरल रिज़र्व में केंद्रीय बैंक के खाते से करोड़ों डॉलर निकाल लिए।",
        "what_happened_en": "Payment instructions were submitted through the SWIFT messaging system in February 2016. Most were blocked or reversed after the money had already been transferred, but a substantial sum reached accounts in South-East Asia.",
        "what_happened_hi": "फ़रवरी 2016 में SWIFT प्रणाली से भुगतान संदेश भेजे गए। अधिकांश पकड़े गए, पर बड़ी राशि दक्षिण-पूर्व एशिया के खातों तक पहुँच गई।",
        "how_it_worked_en": "The attackers operated inside the bank's network for a period, studied the payment process, altered or deleted records, and disabled the printer that would normally have produced the confirmations that staff reviewed.",
        "how_it_worked_hi": "हमलावर कुछ समय तक बैंक के नेटवर्क में रहे, भुगतान प्रक्रिया समझी, रिकॉर्ड बदले या मिटाए, और उस प्रिंटर को बंद कर दिया जिससे पुष्टि की पर्चियाँ निकलती थीं।",
        "weaknesses_en": "Weak network segmentation, inexpensive networking equipment, no firewall, and a payment process where printing was the only visible control.",
        "weaknesses_hi": "कमज़ोर नेटवर्क विभाजन, सस्ते नेटवर्किंग उपकरण, फ़ायरवॉल का अभाव, और ऐसी प्रक्रिया जिसमें प्रिंट की गई पर्ची ही एकमात्र दिखने वाला नियंत्रण थी।",
        "consequences_en": "Around 81 million US dollars was reported lost; several people were investigated; banking regulators worldwide increased scrutiny of SWIFT-connected environments.",
        "consequences_hi": "लगभग 81 मिलियन अमेरिकी डॉलर घाटे की खबर आई; कई लोगों की जाँच हुई; दुनिया भर के नियामकों ने SWIFT से जुड़े वातावरण पर निगरानी बढ़ाई।",
        "discovery_en": "A spelling error in one payment instruction caused a receiving bank to query it, which led to the fraud being noticed.",
        "discovery_en_alt": None,
        "discovery_hi": "एक भुगतान संदेश में वर्तनी की गलती के कारण प्राप्त करने वाले बैंक ने पूछताछ की, और ठगी पकड़ में आई।",
        "response_en": "Recovery efforts with correspondent banks, internal investigation, and new SWIFT-related security guidance for the industry.",
        "response_hi": "संबंधित बैंकों के सहयोग से राशि वापस पाने की कोशिश, आंतरिक जाँच, और उद्योग के लिए नई SWIFT सुरक्षा गाइड।",
        "remediation_en": "Network segmentation for payment systems, two-person release of instructions, out-of-band confirmation of large transfers, and alerting on printer or log tampering.",
        "remediation_hi": "भुगतान प्रणालियों का अलग नेटवर्क, दो व्यक्तियों की मंज़ूरी, बड़े भुगतान की अलग माध्यम से पुष्टि, और लॉग/प्रिंटर से छेड़छाड़ पर चेतावनी।",
        "precautions_en": "Never rely on a single visible control; make internal fraud detection independent of the systems being attacked.",
        "precautions_hi": "सिर्फ़ एक दिखने वाले नियंत्रण पर निर्भर न रहें; जाँच ऐसी हो जो हमले की चपेट वाली प्रणाली से स्वतंत्र हो।",
        "lessons_en": "Verify payments through a separate channel; segment critical networks; monitor for tampering with logs and printers; assume payment instructions can be forged; test recovery plans with correspondent banks.",
        "lessons_hi": "भुगतान की पुष्टि अलग माध्यम से करें; महत्वपूर्ण नेटवर्क अलग रखें; लॉग और प्रिंटर से छेड़छाड़ पर नज़र रखें; भुगतान संदेश जाली हो सकते हैं; रिकवरी योजना का अभ्यास करें।",
        "technical_detail_en": "Reported details include the use of SWIFT terminal credentials, custom malware for manipulating transaction records, and disabling of the confirmation printer. Some reported figures have varied across investigations.",
        "sources": [
            ("SWIFT — customer security programme", "https://www.swift.com", "SWIFT"),
            ("FBI public statements on business email compromise and payment fraud", "https://www.fbi.gov", "FBI"),
            ("Bangladesh Bank public statements", "https://www.bb.org.bd", "Bangladesh Bank"),
        ],
        "source_published_on": "2016-03-01",
        "uncertainty_note_en": "Exact total losses and recovery amounts have been reported differently by different investigations; treat the figures as approximate.",
        "uncertainty_note_hi": "कुल नुकसान और वसूली की राशि अलग-अलग जाँचों में अलग बताई गई है; इन्हें अनुमानित मानें।",
    },
    {
        "slug": "target-2013",
        "title_en": "The Target breach and third-party access (2013)",
        "year": 2013,
        "organization": "Target Corporation",
        "sector": "Retail",
        "category": "Third-party compromise",
        "attack_type": "Vendor credentials used to reach a payment network",
        "confidence": "reported",
        "summary_en": "Credentials belonging to a heating and refrigeration contractor were reportedly used to enter Target's vendor portal and then reach point-of-sale systems.",
        "summary_hi": "बताया जाता है कि हीटिंग-रेफ्रिजरेशन ठेकेदार की चोरी हुई जानकारी से Target के विक्रेता पोर्टल में घुसकर पॉइंट-ऑफ़-सेल प्रणालियों तक पहुँचा गया।",
        "what_happened_en": "During late 2013, attackers accessed payment card data and customer records. Millions of payment cards and customer records were affected, and the company later reported significant costs.",
        "what_happened_hi": "2013 के अंत में हमलावरों ने कार्ड डेटा और ग्राहक रिकॉर्ड तक पहुँच बनाई। करोड़ों कार्ड और रिकॉर्ड प्रभावित हुए और कंपनी को बड़ा खर्च उठाना पड़ा।",
        "how_it_worked_en": "Attackers reportedly obtained a contractor's credentials through a phishing email, entered the vendor portal, and moved laterally into the card-processing environment where malware captured payment data.",
        "how_it_worked_hi": "बताया जाता है कि फ़िशिंग ईमेल से ठेकेदार की जानकारी मिली, विक्रेता पोर्टल में प्रवेश हुआ, और मैलवेयर ने कार्ड डेटा चुराया।",
        "weaknesses_en": "Third-party access with broad reach, insufficient segmentation between the vendor portal and the payment environment, and limited monitoring of vendor accounts.",
        "weaknesses_hi": "तीसरे पक्ष की पहुँच बहुत व्यापक थी, विक्रेता पोर्टल और भुगतान प्रणाली के बीच विभाजन कम था, और विक्रेता खातों की निगरानी सीमित थी।",
        "consequences_en": "Tens of millions of payment cards and customer records were affected; the company reported substantial remediation and legal costs; the CEO and CIO departed.",
        "consequences_hi": "करोड़ों कार्ड और ग्राहक रिकॉर्ड प्रभावित हुए; कंपनी को बड़ा सुधार व कानूनी खर्च उठाना पड़ा; CEO और CIO ने पद छोड़ा।",
        "discovery_en": "Discovery came from fraud-monitoring partners and internal investigation during the busy shopping season.",
        "discovery_hi": "ठगी निगरानी करने वाले साझेदारों और आंतरिक जाँच से घटना का पता चला।",
        "response_en": "Malware removal, accelerated chip-card rollout, new security leadership, and industry-wide attention to third-party risk.",
        "response_hi": "मैलवेयर हटाया गया, चिप कार्ड की शुरुआत तेज़ की गई, नई सुरक्षा टीम बनी, और तीसरे पक्ष के जोखिम पर उद्योग भर में ध्यान बढ़ा।",
        "remediation_en": "Segmentation between business and payment networks, least-privilege vendor access, multi-factor authentication for vendors, and monitoring of third-party accounts.",
        "remediation_hi": "व्यापारिक और भुगतान नेटवर्क का अलगाव, विक्रेता को न्यूनतम अधिकार, विक्रेता के लिए MFA, और तीसरे पक्ष के खातों की निगरानी।",
        "precautions_en": "Your security is only as strong as the least protected account with access to it.",
        "precautions_hi": "आपकी सुरक्षा उतनी ही मज़बूत है जितना उसमें पहुँच रखने वाला सबसे कमज़ोर खाता।",
        "lessons_en": "Vendor access is an attack path; segment payment networks; require MFA for third parties; monitor contractor accounts closely; supply-chain security needs contracts, not just tools.",
        "lessons_hi": "विक्रेता की पहुँच हमले का रास्ता है; भुगतान नेटवर्क अलग रखें; तीसरे पक्ष के लिए MFA ज़रूरी करें; ठेकेदार खातों पर नज़र रखें; आपूर्ति-श्रृंखला सुरक्षा के लिए नियम भी ज़रूरी हैं।",
        "technical_detail_en": "Investigations described point-of-sale malware and the use of a vendor portal as the entry path. Specific internal details have been disputed in litigation.",
        "sources": [
            ("US Senate committee report on the Target breach", "https://www.hsgac.senate.gov", "US Senate"),
            ("FBI cybercrime advisories", "https://www.ic3.gov", "FBI IC3"),
        ],
        "source_published_on": "2014-03-01",
        "uncertainty_note_en": "Some internal details are drawn from litigation and have been contested; the entry path via vendor credentials is widely reported but should be described as reported rather than court-established fact here.",
        "uncertainty_note_hi": "कुछ आंतरिक विवरण मुकदमों से हैं और विवादित रहे हैं; विक्रेता जानकारी से प्रवेश के बारे में यह व्यापक रूप से बताया गया है।",
    },
    {
        "slug": "twitter-2020",
        "title_en": "The Twitter account takeover (2020)",
        "year": 2020,
        "organization": "Twitter",
        "sector": "Social media",
        "category": "Social engineering / vishing",
        "attack_type": "Phone-based spear phishing of employees, then internal tool abuse",
        "confidence": "confirmed",
        "summary_en": "Attackers phoned Twitter employees, obtained access to internal tools, and took over high-profile accounts to run a cryptocurrency scam.",
        "summary_hi": "हमलावरों ने Twitter कर्मचारियों को फ़ोन किया, आंतरिक टूल तक पहुँच बनाई और बड़े खातों से क्रिप्टोकरेंसी ठगी की।",
        "what_happened_en": "In July 2020 a small number of employees were targeted by phone. The attackers used the access they gained to reset passwords, disable multi-factor protection on selected accounts, and post cryptocurrency scam messages from prominent accounts.",
        "what_happened_hi": "जुलाई 2020 में कुछ कर्मचारियों को फ़ोन पर निशाना बनाया गया। मिली पहुँच से हमलावरों ने पासवर्ड बदले, कुछ खातों की MFA हटाई और बड़े खातों से ठगी वाले संदेश भेजे।",
        "how_it_worked_en": "The attackers posed as internal IT support, directing employees to a fake VPN page that captured their credentials. With those credentials they entered internal administration tools and acted on accounts directly.",
        "how_it_worked_hi": "हमलावरों ने खुद को आंतरिक IT सपोर्ट बताया और कर्मचारियों को नकली VPN पेज पर भेजा जहाँ उनकी जानकारी दर्ज हो गई। उससे वे आंतरिक व्यवस्थापन टूल तक पहुँचे।",
        "weaknesses_en": "Employees could be reached by phone and persuaded to act; internal tools permitted powerful account actions; MFA could be weakened for some accounts.",
        "weaknesses_hi": "कर्मचारियों को फ़ोन से बहकाया जा सका; आंतरिक टूल बहुत शक्तिशाली कार्रवाई कर सकते थे; कुछ खातों में MFA कमज़ोर की जा सकती थी।",
        "consequences_en": "About 130 accounts were accessed and scam messages generated cryptocurrency payments from many users before the operation was stopped.",
        "consequences_hi": "लगभग 130 खातों तक पहुँच हुई और कई उपयोगकर्ताओं ने ठगी में पैसे भेजे, तब रोक लगाई गई।",
        "discovery_en": "Twitter detected the suspicious activity while it was in progress and locked affected accounts within hours.",
        "discovery_hi": "Twitter को चल रही गतिविधि का पता चला और कुछ घंटों में प्रभावित खाते लॉक कर दिए।",
        "response_en": "Widespread account lockdowns, removal of access, coordination with law enforcement, and publication of a detailed incident thread.",
        "response_hi": "बड़े पैमाने पर खाते लॉक किए गए, पहुँच हटाई गई, कानून प्रवर्तन से समन्वय हुआ और विस्तृत जानकारी सार्वजनिक की गई।",
        "remediation_en": "Phishing-resistant authentication for staff, restricting internal tools to least privilege with approval flows, and hardening support processes against phone-based requests.",
        "remediation_hi": "कर्मचारियों के लिए फ़िशिंग-रोधी प्रमाणीकरण, आंतरिक टूल में न्यूनतम अधिकार व मंज़ूरी प्रक्रिया, और फ़ोन से आने वाले अनुरोधों के लिए सख्त प्रक्रिया।",
        "precautions_en": "Identify callers by procedure, not by tone: no legitimate IT desk needs your password in a phone call.",
        "precautions_hi": "कॉल करने वाले की पहचान प्रक्रिया से करें, बोलने के तरीक़े से नहीं: कोई असली IT डेस्क फ़ोन पर पासवर्ड नहीं माँगता।",
        "lessons_en": "Voice phishing bypasses email filters; internal admin tools need their own controls; powerful actions need two people; employee awareness must include phone calls; rapid disclosure limits harm.",
        "lessons_hi": "वॉइस फ़िशिंग ईमेल फ़िल्टर से बच निकलती है; आंतरिक टूल के अपने नियंत्रण चाहिए; बड़ी कार्रवाई के लिए दो लोगों की मंज़ूरी; कर्मचारी जागरूकता में फ़ोन कॉल भी शामिल हो; तेज़ सूचना से नुकसान घटता है।",
        "technical_detail_en": "Twitter stated that the attackers targeted a small number of employees by phone and used credentials from a fake VPN page to reach internal account-management tools.",
        "sources": [
            ("Twitter public statement on the incident", "https://blog.twitter.com", "Twitter"),
            ("US Department of Justice press release on charges", "https://www.justice.gov", "US DOJ"),
        ],
        "source_published_on": "2020-07-15",
    },
    {
        "slug": "solarwinds-2020",
        "title_en": "The SolarWinds Orion supply-chain compromise (2020)",
        "year": 2020,
        "organization": "SolarWinds and its customers",
        "sector": "Software supply chain / government",
        "category": "Supply-chain compromise",
        "attack_type": "Trojanised software update",
        "confidence": "confirmed",
        "summary_en": "Malicious code was inserted into a widely used IT management product, so customers installed it through a trusted update mechanism.",
        "summary_hi": "एक लोकप्रिय IT प्रबंधन उत्पाद में दुर्भावनापूर्ण कोड डाला गया, और ग्राहकों ने भरोसेमंद अपडेट के ज़रिए उसे इंस्टॉल कर लिया।",
        "what_happened_en": "Between early 2020 and its discovery in December 2020, a compromised build of the Orion platform was distributed to many organisations. Affected organisations included government agencies and technology companies.",
        "what_happened_hi": "2020 की शुरुआत से दिसंबर 2020 में पता चलने तक Orion का बदला हुआ बिल्ड कई संस्थाओं तक पहुँचा, जिनमें सरकारी एजेंसियाँ और टेक्नोलॉजी कंपनियाँ शामिल थीं।",
        "how_it_worked_en": "Attackers gained access to the software build environment and inserted code into a legitimate update. Because the update was signed and came from the vendor, it bypassed many defences.",
        "how_it_worked_hi": "हमलावरों ने सॉफ़्टवेयर बिल्ड के वातावरण में पहुँच बनाई और असली अपडेट में कोड जोड़ दिया। अपडेट हस्ताक्षरित और विक्रेता से आने के कारण कई सुरक्षा परतें पार कर गया।",
        "weaknesses_en": "Trust in vendor updates, limited monitoring of update packages, and identity systems that allowed quiet lateral movement.",
        "weaknesses_hi": "विक्रेता के अपडेट पर भरोसा, अपडेट पैकेज की सीमित निगरानी, और ऐसी पहचान प्रणाली जिससे चुपचाप आगे बढ़ना आसान था।",
        "consequences_en": "Thousands of customers installed the affected version; a smaller number were further compromised; governments issued emergency directives and attribution statements.",
        "consequences_hi": "हज़ारों ग्राहकों ने प्रभावित संस्करण इंस्टॉल किया; कुछ में आगे भी घुसपैठ हुई; सरकारों ने आपात निर्देश और श्रेय-संबंधी बयान जारी किए।",
        "discovery_en": "A security vendor investigating unusual activity identified the trojanised update and reported it publicly.",
        "discovery_hi": "असामान्य गतिविधि की जाँच कर रही एक सुरक्षा कंपनी ने बदला हुआ अपडेट पहचाना और सार्वजनिक किया।",
        "response_en": "Emergency patching, isolation of affected systems, and widespread review of identity and monitoring controls.",
        "response_hi": "आपात पैचिंग, प्रभावित प्रणालियों को अलग करना, और पहचान व निगरानी नियंत्रणों की व्यापक समीक्षा।",
        "remediation_en": "Verify software integrity independently, monitor update infrastructure, restrict administrative identities, and alert on unusual authentication patterns.",
        "remediation_hi": "सॉफ़्टवेयर की अखंडता की स्वतंत्र जाँच, अपडेट ढाँचे की निगरानी, प्रशासनिक पहचानों पर रोक, और असामान्य लॉगिन पर चेतावनी।",
        "precautions_en": "A trusted update path is also an attack path — monitor what enters through it.",
        "precautions_hi": "भरोसेमंद अपडेट का रास्ता भी हमले का रास्ता है — उससे जो आता है, उस पर नज़र रखें।",
        "lessons_en": "Supply chains multiply trust; update infrastructure must be monitored; administrative identities need strict control; detection must not depend only on signatures; clear attribution takes time and evidence.",
        "lessons_hi": "आपूर्ति-श्रृंखला भरोसे को कई गुना बढ़ा देती है; अपडेट ढाँचे की निगरानी ज़रूरी है; प्रशासनिक पहचान पर कड़ा नियंत्रण हो; पहचान केवल सिग्नेचर पर निर्भर न हो; श्रेय तय करने में समय और प्रमाण चाहिए।",
        "technical_detail_en": "Public reporting named the malicious component SUNBURST. Government statements attributed the campaign to Russian state-linked actors; the platform reports this attribution as a government finding.",
        "sources": [
            ("CISA emergency directive 21-01", "https://www.cisa.gov", "CISA"),
            ("SolarWinds public security advisories", "https://www.solarwinds.com", "SolarWinds"),
            ("US Cyber Command / NSA statements", "https://www.nsa.gov", "NSA"),
        ],
        "source_published_on": "2020-12-13",
    },
    {
        "slug": "colonial-pipeline-2021",
        "title_en": "The Colonial Pipeline ransomware incident (2021)",
        "year": 2021,
        "organization": "Colonial Pipeline",
        "sector": "Critical infrastructure / energy",
        "category": "Ransomware",
        "attack_type": "Compromised VPN account credential",
        "confidence": "confirmed",
        "summary_en": "A single compromised password allowed ransomware to be deployed in the corporate network, prompting a precautionary shutdown of a major fuel pipeline.",
        "summary_hi": "एक चोरी हुए पासवर्ड से कॉर्पोरेट नेटवर्क में रैनसमवेयर फैला, जिसके कारण एक बड़ी ईंधन पाइपलाइन को एहतियातन बंद करना पड़ा।",
        "what_happened_en": "In May 2021 the company shut down pipeline operations after ransomware was found in its business systems. Fuel distribution across the south-eastern United States was disrupted for several days.",
        "what_happened_hi": "मई 2021 में व्यावसायिक प्रणालियों में रैनसमवेयर मिलने के बाद कंपनी ने पाइपलाइन बंद कर दी। दक्षिण-पूर्वी अमेरिका में कई दिन ईंधन वितरण प्रभावित रहा।",
        "how_it_worked_en": "Attackers entered using a password for a remote access account that was no longer actively used but still enabled, and which was not protected by multi-factor authentication.",
        "how_it_worked_hi": "हमलावर ऐसे रिमोट एक्सेस खाते के पासवर्ड से अंदर आए जो इस्तेमाल में नहीं था पर बंद भी नहीं किया गया था, और जिस पर MFA नहीं थी।",
        "weaknesses_en": "An unused account left enabled, a password reused elsewhere, and no multi-factor authentication on remote access.",
        "weaknesses_hi": "इस्तेमाल न होने वाला खाता बंद न करना, पासवर्ड कहीं और भी इस्तेमाल होना, और रिमोट एक्सेस पर MFA का अभाव।",
        "consequences_en": "Days of fuel supply disruption and panic buying; a ransom payment was later reported and partially recovered by authorities.",
        "consequences_hi": "कई दिन ईंधन आपूर्ति बाधित रही और लोगों ने जमाखोरी की; बाद में फ़िरौती भुगतान की जानकारी आई जिसका कुछ हिस्सा अधिकारियों ने वापस पाया।",
        "discovery_en": "The company discovered the intrusion and shut down operations as a precaution to contain it.",
        "discovery_hi": "कंपनी ने घुसपैठ पकड़ी और रोकने के लिए एहतियातन परिचालन बंद किया।",
        "response_en": "Operational shutdown, incident response engagement, and later regulatory attention to pipeline cybersecurity requirements.",
        "response_hi": "परिचालन बंद, घटना-प्रतिक्रिया विशेषज्ञों की नियुक्ति, और बाद में पाइपलाइन सुरक्षा नियमों पर नियामकीय ध्यान।",
        "remediation_en": "Multi-factor authentication on all remote access, decommissioning unused accounts, unique passwords, and monitoring for anomalous logins.",
        "remediation_hi": "हर रिमोट एक्सेस पर MFA, अप्रयुक्त खाते बंद करना, अलग-अलग पासवर्ड, और असामान्य लॉगिन पर निगरानी।",
        "precautions_en": "Old accounts and reused passwords are the quietest way into a network.",
        "precautions_hi": "पुराने खाते और दोबारा इस्तेमाल किए पासवर्ड नेटवर्क में घुसने का सबसे चुपचाप रास्ता हैं।",
        "lessons_en": "Inventory accounts and disable unused ones; require MFA on remote access; never reuse passwords; plan for operational decisions during a cyber incident; keep offline backups of critical data.",
        "lessons_hi": "खातों की सूची रखें और अप्रयुक्त बंद करें; रिमोट एक्सेस पर MFA ज़रूरी करें; पासवर्ड दोहराएँ नहीं; साइबर घटना के समय परिचालन निर्णय की योजना बनाएँ; ज़रूरी डेटा का ऑफ़लाइन बैकअप रखें।",
        "technical_detail_en": "The initial access vector was reported as a compromised password for a legacy remote-access profile. The platform notes this as reported by the company and by government statements.",
        "sources": [
            ("CISA and FBI joint advisory on the incident", "https://www.cisa.gov", "CISA"),
            ("US Department of Justice statement on ransom recovery", "https://www.justice.gov", "US DOJ"),
        ],
        "source_published_on": "2021-05-07",
    },
    {
        "slug": "uber-2022",
        "title_en": "The Uber social engineering incident (2022)",
        "year": 2022,
        "organization": "Uber",
        "sector": "Technology / ride hailing",
        "category": "Social engineering / MFA fatigue",
        "attack_type": "MFA push fatigue and help-desk impersonation",
        "confidence": "reported",
        "summary_en": "An attacker reportedly posed as IT support, repeatedly triggered multi-factor prompts, and then obtained access to internal systems.",
        "summary_hi": "बताया जाता है कि हमलावर ने खुद को IT सपोर्ट बताया, बार-बार MFA सूचनाएँ भेजीं और फिर आंतरिक प्रणालियों तक पहुँच बना ली।",
        "what_happened_en": "In September 2022 Uber reported a security incident in which an attacker gained access to internal tools and posted evidence publicly. The company said customer data and production systems were not apparently affected.",
        "what_happened_hi": "सितंबर 2022 में Uber ने बताया कि एक हमलावर आंतरिक टूल तक पहुँचा और सबूत सार्वजनिक किए। कंपनी के अनुसार ग्राहक डेटा और उत्पादन प्रणालियाँ प्रभावित नहीं दिखीं।",
        "how_it_worked_en": "The attacker reportedly obtained a contractor's credentials, triggered repeated second-factor prompts, then contacted the contractor posing as support and asked them to approve the prompt. Later, hardcoded administrative credentials on an internal share widened the access.",
        "how_it_worked_hi": "बताया जाता है कि हमलावर ने ठेकेदार की जानकारी हासिल की, बार-बार दूसरा कारक ट्रिगर किया, फिर सपोर्ट बनकर उनसे उसे मंज़ूर करने को कहा। बाद में आंतरिक शेयर पर रखी प्रशासनिक जानकारी से पहुँच बढ़ गई।",
        "weaknesses_en": "Allow-anywhere MFA prompts, credentials stored in plain text on an internal share, and access paths that were broader than necessary.",
        "weaknesses_hi": "कहीं से भी मंज़ूर हो सकने वाली MFA सूचनाएँ, आंतरिक शेयर पर सादे टेक्स्ट में रखी जानकारी, और ज़रूरत से ज़्यादा व्यापक पहुँच।",
        "consequences_en": "Internal tools and administrative consoles were reached; the incident drew wide attention and prompted hardening of authentication and secrets management.",
        "consequences_hi": "आंतरिक टूल और प्रशासनिक कंसोल तक पहुँच हो गई; घटना ने व्यापक ध्यान खींचा और प्रमाणीकरण व सीक्रेट प्रबंधन को मज़बूत करने पर ज़ोर बढ़ा।",
        "discovery_en": "The intrusion was noticed quickly and the company took systems offline while responding, then reported publicly.",
        "discovery_hi": "घुसपैठ जल्दी पकड़ी गई, कंपनी ने प्रणालियाँ बंद कर जवाब दिया और फिर सार्वजनिक जानकारी दी।",
        "response_en": "Systems taken offline, credentials rotated, and public communication about the response.",
        "response_hi": "प्रणालियाँ बंद करना, जानकारी बदलना, और सार्वजनिक जानकारी देना।",
        "remediation_en": "Number-matching MFA, removal of hardcoded secrets, least-privilege administrative access, and staff training on phone-based support impersonation.",
        "remediation_hi": "नंबर मिलान वाली MFA, कोड में लिखी गुप्त जानकारी हटाना, प्रशासनिक पहुँच न्यूनतम करना, और फ़ोन पर सपोर्ट बनकर ठगी करने वालों पर कर्मचारी प्रशिक्षण।",
        "precautions_en": "If a second-factor prompt arrives when you did not sign in, never approve it — and report it.",
        "precautions_hi": "जब आपने लॉगिन न किया हो और MFA सूचना आए, उसे कभी मंज़ूर न करें — रिपोर्ट करें।",
        "lessons_en": "Prompt fatigue is an attack; never approve an unexpected push; never store secrets in plain text; support staff need scripted verification; fast detection limits damage.",
        "lessons_hi": "बार-बार MFA सूचना भेजना हमला है; अनजान सूचना मंज़ूर न करें; गुप्त जानकारी सादे टेक्स्ट में न रखें; सपोर्ट कर्मचारी के लिए पुष्टि की तय प्रक्रिया हो; तेज़ पहचान नुकसान घटाती है।",
        "technical_detail_en": "This description is based on the company's incident statement and the attacker's own public claims; some details come from third-party reporting and remain reported rather than independently verified.",
        "sources": [
            ("Uber security update statement", "https://www.uber.com", "Uber"),
            ("CISA guidance on MFA fatigue and push bombing", "https://www.cisa.gov", "CISA"),
        ],
        "source_published_on": "2022-09-16",
        "uncertainty_note_en": "Some technical detail comes from the attacker's public claims and should be treated as reported, not independently confirmed.",
        "uncertainty_note_hi": "कुछ तकनीकी विवरण हमलावर के सार्वजनिक दावों से हैं — इन्हें बताया गया मानें, स्वतंत्र रूप से पुष्ट नहीं।",
    },
    {
        "slug": "mgm-resorts-2023",
        "title_en": "The MGM Resorts incident (2023)",
        "year": 2023,
        "organization": "MGM Resorts International",
        "sector": "Hospitality / gaming",
        "category": "Social engineering / ransomware",
        "attack_type": "Help-desk impersonation leading to ransomware",
        "confidence": "reported",
        "summary_en": "Attackers reportedly phoned a help desk and used impersonation to obtain access, after which operations at multiple properties were disrupted for days.",
        "summary_hi": "बताया जाता है कि हमलावरों ने हेल्प डेस्क को फ़ोन कर पहचान बदलकर पहुँच बनाई, जिसके बाद कई होटलों का परिचालन कई दिन बाधित रहा।",
        "what_happened_en": "In September 2023 several casino and hotel systems were disrupted: reservations, key cards, slot machines and websites were affected. The company stated that it worked with law enforcement and external specialists.",
        "what_happened_hi": "सितंबर 2023 में कई कैसीनो और होटल प्रणालियाँ ठप हुईं: बुकिंग, रूम कार्ड, स्लॉट मशीन और वेबसाइट प्रभावित हुईं। कंपनी ने कानून प्रवर्तन और विशेषज्ञों के साथ काम करने की बात कही।",
        "how_it_worked_en": "Reporting described a phone call to a help desk by someone impersonating an employee, followed by theft of credentials and lateral movement, then ransomware deployment.",
        "how_it_worked_hi": "रिपोर्टों के अनुसार किसी ने कर्मचारी बनकर हेल्प डेस्क को कॉल किया, जानकारी हासिल की, आगे बढ़ा और फिर रैनसमवेयर फैलाया।",
        "weaknesses_en": "Identity verification over the phone, privileged access reachable from a single successful impersonation, and limited separation between corporate and operational networks.",
        "weaknesses_hi": "फ़ोन पर पहचान की जाँच, एक सफल पहचान-ठगी से मिलने वाली विशेषाधिकार पहुँच, और कॉर्पोरेट व परिचालन नेटवर्क में कम विभाजन।",
        "consequences_en": "Multi-day disruption across properties, reported financial impact, and regulatory attention to the sector.",
        "consequences_hi": "कई दिन तक होटलों में बाधा, बताया गया वित्तीय नुकसान, और क्षेत्र पर नियामकीय ध्यान।",
        "discovery_en": "The disruption became obvious almost immediately as systems failed across properties.",
        "discovery_hi": "प्रणालियाँ ठप होते ही बाधा तुरंत सामने आ गई।",
        "response_en": "Systems taken offline, manual processes adopted at properties, law enforcement involvement and public statements.",
        "response_hi": "प्रणालियाँ बंद, होटलों में मैनुअल प्रक्रिया, कानून प्रवर्तन की भागीदारी और सार्वजनिक बयान।",
        "remediation_en": "Strong identity proofing for help desks, multi-factor authentication everywhere, network segmentation between corporate and operational technology, and rehearsed manual fallbacks.",
        "remediation_hi": "हेल्प डेस्क के लिए सख्त पहचान पुष्टि, हर जगह MFA, कॉर्पोरेट और परिचालन तकनीक के बीच विभाजन, और मैनुअल विकल्प का अभ्यास।",
        "precautions_en": "Help desks are a front door: identity must be proven, not asserted.",
        "precautions_hi": "हेल्प डेस्क सामने का दरवाज़ा है: पहचान साबित होनी चाहिए, कहने भर से नहीं।",
        "lessons_en": "Phone impersonation defeats strong technical controls; verify identity with procedures; segment operational networks; rehearse downtime; keep leadership communication ready.",
        "lessons_hi": "फ़ोन पर पहचान बदलना मज़बूत तकनीकी नियंत्रणों को भी पार कर जाता है; पहचान तय प्रक्रिया से जाँचें; परिचालन नेटवर्क अलग रखें; बंद पड़ने की स्थिति का अभ्यास करें; संचार योजना तैयार रखें।",
        "technical_detail_en": "Details are drawn from company statements, law enforcement announcements and press reporting; some specifics remain reported rather than confirmed.",
        "sources": [
            ("MGM Resorts public statement", "https://www.mgmresorts.com", "MGM Resorts"),
            ("CISA guidance on help-desk social engineering", "https://www.cisa.gov", "CISA"),
        ],
        "source_published_on": "2023-09-12",
        "uncertainty_note_en": "The precise sequence of attacker actions is described in press reporting and has not been fully confirmed by the company.",
        "uncertainty_note_hi": "हमलावरों की कार्रवाई का सटीक क्रम प्रेस रिपोर्टों से है और कंपनी ने इसे पूरी तरह पुष्ट नहीं किया।",
    },
    {
        "slug": "okta-support-2023",
        "title_en": "The Okta support-system incident (2023)",
        "year": 2023,
        "organization": "Okta",
        "sector": "Identity and access management",
        "category": "Third-party / credential compromise",
        "attack_type": "Stolen credentials used against a support system",
        "confidence": "confirmed",
        "summary_en": "Stolen credentials were used against an identity provider's customer support system, exposing support case data and, for a small number of customers, session tokens.",
        "summary_hi": "चोरी हुई जानकारी का उपयोग एक पहचान सेवा प्रदाता के ग्राहक सहायता सिस्टम पर किया गया, जिससे सहायता केस डेटा और कुछ ग्राहकों के सेशन टोकन उजागर हुए।",
        "what_happened_en": "In October 2023 Okta disclosed that an attacker had used stolen credentials to access files uploaded by its support team for customer troubleshooting, such as browser records used to diagnose issues.",
        "what_happened_hi": "अक्टूबर 2023 में Okta ने बताया कि हमलावर ने चोरी की जानकारी से सहायता टीम द्वारा अपलोड की गई फ़ाइलों तक पहुँच बनाई।",
        "how_it_worked_en": "Credentials for a support case-management system were obtained and used; files in the support system occasionally contained sensitive artefacts such as session tokens.",
        "how_it_worked_hi": "सहायता केस प्रबंधन प्रणाली की जानकारी चोरी हुई और इस्तेमाल की गई; इन फ़ाइलों में कभी-कभी सेशन टोकन जैसी संवेदनशील सामग्री होती थी।",
        "weaknesses_en": "Sensitive tokens being present in support artefacts, and support accounts protected only by single-factor credentials.",
        "weaknesses_hi": "सहायता सामग्री में संवेदनशील टोकन का होना, और सहायता खातों पर केवल एक कारक की सुरक्षा।",
        "consequences_en": "A limited number of customers were affected; the incident prompted a broad industry review of support-process handling of sensitive data.",
        "consequences_hi": "सीमित ग्राहक प्रभावित हुए; घटना के बाद उद्योग में सहायता प्रक्रिया और संवेदनशील डेटा की समीक्षा हुई।",
        "discovery_en": "A customer's own investigation surfaced activity that led to the vendor's disclosure.",
        "discovery_hi": "एक ग्राहक की अपनी जाँच से गतिविधि सामने आई और फिर विक्रेता ने जानकारी दी।",
        "response_en": "Involved accounts disabled, credential rotation, and additional controls in the support environment.",
        "response_hi": "संबंधित खाते बंद, जानकारी बदली गई, और सहायता वातावरण में अतिरिक्त नियंत्रण जोड़े गए।",
        "remediation_en": "Require phishing-resistant authentication for support staff, redact tokens from support artefacts, and monitor support-system access.",
        "remediation_hi": "सहायता कर्मचारियों के लिए फ़िशिंग-रोधी प्रमाणीकरण, सहायता सामग्री से टोकन हटाना, और सहायता सिस्टम की पहुँच पर निगरानी।",
        "precautions_en": "Troubleshooting artefacts often contain secrets — handle them like credentials.",
        "precautions_hi": "समस्या-समाधान की फ़ाइलों में अक्सर गुप्त जानकारी होती है — उन्हें पासवर्ड की तरह संभालें।",
        "lessons_en": "Identity providers are high-value targets; support systems need the same rigour as production; never store tokens in case files; require strong authentication for support staff; rapid, precise disclosure helps customers respond.",
        "lessons_hi": "पहचान सेवा प्रदाता बड़ा निशाना होते हैं; सहायता सिस्टम को भी उतनी ही सख्ती चाहिए; केस फ़ाइलों में टोकन न रखें; सहायता कर्मचारियों के लिए मज़बूत प्रमाणीकरण; तेज़ और सटीक सूचना से ग्राहक बचाव कर पाते हैं।",
        "technical_detail_en": "Okta's own advisories described access to support case files; the number of customers whose data was viewed and the subset with token exposure were both described as limited.",
        "sources": [
            ("Okta security advisory on the support system incident", "https://sec.okta.com", "Okta"),
            ("CISA advisory referencing the incident", "https://www.cisa.gov", "CISA"),
        ],
        "source_published_on": "2023-10-20",
    },
    {
        "slug": "change-healthcare-2024",
        "title_en": "The Change Healthcare cyberattack (2024)",
        "year": 2024,
        "organization": "Change Healthcare (UnitedHealth Group)",
        "sector": "Healthcare payments",
        "category": "Ransomware / access control failure",
        "attack_type": "Compromised remote-access account without multi-factor authentication",
        "confidence": "reported",
        "summary_en": "A compromised remote-access credential without multi-factor authentication reportedly allowed ransomware to disrupt healthcare payment processing across the United States.",
        "summary_hi": "बताया जाता है कि बिना MFA वाले रिमोट एक्सेस खाते की जानकारी चोरी होने से रैनसमवेयर फैला और अमेरिका भर में स्वास्थ्य भुगतान प्रक्रिया बाधित हुई।",
        "what_happened_en": "In February 2024 the company took systems offline, disrupting claims and pharmacy payments for weeks and affecting a very large number of people's data.",
        "what_happened_hi": "फ़रवरी 2024 में कंपनी ने प्रणालियाँ बंद कीं, जिससे हफ़्तों तक दावे और फ़ार्मेसी भुगतान बाधित रहे और बहुत बड़ी संख्या में लोगों का डेटा प्रभावित हुआ।",
        "how_it_worked_en": "Reporting described entry through a remote access service using a stolen credential for an account that was not protected with multi-factor authentication.",
        "how_it_worked_hi": "रिपोर्टों के अनुसार ऐसे खाते की चोरी हुई जानकारी से रिमोट एक्सेस सेवा में प्रवेश हुआ जिस पर MFA नहीं थी।",
        "weaknesses_en": "Remote access without multi-factor authentication and insufficient network separation.",
        "weaknesses_hi": "MFA रहित रिमोट एक्सेस और नेटवर्क में अपर्याप्त विभाजन।",
        "consequences_en": "Weeks of disruption to healthcare providers and pharmacies, very large scale data exposure, and significant reported financial impact.",
        "consequences_hi": "हफ़्तों तक स्वास्थ्य सेवा और फ़ार्मेसी में बाधा, बहुत बड़े पैमाने पर डेटा उजागर, और बड़ा वित्तीय नुकसान।",
        "discovery_en": "The attack was detected through monitoring of the affected systems, after which the company disconnected them.",
        "discovery_hi": "प्रभावित प्रणालियों की निगरानी से हमले का पता चला और कंपनी ने उन्हें डिस्कनेक्ट कर दिया।",
        "response_en": "Systems taken offline, temporary payment workarounds for providers, and restoration over an extended period.",
        "response_hi": "प्रणालियाँ बंद, सेवा देने वालों के लिए अस्थायी भुगतान विकल्प, और लंबे समय में बहाली।",
        "remediation_en": "Multi-factor authentication on every remote access path, network segmentation, privileged access review, and offline backups.",
        "remediation_hi": "हर रिमोट एक्सेस पर MFA, नेटवर्क विभाजन, विशेषाधिकार पहुँच की समीक्षा, और ऑफ़लाइन बैकअप।",
        "precautions_en": "Any remote entry point without a second factor is an open door — close it today, not later.",
        "precautions_hi": "दूसरे कारक के बिना कोई भी रिमोट प्रवेश द्वारा खुला दरवाज़ा है — इसे आज ही बंद करें।",
        "lessons_en": "MFA on remote access is not optional; single points of failure in critical sectors create national impact; segmentation limits spread; contingency plans must cover payment flows; notifications must reach affected people honestly.",
        "lessons_hi": "रिमोट एक्सेस पर MFA वैकल्पिक नहीं; महत्वपूर्ण क्षेत्र में एक बिंदु का ठप होना व्यापक असर डालता है; विभाजन फैलाव रोकता है; आपात योजना में भुगतान प्रक्रिया भी शामिल हो; प्रभावित लोगों को सच बताएँ।",
        "technical_detail_en": "Entry via a compromised Citrix remote-access credential without MFA has been widely reported; treat the specific technical path as reported rather than company-confirmed.",
        "sources": [
            ("Change Healthcare consumer notice", "https://www.changehealthcare.com", "Change Healthcare"),
            ("US Department of Health and Human Services breach information", "https://www.hhs.gov", "HHS"),
        ],
        "source_published_on": "2024-02-21",
        "uncertainty_note_en": "The precise initial access path is drawn from press reporting and security-vendor analysis rather than a complete public technical report.",
        "uncertainty_note_hi": "प्रवेश का सटीक तरीक़ा प्रेस रिपोर्ट और सुरक्षा कंपनियों के विश्लेषण से है, पूरी सार्वजनिक तकनीकी रिपोर्ट से नहीं।",
    },
]

# Export expanded comprehensive catalogues
from app.services.catalog_videos import CATALOG_VIDEOS as VIDEO_LESSONS  # 50 video lessons
from app.services.catalog_comics import COMICS  # 100 comic stories
from app.services.catalog_incidents import CATALOG_INCIDENTS as INCIDENTS  # 30 researched cases
