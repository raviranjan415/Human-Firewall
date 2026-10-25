"""Seed content catalogues.

HONESTY NOTE — what is real in this file:
  * Labs 1–10 are fully authored: scenario, artefact, options, validation
    rules, hints, step-by-step explanation and remediation, in English and
    Hindi. They are published.
  * Labs 11–100 exist as planned catalogue entries (title, level, ordered
    prerequisites) in ``draft`` state. They are NOT authored yet and are not
    visible to learners — see README "Content status".
  * Videos and comics are clearly flagged prototype assets: scripts,
    narration and transcripts are original and complete enough to build the
    finished media from, but no rendered video or drawn artwork ships yet.
  * Historical incidents carry a confidence label. Facts are limited to what
    is well documented publicly; sources point to the publishing
    organisation, and nothing is invented.
"""

# ---------------------------------------------------------------------------
# Achievements (specification section 10)
# ---------------------------------------------------------------------------

ACHIEVEMENTS = [
    ("first_steps", "First Steps", "पहला कदम", "Complete your first learning activity.",
     "अपना पहला पाठ पूरा करें।", "rocket", "labs_completed", 1, None, 10),
    ("phishing_hunter", "Phishing Hunter", "फ़िशिंग शिकारी", "Pass 5 labs.",
     "5 लैब पूरी करें।", "hook", "labs_completed", 5, None, 25),
    ("scam_spotter", "Scam Spotter", "ठगी पहचानकर्ता", "Pass 10 labs.",
     "10 लैब पूरी करें।", "eye", "labs_completed", 10, None, 50),
    ("digital_detective", "Digital Detective", "डिजिटल जासूस", "Pass 25 labs.",
     "25 लैब पूरी करें।", "magnifier", "labs_completed", 25, None, 100),
    ("incident_investigator", "Incident Investigator", "घटना अन्वेषक", "Pass 60 labs.",
     "60 लैब पूरी करें।", "shield", "labs_completed", 60, None, 200),
    ("privacy_protector", "Privacy Protector", "निजता रक्षक", "Complete 10 comics.",
     "10 कॉमिक पूरी करें।", "lock", "comics_completed", 10, None, 60),
    ("lesson_scholar", "Lesson Scholar", "पाठ पंडित", "Finish 20 video lessons.",
     "20 वीडियो पाठ पूरे करें।", "book", "videos_completed", 20, None, 80),
    ("game_champion", "Game Champion", "गेम चैंपियन", "Complete 5 games.",
     "5 गेम पूरे करें।", "trophy", "games_completed", 5, None, 60),
    ("seven_day_streak", "Seven-Day Streak", "सात दिन की लय", "Study seven days in a row.",
     "लगातार सात दिन सीखें।", "flame", "streak", 7, None, 70),
    ("thirty_day_streak", "Thirty-Day Streak", "तीस दिन की लय", "Study thirty days in a row.",
     "लगातार तीस दिन सीखें।", "flame", "streak", 30, None, 250),
    ("perfect_score", "Perfect Score", "शत-प्रतिशत अंक", "Score 100% in any lab.",
     "किसी लैब में 100% अंक लें।", "star", "perfect_score", 1, None, 30),
    ("hint_free_hero", "Hint-Free Hero", "बिना संकेत विजेता", "Pass 10 labs without hints.",
     "बिना संकेत 10 लैब पूरी करें।", "medal", "no_hint_labs", 10, None, 120),
    ("lab_marathon", "Lab Marathon", "लैब मैराथन", "Pass 40 labs.",
     "40 लैब पूरी करें।", "runner", "labs_completed", 40, None, 150),
    ("basic_graduate", "Basic Graduate", "बुनियादी स्नातक", "Earn the Basic certificate.",
     "बुनियादी प्रमाणपत्र लें।", "certificate", "certificate_tier", 1, "basic", 100),
    ("intermediate_defender", "Intermediate Defender", "मध्यम रक्षक", "Earn the Intermediate certificate.",
     "मध्यम प्रमाणपत्र लें।", "certificate", "certificate_tier", 1, "intermediate", 200),
    ("advanced_investigator", "Advanced Investigator", "उच्च अन्वेषक", "Earn the Advanced certificate.",
     "उच्च प्रमाणपत्र लें।", "certificate", "certificate_tier", 1, "advanced", 300),
    ("cyberquest_master", "CyberQuest Master", "साइबरक्वेस्ट मास्टर", "Earn the Master certificate.",
     "मास्टर प्रमाणपत्र लें।", "crown", "certificate_tier", 1, "master", 500),
]


# ---------------------------------------------------------------------------
# Labs 1–10 — fully authored
# ---------------------------------------------------------------------------

_INITIAL_10_LABS = [
    {
        "number": 1,
        "slug": "identify-suspicious-email",
        "title_en": "Identify a suspicious email",
        "title_hi": "संदिग्ध ईमेल पहचानें",
        "level": "basic",
        "difficulty": "beginner",
        "estimated_minutes": 8,
        "objectives_en": "Spot the warning signs inside a message before you act on it.",
        "objectives_hi": "किसी संदेश पर कार्रवाई करने से पहले उसके चेतावनी संकेत पहचानें।",
        "scenario_en": (
            "You are an accounts assistant at Bluewave Traders. This morning an email "
            "arrives about your salary revision. Read it carefully before you click anything."
        ),
        "scenario_hi": (
            "आप ब्लूवेव ट्रेडर्स में अकाउंट सहायक हैं। आज सुबह वेतन संशोधन के बारे में एक ईमेल आया है। "
            "कुछ भी क्लिक करने से पहले ध्यान से पढ़ें।"
        ),
        "task_en": "Select every warning sign you can find in this email.",
        "task_hi": "इस ईमेल में दिखने वाले हर चेतावनी संकेत को चुनें।",
        "task_type": "multi_select",
        "payload": {
            "kind": "email",
            "from": "hr.payroll@bluewave-traders.co.in",
            "reply_to": "bluewave.hr.desk@gmail.com",
            "subject": "URGENT: Salary revision — confirm within 2 hours",
            "body": (
                "Dear Employee,\n\n"
                "Your revised salary will be cancelled unless you confirm your bank details now. "
                "Open the attached form (salary_update.xlsm) and enter your net-banking username, "
                "password and OTP to activate the revision.\n\n"
                "This link expires in 2 hours: http://bluevvave-traders.verify-login.com/form\n\n"
                "Regards,\nHR Team"
            ),
        },
        "options": [
            {"id": "sender_domain", "en": "The sender domain is not the company's real domain",
             "hi": "प्रेषक का डोमेन कंपनी का असली डोमेन नहीं है"},
            {"id": "reply_to_mismatch", "en": "Reply-to address is a free Gmail account",
             "hi": "रिप्लाई-टू पता एक मुफ़्त जीमेल खाता है"},
            {"id": "urgency", "en": "Artificial urgency with a deadline",
             "hi": "कृत्रिम जल्दबाज़ी और समय सीमा"},
            {"id": "credential_request", "en": "Requests username, password and OTP",
             "hi": "उपयोगकर्ता नाम, पासवर्ड और OTP माँगता है"},
            {"id": "macro_attachment", "en": "Unexpected macro-enabled attachment (.xlsm)",
             "hi": "अचानक मैक्रो वाली अटैचमेंट (.xlsm)"},
            {"id": "typosquat_link", "en": "Link look-alike domain (bluevvave) with an odd subdomain",
             "hi": "मिलता-जुलता नकली डोमेन (bluevvave) और अजीब सबडोमेन"},
            {"id": "generic_greeting", "en": "Generic greeting instead of your name",
             "hi": "आपके नाम की जगह सामान्य संबोधन"},
        ],
        "correct": ["sender_domain", "reply_to_mismatch", "urgency", "credential_request",
                    "macro_attachment", "typosquat_link"],
        "hints": [
            {"en": "Compare the domain after the @ symbol with your real company domain.",
             "hi": "@ के बाद वाला डोमेन अपनी असली कंपनी के डोमेन से मिलाएँ।"},
            {"en": "A legitimate payroll team never needs your password or OTP.",
             "hi": "असली पेरोल टीम को आपका पासवर्ड या OTP कभी नहीं चाहिए।"},
            {"en": "Look for double letters or extra words inside the link.",
             "hi": "लिंक में दोहरे अक्षर या अतिरिक्त शब्द देखें।"},
        ],
        "step_by_step_en": (
            "1. Check the sender domain character by character.\n"
            "2. Expand the reply-to address — a mismatch is a red flag.\n"
            "3. Notice the countdown pressure; real HR processes allow time.\n"
            "4. No legitimate employer asks for your password or OTP.\n"
            "5. Macro-enabled spreadsheets are a common malware carrier.\n"
            "6. Read links right-to-left before the first slash."
        ),
        "step_by_step_hi": (
            "1. प्रेषक का डोमेन अक्षर-दर-अक्षर जाँचें।\n"
            "2. रिप्लाई-टू पता देखें — मेल न खाना खतरे का संकेत है।\n"
            "3. समय का दबाव बनाना ठगी की पहचान है; असली HR समय देता है।\n"
            "4. कोई असली नियोक्ता पासवर्ड या OTP नहीं माँगता।\n"
            "5. मैक्रो वाली स्प्रेडशीट अक्सर मैलवेयर लाती है।\n"
            "6. पहले स्लैश से पहले का पता दाएँ से बाएँ पढ़ें।"
        ),
        "remediation_en": "Revise lesson 6 (Anatomy of a Phishing Email) and replay Spot the Phish.",
        "remediation_hi": "पाठ 6 (फ़िशिंग ईमेल की बनावट) दोहराएँ और 'Spot the Phish' फिर खेलें।",
    },
    {
        "number": 2,
        "slug": "detect-fake-sender-address",
        "title_en": "Detect a fake sender address",
        "title_hi": "नकली प्रेषक पता पहचानें",
        "level": "basic",
        "difficulty": "beginner",
        "estimated_minutes": 6,
        "objectives_en": "Compare the display name with the real address behind it.",
        "objectives_hi": "दिखने वाले नाम की तुलना उसके पीछे के असली पते से करें।",
        "scenario_en": "Four messages claim to come from your bank. Only one uses a genuine bank address.",
        "scenario_hi": "चार संदेश आपके बैंक से होने का दावा करते हैं। सिर्फ़ एक असली बैंक पता इस्तेमाल करता है।",
        "task_en": "Which sender address genuinely belongs to the bank?",
        "task_hi": "कौन-सा प्रेषक पता वाकई बैंक का है?",
        "task_type": "single_choice",
        "payload": {
            "kind": "sender_list",
            "items": [
                "HDFC Bank <alerts@hdfcbank.com>",
                "HDFC Bank <alerts@hdfcbank-secure.in>",
                "HDFC Bank <alerts@hdfcbank.co>",
                "HDFC Bank <hdfcbank.alerts@gmail.com>",
            ],
        },
        "options": [
            {"id": "a", "en": "HDFC Bank <alerts@hdfcbank.com>", "hi": "HDFC Bank <alerts@hdfcbank.com>"},
            {"id": "b", "en": "HDFC Bank <alerts@hdfcbank-secure.in>", "hi": "HDFC Bank <alerts@hdfcbank-secure.in>"},
            {"id": "c", "en": "HDFC Bank <alerts@hdfcbank.co>", "hi": "HDFC Bank <alerts@hdfcbank.co>"},
            {"id": "d", "en": "HDFC Bank <hdfcbank.alerts@gmail.com>", "hi": "HDFC Bank <hdfcbank.alerts@gmail.com>"},
        ],
        "correct": ["a"],
        "hints": [
            {"en": "The display name can say anything — only the part after @ matters.",
             "hi": "दिखने वाला नाम कुछ भी हो सकता है — सिर्फ़ @ के बाद वाला हिस्सा मायने रखता है।"},
        ],
        "step_by_step_en": (
            "Read the domain after @ in each row. '-secure' and '.co' variants are "
            "look-alikes registered by attackers; a free mailbox is never a bank address."
        ),
        "step_by_step_hi": (
            "हर पंक्ति में @ के बाद का डोमेन पढ़ें। '-secure' और '.co' जैसे रूप ठगों द्वारा बनाए जाते हैं; "
            "मुफ़्त मेलबॉक्स कभी बैंक का पता नहीं होता।"
        ),
        "remediation_en": "Practise reading domains right after the @ symbol.",
        "remediation_hi": "@ चिह्न के ठीक बाद वाला डोमेन पढ़ने का अभ्यास करें।",
    },
    {
        "number": 3,
        "slug": "find-suspicious-url",
        "title_en": "Find a suspicious URL",
        "title_hi": "संदिग्ध लिंक खोजें",
        "level": "basic",
        "difficulty": "beginner",
        "estimated_minutes": 7,
        "objectives_en": "Read a URL safely without opening it.",
        "objectives_hi": "लिंक खोले बिना उसे सुरक्षित तरीके से पढ़ें।",
        "scenario_en": "A courier notification asks you to confirm your address using one of these links.",
        "scenario_hi": "एक कूरियर सूचना आपसे इनमें से किसी लिंक से पता पुष्टि करने को कहती है।",
        "task_en": "Which link is the safest to trust for a real courier company?",
        "task_hi": "असली कूरियर कंपनी के लिए कौन-सा लिंक भरोसेमंद है?",
        "task_type": "single_choice",
        "payload": {
            "kind": "links",
            "items": [
                "https://bluedart.com/track/12345",
                "https://bluedart.track-my-parcel.info/verify",
                "http://bluedart.com.secure-login.net/confirm?id=12345",
                "https://bit.ly/3xQz9ab",
            ],
        },
        "options": [
            {"id": "a", "en": "https://bluedart.com/track/12345", "hi": "https://bluedart.com/track/12345"},
            {"id": "b", "en": "https://bluedart.track-my-parcel.info/verify",
             "hi": "https://bluedart.track-my-parcel.info/verify"},
            {"id": "c", "en": "http://bluedart.com.secure-login.net/confirm?id=12345",
             "hi": "http://bluedart.com.secure-login.net/confirm?id=12345"},
            {"id": "d", "en": "https://bit.ly/3xQz9ab", "hi": "https://bit.ly/3xQz9ab"},
        ],
        "correct": ["a"],
        "hints": [
            {"en": "The real domain sits immediately before the first single slash.",
             "hi": "असली डोमेन पहले अकेले स्लैश से ठीक पहले होता है।"},
            {"en": "Shortened links hide their destination — never trust them blindly.",
             "hi": "छोटे लिंक अपना गंतव्य छिपाते हैं — उन पर आँख मूँदकर भरोसा न करें।"},
        ],
        "step_by_step_en": (
            "In option b the registered domain is 'track-my-parcel.info'. In option c it is "
            "'secure-login.net'. Option d hides where it goes. Only option a shows the courier's "
            "own domain immediately before the path."
        ),
        "step_by_step_hi": (
            "विकल्प b में असली डोमेन 'track-my-parcel.info' है। विकल्प c में 'secure-login.net' है। "
            "विकल्प d छिपा हुआ है। सिर्फ़ विकल्प a में कूरियर का असली डोमेन दिखता है।"
        ),
        "remediation_en": "Practise the rule: the domain is what sits right before the first '/'.",
        "remediation_hi": "नियम याद रखें: पहले '/' से ठीक पहले जो लिखा है, वही असली डोमेन है।",
    },
    {
        "number": 4,
        "slug": "recognize-urgent-language",
        "title_en": "Recognize urgent language",
        "title_hi": "जल्दबाज़ी वाली भाषा पहचानें",
        "level": "basic",
        "difficulty": "beginner",
        "estimated_minutes": 6,
        "objectives_en": "Identify the pressure phrases attackers rely on.",
        "objectives_hi": "ठगों द्वारा इस्तेमाल किए जाने वाले दबाव वाले वाक्य पहचानें।",
        "scenario_en": "A message about your electricity bill arrives on a Friday evening.",
        "scenario_hi": "शुक्रवार शाम बिजली बिल के बारे में एक संदेश आता है।",
        "task_en": "Select every phrase designed to create panic.",
        "task_hi": "घबराहट बनाने वाले हर वाक्य को चुनें।",
        "task_type": "multi_select",
        "payload": {
            "kind": "sms",
            "from": "VM-BSESL",
            "body": (
                "Dear consumer, your electricity will be DISCONNECTED TONIGHT at 9:30 PM because your "
                "last bill payment failed. Pay immediately on this link or your connection will be "
                "permanently removed and a legal case will be filed. Offer expires in 30 minutes."
            ),
        },
        "options": [
            {"id": "disconnect", "en": "\"DISCONNECTED TONIGHT\"", "hi": "\"आज रात काट दिया जाएगा\""},
            {"id": "pay_now", "en": "\"Pay immediately\"", "hi": "\"तुरंत भुगतान करें\""},
            {"id": "legal", "en": "\"A legal case will be filed\"", "hi": "\"कानूनी कार्रवाई होगी\""},
            {"id": "expires", "en": "\"Offer expires in 30 minutes\"", "hi": "\"ऑफ़र 30 मिनट में खत्म\""},
            {"id": "greeting", "en": "\"Dear consumer\"", "hi": "\"प्रिय उपभोक्ता\""},
        ],
        "correct": ["disconnect", "pay_now", "legal", "expires"],
        "hints": [
            {"en": "Panic is the pressure tactic; a busy tone of voice, not facts.",
             "hi": "घबराहट बनाना ही ठगी का तरीका है — तथ्य नहीं, डर बेचा जाता है।"},
        ],
        "step_by_step_en": (
            "Real utilities give written notice with account numbers and never demand payment "
            "within minutes. The generic greeting is a weakness too, but the four pressure "
            "phrases are the core tactic."
        ),
        "step_by_step_hi": (
            "असली बिजली कंपनियाँ खाता संख्या के साथ लिखित सूचना देती हैं और मिनटों में भुगतान नहीं माँगती। "
            "सामान्य संबोधन भी कमज़ोरी है, लेकिन चारों दबाव वाले वाक्य मुख्य चाल हैं।"
        ),
        "remediation_en": "Revise lesson 4 (Recognizing Manipulation and Urgency).",
        "remediation_hi": "पाठ 4 (हेर-फेर और जल्दबाज़ी पहचानना) दोहराएँ।",
    },
    {
        "number": 5,
        "slug": "malicious-attachment-warning",
        "title_en": "Identify a malicious attachment warning",
        "title_hi": "खतरनाक अटैचमेंट के संकेत पहचानें",
        "level": "basic",
        "difficulty": "beginner",
        "estimated_minutes": 7,
        "objectives_en": "Recognise file types and wording that precede malware.",
        "objectives_hi": "मैलवेयर से पहले आने वाली फ़ाइल प्रकार और भाषा पहचानें।",
        "scenario_en": "An invoice email arrives from a supplier you have never used.",
        "scenario_hi": "एक ऐसे सप्लायर से इनवॉइस ईमेल आता है जिससे आपने कभी काम नहीं किया।",
        "task_en": "What should you do with the attachment invoice_2026.zip?",
        "task_hi": "invoice_2026.zip अटैचमेंट का क्या करना चाहिए?",
        "task_type": "single_choice",
        "payload": {
            "kind": "email",
            "from": "accounts@northwind-supplies.co",
            "subject": "Overdue invoice — password protected",
            "body": (
                "Please find the overdue invoice attached as a ZIP file. The document inside is "
                "password protected, the password is 1234. Enable macros to view the totals."
            ),
        },
        "options": [
            {"id": "open", "en": "Open it — invoices must be paid",
             "hi": "खोल लें — बिल तो देना ही होगा"},
            {"id": "verify", "en": "Do not open it. Verify the supplier through a known channel",
             "hi": "न खोलें। जाने-पहचाने माध्यम से सप्लायर की पुष्टि करें"},
            {"id": "forward", "en": "Forward it to colleagues to check",
             "hi": "साथियों को जाँचने के लिए भेज दें"},
            {"id": "scan", "en": "Download it and run it through an online scanner later",
             "hi": "डाउनलोड कर बाद में ऑनलाइन स्कैनर से जाँचें"},
        ],
        "correct": ["verify"],
        "hints": [
            {"en": "Password-protected archives are used to slip past email scanners.",
             "hi": "पासवर्ड वाली ZIP फ़ाइलें ईमेल स्कैनर से बचने के लिए बनाई जाती हैं।"},
        ],
        "step_by_step_en": (
            "ZIP + password + 'enable macros' is a classic malware delivery chain. Never open it; "
            "call the supplier using a number you already have and ask whether they sent it."
        ),
        "step_by_step_hi": (
            "ZIP + पासवर्ड + 'मैक्रो चालू करें' — यह मैलवेयर फैलाने का पुराना तरीका है। इसे न खोलें; "
            "अपने पास मौजूद पुराने नंबर पर सप्लायर को फ़ोन कर पूछें।"
        ),
        "remediation_en": "Revise lesson 14 (Malicious Attachments).",
        "remediation_hi": "पाठ 14 (खतरनाक अटैचमेंट) दोहराएँ।",
    },
    {
        "number": 6,
        "slug": "classify-suspicious-sms",
        "title_en": "Classify a suspicious SMS",
        "title_hi": "संदिग्ध SMS की पहचान करें",
        "level": "basic",
        "difficulty": "beginner",
        "estimated_minutes": 6,
        "objectives_en": "Tell a genuine bank alert apart from smishing.",
        "objectives_hi": "असली बैंक सूचना और SMS ठगी में फ़र्क़ करें।",
        "scenario_en": "Two SMS messages arrive about the same card.",
        "scenario_hi": "एक ही कार्ड के बारे में दो SMS आते हैं।",
        "task_en": "Which message is a smishing attempt?",
        "task_hi": "कौन-सा संदेश SMS ठगी है?",
        "task_type": "single_choice",
        "payload": {
            "kind": "sms_pair",
            "items": [
                "HDFCBK: Rs.2,499.00 spent on card XX4821 at BIGBAZAAR on 12-06. Not you? Call 18002586161.",
                "AD-HDFCBK: Your card will be BLOCKED today. Update KYC at http://hdfc-kyc-update.xyz now.",
            ],
        },
        "options": [
            {"id": "a", "en": "The first message — it mentions a transaction",
             "hi": "पहला संदेश — इसमें लेन-देन का ज़िक्र है"},
            {"id": "b", "en": "The second message — it threatens and links to an unknown site",
             "hi": "दूसरा संदेश — इसमें धमकी और अनजान वेबसाइट का लिंक है"},
            {"id": "c", "en": "Both are fraud", "hi": "दोनों ठगी हैं"},
            {"id": "d", "en": "Neither is fraud", "hi": "कोई भी ठगी नहीं है"},
        ],
        "correct": ["b"],
        "hints": [
            {"en": "Real bank alerts state facts; they never push you to a strange link with a threat.",
             "hi": "असली बैंक सूचना तथ्य बताती है; धमकी के साथ अजीब लिंक नहीं भेजती।"},
        ],
        "step_by_step_en": (
            "Message one lists the amount, merchant and a verifiable helpline. Message two uses "
            "an unknown domain (hdfc-kyc-update.xyz) and a blocking threat."
        ),
        "step_by_step_hi": (
            "पहला संदेश राशि, दुकान और असली हेल्पलाइन बताता है। दूसरा संदेश अनजान डोमेन "
            "(hdfc-kyc-update.xyz) और ब्लॉक होने की धमकी देता है।"
        ),
        "remediation_en": "Revise lesson 22 (Smishing and SMS Fraud).",
        "remediation_hi": "पाठ 22 (SMS ठगी) दोहराएँ।",
    },
    {
        "number": 7,
        "slug": "fake-delivery-notification",
        "title_en": "Detect a fake delivery notification",
        "title_hi": "नकली डिलीवरी सूचना पहचानें",
        "level": "basic",
        "difficulty": "beginner",
        "estimated_minutes": 6,
        "objectives_en": "Verify a delivery claim without clicking the link.",
        "objectives_hi": "लिंक पर क्लिक किए बिना डिलीवरी के दावे की पुष्टि करें।",
        "scenario_en": "A WhatsApp message says a parcel is waiting and needs a ₹25 fee.",
        "scenario_hi": "एक WhatsApp संदेश कहता है कि पार्सल रुका है और ₹25 शुल्क चाहिए।",
        "task_en": "What is the safest next step?",
        "task_hi": "सबसे सुरक्षित अगला कदम क्या है?",
        "task_type": "single_choice",
        "payload": {
            "kind": "chat",
            "sender": "+91 70XXXXXX43 (unknown)",
            "body": (
                "India Post: Your parcel IND9823 is held at the depot. A redelivery fee of Rs.25 is "
                "pending. Pay here within 12 hours or the parcel is returned: "
                "http://indiapost-fee.redeliver.top/pay"
            ),
        },
        "options": [
            {"id": "pay", "en": "Pay ₹25 — it is a small amount",
             "hi": "₹25 भर दें — राशि छोटी है"},
            {"id": "track", "en": "Track the parcel on the official India Post website using the number",
             "hi": "आधिकारिक India Post वेबसाइट पर नंबर डालकर पार्सल ट्रैक करें"},
            {"id": "reply", "en": "Reply and ask for the depot address",
             "hi": "जवाब देकर डिपो का पता पूछें"},
            {"id": "forward", "en": "Forward the message to your family group as a warning",
             "hi": "चेतावनी के तौर पर परिवार के ग्रुप में भेज दें"},
        ],
        "correct": ["track"],
        "hints": [
            {"en": "The official app or website is the only place you should enter a tracking number.",
             "hi": "ट्रैकिंग नंबर सिर्फ़ आधिकारिक ऐप या वेबसाइट पर ही डालें।"},
        ],
        "step_by_step_en": (
            "Small fees exist to capture card details. Verify independently on the official site; "
            "do not reply or forward — replying confirms your number is active."
        ),
        "step_by_step_hi": (
            "छोटी राशि माँगकर कार्ड की जानकारी ले ली जाती है। आधिकारिक साइट पर खुद जाँचें; "
            "जवाब न दें, न फ़ॉरवर्ड करें — जवाब देने से पता चल जाता है कि नंबर चालू है।"
        ),
        "remediation_en": "Revise lesson 7 (Spotting Suspicious Links) and lab 3.",
        "remediation_hi": "पाठ 7 (संदिग्ध लिंक पहचानना) और लैब 3 दोहराएँ।",
    },
    {
        "number": 8,
        "slug": "fraudulent-prize-message",
        "title_en": "Identify a fraudulent prize message",
        "title_hi": "नकली इनाम संदेश पहचानें",
        "level": "basic",
        "difficulty": "beginner",
        "estimated_minutes": 6,
        "objectives_en": "Recognise lottery and prize bait.",
        "objectives_hi": "लॉटरी और इनाम के लालच को पहचानें।",
        "scenario_en": "Your parent receives a message about a KBC lottery win.",
        "scenario_hi": "आपके माता-पिता को KBC लॉटरी जीतने का संदेश मिलता है।",
        "task_en": "Select every warning sign in this message.",
        "task_hi": "इस संदेश में हर चेतावनी संकेत चुनें।",
        "task_type": "multi_select",
        "payload": {
            "kind": "chat",
            "sender": "+92 3XX XXXXXX17 (unknown)",
            "body": (
                "Congratulations! Your number has won Rs.25,00,000 in the KBC Lucky Draw. To release "
                "the prize, pay a processing fee of Rs.6,500 and share your Aadhaar and bank account "
                "number. Claim within 24 hours via WhatsApp only."
            ),
        },
        "options": [
            {"id": "you_won", "en": "You never entered the draw", "hi": "आपने कभी ड्रॉ में हिस्सा नहीं लिया"},
            {"id": "advance_fee", "en": "Advance 'processing fee' before receiving money",
             "hi": "पैसे मिलने से पहले 'प्रोसेसिंग फ़ीस'"},
            {"id": "id_docs", "en": "Asks for Aadhaar and bank details", "hi": "आधार और बैंक जानकारी माँगी जा रही है"},
            {"id": "urgency2", "en": "24-hour deadline", "hi": "24 घंटे की समय सीमा"},
            {"id": "channel", "en": "Only WhatsApp, no official office or website",
             "hi": "सिर्फ़ WhatsApp, कोई आधिकारिक कार्यालय या वेबसाइट नहीं"},
            {"id": "foreign_number", "en": "Unknown foreign number", "hi": "अनजान विदेशी नंबर"},
        ],
        "correct": ["you_won", "advance_fee", "id_docs", "urgency2", "channel"],
        "hints": [
            {"en": "A real prize never requires you to pay first.",
             "hi": "असली इनाम में पहले पैसे देने नहीं पड़ते।"},
        ],
        "step_by_step_en": (
            "Legitimate draws never ask for an advance fee, never request identity documents over "
            "chat, and always have an official office and website."
        ),
        "step_by_step_hi": (
            "असली ड्रॉ कभी पहले फ़ीस नहीं माँगते, चैट पर पहचान दस्तावेज़ नहीं लेते, और उनका आधिकारिक "
            "कार्यालय व वेबसाइट होती है।"
        ),
        "remediation_en": "Revise lesson 20 (Investment and Prize Scams).",
        "remediation_hi": "पाठ 20 (निवेश और इनाम ठगी) दोहराएँ।",
    },
    {
        "number": 9,
        "slug": "recognize-fake-job-offer",
        "title_en": "Recognize a fake job offer",
        "title_hi": "नकली नौकरी प्रस्ताव पहचानें",
        "level": "basic",
        "difficulty": "beginner",
        "estimated_minutes": 8,
        "objectives_en": "Verify a recruiter independently before sharing anything.",
        "objectives_hi": "कुछ साझा करने से पहले भर्तीकर्ता की स्वतंत्र पुष्टि करें।",
        "scenario_en": "A final-year student receives an internship offer on WhatsApp.",
        "scenario_hi": "एक अंतिम वर्ष के छात्र को WhatsApp पर इंटर्नशिप का प्रस्ताव मिलता है।",
        "task_en": "Select every warning sign in this job offer.",
        "task_hi": "इस नौकरी प्रस्ताव में हर चेतावनी संकेत चुनें।",
        "task_type": "multi_select",
        "payload": {
            "kind": "email",
            "from": "hr@techmahindra-careers.online",
            "subject": "Selected for Internship — ₹45,000/month, registration fee required",
            "body": (
                "Congratulations! You have been selected for a work-from-home internship with "
                "₹45,000 per month for 2 hours of daily work. To confirm your seat, pay a refundable "
                "registration fee of ₹1,999 and share your PAN, Aadhaar and bank passbook photo. "
                "Offer valid for today only. Selection was based on your resume from a job portal."
            ),
        },
        "options": [
            {"id": "domain", "en": "Recruiter domain is not the company's official domain",
             "hi": "भर्तीकर्ता का डोमेन कंपनी का आधिकारिक डोमेन नहीं है"},
            {"id": "fee", "en": "Fee charged for a job or internship",
             "hi": "नौकरी या इंटर्नशिप के लिए फ़ीस"},
            {"id": "salary", "en": "Unrealistic pay for very little work",
             "hi": "बहुत कम काम के लिए अवास्तविक वेतन"},
            {"id": "documents", "en": "Asks for PAN, Aadhaar and bank passbook together",
             "hi": "एक साथ PAN, आधार और बैंक पासबुक माँगना"},
            {"id": "deadline2", "en": "\"Valid today only\" pressure", "hi": "\"सिर्फ़ आज तक\" का दबाव"},
            {"id": "no_interview", "en": "No interview or technical round at all",
             "hi": "कोई इंटरव्यू या तकनीकी चरण नहीं"},
        ],
        "correct": ["domain", "fee", "salary", "documents", "deadline2", "no_interview"],
        "hints": [
            {"en": "Legitimate employers pay you; you never pay them.",
             "hi": "असली नियोक्ता आपको पैसे देते हैं; आप उन्हें कभी नहीं देते।"},
        ],
        "step_by_step_en": (
            "Check the company's official careers page, search the recruiter's email domain, and "
            "never share identity documents before a signed offer and verified contact."
        ),
        "step_by_step_hi": (
            "कंपनी के आधिकारिक करियर पेज पर देखें, भर्तीकर्ता के ईमेल डोमेन की जाँच करें, और "
            "हस्ताक्षरित ऑफ़र व पुष्ट संपर्क से पहले पहचान दस्तावेज़ साझा न करें।"
        ),
        "remediation_en": "Revise lesson 19 (Fake Job and Internship Offers) and comic 'The Internship That Never Existed'.",
        "remediation_hi": "पाठ 19 (नकली नौकरी प्रस्ताव) और कॉमिक 'जो इंटर्नशिप कभी थी ही नहीं' दोहराएँ।",
    },
    {
        "number": 10,
        "slug": "suspicious-qr-code-scenario",
        "title_en": "Detect a suspicious QR-code scenario",
        "title_hi": "संदिग्ध QR कोड की स्थिति पहचानें",
        "level": "basic",
        "difficulty": "beginner",
        "estimated_minutes": 7,
        "objectives_en": "Treat QR codes as untrusted input.",
        "objectives_hi": "QR कोड को अविश्वसनीय इनपुट मानें।",
        "scenario_en": "A QR code is stuck over the counter at a tea stall; a poster says it is for a reward.",
        "scenario_hi": "चाय की दुकान के काउंटर पर एक QR कोड चिपका है; पोस्टर कहता है इनाम मिलेगा।",
        "task_en": "What is the safest action?",
        "task_hi": "सबसे सुरक्षित कार्रवाई क्या है?",
        "task_type": "single_choice",
        "payload": {
            "kind": "qr",
            "body": (
                "A sticker QR code pasted over the shop's original code reads: "
                "\"Scan to claim a ₹200 cashback — enter your UPI PIN to receive money.\""
            ),
        },
        "options": [
            {"id": "scan", "en": "Scan it and enter the UPI PIN to receive the cashback",
             "hi": "स्कैन करें और कैशबैक पाने के लिए UPI पिन डालें"},
            {"id": "check_sticker", "en": "Refuse; inspect the sticker and ask the shop owner for the real code",
             "hi": "मना करें; स्टिकर जाँचें और दुकानदार से असली कोड पूछें"},
            {"id": "small_scan", "en": "Scan it but only enter the PIN if the page looks official",
             "hi": "स्कैन करें, लेकिन पिन सिर्फ़ तब डालें जब पेज असली लगे"},
            {"id": "note_number", "en": "Scan it and note down the UPI ID for later",
             "hi": "स्कैन करके UPI आईडी नोट कर लें"},
        ],
        "correct": ["check_sticker"],
        "hints": [
            {"en": "You never need a PIN to *receive* money.",
             "hi": "पैसे *लेने* के लिए पिन कभी नहीं लगता।"},
            {"en": "A sticker pasted over the original code is a classic QR-swap trick.",
             "hi": "असली कोड के ऊपर चिपकाया स्टिकर QR बदलने की पुरानी चाल है।"},
        ],
        "step_by_step_en": (
            "Entering a UPI PIN always authorises a payment — never a receipt. Peel-back stickers "
            "over merchant codes are one of the most common retail frauds."
        ),
        "step_by_step_hi": (
            "UPI पिन डालने का मतलब हमेशा भुगतान होता है — पैसे मिलना नहीं। दुकानदार के कोड पर "
            "चिपकाया स्टिकर सबसे आम ठगी में से है।"
        ),
        "remediation_en": "Revise lesson 10 (QR-Code Phishing).",
        "remediation_hi": "पाठ 10 (QR कोड फ़िशिंग) दोहराएँ।",
    },
]

# Export all 40 fully authored game rooms
from app.services.catalog_labs import CATALOG_LABS as LABS_AUTHORED
