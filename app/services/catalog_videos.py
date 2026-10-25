"""Catalogue of 50 video lessons with complete English and Hindi narration and scripts.
Covering all 10 learning modules from foundations to advanced defense.
"""

CATALOG_VIDEOS = [
    # -------------------------------------------------------------------------
    # Module 1: foundations (Lessons 1 - 5)
    # -------------------------------------------------------------------------
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
        "script_hi": (
            "रात में ताला बंद दफ्तर से शुरुआत होती है। आवाज: 'इस इमारत में कैमरे, ताले और अलार्म हैं, फिर भी हमलावर अंदर कैसे पहुंच जाते हैं?'\n"
            "सुबह का दृश्य: वर्दी में एक डिलीवरी वाला भारी बक्से उठाए खड़ा है। रिसेप्शनिस्ट मुस्कुराकर दरवाजा खोल देती है।\n"
            "आवाज: 'क्योंकि हर तकनीकी सुरक्षा को पार करने का सबसे आसान तरीका है एक विनम्र निवेदन।'\n"
            "परिभाषा: सोशल इंजीनियरिंग मानवीय मनोविज्ञान — भरोसा, डर, लालच, जल्दबाजी — का गलत फायदा उठाकर सुरक्षा में सेंध लगाने की कला है।"
        ),
        "narration_en": (
            "Every lock on that building was working. The weakness was a person trying to be helpful. "
            "Social engineering is not hacking a computer. It is hacking a human decision."
        ),
        "narration_hi": (
            "इमारत का हर ताला ठीक काम कर रहा था। कमजोरी थी मदद करने की मानवीय भावना। "
            "सोशल इंजीनियरिंग कंप्यूटर को हैक करना नहीं, बल्कि इंसान के फैसले को हैक करना है।"
        ),
        "transcript_en": "[00:00] Locked office building. [00:15] Delivery person scene. [00:30] Psychology diagram. [00:50] Key takeaway.",
        "transcript_hi": "[00:00] बंद दफ्तर का दृश्य। [00:15] डिलीवरी वाला दृश्य। [00:30] मनोवैज्ञानिक विश्लेषण। [00:50] मुख्य सुरक्षा सीख।",
        "questions": [
            ("Social engineering primarily exploits which vulnerability?",
             ["Outdated router firmware", "Human emotions and helpfulness", "Unpatched operating systems", "Weak Wi-Fi encryption"],
             1, "Social engineering manipulates human psychology, trust, and helpfulness rather than software flaws."),
        ],
    },
    {
        "module": "foundations",
        "slug": "why-humans-become-targets",
        "title_en": "Why Humans Become Targets",
        "title_hi": "इंसान ही मुख्य निशाना क्यों बनते हैं?",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Helpfulness, habit and authority are normal traits an attacker can borrow.",
        "summary_hi": "मदद की आदत, जल्दबाजी और अधिकार का डर — ठग इन्हीं मानवीय कमजोरियों का फायदा उठाते हैं।",
        "script_en": (
            "Four short scenes. One: a guard opens a door for someone with coffee. Two: an employee clicks 'OK' without reading a pop-up. "
            "Three: a junior answers a call from 'the CEO'. Four: a student accepts a friend request from a clone profile.\n"
            "Narration: 'None of these people were careless. They were human.'\n"
            "Diagram of the six levers: authority, urgency, helpfulness, familiarity, curiosity, fear of consequences."
        ),
        "script_hi": (
            "चार दृश्य: गार्ड कॉफी लिए व्यक्ति के लिए दरवाजा खोलता है। कर्मचारी बिना पढ़े पॉप-अप पर क्लिक करता है। "
            "जूनियर कर्मचारी फर्जी 'सीईओ' की कॉल उठाता है। विद्यार्थी मिलते-जुलते प्रोफाइल की फ्रेंड रिक्वेस्ट स्वीकार करता है।\n"
            "आवाज: 'इनमें से कोई लापरवाह नहीं था। वे केवल सामान्य इंसान थे।'"
        ),
        "narration_en": "The traits that make a good colleague make a good target: you help, you trust, and you are usually in a hurry.",
        "narration_hi": "जो गुण आपको एक अच्छा साथी बनाते हैं, वही आपको आसान शिकार भी बना सकते हैं: परोपकार, भरोसा और जल्दबाजी।",
        "transcript_en": "[00:00] Four real-life scenes. [00:20] The six psychological levers. [00:45] How to pause before clicking.",
        "transcript_hi": "[00:00] चार दैनिक जीवन के उदाहरण। [00:20] छह मनोवैज्ञानिक ट्रिगर। [00:45] क्लिक करने से पहले रुकने की आदत।",
        "questions": [
            ("Which factor makes humans an attractive target for cyber attackers?",
             ["Computers have emotions", "Technical firewalls are cheaper to breach", "Humans can be hurried and emotionally pressured", "Humans have no passwords"],
             2, "Attackers target humans because social manipulation circumvents multimillion-dollar technical firewalls."),
        ],
    },
    {
        "module": "foundations",
        "slug": "the-cost-of-a-breach",
        "title_en": "The Real Cost of a Security Breach",
        "title_hi": "सुरक्षा उल्लंघन की असली कीमत",
        "difficulty": "beginner",
        "duration": 6,
        "summary_en": "Breaches don't just cost money — they cost customer trust, jobs, and institutional reputations.",
        "summary_hi": "डेटा लीक से केवल वित्तीय नुकसान नहीं होता, बल्कि ग्राहकों का भरोसा और प्रतिष्ठा भी खत्म हो जाती है।",
        "script_en": (
            "Visual of a digital news ticker reporting a major corporate breach. "
            "Breakdown of hidden impacts: regulatory fines, forensic recovery costs, customer compensation, and permanent brand erosion.\n"
            "Case study highlight: How a single stolen password led to weeks of halted operations."
        ),
        "script_hi": (
            "डिजिटल स्क्रीन पर एक बड़ी कंपनी के डेटा लीक की खबर। "
            "छिपे हुए नुकसानों का विश्लेषण: कानूनी जुर्माना, फॉरेंसिक जांच का खर्च, ग्राहकों का मुआवजा और ब्रांड की बदनामी।\n"
            "वास्तविक उदाहरण: कैसे एक साधारण पासवर्ड लीक से पूरा कामकाज हफ्तों ठप रहा।"
        ),
        "narration_en": "When an attacker gains a foothold, the remediation bill is hundreds of times more expensive than the training needed to prevent it.",
        "narration_hi": "जब हमलावर एक बार अंदर घुस जाता है, तो नुकसान की भरपाई सुरक्षा प्रशिक्षण के खर्च से सैकड़ों गुना भारी पड़ती है।",
        "transcript_en": "[00:00] The news headline. [00:20] Direct vs indirect costs. [00:40] Why prevention is personal.",
        "transcript_hi": "[00:00] समाचार की सुर्खियां। [00:20] प्रत्यक्ष बनाम अप्रत्यक्ष नुकसान। [00:40] बचाव ही सबसे बड़ा उपाय।",
        "questions": [
            ("Beyond direct financial theft, what is often the most damaging consequence of a breach?",
             ["A slow internet connection", "Loss of customer trust and regulatory penalties", "Having to restart laptops", "Replacing office furniture"],
             1, "Reputational loss and heavy regulatory fines often exceed the direct monetary theft."),
        ],
    },
    {
        "module": "foundations",
        "slug": "the-human-firewall-mindset",
        "title_en": "The Human Firewall Mindset",
        "title_hi": "ह्यूमन फ़ायरवॉल सोच और सतर्कता",
        "difficulty": "beginner",
        "duration": 6,
        "summary_en": "Technology detects signatures; humans detect context and nuance. Cultivate positive defense instincts.",
        "summary_hi": "तकनीक कोड को पकड़ती है, लेकिन इंसान संदर्भ और असामान्य व्यवहार को पहचानता है।",
        "script_en": (
            "Split screen: On the left, an automated spam filter marks an email as safe because the sender IP is clean. "
            "On the right, an employee notices the wording is oddly urgent and the bank details changed.\n"
            "The human eye catches what the algorithm missed."
        ),
        "script_hi": (
            "विभाजित स्क्रीन: बाईं ओर स्पैम फिल्टर ईमेल को सुरक्षित बताता है क्योंकि आईपी साफ है। "
            "दाईं ओर कर्मचारी पकड़ता है कि ईमेल की भाषा असामान्य रूप से जल्दबाजी भरी है और बैंक खाता नया है।\n"
            "मानवीय समझ वह पकड़ लेती है जो ऑटोमेशन छोड़ देता है।"
        ),
        "narration_en": "You are not the weakest link. When trained and supported, every employee is the strongest security sensor in the organization.",
        "narration_hi": "आप सुरक्षा की सबसे कमजोर कड़ी नहीं हैं। सही जागरूकता के साथ हर कर्मचारी सबसे सशक्त सुरक्षा संवेदक बन सकता है।",
        "transcript_en": "[00:00] Filter vs human intuition. [00:25] Spotting out-of-character requests. [00:50] The 3-second pause.",
        "transcript_hi": "[00:00] फिल्टर बनाम मानवीय समझ। [00:25] असामान्य अनुरोधों की पहचान। [00:50] 3 सेकंड रुकने का नियम।",
        "questions": [
            ("What defines the 'Human Firewall' mindset?",
             ["Refusing to ever open email", "Pausing to verify unexpected or urgent requests", "Allowing IT to handle 100% of safety", "Sharing passwords with teammates"],
             1, "A Human Firewall pauses to verify unusual or high-pressure requests through independent channels."),
        ],
    },
    {
        "module": "foundations",
        "slug": "spotting-psychological-triggers",
        "title_en": "Spotting Psychological Triggers",
        "title_hi": "मनोवैज्ञानिक चालबाज़ियों को पहचानना",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Recognize the 5 emotional triggers attackers use: Fear, Urgency, Greed, Curiosity, and Helpful Sympathy.",
        "summary_hi": "हमलावरों द्वारा प्रयुक्त 5 प्रमुख भावनाओं को पहचानें: डर, जल्दबाजी, लालच, उत्सुकता और दया।",
        "script_en": (
            "Animated spotlight on 5 warning icons. Fear: 'Your account will be suspended!' "
            "Urgency: 'Act in 10 minutes!' Greed: 'You won a lottery!' Curiosity: 'Check this leaked video!' "
            "Sympathy: 'I am stranded without a wallet, help me!'"
        ),
        "script_hi": (
            "5 चेतावनी संकेतों पर प्रकाश: डर: 'आपका खाता बंद हो जाएगा!' जल्दबाजी: '10 मिनट में जवाब दें!' "
            "लालच: 'आपने लॉटरी जीती है!' उत्सुकता: 'यह लीक हुआ वीडियो देखें!' सहानुभूति: 'मैं मुसीबत में हूं, मदद करें!'"
        ),
        "narration_en": "Whenever a message makes your heart beat faster or tells you not to tell anyone, step back. That emotional spike is the trap.",
        "narration_hi": "जब भी कोई संदेश आपको घबराहट, लालच या अत्यधिक उत्सुकता में डाले, तुरंत रुक जाएं। वह भावना ही जाल है।",
        "transcript_en": "[00:00] The 5 core triggers. [00:25] Real-world message examples. [00:45] Disarming the emotional hijack.",
        "transcript_hi": "[00:00] 5 मुख्य मनोवैज्ञानिक ट्रिगर। [00:25] वास्तविक संदेशों के उदाहरण। [00:45] भावनात्मक दबाव से बचाव।",
        "questions": [
            ("If a message demands immediate action under threat of penalty, what trigger is being used?",
             ["Familiarity", "Urgency and Fear", "Politeness", "Transparency"],
             1, "Urgency and fear are combined to bypass logical thinking and force rushed compliance."),
        ],
    },

    # -------------------------------------------------------------------------
    # Module 2: phishing (Lessons 6 - 10)
    # -------------------------------------------------------------------------
    {
        "module": "phishing",
        "slug": "anatomy-of-a-phishing-email",
        "title_en": "Anatomy of a Phishing Email",
        "title_hi": "फ़िशिंग ईमेल की अंदरूनी बनावट",
        "difficulty": "beginner",
        "duration": 6,
        "summary_en": "Break down headers, disguised URLs, spoofed display names, and coercive calls to action.",
        "summary_hi": "ईमेल हेडर, छिपे हुए लिंक, मिलते-जुलते नाम और दबाव डालने वाली भाषा को बारीकी से समझें।",
        "script_en": (
            "Graphic overlay of an email message. Highlight 1: Display name 'IT Support' vs actual address 'support@it-desk-portal382.com'. "
            "Highlight 2: Generic greeting 'Dear User'. Highlight 3: Hyperlink pointing to an unverified IP address.\n"
            "Highlight 4: Pressure tactic claiming server maintenance."
        ),
        "script_hi": (
            "ईमेल का विस्तृत दृश्य। संकेत 1: डिस्प्ले नाम 'आईटी सपोर्ट' लेकिन वास्तविक पता 'support@it-desk-portal382.com'। "
            "संकेत 2: सामान्य संबोधन 'प्रिय उपयोगकर्ता'। संकेत 3: लिंक किसी अनजान वेबसाइट पर ले जाता है। "
            "संकेत 4: सर्वर बंद होने की धमकी देकर डराना।"
        ),
        "narration_en": "Never judge an email by its subject line or logo. Look under the hood at the domain and where the link actually leads.",
        "narration_hi": "किसी ईमेल को उसके लोगो या हेडिंग से न पहचानें। हमेशा प्रेषक के असली डोमेन और लिंक के गंतव्य को जांचें।",
        "transcript_en": "[00:00] Email breakdown. [00:20] Display name spoofing. [00:40] Inspecting hyperlinks safely.",
        "transcript_hi": "[00:00] ईमेल के पुर्जे। [00:20] नाम की नकल। [00:40] बिना क्लिक किए लिंक की जांच।",
        "questions": [
            ("What is the safest way to see where an email hyperlink truly leads?",
             ["Click on it in an incognito tab", "Hover your cursor over the link to preview the URL without clicking", "Forward it to a friend", "Reply to the sender"],
             1, "Hovering over the link (or long-pressing on mobile) displays the true destination URL without executing dangerous code."),
        ],
    },
    {
        "module": "phishing",
        "slug": "spear-phishing-and-whaling",
        "title_en": "Spear Phishing and Executive Whaling",
        "title_hi": "सटीक फ़िशिंग और वरिष्ठ अधिकारियों पर हमला",
        "difficulty": "intermediate",
        "duration": 6,
        "summary_en": "Targeted attacks use LinkedIn and public news to craft personalized, high-conviction traps.",
        "summary_hi": "हमलावर सोशल मीडिया और खबरों से आपकी जानकारी जुटाकर बेहद निजी और भरोसेमंद जाल बुनते हैं।",
        "script_en": (
            "Attacker profiling demo: The attacker checks LinkedIn, sees a company just hired a new CFO, "
            "and creates a fake email spoofing the CEO asking for an urgent confidential wire transfer."
        ),
        "script_hi": (
            "हमलावर की तैयारी: हमलावर लिंक्डइन पर देखता है कि कंपनी में नए सीएफओ आए हैं। "
            "वह तुरंत सीईओ के नाम से फर्जी ईमेल बनाकर गोपनीय फंड ट्रांसफर का आदेश भेजता है।"
        ),
        "narration_en": "Spear phishing has no spelling errors or generic greetings. It mentions your real boss, your real projects, and your real deadlines.",
        "narration_hi": "सटीक फ़िशिंग में कोई वर्तनी की गलती नहीं होती। इसमें आपके असली प्रोजेक्ट और असली अधिकारियों के नाम होते हैं।",
        "transcript_en": "[00:00] Reconnaissance phase. [00:25] The tailored lure. [00:50] Out-of-band verification protocol.",
        "transcript_hi": "[00:00] हमलावर की जासूसी। [00:25] व्यक्तिगत संदेश। [00:50] स्वतंत्र फोन कॉल से पुष्टि।",
        "questions": [
            ("How does spear phishing differ from ordinary bulk phishing?",
             ["It only happens on weekends", "It is customized with researched personal/work details about the target", "It never contains links", "It is sent via postal mail"],
             1, "Spear phishing is highly targeted and personalized using researched information about the victim."),
        ],
    },
    {
        "module": "phishing",
        "slug": "fake-login-pages-and-credential-theft",
        "title_en": "Fake Login Portals & Credential Theft",
        "title_hi": "नकली लॉगिन पोर्टल और पासवर्ड चोरी",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Identify pixel-perfect replica login screens and look-alike domains before typing passwords.",
        "summary_hi": "बिल्कुल असली जैसी दिखने वाली फर्जी लॉगिन वेबसाइट और भ्रामक डोमेन की पहचान करना सीखें।",
        "script_en": (
            "Side by side: login.microsoftonline.com vs login-microsoft-verify.net. "
            "Demonstrate how an attacker clones CSS stylesheets and corporate logos in minutes.\n"
            "Show what happens behind the scenes: Credentials typed into the fake page are instantly sent to a hacker's Telegram bot."
        ),
        "script_hi": (
            "तुलना: असली login.microsoftonline.com बनाम फर्जी login-microsoft-verify.net। "
            "दिखाएं कि कैसे हमलावर कुछ मिनटों में असली लोगो और डिजाइन की हूबहू नकल कर लेते हैं। "
            "पर्दे के पीछे: जैसे ही आप पासवर्ड डालते हैं, वह तुरंत हैकर के सर्वर पर पहुंच जाता है।"
        ),
        "narration_en": "A padlock in the address bar only means the connection is encrypted — it does NOT mean the website is honest.",
        "narration_hi": "ब्राउज़र में ताले का निशान केवल यह बताता है कि कनेक्शन एन्क्रिप्टेड है, यह नहीं कि वेबसाइट ईमानदार है।",
        "transcript_en": "[00:00] Clone page demonstration. [00:25] Examining the exact domain name. [00:45] Password managers as defense.",
        "transcript_hi": "[00:00] क्लोन वेबसाइट का सच। [00:25] डोमेन स्पेलिंग की सूक्ष्म जांच। [00:45] पासवर्ड मैनेजर की सुरक्षा।",
        "questions": [
            ("Does an HTTPS padlock icon guarantee that a website is legitimate and safe?",
             ["Yes, fake sites cannot obtain SSL certificates", "No, attackers can easily obtain free SSL certificates for phishing domains", "Yes, banks own the padlock symbol", "Only on Google Chrome"],
             1, "HTTPS only encrypts the traffic in transit; malicious websites frequently use free SSL certificates."),
        ],
    },
    {
        "module": "phishing",
        "slug": "deceptive-attachments-and-hidden-macros",
        "title_en": "Deceptive Attachments & Hidden Macros",
        "title_hi": "खतरनाक अटैचमेंट और छुपे हुए मैक्रो",
        "difficulty": "intermediate",
        "duration": 6,
        "summary_en": "Learn why enabling macros or extracting double-extension files (.pdf.exe) unleashes malware.",
        "summary_hi": "जानें कि मैक्रो इनेबल करने या दोहरे एक्सटेंशन वाली फाइलों को खोलने से मैलवेयर कैसे फैलता है।",
        "script_en": (
            "Animation showing an email attachment titled 'Q4_Bonuses.xlsm'. "
            "A yellow banner inside Excel prompts: 'Enable Editing and Macros to view content'. "
            "Show how clicking that button runs a hidden visual basic script that downloads ransomware."
        ),
        "script_hi": (
            "एनिमेशन: 'Q4_Bonuses.xlsm' नाम की फाइल। "
            "एक्सेल में पीली पट्टी दिखती है: 'सामग्री देखने के लिए मैक्रो सक्षम करें'। "
            "दिखाएं कि उस बटन पर क्लिक करते ही बैकग्राउंड में रैनसमवेयर डाउनलोड हो जाता है।"
        ),
        "narration_en": "Never enable macros for an unexpected document. Legitimate companies will never require macros just to display text.",
        "narration_hi": "अचानक आई किसी भी फाइल में मैक्रो सक्षम न करें। सामान्य दस्तावेज पढ़ने के लिए मैक्रो की कभी आवश्यकता नहीं होती।",
        "transcript_en": "[00:00] The lure file. [00:20] The yellow macro warning trap. [00:45] File extension tricks (.pdf.exe).",
        "transcript_hi": "[00:00] लालच भरी फाइल। [00:20] मैक्रो चेतावनी का जाल। [00:45] फाइल एक्सटेंशन के धोखे।",
        "questions": [
            ("If an emailed document asks you to 'Enable Content/Macros' to view text, you should:",
             ["Click enable immediately", "Close the document and report it to IT security", "Email it to your personal account", "Print it without reading"],
             1, "Requiring macros to view text is a classic trick used by malware loaders."),
        ],
    },
    {
        "module": "phishing",
        "slug": "qr-code-quishing-attacks",
        "title_en": "QR Code Phishing - Quishing Traps",
        "title_hi": "क्यूआर कोड फ़िशिंग यानी क्विशिंग",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Physical stickers pasted on parking meters and embedded in emails bypass security scanners.",
        "summary_hi": "पार्किंग मीटर पर चिपकाए गए फर्जी क्यूआर स्टिकर और ईमेल में छिपे क्यूआर कोड से बचाव।",
        "script_en": (
            "Camera zooms in on a public parking meter. A fraudster has placed a sticker over the genuine QR code. "
            "A driver scans it with their phone, leading to a fake payment gateway that steals credit card data."
        ),
        "script_hi": (
            "पार्किंग मीटर का दृश्य: जालसाज ने असली क्यूआर कोड पर अपना फर्जी स्टिकर चिपका दिया है। "
            "ड्राइवर स्कैन करता है और एक फर्जी पेमेंट गेटवे पर पहुंच जाता है जो कार्ड का विवरण चुरा लेता है।"
        ),
        "narration_en": "You cannot read a QR code with the naked eye. Always preview the full destination web address before tapping open.",
        "narration_hi": "आप नंगी आंखों से क्यूआर कोड का लिंक नहीं पढ़ सकते। हमेशा फोन में खुलने वाले पूरे वेब पते की जांच करें।",
        "transcript_en": "[00:00] The parking meter scam. [00:20] Email quishing bypassing corporate gateways. [00:45] Safe scanning tips.",
        "transcript_hi": "[00:00] पार्किंग का क्यूआर घोटाला। [00:20] ईमेल में क्यूआर से फिल्टर को चकमा देना। [00:45] सुरक्षित स्कैनिंग नियम।",
        "questions": [
            ("Why do cybercriminals use QR codes instead of regular text hyperlinks in phishing emails?",
             ["QR codes load faster", "QR codes often bypass automated email text filters and force victims onto unmanaged mobile devices", "QR codes are immune to antivirus", "QR codes cannot be tracked"],
             1, "QR images hide the URL from traditional email gateway inspection engines and shift the victim to mobile devices."),
        ],
    },

    # -------------------------------------------------------------------------
    # Module 3: messaging (Lessons 11 - 15)
    # -------------------------------------------------------------------------
    {
        "module": "messaging",
        "slug": "whatsapp-and-sms-smishing",
        "title_en": "WhatsApp & SMS Smishing Scams",
        "title_hi": "व्हाट्सएप और एसएमएस स्मिशिंग ठगी",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Shortened links and fake delivery updates sent directly to your phone's notification bar.",
        "summary_hi": "फोन पर आने वाले छोटे लिंक और फर्जी कूरियर अपडेट के जरिए होने वाली ठगी से सतर्क रहें।",
        "script_en": (
            "Phone vibrates: SMS from 'VK-INDPOST' stating: 'Your parcel is blocked due to incomplete address. Update now: bit.ly/post-track'. "
            "Explain how URL shorteners conceal dangerous phishing pages."
        ),
        "script_hi": (
            "फोन पर घंटी बजती है: 'VK-INDPOST' से मैसेज: 'अधूरे पते के कारण आपका पार्सल रुका हुआ है। अभी अपडेट करें: bit.ly/post-track'। "
            "समझाएं कि कैसे छोटे लिंक खतरनाक वेबसाइट को छुपाते हैं।"
        ),
        "narration_en": "Postal services and courier companies will never ask you to pay small ₹10 fees via an unverified shortened link.",
        "narration_hi": "डाक विभाग या कूरियर कंपनियां कभी भी छोटे लिंक के जरिए ₹10 या ₹25 जैसी छोटी फीस नहीं मांगतीं।",
        "transcript_en": "[00:00] The delivery SMS notification. [00:20] Deobfuscating short links. [00:40] Official tracking apps.",
        "transcript_hi": "[00:00] पार्सल डिलीवरी का फर्जी एसएमएस। [00:20] छोटे लिंक का सच। [00:40] आधिकारिक ऐप से ट्रैकिंग।",
        "questions": [
            ("What should you do if an SMS claims your bank account or parcel is blocked and provides a shortened link?",
             ["Click the link immediately to prevent delays", "Open the official bank/courier app or website independently to check", "Forward the SMS to family", "Text back with your name"],
             1, "Never click links in urgent SMS messages; verify directly using official apps or independently looked-up websites."),
        ],
    },
    {
        "module": "messaging",
        "slug": "social-media-impersonation",
        "title_en": "Social Media Impersonation",
        "title_hi": "सोशल मीडिया पर नकली प्रोफ़ाइल और प्रतिरूपण",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "How attackers steal profile photos to create clone accounts and message your closest contacts.",
        "summary_hi": "जानें कैसे ठग आपकी प्रोफाइल फोटो चुराकर फर्जी अकाउंट बनाते हैं और दोस्तों से पैसे मांगते हैं।",
        "script_en": (
            "Instagram/Facebook clone demonstration: An attacker copies your avatar, bio, and posts. "
            "They send DMs to your mutual friends: 'Hey, I lost access to my old account and need ₹5,000 urgently for an emergency hospital bill!'"
        ),
        "script_hi": (
            "सोशल मीडिया क्लोन का उदाहरण: ठग आपकी फोटो और नाम से नया अकाउंट बनाता है। "
            "वह आपके मित्रों को मैसेज करता है: 'मेरा पुराना फोन खो गया है, अस्पताल में भर्ती हूं, तुरंत ₹5,000 भेज दो!'"
        ),
        "narration_en": "If a friend messages from a new profile asking for money or gift cards, call their known phone number immediately to confirm.",
        "narration_hi": "यदि कोई दोस्त नए प्रोफाइल से पैसे मांगे, तो तुरंत उसके पुराने फोन नंबर पर सीधे कॉल करके पुष्टि करें।",
        "transcript_en": "[00:00] Clone account creation. [00:25] The emergency money script. [00:45] Reporting and warning mutuals.",
        "transcript_hi": "[00:00] क्लोन अकाउंट कैसे बनता है। [00:25] इमरजेंसी में पैसे मांगने की चाल। [00:45] रिपोर्ट करना और दोस्तों को सचेत करना।",
        "questions": [
            ("A social media friend messages from a 'new secondary account' asking for urgent financial help. Your first step is:",
             ["Send money via UPI right away", "Call them directly on their known phone number to verify their identity", "Ignore it forever", "Ask for their password"],
             1, "Always verify identity through a known, trusted voice phone call before transferring funds."),
        ],
    },
    {
        "module": "messaging",
        "slug": "urgent-family-emergency-scams",
        "title_en": "Emergency & Distress Message Traps",
        "title_hi": "आपातकाल और संकट के नाम पर ठगी",
        "difficulty": "intermediate",
        "duration": 6,
        "summary_en": "Scammers pose as police, lawyers, or hospitals claiming a loved one is in grave trouble.",
        "summary_hi": "ठग पुलिस, वकील या डॉक्टर बनकर दावा करते हैं कि आपका कोई परिजन गंभीर संकट में है।",
        "script_en": (
            "A frantic WhatsApp voice note from an unknown international number: "
            "'Your son has been detained in a foreign country. Pay bail immediately or he goes to prison.' "
            "Break down how emotional panic prevents parents from calling their son directly."
        ),
        "script_hi": (
            "व्हाट्सएप पर घबराई हुई आवाज: 'आपका बेटा विदेश में हिरासत में है। तुरंत जमानत की रकम भेजो वर्ना जेल हो जाएगी।' "
            "समझें कि कैसे अचानक डर के कारण माता-पिता सीधे अपने बेटे को कॉल करना भूल जाते हैं।"
        ),
        "narration_en": "Panic shuts down analytical reasoning. Take 60 seconds, breathe, and call your family member directly before taking any action.",
        "narration_hi": "डर इंसान के सोचने की शक्ति छीन लेता है। 60 सेकंड रुकें, गहरी सांस लें और सीधे अपने परिजन को फोन मिलाएं।",
        "transcript_en": "[00:00] The hostage/bail scam script. [00:25] Why attackers insist you stay on the line. [00:45] Verification protocols.",
        "transcript_hi": "[00:00] फर्जी गिरफ्तारी की स्क्रिप्ट। [00:25] ठग फोन काटने क्यों नहीं देते। [00:45] सुरक्षित पुष्टि का तरीका।",
        "questions": [
            ("Why do emergency scammers insist that you 'stay on the phone and tell nobody'?",
             ["To save battery", "To prevent you from contacting your loved one or seeking third-party advice", "Because long calls are free", "They want to practice talking"],
             1, "Isolating you on the phone prevents you from independently checking on your family member."),
        ],
    },
    {
        "module": "messaging",
        "slug": "fake-job-and-internship-offers",
        "title_en": "Fake Job Offers & Freelance Bait",
        "title_hi": "नकली नौकरी और पार्ट-टाइम कमाई का जाल",
        "difficulty": "beginner",
        "duration": 6,
        "summary_en": "Work-from-home tasks, YouTube like scams, and upfront 'registration fees' that drain savings.",
        "summary_hi": "घर बैठे काम, वीडियो लाइक करके कमाई और 'रजिस्ट्रेशन फीस' के नाम पर होने वाले फ्रॉड से बचें।",
        "script_en": (
            "Telegram message: 'Earn ₹3,000 daily by liking YouTube videos!'. "
            "Stage 1: They pay small ₹150 rewards to build trust. "
            "Stage 2: They ask you to deposit ₹10,000 into a 'crypto investment portal' to unlock VIP tasks. "
            "Stage 3: Your deposited money is locked forever."
        ),
        "script_hi": (
            "टेलीग्राम पर मैसेज: 'यूट्यूब वीडियो लाइक करके रोज ₹3,000 कमाएं!' "
            "पहला चरण: भरोसा जीतने के लिए ₹150 का भुगतान करते हैं। "
            "दूसरा चरण: वीआईपी टास्क के नाम पर ₹10,000 जमा करने को कहते हैं। "
            "तीसरा चरण: आपके जमा पैसे कभी वापस नहीं मिलते।"
        ),
        "narration_en": "Real companies pay you for your work — you never have to pay a company to work for them.",
        "narration_hi": "असली नौकरियां काम के बदले आपको पैसे देती हैं — आपको नौकरी पाने के लिए कभी पैसे नहीं भरने पड़ते।",
        "transcript_en": "[00:00] The task scam lifecycle. [00:25] The bait payments. [00:45] Spotting legitimate recruitment channels.",
        "transcript_hi": "[00:00] टास्क घोटाले का चक्र। [00:25] विश्वास जगाने के छोटे भुगतान। [00:45] असली भर्ती प्रक्रियाओं की पहचान।",
        "questions": [
            ("A recruiter offers a high-paying remote job but requires an upfront ₹2,500 'laptop security deposit'. This is:",
             ["Standard industry practice", "A recruitment scam designed to steal your money", "A government tax", "A refundable bonus"],
             1, "Legitimate employers never charge candidates upfront fees for equipment, registration, or onboarding."),
        ],
    },
    {
        "module": "messaging",
        "slug": "malicious-direct-messages-and-links",
        "title_en": "Malicious DMs & Compressed Archives",
        "title_hi": "निजी संदेशों में खतरनाक लिंक और ज़िप फ़ाइलें",
        "difficulty": "intermediate",
        "duration": 5,
        "summary_en": "Beware of password-protected zip files (.rar/.7z) sent on Discord and LinkedIn claiming to be portfolios.",
        "summary_hi": "डिस्कॉर्ड और लिंक्डइन पर पोर्टफोलियो या रिज्यूमे के नाम पर भेजी जाने वाली पासवर्ड युक्त ज़िप फाइलों से सावधान रहें।",
        "script_en": (
            "A freelancer receives a DM: 'I love your designs, please see our brief inside this archive (password: 1234)'. "
            "Why the password? It encrypts the payload so cloud scanners cannot detect the info-stealer Trojan inside."
        ),
        "script_hi": (
            "फ्रीलांसर को संदेश मिलता है: 'मुझे आपका काम पसंद आया, हमारा प्रोजेक्ट इस ज़िप फाइल में है (पासवर्ड: 1234)'। "
            "पासवर्ड क्यों दिया जाता है? ताकि एंटीवायरस और क्लाउड स्कैनर अंदर छिपे ट्रोजन वायरस को स्कैन न कर सकें।"
        ),
        "narration_en": "Encrypted archives from unknown senders are designed to bypass perimeter inspection. Treat them as toxic.",
        "narration_hi": "अपरिचित स्रोतों से आई पासवर्ड लगी ज़िप फाइलें एंटीवायरस को धोखा देने के लिए बनाई जाती हैं। उन्हें कभी न खोलें।",
        "transcript_en": "[00:00] The freelance bait lure. [00:20] How encrypted archives evade scanners. [00:45] Safe sandbox inspection.",
        "transcript_hi": "[00:00] प्रोजेक्ट का झांसा। [00:20] पासवर्ड से एंटीवायरस को मात देना। [00:45] सुरक्षित सैंडबॉक्स जांच।",
        "questions": [
            ("Why do cybercriminals send malware in password-protected zip archives?",
             ["It saves internet bandwidth", "The password encryption prevents email security scanners from inspecting the malware inside", "ZIP files are approved by Microsoft", "To make it look professional"],
             1, "Password protection encrypts archive contents, preventing automated perimeter security tools from scanning the payload."),
        ],
    },

    # -------------------------------------------------------------------------
    # Module 4: financial (Lessons 16 - 20)
    # -------------------------------------------------------------------------
    {
        "module": "financial",
        "slug": "urgent-wire-transfer-ceo-fraud",
        "title_en": "Urgent Wire Transfer & CEO Fraud",
        "title_hi": "तत्काल बैंक ट्रांसफर और सीईओ फ्रॉड",
        "difficulty": "intermediate",
        "duration": 6,
        "summary_en": "Business Email Compromise (BEC): How attackers manipulate finance teams into rerouting millions.",
        "summary_hi": "बिजनेस ईमेल कंप्रोमाइज: कैसे हैकर्स खातों की टीम पर दबाव डालकर करोड़ों रुपये डायवर्ट कर लेते हैं।",
        "script_en": (
            "Simulation of Pooja, accounts specialist. She receives an urgent email from her CEO: "
            "'Pooja, I am in a confidential board meeting. Reroute $45,000 for an urgent supplier acquisition today. Do not call, just execute.'\n"
            "Walk through the out-of-band verification protocol that saves the company."
        ),
        "script_hi": (
            "पूजा, अकाउंट विशेषज्ञ का सिमुलेशन। उसे अपने सीईओ से तत्काल ईमेल मिलता है: "
            "'पूजा, मैं एक महत्वपूर्ण मीटिंग में हूं। वेंडर के नए खाते में आज ही ₹15 लाख ट्रांसफर करो। फोन मत करना, तुरंत करो।'\n"
            "वह सुरक्षा प्रक्रिया अपनाकर सीधे फोन करती है और फ्रॉड रोक देती है।"
        ),
        "narration_en": "No executive request, regardless of rank, overrides written dual-authorization procedures for wire transfers.",
        "narration_hi": "चाहे अधिकारी कितने भी बड़े पद पर हों, बैंक ट्रांसफर के दोहरे सत्यापन के सुरक्षा नियमों का उल्लंघन कभी न करें।",
        "transcript_en": "[00:00] The urgent CEO email. [00:25] The psychology of organizational hierarchy. [00:50] The dual-authorization rule.",
        "transcript_hi": "[00:00] सीईओ का फर्जी ईमेल। [00:25] पद के डर का मनोवैज्ञानिक फायदा। [00:50] दोहरे सत्यापन का अनिवार्य नियम।",
        "questions": [
            ("If an email ostensibly from your CEO orders an immediate wire transfer and forbids phone verification, you should:",
             ["Wire the money immediately to avoid being fired", "Follow standard corporate verification protocol and verify through a pre-agreed secondary channel", "Reply to the email asking if it's real", "Forward it to all colleagues"],
             1, "Always follow dual-authorization controls; genuine executives respect and enforce financial defense protocols."),
        ],
    },
    {
        "module": "financial",
        "slug": "upi-qr-payment-reversal-traps",
        "title_en": "UPI QR Code & Reverse Payment Traps",
        "title_hi": "यूपीआई क्यूआर और रिवर्स पेमेंट का झांसा",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "The golden rule of digital payments: You NEVER enter your UPI PIN to receive money.",
        "summary_hi": "डिजिटल भुगतान का स्वर्णिम नियम: पैसे प्राप्त करने के लिए कभी भी अपना यूपीआई पिन दर्ज न करें।",
        "script_en": (
            "OLX/Marketplace seller listing furniture for ₹15,000. Buyer calls: 'I am sending you a QR code on WhatsApp. "
            "Scan it and enter your PIN, and the ₹15,000 will be credited directly to your bank account.' "
            "Visual demonstration of the money getting debited instead."
        ),
        "script_hi": (
            "ऑनलाइन सामान बेचने का दृश्य। खरीदार कॉल करता है: 'मैं व्हाट्सएप पर क्यूआर कोड भेज रहा हूं। "
            "उसे स्कैन करके अपना पिन डालें, पैसे तुरंत आपके बैंक में क्रेडिट हो जाएंगे।' "
            "दिखाएं कि पिन डालते ही पैसे खाते से कट जाते हैं।"
        ),
        "narration_en": "Remember the fundamental law: UPI PIN is ONLY for giving money away. Receiving money requires zero authorization from you.",
        "narration_hi": "याद रखें: यूपीआई पिन केवल पैसे भेजने के लिए होता है। पैसे प्राप्त करने के लिए किसी पिन की जरूरत नहीं होती।",
        "transcript_en": "[00:00] The marketplace buyer call. [00:20] The reverse payment trick. [00:40] The universal UPI rule.",
        "transcript_hi": "[00:00] फर्जी खरीदार की कॉल। [00:20] रिवर्स पेमेंट का झांसा। [00:40] यूपीआई का बुनियादी नियम।",
        "questions": [
            ("When does a UPI user need to enter their secret PIN?",
             ["When receiving money from a stranger", "Only when sending money or checking bank balance", "When claiming a cash refund", "When scanning any QR code"],
             1, "Your UPI PIN is strictly for authorizing debits from your account; you never enter it to receive funds."),
        ],
    },
    {
        "module": "financial",
        "slug": "fake-invoice-and-vendor-redirection",
        "title_en": "Fake Invoices & Vendor Account Changes",
        "title_hi": "फर्जी इनवॉइस और सप्लायर खाता बदलना",
        "difficulty": "intermediate",
        "duration": 6,
        "summary_en": "How attackers compromise vendor mailboxes and send updated bank account details right before payment dates.",
        "summary_hi": "जानें कैसे हैकर्स वेंडर का ईमेल हैक कर भुगतान से ठीक पहले बैंक खाता बदलने का फर्जी पत्र भेजते हैं।",
        "script_en": (
            "Case study: A long-time supplier sends an email with an authentic PDF invoice. "
            "A small note reads: 'Our bank changed. Please update our account number to XXXXX.' "
            "Show how calling the supplier's vendor manager on their known office landline uncovers the compromise."
        ),
        "script_hi": (
            "केस स्टडी: पुराने सप्लायर का ईमेल आता है जिसमें असली जैसा बिल लगा है। "
            "नीचे लिखा है: 'हमारा बैंक बदल गया है, कृपया नए खाते में भुगतान करें।' "
            "सप्लायर के पुराने लैंडलाइन नंबर पर कॉल करके पुष्टि करने पर फ्रॉड का खुलासा होता है।"
        ),
        "narration_en": "Any change to a vendor's bank coordinates must require mandatory verbal verification using pre-registered contact details.",
        "narration_hi": "वेंडर के बैंक खाते में किसी भी बदलाव के लिए पुराने पंजीकृत फोन नंबर पर बात करके पुष्टि करना अनिवार्य होना चाहिए।",
        "transcript_en": "[00:00] Vendor email compromise. [00:25] The altered bank details notice. [00:45] The mandatory callback policy.",
        "transcript_hi": "[00:00] वेंडर के ईमेल में सेंध। [00:25] बैंक खाता बदलने की सूचना। [00:45] आधिकारिक फोन कॉल से सत्यापन।",
        "questions": [
            ("A recognized supplier emails requesting their payment be sent to a new bank account. The proper response is:",
             ["Update the account number in your payroll system immediately", "Call the supplier's verified accounting contact on an existing phone record to confirm", "Email them back asking for their credit card", "Ignore the bill entirely"],
             1, "Never update banking details without verbal confirmation via independently verified, pre-existing contact channels."),
        ],
    },
    {
        "module": "financial",
        "slug": "cryptocurrency-investment-schemes",
        "title_en": "Cryptocurrency & High-Yield Scams",
        "title_hi": "क्रिप्टोकरेंसी और भारी मुनाफे का धोखा",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Guaranteed 200% returns, fake trading dashboards, and romance investment traps (Pig Butchering).",
        "summary_hi": "200% गारंटीड रिटर्न, फर्जी ट्रेडिंग वेबसाइट और दोस्ती के बहाने निवेश के नाम पर होने वाली लूट।",
        "script_en": (
            "Walkthrough of a slick trading portal. The victim deposits $500. The fake dashboard shows their balance growing to $2,500! "
            "Excited, they deposit $10,000. When they try to withdraw, the platform demands a 20% 'tax fee'. They never get a single cent back."
        ),
        "script_hi": (
            "फर्जी ट्रेडिंग वेबसाइट का सच: पीड़ित ₹10,000 लगाता है। स्क्रीन पर उसका मुनाफा ₹50,000 दिखता है! "
            "उत्साह में वह ₹2 लाख और जमा करता है। जब पैसे निकालने की कोशिश करता है, तो 'टैक्स' के नाम पर और पैसे मांगे जाते हैं। "
            "एक भी रुपया वापस नहीं मिलता।"
        ),
        "narration_en": "If an investment promises guaranteed high returns with zero risk, it is mathematically a scam.",
        "narration_hi": "यदि कोई योजना बिना किसी जोखिम के भारी मुनाफे का वादा करे, तो वह सौ प्रतिशत धोखाधड़ी है।",
        "transcript_en": "[00:00] The fake trading simulator. [00:25] Fabricated profits on screen. [00:45] The withdrawal extortion trap.",
        "transcript_hi": "[00:00] फर्जी ट्रेडिंग का जाल। [00:25] स्क्रीन पर दिखाया गया नकली मुनाफा। [00:45] निकासी के नाम पर ब्लैकमेल।",
        "questions": [
            ("A new contact invites you to an exclusive crypto app promising guaranteed 15% daily profits. This is:",
             ["A revolutionary financial technology", "A fraudulent Ponzi/investment scam", "A government-backed program", "A normal stock market return"],
             1, "Guaranteed astronomical returns are the hallmark indicator of fraudulent investment scams."),
        ],
    },
    {
        "module": "financial",
        "slug": "lottery-refund-and-tax-rebate-fraud",
        "title_en": "Lottery, Refund & Tax Rebate Schemes",
        "title_hi": "लॉटरी, रिफंड और टैक्स छूट के बहाने ठगी",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Tax department impersonators offering refunds in exchange for entering bank account passwords.",
        "summary_hi": "आयकर विभाग के नाम पर रिफंड का झांसा देकर बैंक पासवर्ड और ओटीपी चुराने की साजिश से बचें।",
        "script_en": (
            "SMS: 'Income Tax Refund of ₹24,800 approved. Click to enter bank details for direct transfer.' "
            "The link leads to an exact replica of the national tax e-filing portal asking for net banking credentials."
        ),
        "script_hi": (
            "एसएमएस: 'आपका ₹24,800 का इनकम टैक्स रिफंड स्वीकृत हुआ। बैंक में पाने के लिए यहां क्लिक करें।' "
            "लिंक आयकर विभाग जैसी दिखने वाली फर्जी वेबसाइट पर ले जाता है जहां नेट बैंकिंग पासवर्ड मांगा जाता है।"
        ),
        "narration_en": "Government tax authorities credit refunds automatically to your pre-validated bank accounts. They never ask for your passwords via SMS.",
        "narration_hi": "आयकर विभाग रिफंड सीधे आपके पूर्व-सत्यापित बैंक खाते में भेजता है। वह कभी एसएमएस में पासवर्ड नहीं मांगता।",
        "transcript_en": "[00:00] The tax refund SMS. [00:20] Replica government portals. [00:45] Official government refund mechanisms.",
        "transcript_hi": "[00:00] टैक्स रिफंड का फर्जी एसएमएस। [00:20] सरकारी पोर्टल की नकल। [00:45] रिफंड पाने का असली आधिकारिक तरीका।",
        "questions": [
            ("How does the government Income Tax department process refunds?",
             ["By sending SMS links asking for net banking passwords", "Directly into verified bank accounts through official automated banking channels", "Via WhatsApp calls", "Through cryptocurrency"],
             1, "Tax authorities disburse refunds directly into pre-validated bank accounts without requesting login credentials via text links."),
        ],
    },

    # -------------------------------------------------------------------------
    # Module 5: voice (Lessons 21 - 25)
    # -------------------------------------------------------------------------
    {
        "module": "voice",
        "slug": "vishing-bank-manager-phone-call",
        "title_en": "Vishing: The Fake Bank Manager Call",
        "title_hi": "विशिंग: बैंक अधिकारी बनकर कॉल",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Voice phishing callers spoof official bank caller IDs and demand OTPs to 'stop unauthorized transactions'.",
        "summary_hi": "बैंक के नाम से आने वाली फर्जी कॉल और 'खाता ब्लॉक होने' का डर दिखाकर ओटीपी मांगने का तरीका।",
        "script_en": (
            "Audio playback of an aggressive caller: 'Hello, this is Cyber Cell Security Manager Sharma. "
            "An unauthorized transaction of ₹85,000 is taking place on your card right now. "
            "Read me the OTP sent to your phone within 30 seconds to block it!'"
        ),
        "script_hi": (
            "कॉल की रिकॉर्डिंग: 'नमस्ते, मैं बैंक का सुरक्षा प्रबंधक बोल रहा हूं। आपके कार्ड से अभी ₹85,000 कट रहे हैं। "
            "ट्रांजैक्शन रोकने के लिए फोन पर आया ओटीपी 30 सेकंड में मुझे बताएं!' "
            "दिखाएं कि ओटीपी देते ही पैसे कट जाते हैं।"
        ),
        "narration_en": "Bank employees can see transactions on their own systems. They never need your OTP to block a fraud.",
        "narration_hi": "बैंक के पास अपना सिस्टम होता है। किसी भी फ्रॉड को रोकने के लिए बैंक को आपके ओटीपी की जरूरत कभी नहीं होती।",
        "transcript_en": "[00:00] The panic phone call. [00:25] Why caller ID numbers can be easily spoofed. [00:45] Hanging up and dialing the official card helpline.",
        "transcript_hi": "[00:00] डराने वाली फोन कॉल। [00:25] कॉलर आईडी नंबर बदलने की तकनीक। [00:45] फोन काटकर कार्ड के पीछे लिखे नंबर पर कॉल करना।",
        "questions": [
            ("A caller claiming to be from your bank asks for the 6-digit OTP sent to your phone. You should:",
             ["Give it to them so they can stop the hacker", "Immediately refuse, hang up, and call the official bank number printed on your card", "Tell them your ATM PIN instead", "Put them on hold for an hour"],
             1, "No genuine bank employee will ever ask for your OTP or password over the phone."),
        ],
    },
    {
        "module": "voice",
        "slug": "ai-deepfake-voice-cloning",
        "title_en": "AI Deepfake Voice Cloning Attacks",
        "title_hi": "एआई वॉइस क्लोनिंग और फर्जी आवाज का जाल",
        "difficulty": "intermediate",
        "duration": 6,
        "summary_en": "With just 3 seconds of audio from Instagram or TikTok, AI can clone anyone's voice with pitch-perfect realism.",
        "summary_hi": "केवल 3 सेकंड की ऑडियो क्लिप से एआई किसी की भी हूबहू आवाज बना सकता है। जानिए इससे कैसे बचें।",
        "script_en": (
            "Audio demonstration: A 3-second Instagram reel of a daughter laughing. "
            "Next: The AI engine generates a synthetic voice clip crying: 'Mom, I was in a car crash, please send ₹50,000 to this clinic right now!'. "
            "Introduce the family safe-word defense."
        ),
        "script_hi": (
            "ऑडियो सिमुलेशन: इंस्टाग्राम वीडियो से 3 सेकंड की आवाज का नमूना। "
            "एआई उसी आवाज में रोते हुए बोलता है: 'मम्मी, मेरा एक्सीडेंट हो गया है, तुरंत इस अस्पताल के खाते में पैसे भेजो!' "
            "परिवार के लिए एक गुप्त 'सेफ-वर्ड' (सुरक्षा कोड) रखने का उपाय बताएं।"
        ),
        "narration_en": "In the era of AI voice cloning, voice is no longer biometric proof of identity. Establish a private family passphrase.",
        "narration_hi": "एआई के इस दौर में आवाज पहचान का अंतिम सबूत नहीं रह गई है। परिवार के साथ एक गुप्त कोड तय करके रखें।",
        "transcript_en": "[00:00] How voice cloning models work. [00:25] The distressed relative scenario. [00:50] The family verbal password safeguard.",
        "transcript_hi": "[00:00] वॉइस क्लोनिंग कैसे काम करती है। [00:25] संकट में परिजन का नाटक। [00:50] पारिवारिक सीक्रेट पासवर्ड का नियम।",
        "questions": [
            ("What is an effective non-technical safeguard against AI voice-cloning family emergency scams?",
             ["Agreeing on a secret family safety word in advance that only genuine family members know", "Listening carefully for robotic static", "Refusing to ever speak to family on the phone", "Only using landlines"],
             1, "A pre-established secret family passphrase disarms even the most convincing AI voice replicas."),
        ],
    },
    {
        "module": "voice",
        "slug": "tech-support-call-center-scams",
        "title_en": "Tech Support Call Center Scams",
        "title_hi": "फर्जी तकनीकी सहायता और स्क्रीन शेयरिंग कॉल",
        "difficulty": "beginner",
        "duration": 6,
        "summary_en": "Bogus computer pop-ups that tell you to call a toll-free number and install remote access tools (AnyDesk/TeamViewer).",
        "summary_hi": "कंप्यूटर में वायरस का फर्जी सायरन बजाकर एनीडेस्क या टीमव्यूअर डाउनलोड कराने वाले ठगों की पहचान।",
        "script_en": (
            "A browser locks up with flashing red text: 'VIRUS DETECTED! Call Microsoft Support at 1-800-XXX'. "
            "The technician instructs the user to download AnyDesk. Once granted access, the scammer opens cmd, types 'tree', "
            "claims it is trojan activity, and drains online banking while the screen is blacked out."
        ),
        "script_hi": (
            "कंप्यूटर पर तेज सायरन और लाल चेतावनी: 'माइक्रोसॉफ्ट सपोर्ट को कॉल करें'। "
            "फोन पर फर्जी इंजीनियर एनीडेस्क डाउनलोड कराता है। "
            "स्क्रीन पर फर्जी कमांड चलाकर डराता है और नेट बैंकिंग से पैसे साफ कर देता है।"
        ),
        "narration_en": "Microsoft, Apple, and Google will never freeze your browser and ask you to call a telephone hotline for virus removal.",
        "narration_hi": "माइक्रोसॉफ्ट या एप्पल कभी भी स्क्रीन पर सायरन बजाकर फोन नंबर पर कॉल करने को नहीं कहते।",
        "transcript_en": "[00:00] The full-screen pop-up trick. [00:20] How remote desktop tools give full control. [00:45] Pressing Esc or terminating the browser.",
        "transcript_hi": "[00:00] फुल स्क्रीन पॉप-अप का धोखा। [00:20] रिमोट सॉफ्टवेयर का खतरा। [00:45] ब्राउज़र बंद करने का सही तरीका।",
        "questions": [
            ("A loud siren sounds and your web browser locks with a message saying 'Microsoft detected 5 viruses, call this number'. You should:",
             ["Call the number immediately", "Force close the browser using Task Manager (or Alt+F4) and run legitimate built-in antivirus", "Install AnyDesk as requested", "Send credit card details"],
             1, "Browser alert pop-ups are fake scareware; force-closing the browser safely dismisses them."),
        ],
    },
    {
        "module": "voice",
        "slug": "police-and-customs-digital-arrest-fraud",
        "title_en": "Digital Arrest & Law Enforcement Pretext",
        "title_hi": "डिजिटल अरेस्ट और पुलिस के नाम पर ब्लैकमेल",
        "difficulty": "intermediate",
        "duration": 6,
        "summary_en": "Scammers wear police uniforms on video calls and claim your Aadhaar was used for illegal contraband.",
        "summary_hi": "वर्दी पहनकर वीडियो कॉल करने वाले और 'डिजिटल अरेस्ट' की धमकी देकर पैसे ऐंठने वाले गिरोह का पर्दाफाश।",
        "script_en": (
            "Victim receives a Skype call. A man in a fake police station background with national emblems says: "
            "'A courier package containing illegal drugs was booked with your identity. You are under Digital Arrest. "
            "Transfer all your savings to the RBI verification escrow account or a patrol car will arrive at your home.'\n"
            "Clarify: There is legally no concept of 'Digital Arrest' under Indian law."
        ),
        "script_hi": (
            "स्काइप कॉल पर पुलिस की वर्दी पहने व्यक्ति: 'आपके आधार कार्ड से ड्रग्स का पार्सल पकड़ा गया है। आप डिजिटल अरेस्ट हैं। "
            "जांच के लिए अपने सारे पैसे सरकारी खाते में ट्रांसफर करें वर्ना पुलिस घर आ जाएगी।'\n"
            "स्पष्ट सीख: भारतीय कानून में 'डिजिटल अरेस्ट' नाम की कोई कानूनी व्यवस्था नहीं है।"
        ),
        "narration_en": "Real law enforcement agencies never conduct arrests or investigations via Skype, WhatsApp, or video calls.",
        "narration_hi": "असली पुलिस या जांच एजेंसियां कभी भी व्हाट्सएप या वीडियो कॉल पर गिरफ्तारी या जांच नहीं करतीं।",
        "transcript_en": "[00:00] The fake police station backdrop. [00:25] The myth of 'Digital Arrest'. [00:50] Dialing 1930 / cybercrime.gov.in immediately.",
        "transcript_hi": "[00:00] फर्जी थाने का सेटअप। [00:25] 'डिजिटल अरेस्ट' का सच। [00:50] तुरंत 1930 हेल्पलाइन पर शिकायत दर्ज करना।",
        "questions": [
            ("Does any legitimate law enforcement or judicial agency have the authority to place citizens under 'Digital Arrest' via video call?",
             ["Yes, in international cases", "No, 'Digital Arrest' is a fraudulent extortion scam with zero legal validity", "Only the CBI can do it", "Yes, on WhatsApp"],
             1, "Legitimate law enforcement never conducts arrests, interrogations, or asset seizures over video calls."),
        ],
    },
    {
        "module": "voice",
        "slug": "robocalls-and-caller-id-spoofing",
        "title_en": "Robocalls & Caller ID Spoofing",
        "title_hi": "कॉलर आईडी स्पूफिंग और फर्जी नंबर",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Understand VoIP protocols that allow anyone to display any telephone number on your phone screen.",
        "summary_hi": "जानिए कैसे वीओआईपी तकनीक से ठग आपके फोन स्क्रीन पर किसी भी बैंक या पुलिस का असली नंबर दिखा सकते हैं।",
        "script_en": (
            "Diagram of VoIP PBX: Show how entering a phone number into an open SIP trunk allows an attacker in another country "
            "to make your phone display 'State Bank Official Helpline 1800-XXXX'. "
            "Demonstrate why caller ID cannot be trusted as identity proof."
        ),
        "script_hi": (
            "वीओआईपी तकनीक का प्रदर्शन: कैसे एक साधारण सॉफ्टवेयर के जरिए फोन स्क्रीन पर किसी भी संस्था का नाम और नंबर दिखाया जा सकता है। "
            "समझाएं कि कॉलर आईडी स्क्रीन देखकर कॉलर पर कभी भरोसा न करें।"
        ),
        "narration_en": "Just because your phone screen displays your bank's real telephone number does not mean they are calling you.",
        "narration_hi": "स्क्रीन पर बैंक का आधिकारिक नंबर दिख रहा हो, तब भी यह जरूरी नहीं कि कॉल वास्तव में बैंक से ही आई हो।",
        "transcript_en": "[00:00] The mechanics of caller ID spoofing. [00:20] Inbound vs outbound call trust. [00:45] The hang-up and callback rule.",
        "transcript_hi": "[00:00] कॉलर आईडी स्पूफिंग की तकनीक। [00:20] इनकमिंग कॉल पर अविश्वास। [00:45] फोन काटकर खुद डायल करने का नियम।",
        "questions": [
            ("Can telephone caller ID numbers be faked or spoofed by criminals?",
             ["No, phone networks strictly prevent spoofing", "Yes, VoIP technology makes it easy to broadcast any fake caller ID number", "Only during thunderstorms", "Only outside business hours"],
             1, "Caller ID spoofing is widespread; incoming numbers should never be taken as proof of identity."),
        ],
    },

    # -------------------------------------------------------------------------
    # Module 6: physical (Lessons 26 - 30)
    # -------------------------------------------------------------------------
    {
        "module": "physical",
        "slug": "tailgating-and-badge-cloning",
        "title_en": "Tailgating & Badge Cloning at the Door",
        "title_hi": "बिना पास के पीछे घुसना और फर्जी आईकार्ड",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Why holding the secure door open for someone with coffee or a ladder compromises the whole building.",
        "summary_hi": "हाथ में सामान लिए अनजान व्यक्ति के लिए सुरक्षित दरवाजा पकड़ने का खतरा और सही सुरक्षा नियम।",
        "script_en": (
            "Video demonstration: An employee scans their RFID badge at a turnstile. A stranger carrying coffee cups smiles: 'Could you hold it? "
            "My badge is in my backpack!' Explain how courtesy overrides physical access control."
        ),
        "script_hi": (
            "दफ्तर का दृश्य: कर्मचारी अपना कार्ड पंच करता है। पीछे खड़ा अनजान व्यक्ति कहता है: 'कृपया दरवाजा पकड़ लीजिए, मेरा कार्ड बैग में है!' "
            "समझाएं कि कैसे विनम्रता के चक्कर में सुरक्षा नियम टूट जाते हैं।"
        ),
        "narration_en": "Politeness cannot replace physical security. Every person must scan their own badge — no exceptions.",
        "narration_hi": "विनम्रता सुरक्षा नियमों का विकल्प नहीं हो सकती। हर व्यक्ति को अपना कार्ड खुद पंच करना चाहिए।",
        "transcript_en": "[00:00] The tailgating scenario. [00:20] The polite security response. [00:45] Visitor badge sign-in protocols.",
        "transcript_hi": "[00:00] बिना कार्ड प्रवेश का उदाहरण। [00:20] विनम्रता से मना करने का तरीका। [00:45] आगंतुकों के लिए रिसेप्शन का नियम।",
        "questions": [
            ("What is the polite and correct response if an unfamiliar person asks you to hold a badge-access door open?",
             ["Hold the door and smile", "Direct them politely to the reception desk to badge in or receive a visitor pass", "Give them your badge to swipe", "Protest loudly"],
             1, "Politely directing individuals to badge in or check in at the reception desk maintains physical perimeter security."),
        ],
    },
    {
        "module": "physical",
        "slug": "the-malicious-usb-drop",
        "title_en": "The Malicious USB Drop in the Parking Lot",
        "title_hi": "पार्किंग में गिरी अनजान पेनड्राइव का खतरा",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Plugging in a found flash drive labeled 'Confidential Salaries' executes a Rubber Ducky keystroke injection attack.",
        "summary_hi": "सड़क पर गिरी 'गोपनीय वेतन' लिखी पेनड्राइव को लैपटॉप में लगाने से होने वाले हैकिंग हमले से बचें।",
        "script_en": (
            "An employee finds a clean USB flash drive on the sidewalk labeled 'Executive Bonuses 2026'. "
            "Curiosity takes over. They plug it into their office workstation. "
            "Within 1.5 seconds, the USB device mimics a high-speed keyboard, opens PowerShell, and downloads an implant."
        ),
        "script_hi": (
            "पार्किंग में गिरी पेनड्राइव जिस पर लिखा है 'अधिकारियों का बोनस 2026'। "
            "जिज्ञासावश कर्मचारी उसे लैपटॉप में लगा देता है। "
            "डेढ़ सेकंड के अंदर वह पेनड्राइव कीबोर्ड बनकर कंप्यूटर की सुरक्षा को तोड़ देती है।"
        ),
        "narration_en": "Never plug an unknown USB device into your computer. Curiosity is an attacker's favorite delivery vehicle.",
        "narration_hi": "किसी भी अनजान पेनड्राइव को कभी कंप्यूटर में न लगाएं। कौतूहल ही हमलावर का सबसे बड़ा हथियार है।",
        "transcript_en": "[00:00] The parking lot bait. [00:20] How BadUSB / Rubber Ducky attacks work. [00:45] Submitting found media to IT.",
        "transcript_hi": "[00:00] पार्किंग में फेंका गया जाल। [00:20] बैड-यूएसबी कैसे काम करती है। [00:45] मिली हुई ड्राइव को आईटी में जमा करना।",
        "questions": [
            ("You find a USB thumb drive in your company's cafeteria labeled 'Confidential Payroll'. You should:",
             ["Plug it in to see who owns it", "Hand it over directly to your IT/Security department without plugging it in", "Take it home for personal use", "Format it on your phone"],
             1, "Never connect untrusted media; deliver found hardware directly to IT security teams for safe inspection."),
        ],
    },
    {
        "module": "physical",
        "slug": "shoulder-surfing-in-public-cafes",
        "title_en": "Shoulder Surfing in Cafes & Metros",
        "title_hi": "कैफे और मेट्रो में स्क्रीन पर ताक-झांक",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Protecting confidential screens and PIN entry from wandering eyes and overhead surveillance cameras.",
        "summary_hi": "सार्वजनिक स्थानों पर लैपटॉप स्क्रीन और एटीएम पिन को ताक-झांक और कैमरों से सुरक्षित रखना।",
        "script_en": (
            "Scene: An employee working on a sensitive client merger at a coffee shop. "
            "A person at the adjacent table records the screen with a smartphone telephoto lens. "
            "Demonstrate how privacy filters (polarizing screen guards) block side-angle viewing."
        ),
        "script_hi": (
            "कैफे में लैपटॉप पर काम करता कर्मचारी। पास की मेज पर बैठा व्यक्ति मोबाइल से गोपनीय दस्तावेज रिकॉर्ड कर रहा है। "
            "दिखाएं कि प्राइवेसी स्क्रीन गार्ड लगाने से अगल-बगल से स्क्रीन बिल्कुल काली दिखाई देती है।"
        ),
        "narration_en": "When working in public, assume someone can see your screen. Use privacy filters and sit with your back to the wall.",
        "narration_hi": "सार्वजनिक स्थानों पर काम करते समय प्राइवेसी फिल्टर का उपयोग करें और दीवार की तरफ पीठ करके बैठें।",
        "transcript_en": "[00:00] The crowded cafe scenario. [00:20] Privacy screen filters in action. [00:40] Shielding keyboards when entering passwords.",
        "transcript_hi": "[00:00] भीड़भाड़ वाले स्थान। [00:20] प्राइवेसी फिल्टर का महत्व। [00:40] पासवर्ड डालते समय हाथ से ढंकना।",
        "questions": [
            ("What is an effective way to prevent shoulder surfing while working on a laptop in public?",
             ["Increase screen brightness to 100%", "Attach a polarized privacy filter screen and position your back toward a wall", "Work in a dark room", "Turn off Wi-Fi"],
             1, "Privacy filters restrict the viewing angle to directly in front of the screen, obscuring visibility from the sides."),
        ],
    },
    {
        "module": "physical",
        "slug": "fake-courier-and-service-technicians",
        "title_en": "Fake Couriers & Maintenance Impostors",
        "title_hi": "नकली डिलीवरी बॉय और सर्विस एजेंट",
        "difficulty": "intermediate",
        "duration": 6,
        "summary_en": "Intruders wearing high-vis vests and carrying clipboards walking unchallenged past front desks.",
        "summary_hi": "वर्दी और टूलबॉक्स लेकर दफ्तर में घुसने वाले और सर्वर रूम तक पहुंचने वाले फर्जी टेक्नीशियन से बचाव।",
        "script_en": (
            "An intruder dressed as an AC repairman enters an office: 'I am here for the server room fan replacement'. "
            "Because he carries tools and a fake work order, the floor manager waves him through without checking with facilities."
        ),
        "script_hi": (
            "एसी मैकेनिक की वर्दी में हमलावर दफ्तर में आता है: 'सर्वर रूम का एसी ठीक करने आया हूं'। "
            "फर्जी लेटर देखकर कर्मचारी उसे बिना पूछे सर्वर रूम में भेज देता है।"
        ),
        "narration_en": "A uniform and a confident smile are not security credentials. Verify all unexpected maintenance with facility management.",
        "narration_hi": "वर्दी या आत्मविश्वास पहचान का प्रमाण नहीं हैं। किसी भी सर्विस विजिट की पुष्टि मैनेजमेंट से जरूर करें।",
        "transcript_en": "[00:00] The maintenance worker pretext. [00:25] Escort policies for sensitive areas. [00:50] The vendor sign-in log.",
        "transcript_hi": "[00:00] सर्विस एजेंट का बहाना। [00:25] संवेदनशील कमरों में साथ रहने का नियम। [00:50] वेंडर रजिस्टर में एंट्री।",
        "questions": [
            ("An unexpected technician arrives to repair the network closet. Your first action should be:",
             ["Unlock the closet and leave them alone", "Verify their appointment with your internal facilities or IT team before granting access", "Ask for a selfie", "Help them carry cables"],
             1, "Unscheduled contractors must be confirmed with responsible internal coordinators before accessing sensitive infrastructure."),
        ],
    },
    {
        "module": "physical",
        "slug": "clean-desk-and-whiteboard-data-leakage",
        "title_en": "Clean Desk Policy & Whiteboard Exposure",
        "title_hi": "मेज और व्हाइटबोर्ड पर गोपनीय जानकारी छोड़ना",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Sticky notes with passwords, printed employee rosters, and sensitive architecture diagrams left on conference whiteboards.",
        "summary_hi": "मॉनिटर पर चिपकी पासवर्ड पर्चियां और मीटिंग रूम के बोर्ड पर लिखी गोपनीय जानकारी मिटाने की महत्ता।",
        "script_en": (
            "Office night inspection: The camera pans across monitors with yellow post-it notes: 'Pass@2026'. "
            "A conference room whiteboard has complete network IP ranges and database passwords from the afternoon brainstorm."
        ),
        "script_hi": (
            "रात में दफ्तर का दृश्य: कंप्यूटर स्क्रीन पर चिपकी पर्ची जिस पर पासवर्ड लिखा है। "
            "मीटिंग रूम के बोर्ड पर पूरे सर्वर का नक्शा और पासवर्ड लिखा छूटा हुआ है।"
        ),
        "narration_en": "Lock your screen every time you step away (Win+L). Wipe whiteboards and file confidential documents before leaving.",
        "narration_hi": "सीट से उठते ही स्क्रीन लॉक करें (Win+L)। मीटिंग के बाद व्हाइटबोर्ड साफ करें और जरूरी कागजात अलमारी में रखें।",
        "transcript_en": "[00:00] The post-it note risk. [00:20] The Win+L habit. [00:40] Clean whiteboard discipline.",
        "transcript_hi": "[00:00] पासवर्ड पर्चियों का खतरा। [00:20] Win+L से स्क्रीन लॉक की आदत। [00:40] बोर्ड साफ करने का नियम।",
        "questions": [
            ("What is the quickest keyboard shortcut to lock a Windows computer when stepping away from your desk?",
             ["Ctrl + C", "Windows Key + L", "Alt + F4", "Ctrl + Alt + Del"],
             1, "Pressing Win+L instantly locks your session, preventing unauthorized physical access to your workstation."),
        ],
    },

    # -------------------------------------------------------------------------
    # Module 7: workplace (Lessons 31 - 35)
    # -------------------------------------------------------------------------
    {
        "module": "workplace",
        "slug": "password-hygiene-and-passphrase-defense",
        "title_en": "Password Hygiene & Passphrase Defense",
        "title_hi": "मजबूत पासवर्ड और सुरक्षा नियम",
        "difficulty": "beginner",
        "duration": 6,
        "summary_en": "Why 4 random dictionary words ('correct-horse-battery-staple') defeat brute-force supercomputers better than 'P@ssw0rd!'.",
        "summary_hi": "जानिए क्यों चार याद रहने वाले शब्दों का संयोजन जटिल पासवर्ड से कहीं अधिक सुरक्षित और मजबूत होता है।",
        "script_en": (
            "Password cracker simulation: 'Welcome123!' cracks in 0.4 seconds. "
            "'P@ssw0rd2026' cracks in 3 minutes. "
            "'mango-bicycle-thunder-window' takes 4 million years to crack."
        ),
        "script_hi": (
            "पासवर्ड क्रैकिंग सिमुलेशन: 'Welcome123!' आधा सेकंड में क्रैक हो जाता है। "
            "'mango-bicycle-thunder-window' जैसे 4 आसान शब्दों को क्रैक करने में लाखों साल लगेंगे।"
        ),
        "narration_en": "Length beats complexity. Use long passphrases and a dedicated password manager so you never reuse passwords across accounts.",
        "narration_hi": "लंबाई जटिलता से बेहतर सुरक्षा देती है। लंबे पासफ्रेज और पासवर्ड मैनेजर का इस्तेमाल करें ताकि पासवर्ड दोहराना न पड़े।",
        "transcript_en": "[00:00] Brute force speeds today. [00:25] The passphrase advantage. [00:50] The role of password managers.",
        "transcript_hi": "[00:00] पासवर्ड क्रैकिंग की गति। [00:25] पासफ्रेज के फायदे। [00:50] पासवर्ड मैनेजर का उपयोग।",
        "questions": [
            ("Which password strategy offers the greatest resistance to modern brute-force cracking?",
             ["A 7-character word with one number", "A long multi-word passphrase of 16+ characters", "Your dog's name backwards", "The same strong password on all accounts"],
             1, "Length is the primary exponential factor in cryptographic entropy against brute-force attacks."),
        ],
    },
    {
        "module": "workplace",
        "slug": "multi-factor-authentication-fatigue",
        "title_en": "MFA Prompt Bombing & Fatigue Attacks",
        "title_hi": "एमएफए प्रॉम्प्ट बॉम्बिंग और थकावट हमला",
        "difficulty": "intermediate",
        "duration": 6,
        "summary_en": "How attackers flood your phone with 50 push notifications at 3:00 AM until you tap 'Approve' to stop the buzzing.",
        "summary_hi": "आधी रात को बार-बार एमएफए नोटिफिकेशन भेजकर परेशान करने और गलती से 'स्वीकार' कराने की चाल से सावधान रहें।",
        "script_en": (
            "Phone screen buzzing repeatedly at 3:15 AM: 'Are you trying to sign in to Okta? [Approve] [Deny]'. "
            "Notification 1, Notification 2... Notification 47. "
            "Show the correct defense: Tap 'Deny', select 'This wasn't me', and immediately change your primary account password."
        ),
        "script_hi": (
            "रात 3:15 बजे फोन लगातार बजता है: 'क्या आप लॉगिन कर रहे हैं? [स्वीकार] [अस्वीकार]'। "
            "40 बार लगातार नोटिफिकेशन आता है। "
            "सही कदम: 'अस्वीकार' दबाएं, 'यह मैं नहीं हूं' चुनें और तुरंत अपना मुख्य पासवर्ड बदलें।"
        ),
        "narration_en": "If you receive an MFA push request when you are not actively logging in, your password has been stolen. Deny and report immediately.",
        "narration_hi": "यदि आपके लॉगिन किए बिना एमएफए का नोटिफिकेशन आए, तो समझें पासवर्ड चोरी हो चुका है। तुरंत मना करें और रिपोर्ट करें।",
        "transcript_en": "[00:00] The prompt bombing scenario. [00:25] Why attackers rely on frustration. [00:50] Number matching MFA defenses.",
        "transcript_hi": "[00:00] बार-बार नोटिफिकेशन का हमला। [00:25] झुंझलाहट का फायदा उठाना। [00:50] नंबर मिलान वाले सुरक्षित एमएफए।",
        "questions": [
            ("You wake up to dozens of login approval pushes on your authenticator app that you didn't initiate. What should you do?",
             ["Approve one so the notifications stop", "Deny the prompt, mark it as fraudulent, and change your password immediately", "Turn off your phone and go back to sleep", "Delete the app"],
             1, "Spam prompts indicate your credentials are compromised; deny the attempt and change your password right away."),
        ],
    },
    {
        "module": "workplace",
        "slug": "byod-and-unsecured-mobile-devices",
        "title_en": "BYOD & Mobile Device Security",
        "title_hi": "निजी मोबाइल और लैपटॉप पर कार्यालय सुरक्षा",
        "difficulty": "intermediate",
        "duration": 6,
        "summary_en": "Managing risks when personal devices access corporate Slack, Google Workspace, and proprietary repositories.",
        "summary_hi": "निजी फोन या लैपटॉप से दफ्तर का काम करते समय डेटा सुरक्षा और डिवाइस एनक्रिप्शन के नियम।",
        "script_en": (
            "A personal tablet left in a taxi has direct access to corporate customer databases. "
            "Demonstrate the essential safeguards: device encryption (BitLocker/FileVault), remote wipe capability, and biometric locks."
        ),
        "script_hi": (
            "टैक्सी में छूटे निजी टैबलेट से कंपनी के ग्राहक डेटा तक सीधी पहुंच। "
            "जरूरी सुरक्षा उपाय: डिवाइस एन्क्रिप्शन, रिमोट वाइप की सुविधा और फिंगरप्रिंट लॉक लगाना।"
        ),
        "narration_en": "Convenience cannot come at the cost of encryption. If you process corporate data on a personal device, secure it like a corporate asset.",
        "narration_hi": "सुविधा के लिए सुरक्षा से समझौता न करें। निजी डिवाइस पर दफ्तर का डेटा हो तो उसे भी मजबूत सुरक्षा में रखें।",
        "transcript_en": "[00:00] The lost tablet risk. [00:25] Full-disk encryption. [00:50] Corporate profiles and segregation.",
        "transcript_hi": "[00:00] खोए डिवाइस का जोखिम। [00:25] फुल-डिस्क एन्क्रिप्शन। [00:50] व्यक्तिगत और आधिकारिक डेटा का विभाजन।",
        "questions": [
            ("What is the primary risk of using an unencrypted personal phone for corporate email and chats?",
             ["The phone battery drains faster", "If the device is lost or stolen, company data can be extracted directly without entering passwords", "Apps become slower", "The camera stops working"],
             1, "Unencrypted mobile storage allows unauthorized parties to extract raw data if the physical device is misplaced."),
        ],
    },
    {
        "module": "workplace",
        "slug": "safe-handling-of-confidential-data",
        "title_en": "Safe Handling of Confidential Customer Data",
        "title_hi": "गोपनीय ग्राहक डेटा का सुरक्षित प्रबंधन",
        "difficulty": "intermediate",
        "duration": 5,
        "summary_en": "Data classification: Public, Internal, Confidential, and Restricted. Preventing accidental leaks via email and cloud shares.",
        "summary_hi": "डेटा का वर्गीकरण और ग्राहक की निजी जानकारी (आधार, पैन, कार्ड) को गलती से लीक होने से बचाना।",
        "script_en": (
            "An employee exports 10,000 customer records to Excel to fix a bug and emails it to their personal Gmail. "
            "Explain how this breaches data privacy laws (DPDP Act/GDPR) and risks massive regulatory liabilities."
        ),
        "script_hi": (
            "कर्मचारी काम आसान करने के लिए 10,000 ग्राहकों का डेटा पर्सनल ईमेल पर भेज लेता है। "
            "समझाएं कि यह डेटा प्रोटेक्शन कानून का गंभीर उल्लंघन है और इससे कंपनी पर भारी जुर्माना लग सकता है।"
        ),
        "narration_en": "Customer data belongs to customers. Never exfiltrate internal records to personal mailboxes or unapproved cloud drives.",
        "narration_hi": "ग्राहकों का डेटा उनकी अमानत है। इसे कभी भी पर्सनल ईमेल या अनाधिकृत क्लाउड ड्राइव पर न भेजें।",
        "transcript_en": "[00:00] The innocent shortcut mistake. [00:25] Data privacy regulations. [00:45] Secure authorized processing.",
        "transcript_hi": "[00:00] शॉर्टकट अपनाने की गलती। [00:25] डेटा सुरक्षा कानून के नियम। [00:45] अधिकृत टूल्स से सुरक्षित काम।",
        "questions": [
            ("Is it permissible to email a customer database spreadsheet to your personal email to finish work from home?",
             ["Yes, as long as you delete it later", "No, exfiltrating customer PII to personal accounts violates security policy and data privacy laws", "Only on weekends", "Yes, if the file is zipped"],
             1, "Transmitting protected customer information to personal accounts circumvents enterprise security monitoring and breaks privacy laws."),
        ],
    },
    {
        "module": "workplace",
        "slug": "shadow-it-and-unapproved-ai-tools",
        "title_en": "Shadow IT & Unapproved Generative AI",
        "title_hi": "बिना अनुमति के क्लाउड और एआई टूल्स का उपयोग",
        "difficulty": "intermediate",
        "duration": 6,
        "summary_en": "Pasting proprietary source code, patient records, or financial models into public generative AI chatbots.",
        "summary_hi": "कंपनी का गोपनीय कोड या वित्तीय डेटा पब्लिक एआई चैटबॉट्स में पेस्ट करने के गंभीर खतरे।",
        "script_en": (
            "A developer pastes proprietary trade secret algorithms into a free online AI code optimizer. "
            "Show how that data can be incorporated into public training datasets and resurface in responses to competitors."
        ),
        "script_hi": (
            "डेवलपर कंपनी का गोपनीय कोड मुफ्त ऑनलाइन एआई टूल में पेस्ट कर देता है। "
            "समझाएं कि वह डेटा एआई के ट्रेनिंग मॉडल में चला जाता है और प्रतिस्पर्धियों के सामने लीक हो सकता है।"
        ),
        "narration_en": "Public AI tools learn from what you feed them. Only use enterprise-approved AI instances that contractually guarantee zero data retention.",
        "narration_hi": "सार्वजनिक एआई टूल्स आपके इनपुट से सीखते हैं। केवल उन्हीं एंटरप्राइज टूल्स का उपयोग करें जो डेटा सुरक्षित रखने की गारंटी देते हैं।",
        "transcript_en": "[00:00] The convenience of public AI. [00:25] How training pipelines retain data. [00:50] Enterprise AI safeguards.",
        "transcript_hi": "[00:00] एआई टूल्स की सुविधा। [00:25] डेटा स्टोर होने का खतरा। [00:50] सुरक्षित एंटरप्राइज एआई का चुनाव।",
        "questions": [
            ("What is the primary cybersecurity risk of pasting unredacted company financial reports into a public AI chatbot?",
             ["It uses up your computer memory", "The confidential data may be retained and used for future model training, leaking trade secrets", "The chatbot will reject the text", "It changes font styles"],
             1, "Public consumer AI services often retain user prompts for continuous model training, risking intellectual property leakage."),
        ],
    },

    # -------------------------------------------------------------------------
    # Module 8: personal (Lessons 36 - 40)
    # -------------------------------------------------------------------------
    {
        "module": "personal",
        "slug": "home-router-and-iot-device-hardening",
        "title_en": "Home Wi-Fi Router & Smart Device Security",
        "title_hi": "घर का वाई-फाई और स्मार्ट डिवाइस सुरक्षा",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Change the default 'admin/admin' credentials on your home router and isolate smart TVs on a guest network.",
        "summary_hi": "अपने घर के राउटर का डिफॉल्ट पासवर्ड बदलना और स्मार्ट टीवी को गेस्ट नेटवर्क पर अलग रखना।",
        "script_en": (
            "A hacker scans IP ranges looking for home routers with factory default passwords 'admin / admin'. "
            "Once inside, they alter the DNS settings so every device in the home is redirected to phishing portals."
        ),
        "script_hi": (
            "हैकर घर के राउटर पर डिफॉल्ट पासवर्ड 'admin/admin' का उपयोग करके कब्जा कर लेता है। "
            "वह डीएनएस सेटिंग्स बदल देता है जिससे घर का हर फोन अपने आप फर्जी वेबसाइटों पर रीडायरेक्ट होने लगता है।"
        ),
        "narration_en": "Your home router is the front door to your digital life. Change the admin password and enable automatic firmware updates.",
        "narration_hi": "घर का राउटर आपकी डिजिटल जिंदगी का मुख्य द्वार है। उसका एडमिन पासवर्ड बदलें और फर्मवेयर अपडेट रखें।",
        "transcript_en": "[00:00] The default credentials vulnerability. [00:25] Segregating IoT devices on a guest Wi-Fi. [00:45] Updating router firmware.",
        "transcript_hi": "[00:00] डिफॉल्ट पासवर्ड की कमजोरी। [00:25] स्मार्ट टीवी के लिए गेस्ट वाई-फाई। [00:45] राउटर अपडेट करने का तरीका।",
        "questions": [
            ("Why is leaving the default administrative password on your home Wi-Fi router hazardous?",
             ["It slows down your download speed", "Attackers can easily log in, hijack your DNS settings, and monitor all connected household traffic", "It voids the warranty", "The router turns off automatically"],
             1, "Factory default credentials allow remote or local attackers to reconfigure the router and reroute traffic to malicious servers."),
        ],
    },
    {
        "module": "personal",
        "slug": "evil-twin-and-public-wifi-dangers",
        "title_en": "Evil Twin Wi-Fi & Public Hotspot Risks",
        "title_hi": "सार्वजनिक वाई-फाई और फर्जी हॉटस्पॉट का खतरा",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Rogue access points at airports named 'Free_Airport_WiFi' that intercept unencrypted browsing traffic.",
        "summary_hi": "हवाई अड्डों और स्टेशनों पर 'Free Wi-Fi' नाम से बनाए गए फर्जी नेटवर्क और डेटा चोरी से बचाव।",
        "script_en": (
            "Airport scene: A hacker powers on a small portable Wi-Fi device named 'Airport_Free_HighSpeed'. "
            "Travelers connect without thinking. The hacker runs a man-in-the-middle tool capturing session cookies and login tokens."
        ),
        "script_hi": (
            "हवाई अड्डे पर हैकर अपना छोटा वाई-फाई हॉटस्पॉट शुरू करता है जिसका नाम रखता है 'Airport_Free_WiFi'। "
            "लोग बिना सोचे कनेक्ट करते हैं और हैकर उनके फोन का सारा इंटरनेट डेटा मॉनिटर करने लगता है।"
        ),
        "narration_en": "Public Wi-Fi is like a public swimming pool — everyone can see what you bring into it. Use a trustworthy VPN or mobile hotspot.",
        "narration_hi": "सार्वजनिक वाई-फाई में आपकी प्राइवेसी खुली होती है। संवेदनशील काम के लिए हमेशा वीपीएन या फोन के मोबाइल डेटा का उपयोग करें।",
        "transcript_en": "[00:00] The rogue access point. [00:20] Man-in-the-middle interception. [00:45] Why VPNs encrypt the tunnel.",
        "transcript_hi": "[00:00] फर्जी वाई-फाई हॉटस्पॉट। [00:20] बीच में डेटा की चोरी। [00:45] वीपीएन से डेटा सुरक्षित करना।",
        "questions": [
            ("When connecting to an open public Wi-Fi network at an airport or coffee shop, what is the best security practice?",
             ["Disable your firewall", "Use a reputable Virtual Private Network (VPN) and avoid conducting banking or typing passwords", "Turn on file sharing", "Clear your browser cache"],
             1, "VPNs establish an encrypted tunnel that shields your network traffic from interception on untrusted public networks."),
        ],
    },
    {
        "module": "personal",
        "slug": "identity-theft-and-credit-monitoring",
        "title_en": "Identity Theft & Personal Data Exposure",
        "title_hi": "पहचान की चोरी और आधार/पैन कार्ड सुरक्षा",
        "difficulty": "intermediate",
        "duration": 6,
        "summary_en": "Masked Aadhaar cards, credit report monitoring, and locking biometric credentials against unauthorized loans.",
        "summary_hi": "मास्क्ड आधार का उपयोग, क्रेडिट स्कोर की नियमित जांच और यूआईडीएआई पोर्टल पर बायोमेट्रिक्स लॉक करना।",
        "script_en": (
            "A victim discovers someone took a ₹5,00,000 personal loan in their name using a photocopied PAN and Aadhaar card. "
            "Step-by-step tutorial: How to lock your biometric data via the mAadhaar app and generate virtual IDs."
        ),
        "script_hi": (
            "पीड़ित को पता चलता है कि उसके आधार और पैन कार्ड की फोटोकॉपी से किसी ने ₹5 लाख का फर्जी लोन ले लिया। "
            "सुरक्षा समाधान: एम-आधार ऐप से बायोमेट्रिक्स को लॉक करना और हमेशा मास्क्ड आधार शेयर करना।"
        ),
        "narration_en": "Never share full photocopies of identity cards without purpose-specific cross-marking and watermarking.",
        "narration_hi": "पहचान पत्र की फोटोकॉपी पर हमेशा इस्तेमाल का कारण और तारीख लिखकर क्रॉस करें ताकि उसका दुरुपयोग न हो सके।",
        "transcript_en": "[00:00] Identity fraud discovery. [00:25] Masked Aadhaar explained. [00:50] Locking biometrics via UIDAI.",
        "transcript_hi": "[00:00] फर्जी लोन की समस्या। [00:25] मास्क्ड आधार क्या है। [00:50] आधार बायोमेट्रिक्स लॉक करने का तरीका।",
        "questions": [
            ("What feature provided by UIDAI prevents unauthorized financial authentication against your Aadhaar card?",
             ["Changing your phone wallpaper", "Biometric Lock feature via UIDAI portal or mAadhaar app", "Throwing away the physical card", "Calling the police"],
             1, "Locking your Aadhaar biometrics prevents anyone from authenticating loans or accounts even if they possess your card details."),
        ],
    },
    {
        "module": "personal",
        "slug": "parental-safety-protecting-seniors-and-kids",
        "title_en": "Protecting Seniors and Kids Online",
        "title_hi": "बुजुर्गों और बच्चों की डिजिटल सुरक्षा",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Teaching digital safety with patience: preventing pension scams, gaming microtransaction fraud, and online grooming.",
        "summary_hi": "घर के बुजुर्गों को पेंशन व बिजली बिल फ्रॉड से बचाना और बच्चों को ऑनलाइन गेमिंग जालसाजी से दूर रखना।",
        "script_en": (
            "Grandfather receives an SMS: 'Your electricity will be disconnected at 9:30 PM due to unpaid bill of ₹120. Call this number'. "
            "How establishing a household 'Check with me first' rule prevents our elders from losing lifetime pensions."
        ),
        "script_hi": (
            "दादाजी को मैसेज: 'बिजली का बिल न भरने के कारण रात 9:30 बजे बिजली कट जाएगी। इस नंबर पर तुरंत फोन करें।' "
            "घर में नियम बनाएं: 'कोई भी संदिग्ध मैसेज आए तो पहले परिवार के युवा सदस्यों को दिखाएं'।"
        ),
        "narration_en": "Scammers deliberately target seniors with technical jargon and artificial deadlines. Foster an open, judgment-free home culture.",
        "narration_hi": "ठग बुजुर्गों को तकनीकी भाषा और बिजली कटने के डर से निशाना बनाते हैं। घर में बिना झिझक बात करने का माहौल बनाएं।",
        "transcript_en": "[00:00] The electricity bill scam. [00:25] The vulnerable demographics. [00:45] The 'Check Before Clicking' household pledge.",
        "transcript_hi": "[00:00] बिजली बिल का फर्जी मैसेज। [00:25] बुजुर्गों को निशाना बनाना। [00:45] घर में सुरक्षा का खुला माहौल।",
        "questions": [
            ("An elderly family member receives a text threatening power disconnection within two hours unless they call a mobile number. You should:",
             ["Tell them to pay immediately", "Verify their real electricity bill status on the official utility provider portal and report the scam number", "Ignore the electricity company forever", "Forward the message"],
             1, "Power utilities never use personal mobile numbers for disconnection threats; always verify via official utility portals."),
        ],
    },
    {
        "module": "personal",
        "slug": "app-permissions-and-mobile-malware",
        "title_en": "Excessive App Permissions & Rogue APKs",
        "title_hi": "ऐप्स की अनावश्यक परमिशन और खतरनाक एपीके",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Why does a flashlight app need access to your contacts, SMS, and microphone? Inspecting runtime permissions.",
        "summary_hi": "टॉर्च या कैलकुलेटर ऐप को आपके संपर्कों, एसएमएस और माइक्रोफोन की परमिशन क्यों चाहिए? जोखिम को समझें।",
        "script_en": (
            "Demonstration of sideloading an APK file from a sketchy website claiming to be 'Modded Free Spotify'. "
            "The app asks for accessibility and notification permissions. Once granted, it reads incoming banking OTPs silently."
        ),
        "script_hi": (
            "मुफ्त गाने सुनने के चक्कर में किसी अनजान वेबसाइट से एपीके फाइल डाउनलोड करना। "
            "ऐप एसएमएस और नोटिफिकेशन की परमिशन मांगता है और बैंक से आने वाले ओटीपी चुपचाप हैकर को भेज देता है।"
        ),
        "narration_en": "Never install apps from outside official app stores. Periodically review which apps have permission to read your SMS and location.",
        "narration_hi": "अनजान वेबसाइटों से कभी ऐप इंस्टॉल न करें। सेटिंग्स में जाकर देखें कि किन ऐप्स को एसएमएस और लोकेशन की परमिशन दी गई है।",
        "transcript_en": "[00:00] The modded APK trap. [00:20] Malicious accessibility services abuse. [00:45] Auditing app permissions in settings.",
        "transcript_hi": "[00:00] फ्री ऐप का लालच। [00:20] एसएमएस परमिशन से ओटीपी की चोरी। [00:45] फोन सेटिंग्स में परमिशन जांचना।",
        "questions": [
            ("A simple calculator app downloaded from the web requests permission to read your contacts and SMS messages. You should:",
             ["Grant permissions because calculators need math", "Deny permissions, uninstall the app immediately, and use verified official apps", "Turn on airplane mode", "Buy a new phone"],
             1, "Utility apps requesting access to sensitive SMS or contact data are often spyware or trojans."),
        ],
    },

    # -------------------------------------------------------------------------
    # Module 9: incident (Lessons 41 - 45)
    # -------------------------------------------------------------------------
    {
        "module": "incident",
        "slug": "first-60-minutes-of-a-suspected-breach",
        "title_en": "The First 60 Minutes of a Suspected Breach",
        "title_hi": "सुरक्षा घटना के शुरुआती 60 मिनट",
        "difficulty": "intermediate",
        "duration": 6,
        "summary_en": "You clicked a bad link and entered your password. Don't panic — immediate action saves the entire enterprise.",
        "summary_hi": "यदि आपने गलती से गलत लिंक पर क्लिक कर दिया है, तो घबराएं नहीं — शुरुआती मिनटों में सही कदम से बड़ा नुकसान टल सकता है।",
        "script_en": (
            "Timeline walkthrough: Minute 0: Click happened. "
            "Minute 2: Disconnect Wi-Fi/Ethernet cable (isolate the machine without shutting it down so RAM evidence is preserved). "
            "Minute 5: Alert IT Security via phone. "
            "Minute 10: Change credentials from a separate clean device. "
            "Minute 30: Document what was seen."
        ),
        "script_hi": (
            "घटना का टाइमलाइन: 0 मिनट: गलत क्लिक हुआ। "
            "2 मिनट: तुरंत वाई-फाई बंद करें या केबल निकालें (कंप्यूटर को शटडाउन न करें ताकि सबूत सुरक्षित रहें)। "
            "5 मिनट: फोन से आईटी सुरक्षा टीम को सूचित करें। "
            "10 मिनट: दूसरे साफ फोन से अपना पासवर्ड बदलें।"
        ),
        "narration_en": "Speed is everything. Attackers count on employees hiding their mistakes for hours. Report immediately and without fear.",
        "narration_hi": "रफ्तार ही सबसे बड़ा बचाव है। हमलावर उम्मीद करते हैं कि आप गलती छुपाएंगे। बिना झिझक तुरंत सूचना दें।",
        "transcript_en": "[00:00] The panic moment. [00:20] Network isolation without power down. [00:45] Contacting incident response.",
        "transcript_hi": "[00:00] घबराहट का क्षण। [00:20] कंप्यूटर को नेटवर्क से अलग करना। [00:45] सुरक्षा टीम को तुरंत अलर्ट करना।",
        "questions": [
            ("If you suspect you entered your credentials on a phishing page, what is the best immediate response?",
             ["Pretend it didn't happen and shut down your laptop for a week", "Disconnect network connectivity and immediately notify IT Security while resetting password from another device", "Delete your browser history", "Format your hard drive"],
             1, "Quick isolation and transparent notification allow security teams to invalidate active session tokens before lateral movement."),
        ],
    },
    {
        "module": "incident",
        "slug": "how-to-report-without-fear-blameless-culture",
        "title_en": "Reporting Without Fear: Blameless Culture",
        "title_hi": "बिना डर के रिपोर्टिंग: सुरक्षा संस्कृति",
        "difficulty": "beginner",
        "duration": 5,
        "summary_en": "Why healthy organizations praise employees who report mistakes, and why hiding an attack destroys companies.",
        "summary_hi": "जानें क्यों एक अच्छी कंपनी गलती बताने वाले कर्मचारी की तारीफ करती है, और डरकर छुपाना कैसे भारी पड़ता है।",
        "script_en": (
            "Contrasting two organizations: Company A punishes anyone who clicks a phish. Employees hide malware for 3 months until all files are ransomed. "
            "Company B awards a 'Security Champion' badge to an employee who reported their own mistake in 4 minutes, allowing SOC to block the attack."
        ),
        "script_hi": (
            "दो कंपनियों की तुलना: पहली कंपनी गलती पर सजा देती है, कर्मचारी डरकर छुपाते हैं और 3 महीने बाद पूरी कंपनी रैनसमवेयर का शिकार हो जाती है। "
            "दूसरी कंपनी 4 मिनट में गलती बताने वाले कर्मचारी की सराहना करती है और बड़ा हमला टल जाता है।"
        ),
        "narration_en": "Security is not about perfection. It is about detection speed. A reported mistake is a neutralized threat.",
        "narration_hi": "सुरक्षा का मतलब कभी गलती न होना नहीं, बल्कि खतरे को तुरंत पहचानना है। रिपोर्ट की गई गलती टला हुआ खतरा है।",
        "transcript_en": "[00:00] Fear vs transparency. [00:25] The compounding cost of delay. [00:50] Building a blameless reporting environment.",
        "transcript_hi": "[00:00] डर बनाम पारदर्शिता। [00:25] देरी का भारी नुकसान। [00:50] बिना डर के काम करने का माहौल।",
        "questions": [
            ("Why is a 'blameless security culture' critical for enterprise safety?",
             ["It means employees don't have to follow rules", "Employees report phishing accidents immediately rather than concealing them out of fear", "It eliminates the need for IT", "It lowers software costs"],
             1, "When employees know they won't be punished for honest mistakes, incidents are reported and contained exponentially faster."),
        ],
    },
    {
        "module": "incident",
        "slug": "evidence-preservation-and-screenshot-etiquette",
        "title_en": "Evidence Preservation & Header Capture",
        "title_hi": "सबूत सुरक्षित रखना और स्क्रीनशॉट लेना",
        "difficulty": "intermediate",
        "duration": 6,
        "summary_en": "How to extract full internet email headers (RFC 822) and take timestamped screenshots to assist security analysts.",
        "summary_hi": "ईमेल के पूरे हेडर निकालना और समय के साथ स्क्रीनशॉट लेकर साइबर सुरक्षा टीम की मदद करना।",
        "script_en": (
            "Tutorial in Outlook & Gmail: How to click 'View Original' or 'Message Details' to copy the raw routing headers. "
            "Show what headers reveal: the actual originating mail server IP, SPF pass/fail records, and DKIM signatures."
        ),
        "script_hi": (
            "आउटलुक और जीमेल में ट्यूटोरियल: 'View Original' या 'Message Details' पर क्लिक करके हेडर कैसे निकालें। "
            "समझाएं कि हेडर से पता चलता है कि ईमेल वास्तव में किस सर्वर और किस देश से भेजा गया था।"
        ),
        "narration_en": "A screenshot shows what the email looked like; the raw headers show where the email truly came from. Provide both to IT.",
        "narration_hi": "स्क्रीनशॉट दिखाता है कि ईमेल कैसा दिखता था; हेडर बताता है कि ईमेल सच में कहां से आया था। जांच के लिए दोनों जरूरी हैं।",
        "transcript_en": "[00:00] Why screenshots alone are incomplete. [00:25] Exporting .eml or raw headers. [00:50] Sending samples safely to security.",
        "transcript_hi": "[00:00] सिर्फ स्क्रीनशॉट काफी क्यों नहीं है। [00:25] असली हेडर कॉपी करना। [00:50] सुरक्षा टीम को सही जानकारी भेजना।",
        "questions": [
            ("What information do raw email headers provide that a regular screenshot lacks?",
             ["The sender's profile picture", "Complete server routing hops, originating IP addresses, and cryptographic SPF/DKIM verification results", "The color of the button", "The battery level"],
             1, "Raw headers contain verifiable technical telemetry detailing the true mail path and authentication status."),
        ],
    },
    {
        "module": "incident",
        "slug": "containment-disconnecting-infected-systems",
        "title_en": "Containment: Disconnecting Infected Devices",
        "title_hi": "संक्रमित सिस्टम को नेटवर्क से अलग करना",
        "difficulty": "intermediate",
        "duration": 5,
        "summary_en": "Isolating compromised machines stops lateral movement and halts ransomware from spreading across network shares.",
        "summary_hi": "मैलवेयर प्रभावित कंप्यूटर को नेटवर्क से अलग करने से रैनसमवेयर बाकी कंप्यूटरों तक नहीं फैल पाता।",
        "script_en": (
            "Network topology animation: Ransomware starts encrypting computer A. "
            "If computer A remains connected to the LAN, it crawls through shared network drives X:, Y:, Z:. "
            "Unplugging the ethernet cable isolates the infection to a single machine, saving hundreds of workstations."
        ),
        "script_hi": (
            "नेटवर्क का एनिमेशन: रैनसमवेयर एक कंप्यूटर में घुसता है। "
            "यदि केबल लगी रहे तो वह पूरे दफ्तर के सभी कंप्यूटरों को लॉक कर देता है। "
            "केबल निकालते ही संक्रमण उसी एक कंप्यूटर तक सीमित रह जाता है।"
        ),
        "narration_en": "When ransomware strikes, pull the network plug immediately. Do not power off — just cut the network connection.",
        "narration_hi": "रैनसमवेयर दिखते ही तुरंत नेटवर्क केबल निकालें या वाई-फाई बंद करें। कंप्यूटर बंद न करें, केवल नेटवर्क काटें।",
        "transcript_en": "[00:00] Lateral movement explained. [00:20] Physical vs software isolation. [00:45] Why powering off can harm forensic recovery.",
        "transcript_hi": "[00:00] नेटवर्क में वायरस का फैलना। [00:20] नेटवर्क केबल अलग करना। [00:45] शटडाउन न करने की वैज्ञानिक वजह।",
        "questions": [
            ("Why should you unplug the network cable rather than simply holding down the power button when ransomware appears?",
             ["Power buttons are dirty", "Severing network access halts lateral encryption, while keeping power on preserves volatile RAM memory for forensic investigation", "Computers break if turned off", "To keep fans running"],
             1, "Network disconnection halts spread immediately, while leaving power on preserves volatile digital evidence in RAM."),
        ],
    },
    {
        "module": "incident",
        "slug": "post-incident-review-and-root-cause-analysis",
        "title_en": "Post-Incident Review & Root Cause Learning",
        "title_hi": "घटना के बाद समीक्षा और सुधार",
        "difficulty": "intermediate",
        "duration": 6,
        "summary_en": "Transforming security failures into collective organizational resilience through honest retrospective analysis.",
        "summary_hi": "किसी सुरक्षा घटना के बाद यह समझना कि चूक कहां हुई और भविष्य में उसे रोकने के लिए क्या बदलाव जरूरी हैं।",
        "script_en": (
            "An incident debrief meeting: The team examines the complete attack timeline without finger-pointing. "
            "They discover that an unpatched gateway and lack of MFA on an older VPN enabled the breach. "
            "Policies and training are updated to ensure it never happens again."
        ),
        "script_hi": (
            "सुरक्षा समीक्षा बैठक: टीम बिना किसी पर आरोप लगाए पूरी घटना का विश्लेषण करती है। "
            "वे पाते हैं कि पुराने वीपीएन पर एमएफए न होने से हमलावर अंदर आ गया। "
            "नियम बदले जाते हैं ताकि ऐसी गलती दोबारा न हो सके।"
        ),
        "narration_en": "Every major breach is a masterclass in defense. The goal of a post-mortem is not to assign blame, but to build an unbreachable wall.",
        "narration_hi": "हर सुरक्षा घटना सीखने का अवसर होती है। उद्देश्य दोष मढ़ना नहीं, बल्कि भविष्य के लिए मजबूत दीवार तैयार करना है।",
        "transcript_en": "[00:00] The post-mortem objective. [00:25] Root cause analysis techniques. [00:50] Updating controls and awareness playbooks.",
        "transcript_hi": "[00:00] समीक्षा बैठक का उद्देश्य। [00:25] असली जड़ की पहचान। [00:50] सुरक्षा नियमों में सुधार।",
        "questions": [
            ("What is the primary objective of an incident post-mortem meeting?",
             ["To assign blame and penalize the responsible team", "To identify systemic root causes and update technical controls and training so the breach cannot recur", "To draft a press release denying everything", "To close the IT department"],
             1, "Post-mortems focus on continuous learning, closing systemic vulnerabilities, and fortifying defenses against future attempts."),
        ],
    },

    # -------------------------------------------------------------------------
    # Module 10: advanced (Lessons 46 - 50)
    # -------------------------------------------------------------------------
    {
        "module": "advanced",
        "slug": "supply-chain-and-third-party-vendor-risks",
        "title_en": "Supply Chain & Third-Party Vendor Risks",
        "title_hi": "सप्लाई चेन और वेंडर से जुड़े जोखिम",
        "difficulty": "advanced",
        "duration": 6,
        "summary_en": "Why attackers target small HVAC contractors and cleaning vendors to infiltrate massive corporate networks.",
        "summary_hi": "जानिए क्यों हैकर्स बड़ी कंपनियों में घुसने के लिए उनके छोटे सप्लायर्स और वेंडर्स के ईमेल को निशाना बनाते हैं।",
        "script_en": (
            "Visual diagram: Enterprise A has bank-grade cybersecurity. "
            "Vendor B (catering/cleaning supplier) uses weak passwords and has remote access to Enterprise A's billing network. "
            "The attacker compromises Vendor B first, then walks right into Enterprise A."
        ),
        "script_hi": (
            "सप्लाई चेन का नक्शा: बड़ी कंपनी की अपनी सुरक्षा बहुत मजबूत है। "
            "लेकिन उसका छोटा वेंडर कमजोर पासवर्ड रखता है और उसके पास कंपनी के नेटवर्क का एक्सेस है। "
            "हैकर पहले वेंडर को हैक करता है और फिर सीधे बड़ी कंपनी में घुस जाता है।"
        ),
        "narration_en": "You are only as secure as the least secure vendor connected to your network. Vet third-party access relentlessly.",
        "narration_hi": "आपकी सुरक्षा उतनी ही मजबूत है जितनी आपके सबसे कमजोर वेंडर की। हर बाहरी एक्सेस की कड़ी निगरानी रखें।",
        "transcript_en": "[00:00] The castle and the side gate. [00:25] The Target breach case study. [00:50] Zero trust vendor segmentation.",
        "transcript_hi": "[00:00] मुख्य द्वार बनाम चोर दरवाजा। [00:25] प्रसिद्ध टारगेट स्टोर की केस स्टडी। [00:50] वेंडर्स के लिए जीरो ट्रस्ट नियम।",
        "questions": [
            ("Why do sophisticated attackers frequently compromise small third-party contractors rather than attacking Fortune 500 companies directly?",
             ["Small contractors have more money", "Contractors often have legitimate network access into large enterprises but weaker security defenses", "Small contractors use faster servers", "Attackers prefer smaller logos"],
             1, "Third-party vendors often possess privileged access into client networks while lacking enterprise-grade defense infrastructure."),
        ],
    },
    {
        "module": "advanced",
        "slug": "sim-swapping-and-sms-intercepts",
        "title_en": "SIM Swapping & SMS Interception",
        "title_hi": "सिम स्वैप और ओटीपी चोरी की साजिश",
        "difficulty": "advanced",
        "duration": 6,
        "summary_en": "How attackers trick telecom carrier retail reps into transferring your mobile number to a blank SIM card in their hands.",
        "summary_hi": "टेलीकॉम स्टोर पर फर्जी पहचान पत्र दिखाकर आपका नंबर अपने सिम पर ट्रांसफर कराने के खतरे से बचाव।",
        "script_en": (
            "An attacker walks into a mobile retail store with a forged driving license and your phone number: "
            "'I lost my phone, please issue a duplicate SIM'. The clerk activates the new SIM. "
            "Suddenly, your phone loses all signal ('No Service'), while the attacker receives all your incoming SMS banking OTPs."
        ),
        "script_hi": (
            "ठग टेलीकॉम स्टोर पर फर्जी आईडी दिखाकर कहता है: 'मेरा फोन खो गया है, नया सिम चालू कर दें'। "
            "अचानक आपके फोन का सिग्नल गायब हो जाता है ('No Service'), और आपके बैंक के सारे ओटीपी हैकर के नए सिम पर जाने लगते हैं।"
        ),
        "narration_en": "If your phone abruptly loses all cellular signal in a normal area, treat it as a potential SIM swap. Contact your carrier immediately.",
        "narration_hi": "यदि सामान्य जगह पर आपके फोन का नेटवर्क अचानक पूरी तरह गायब हो जाए, तो तुरंत टेलीकॉम कंपनी से संपर्क करें।",
        "transcript_en": "[00:00] The retail store social engineering. [00:25] The 'No Service' indicator. [00:50] Migrating from SMS OTPs to authenticator apps.",
        "transcript_hi": "[00:00] स्टोर पर फर्जी दस्तावेज का खेल। [00:25] 'No Service' का खतरा। [00:50] एसएमएस के बजाय ऐप आधारित प्रमाणीकरण का उपयोग।",
        "questions": [
            ("What is the most secure replacement for SMS-based two-factor authentication to protect against SIM-swapping?",
             ["Email OTPs", "Time-based hardware security keys (FIDO2/YubiKey) or authenticator apps (TOTP)", "Sending letters via post", "Writing PIN on a paper"],
             1, "Hardware security keys and authenticator apps cannot be intercepted via cellular SIM swapping attacks."),
        ],
    },
    {
        "module": "advanced",
        "slug": "watering-hole-and-strategic-web-compromises",
        "title_en": "Watering Hole Attacks on Industry Sites",
        "title_hi": "वाटरिंग होल हमले और संक्रमित वेबसाइटें",
        "difficulty": "advanced",
        "duration": 6,
        "summary_en": "Instead of hunting you directly, attackers poison the niche industry blogs and supplier forums you visit every morning.",
        "summary_hi": "सीधे आप पर हमला करने के बजाय उस इंडस्ट्री फोरम या वेबसाइट को हैक करना जिसे आप रोज पढ़ते हैं।",
        "script_en": (
            "Analogy: A predator doesn't chase gazelles across the desert; it waits by the water hole where they must drink. "
            "Attackers compromise a popular defense contracting news blog and inject a zero-day drive-by browser exploit."
        ),
        "script_hi": (
            "उदाहरण: शिकारी पूरे जंगल में शिकार नहीं ढूंढता, वह उस तालाब पर बैठता है जहां सबको पानी पीने आना ही है। "
            "हैकर्स किसी लोकप्रिय ट्रेड फोरम को हैक कर लेते हैं ताकि वहां आने वाले सभी पेशेवरों के सिस्टम में मैलवेयर चला जाए।"
        ),
        "narration_en": "Even trusted websites can be silently compromised. Keep your browser and operating system updated with latest security patches.",
        "narration_hi": "भरोसेमंद वेबसाइटें भी हैक हो सकती हैं। हमेशा अपने ब्राउज़र और कंप्यूटर को नवीनतम सुरक्षा पैच से अपडेट रखें।",
        "transcript_en": "[00:00] The watering hole predator analogy. [00:25] Drive-by download exploits. [00:50] Browser isolation and patching.",
        "transcript_hi": "[00:00] तालाब वाले शिकारी का उदाहरण। [00:25] वेबसाइट से सीधे डाउनलोड होने वाला वायरस। [00:50] ब्राउज़र अपडेट रखने की महत्ता।",
        "questions": [
            ("What defines a 'Watering Hole' cyber attack?",
             ["Dumping computers in lakes", "Compromising legitimate websites frequently visited by target industry members to infect visitors", "Attacking water treatment facilities only", "Phishing via marine biology forums"],
             1, "Watering hole attacks infect trusted third-party websites frequently visited by a target organization or community."),
        ],
    },
    {
        "module": "advanced",
        "slug": "insider-threat-indicators-and-defense",
        "title_en": "Insider Threat Indicators & Prevention",
        "title_hi": "अंदरूनी खतरे के संकेत और रोकथाम",
        "difficulty": "advanced",
        "duration": 6,
        "summary_en": "Recognizing signs of credential misuse, unauthorized mass data exports, and disgruntled employee sabotage.",
        "summary_hi": "संस्था के भीतर से होने वाले डेटा रिसाव, असामान्य समय पर लॉगिन और अधिकृत क्रेडेंशियल के दुरुपयोग की पहचान।",
        "script_en": (
            "Security Operations Center (SOC) dashboard alert: An engineer who submitted resignation yesterday "
            "downloads 45 gigabytes of proprietary CAD drawings at 2:00 AM on a Sunday. "
            "Walk through principle of least privilege and offboarding access revocation."
        ),
        "script_hi": (
            "सुरक्षा डैशबोर्ड पर अलर्ट: इस्तीफा दे चुके कर्मचारी द्वारा रविवार रात 2 बजे भारी मात्रा में गोपनीय डेटा डाउनलोड करना। "
            "न्यूनतम अधिकार (Least Privilege) और तुरंत एक्सेस समाप्त करने की प्रक्रियाओं का महत्व।"
        ),
        "narration_en": "The most dangerous attacker may already have an authorized badge. Defense in depth monitors abnormal internal behaviors.",
        "narration_hi": "सबसे खतरनाक हमलावर वह हो सकता है जिसके पास वैध पहचान पत्र हो। आंतरिक डेटा एक्सेस पर भी निगरानी जरूरी है।",
        "transcript_en": "[00:00] The departing employee scenario. [00:25] Behavioral anomaly detection. [00:50] The principle of least privilege.",
        "transcript_hi": "[00:00] नौकरी छोड़ने वाले कर्मचारी का केस। [00:25] असामान्य व्यवहार का विश्लेषण। [00:50] न्यूनतम अधिकार का सिद्धांत।",
        "questions": [
            ("Which administrative practice best mitigates the damage an insider threat can inflict?",
             ["Giving all staff global administrator access", "Enforcing the Principle of Least Privilege so users only access data strictly needed for their role", "Allowing unlimited USB copying", "Never terminating accounts"],
             1, "The Principle of Least Privilege limits access strictly to the resources required for an employee's specific daily role."),
        ],
    },
    {
        "module": "advanced",
        "slug": "zero-trust-architecture-for-everyday-users",
        "title_en": "Zero Trust Security for Everyday Users",
        "title_hi": "आम उपयोगकर्ताओं के लिए जीरो ट्रस्ट मॉडल",
        "difficulty": "advanced",
        "duration": 6,
        "summary_en": "'Never Trust, Always Verify': Moving beyond the castle-and-moat perimeter to continuous cryptographic verification.",
        "summary_hi": "'कभी भरोसा न करें, हमेशा सत्यापित करें': पुराने सुरक्षा मॉडल को छोड़कर हर डिवाइस और यूजर का लगातार सत्यापन।",
        "script_en": (
            "Old model: If you are inside the office building, the network trusts you completely. "
            "Zero Trust model: Every request — whether from the CEO in headquarters or an intern at an airport — must verify device health, "
            "user identity, and contextual risk before access is granted."
        ),
        "script_hi": (
            "पुराना मॉडल: यदि आप दफ्तर के अंदर हैं, तो नेटवर्क आप पर पूरा भरोसा करता था। "
            "जीरो ट्रस्ट मॉडल: चाहे आप दफ्तर में हों या घर पर, हर बार आपकी पहचान और डिवाइस की सुरक्षा जांच के बाद ही पहुंच मिलती है।"
        ),
        "narration_en": "Zero Trust isn't paranoia. It is realism. In a world where perimeters have dissolved, verification is our only shield.",
        "narration_hi": "जीरो ट्रस्ट कोई अविश्वास नहीं, बल्कि आधुनिक हकीकत है। जब कोई बाहरी सीमा नहीं बची, तो हर कदम पर सत्यापन ही हमारा कवच है।",
        "transcript_en": "[00:00] The demise of the perimeter moat. [00:25] The three pillars of Zero Trust. [00:50] Applying Zero Trust in daily habits.",
        "transcript_hi": "[00:00] पुराने सुरक्षा मॉडल का अंत। [00:25] जीरो ट्रस्ट के तीन मजबूत स्तंभ। [00:50] दैनिक आदतों में जीरो ट्रस्ट सोच।",
        "questions": [
            ("What is the core foundational maxim of Zero Trust architecture?",
             ["Trust everyone inside the office LAN", "Never trust, always verify every user and device continuously", "Passwords should never be changed", "Firewalls are obsolete"],
             1, "'Never Trust, Always Verify' requires continuous authentication and authorization regardless of location or network."),
        ],
    },
]
