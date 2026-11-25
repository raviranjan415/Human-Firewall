"""Synchronized Learning Defense Room Content Engine
===================================================
Provides 100% topic-synchronized learning assets for every lesson opened by the user:
1. Interactive Classroom Study Video & Dual-Language Audio Narration Engine
2. Topic-Matched Incident Dialogue & Comic Debrief with 3 Human Takeaways
3. Merged Practical Lab Sandbox with Forensics Artifact & Interactive Verification
4. TryHackMe-Style Compact Theory Room (Objectives, Concepts, Scenarios, Technical Breakdown,
   Practical Investigation, Analyst Notes, Common Mistakes, Knowledge Check, and Statutory Laws)
5. 3 Practical Scenario MCQs (Q1 Indicator Detection, Q2 Defense Protocol [ID 9001],
   Q3 Legal & Regulatory Recourse [ID 9002]) with Instant Coaching Explanations.
"""

import json
from pathlib import Path
from typing import Any

from app.services.i18n import current_locale

_JSON_FILE = Path(__file__).parent / "curated_lessons.json"
with open(_JSON_FILE, "r", encoding="utf-8") as _f:
    _RAW_LESSONS = json.load(_f)

# Curated synchronized lesson repository (50 comprehensive topics)
CURATED_LESSONS: dict[int, dict[str, Any]] = {
    int(k): v for k, v in _RAW_LESSONS.items()
}


def get_lesson_by_id_or_slug(
    lesson_id: int | None, slug: str | None = None
) -> dict[str, Any] | None:
    """Retrieve curated lesson data by numerical ID or slug."""
    if lesson_id and lesson_id in CURATED_LESSONS:
        return CURATED_LESSONS[lesson_id]
    if slug:
        for lesson_item in CURATED_LESSONS.values():
            if lesson_item.get("slug") == slug:
                return lesson_item
    return None


def _get_category_technical_specs(cat: str, title: str) -> dict[str, Any]:
    """Provide domain-specific technical terminology, protocols, commands and triage IOCs."""
    specs: dict[str, dict[str, Any]] = {
        "phishing": {
            "terms": [
                {"term": "SPF (Sender Policy Framework)", "def": "DNS TXT record (RFC 7208) that authorizes specific IP addresses to send mail on behalf of a domain."},
                {"term": "DKIM (DomainKeys Identified Mail)", "def": "Cryptographic signature header (RFC 6376) proving email content was not altered in transit."},
                {"term": "DMARC", "def": "Policy protocol (RFC 7489) that leverages SPF and DKIM to instruct receiving servers to quarantine or reject failures."},
                {"term": "Homoglyph / Punycode", "def": "Use of visually identical foreign characters (e.g. Cyrillic 'а') or xn-- prefixes to fake legitimate corporate domains."}
            ],
            "protocols": [
                {"name": "SMTP", "port": "Port 25 / 587", "detail": "Simple Mail Transfer Protocol used for mail relaying across network boundaries."},
                {"name": "DNS", "port": "Port 53 (UDP/TCP)", "detail": "Queries MX records, SPF TXT records, and DMARC policies for sender validation."},
                {"name": "HTTPS", "port": "Port 443 (TCP)", "detail": "Encrypted web channel hosting deceptive credential harvesting portals."}
            ],
            "tools": [
                {"tool": "dig / nslookup", "purpose": "Query domain MX, SPF TXT and DMARC records", "cmd": "dig +short TXT _dmarc.targetdomain.com"},
                {"tool": "curl / HTTP Inspect", "purpose": "Safely inspect HTTP response headers without browser script execution", "cmd": "curl -I -A 'Mozilla/5.0' https://suspect-link.example"},
                {"tool": "MXToolbox / Mail Header Analyzer", "purpose": "Parse Received: and Return-Path hops to trace sender IP origin", "cmd": "Analyze RFC 5322 headers"}
            ],
            "ioc_table": [
                {"layer": "Email Header", "signal": "Mismatched Return-Path or SPF softfail (~all)", "rule": "Inspect Received: relay hops and authenticated sender IP", "action": "Quarantine email & block sender IP"},
                {"layer": "Domain Identity", "signal": "Homoglyph / Punycode (e.g. xn-- or typosquatting)", "rule": "Verify WHOIS registration age (<30 days = high risk)", "action": "Add domain to perimeter DNS sinkhole"},
                {"layer": "Attachment Payload", "signal": "Double extension (.pdf.exe) or macro .docm", "rule": "Calculate SHA-256 hash and verify against VirusTotal sandbox", "action": "Submit to EDR sandbox for dynamic detonation"}
            ]
        },
        "financial": {
            "terms": [
                {"term": "BEC (Business Email Compromise)", "def": "Impersonation of senior executives, vendors, or legal counsel to execute unauthorized wire transfers."},
                {"term": "Dual-Custody Approval", "def": "Internal control requiring two authorized individuals to independently approve bank account or payment changes."},
                {"term": "Mule Account Churn", "def": "Rapid transfer of stolen funds across temporary intermediary accounts to defeat post-transaction recall."},
                {"term": "Out-of-Band Callback", "def": "Verifying transaction alterations via a verified corporate landline, never using the email's contact details."}
            ],
            "protocols": [
                {"name": "ERP Financial API", "port": "REST/JSON over TLS 1.3", "detail": "Enterprise Resource Planning ledger interface processing vendor invoices."},
                {"name": "NEFT / RTGS / SWIFT", "port": "Secure Financial Bus", "detail": "Inter-bank electronic funds settlement networks subject to bank cutoff deadlines."}
            ],
            "tools": [
                {"tool": "ERP Vendor Master Audit", "purpose": "Validate vendor bank account change history and approver identity", "cmd": "SELECT * FROM vendor_bank_audit WHERE mod_date > NOW() - INTERVAL 24 HOUR"},
                {"tool": "Corporate PBX Directory", "purpose": "Execute authenticated telephone verification to pre-registered finance executives", "cmd": "Call verified PBX extension directly"}
            ],
            "ioc_table": [
                {"layer": "Invoice Metadata", "signal": "Last-minute beneficiary account change with urgent tone", "rule": "Match bank account against approved corporate master vendor record", "action": "Freeze transfer and enforce physical/verbal callback"},
                {"layer": "Email Context", "signal": "Demand to bypass secondary signatory or keep transaction secret", "rule": "Zero-trust policy: No executive has authority to waive dual-custody", "action": "Escalate to Finance Controller and Head of Internal Audit"},
                {"layer": "Routing Details", "signal": "Beneficiary name differs from entity name on official contract", "rule": "Verify beneficiary IFSC / SWIFT routing against official contract", "action": "Reject transaction in banking portal"}
            ]
        },
        "voice": {
            "terms": [
                {"term": "Vishing (Voice Phishing)", "def": "Phone scams using emotional manipulation, social engineering, or fake authorities to elicit OTPs or access."},
                {"term": "Caller ID Spoofing", "def": "Manipulating SIP INVITE headers on VoIP trunks to display legitimate corporate or government phone numbers."},
                {"term": "Deepfake Voice Cloning", "def": "Using generative AI models trained on public audio to synthesize a target executive's exact vocal timbre and pitch."}
            ],
            "protocols": [
                {"name": "SIP", "port": "Port 5060 (UDP/TCP)", "detail": "Session Initiation Protocol initiating multimedia voice sessions with malleable caller identity."},
                {"name": "RTP", "port": "Ports 16384-32767", "detail": "Real-time Transport Protocol delivering audio media packets across VoIP networks."}
            ],
            "tools": [
                {"tool": "Telecom PBX CDR Logs", "purpose": "Inspect Call Detail Records to determine true trunk carrier origin", "cmd": "grep 'Call-ID\\|From:' /var/log/asterisk/cdr.log"},
                {"tool": "Out-of-Band Callback", "purpose": "Hang up and dial the official switchboard from internal company directory", "cmd": "Initiate verified callback on official extension"}
            ],
            "ioc_table": [
                {"layer": "Audio Channel", "signal": "Unusual vocal cadence, synthetic breath pauses, or background noise mismatch", "rule": "Ask out-of-context personal challenge question known only to real colleague", "action": "Terminate call immediately"},
                {"layer": "Caller ID", "signal": "Inbound call displaying exact corporate HQ or police helpline number", "rule": "Remember incoming caller ID is fully spoofable on VoIP trunks", "action": "Never disclose OTP or credentials over inbound call"},
                {"layer": "Request Nature", "signal": "Urgent demand to read out SMS verification code or approve 2FA push prompt", "rule": "Standard security policy: IT staff will never request 2FA codes", "action": "Lock account in identity dashboard and report to SOC"}
            ]
        },
        "messaging": {
            "terms": [
                {"term": "Smishing (SMS Phishing)", "def": "Deceptive SMS text messages directing recipients to malicious credential-harvesting sites."},
                {"term": "Sender ID Spoofing", "def": "Forging alphanumeric sender headers (e.g. 'AX-HDFCBK') through rogue bulk SMS gateways."},
                {"term": "SIM Swapping", "def": "Fraudulently convincing a mobile carrier to reassign a target's phone number to a scammer's SIM card."}
            ],
            "protocols": [
                {"name": "SMPP", "port": "Port 2775 (TCP)", "detail": "Short Message Peer-to-Peer protocol used by bulk SMS aggregators."},
                {"name": "GSM SMS Signaling", "port": "SS7 / MAP", "detail": "Cellular network signaling delivering short messages without origin authentication."}
            ],
            "tools": [
                {"tool": "URL Expander / Sandbox", "purpose": "Unshorten bit.ly or tinyurl links to inspect target destination", "cmd": "curl -sIL 'https://bit.ly/suspect' | grep -i 'location:'"},
                {"tool": "Mobile Security / MDM", "purpose": "Check device management logs for rogue SMS links and malicious profiles", "cmd": "Inspect enterprise MDM telemetry"}
            ],
            "ioc_table": [
                {"layer": "Message Body", "signal": "Threat of immediate SIM deactivation, electricity disconnection, or bank block", "rule": "Legitimate utilities never issue 30-minute disconnection threats via SMS", "action": "Do not tap embedded links; delete and report to 1930"},
                {"layer": "Embedded Link", "signal": "Shortened or non-standard URL (e.g. .xyz, .top, or typoed domain)", "rule": "Expand link safely in isolated sandbox; verify root domain", "action": "Block URL at corporate web gateway"},
                {"layer": "Sender Header", "signal": "Alphanumeric header with subtle character substitution or random foreign country code", "rule": "Verify against TRAI official telemarketer registry", "action": "Forward spam SMS to 1909 for carrier blocking"}
            ]
        },
        "physical": {
            "terms": [
                {"term": "Tailgating / Piggybacking", "def": "An unauthorized person closely following an authorized employee through a secure door or turnstile."},
                {"term": "RFID / NFC Badge Cloning", "def": "Using portable high-frequency or low-frequency antennas (e.g. Proxmark3) to capture and duplicate employee badges."},
                {"term": "Rogue USB Drop (BadUSB)", "def": "Leaving weaponized flash drives in public office areas that execute malicious HID keystrokes when inserted."}
            ],
            "protocols": [
                {"name": "Wiegand Protocol", "port": "Physical Data0/Data1", "detail": "Unencrypted legacy wiring protocol linking access card readers to door control panels."},
                {"name": "USB HID", "port": "Universal Serial Bus", "detail": "Human Interface Device protocol that allows USB devices to register as trusted keyboards."}
            ],
            "tools": [
                {"tool": "Access Control System (ACS)", "purpose": "Audit physical badge swipe logs against sensor breakbeam alarms", "cmd": "Check access log for door_forced_open or tailgating events"},
                {"tool": "Endpoint EDR USB Control", "purpose": "Enforce strict hardware whitelist preventing unauthorized USB device mounting", "cmd": "Get-PnpDevice -Class USB | Where-Object Status -ne 'OK'"}
            ],
            "ioc_table": [
                {"layer": "Physical Perimeter", "signal": "Individual asking to hold secure door while holding coffee cups or fake delivery boxes", "rule": "Enforce 'One Badge, One Entry' rule without exception", "action": "Politely ask person to badge in or escort them to reception"},
                {"layer": "Workstation Hardware", "signal": "Unfamiliar USB thumb drive found in cafeteria, lobby, or parking lot", "rule": "Assume any untrusted USB contains Keystroke Injection (BadUSB)", "action": "Never insert into any computer; deliver directly to Security Desk"},
                {"layer": "Visitor Verification", "signal": "Unescorted contractor in server room or sensitive department without visitor badge", "rule": "All visitors must display colored day passes and be accompanied", "action": "Challenge individual and escort immediately to security"}
            ]
        }
    }

    # Default fallback spec for workplace, incident, personal, advanced, foundations
    default_spec = {
        "terms": [
            {"term": "Zero Trust Architecture", "def": "Security model based on 'Never Trust, Always Verify' across users, devices, and network sessions."},
            {"term": "Least Privilege Principle", "def": "Granting users only the minimal access permissions necessary to perform authorized duties."},
            {"term": "Defense in Depth", "def": "Layering administrative, technical, and physical safeguards so failure of one layer is caught by another."},
            {"term": "Cognitive Immunity", "def": "Developing verified human habits (pause, inspect, verify) that neutralize psychological social engineering."}
        ],
        "protocols": [
            {"name": "TLS 1.3", "port": "Port 443", "detail": "Modern transport layer security protecting network data in transit with forward secrecy."},
            {"name": "OAuth 2.0 / OIDC", "port": "HTTPS Auth Bus", "detail": "Industry-standard delegated token authorization framework governing application access."}
        ],
        "tools": [
            {"tool": "SIEM Log Query", "purpose": "Correlate user authentication and session events across enterprise endpoints", "cmd": "index=security event_type=auth_anomaly status=failure"},
            {"tool": "EDR Process Monitor", "purpose": "Inspect parent-child process execution trees for anomalous spawned shells", "cmd": "Get-Process | Where-Object {$_.Path -like '*temp*'}"}
        ],
        "ioc_table": [
            {"layer": "Endpoint Behavior", "signal": "Unexpected permission prompt or software installation request", "rule": "Verify application code signing certificate and hash against enterprise catalog", "action": "Block execution and escalate to IT Helpdesk"},
            {"layer": "User Authentication", "signal": "Multiple 2FA push notifications received while not logging in (MFA Fatigue)", "rule": "Never tap 'Approve' to silence notifications", "action": "Select 'Deny' and change password immediately from secure device"},
            {"layer": "Data Access", "signal": "Unscheduled massive file download or sensitive document sharing", "rule": "Enforce DLP (Data Loss Prevention) policy monitoring", "action": "Revoke active session token and initiate forensic triage"}
        ]
    }

    return specs.get(cat, default_spec)


def build_compact_theory(data: dict[str, Any], locale: str) -> dict[str, Any]:
    """Construct TryHackMe-style modular compact reading material for the Defense Room."""
    is_hi = locale == "hi"
    title = data["title_hi"] if is_hi else data["title_en"]
    cat = data.get("cat", "foundations")
    specs = _get_category_technical_specs(cat, data["title_en"])
    raw_c = data["comic"]

    # Module A: Learning Objectives
    if is_hi:
        objectives = [
            f"1. {title} की तकनीकी हमला संरचना, निगरानी के तरीकों और घुसपैठ के रास्तों का विश्लेषण करना।",
            "2. खतरे के मुख्य तकनीकी संकेतों (IOCs), हेडर विसंगतियों और मनोवैज्ञानिक दबाव की समय रहते पहचान करना।",
            "3. मानक सुरक्षा प्रतिक्रिया (SOC) नियमों का पालन करना, स्वतंत्र पुष्टि करना और कानूनी अधिकारों का लाभ उठाना।"
        ]
    else:
        objectives = [
            f"1. Analyze the technical attack anatomy, reconnaissance vectors, and delivery methods of {title}.",
            "2. Identify high-fidelity Indicators of Compromise (IOCs), anomaly signals, and psychological manipulation triggers.",
            "3. Execute standardized SOC triage protocols, enforce out-of-band verification, and leverage statutory legal protections."
        ]

    # Module B: Concept Explanation
    if is_hi:
        concept_explanation = (
            f"साइबर सुरक्षा में '{title}' एक गंभीर मानवीय और तकनीकी चुनौती है। "
            "पारंपरिक फ़ायरवॉल और एंटीवायरस सॉफ़्टवेयर कंप्यूटर नेटवर्क को सुरक्षित रखते हैं, "
            "लेकिन जब कोई हमलावर अधिकृत कर्मचारी के भरोसे या घबराहट का फायदा उठाकर सीधे संपर्क करता है, "
            "तो तकनीकी सुरक्षा कवच निष्प्रभावी हो जाते हैं। "
            "हमलावर पहले सोशल मीडिया या डेटा लीक्स से जानकारी जुटाते हैं, फिर एक विश्वसनीय व्यक्ति या संस्था का मुखौटा पहनते हैं। "
            "इसके बाद वे कृत्रिम जल्दबाजी या डर पैदा करके बिना जांचे-परखे गोपनीय जानकारी निकालने या लेन-देन कराने का प्रयास करते हैं। "
            "ह्यूमन फ़ायरवॉल का उद्देश्य आपको इस मनोवैज्ञानिक दबाव को पहचानना और 60-सेकंड के ठहराव नियम से इसे विफल करना सिखाना है।"
        )
    else:
        concept_explanation = (
            f"In modern enterprise security, '{title}' represents a critical intersection between technical controls and human behavior. "
            "While network perimeters, web application firewalls, and EDR solutions defend against automated technical exploits, "
            "adversaries routinely bypass these multi-million dollar defenses by exploiting the human operating system. "
            "The exploitation lifecycle typically follows structured stages: target reconnaissance using OSINT and credential leaks, "
            "pretext development impersonating trusted figures (executives, vendors, or IT authorities), "
            "manufactured urgency to suppress analytical reasoning, and finally execution on objectives. "
            "Developing cognitive cyber immunity means recognizing that every unexpected or urgent demand is an unverified entry point "
            "that requires standardized out-of-band verification before compliance."
        )

    # Module C: Real-World Scenario
    sit = raw_c.get("situation_hi" if is_hi else "situation_en", "A corporate employee receives an urgent message")
    prob = raw_c.get("problem_hi" if is_hi else "problem_en", "High risk of security compromise")
    res = raw_c.get("resolution_hi" if is_hi else "resolution_en", "The attack was neutralized by verifying independently")

    if is_hi:
        real_world_scenario = (
            f"वास्तविक घटना परिदृश्य: {sit}। "
            f"हमलावर का मुख्य दबाव: {prob}। "
            f"सुरक्षा परिणाम: सतर्क कर्मचारी ने सुरक्षा प्रोटोकॉल का पालन किया — {res}। "
            "यह घटना दर्शाती है कि वास्तविक कार्यक्षेत्र में एक सतर्क निर्णय पूरी कंपनी को करोड़ों रुपये के नुकसान और डेटा लीक से बचा सकता है।"
        )
    else:
        real_world_scenario = (
            f"Incident Scenario Breakdown: {sit}. "
            f"Threat Vector & Exposure: {prob}. "
            f"Defense Resolution: The employee upheld standard operational security — {res}. "
            "This real-world case demonstrates that in active corporate environments, a single disciplined pause stops sophisticated breaches before they reach financial or data escrow systems."
        )

    # Module D: Technical Breakdown
    technical_breakdown = {
        "terminology": specs["terms"],
        "protocols": specs["protocols"],
        "tools": specs["tools"],
        "ioc_table": specs["ioc_table"]
    }

    # Module E: Practical Investigation
    if is_hi:
        practical_investigation = [
            {"step": 1, "title": "उत्पत्ति एवं हेडर की जांच", "action": "संदेश के प्रेषक पते, हेडर और मूल आईपी (IP) की जांच करें। प्रदर्शन नाम (Display Name) के पीछे छिपे वास्तविक पते को देखें।"},
            {"step": 2, "title": "लिंक व अनुलग्नक की सुरक्षा", "action": "किसी भी लिंक पर सीधे क्लिक न करें। माउस घुमाकर (Hover) वास्तविक URL देखें। फ़ाइल एक्सटेंशन (.exe, .pdf.exe) की जांच करें।"},
            {"step": 3, "title": "स्वतंत्र फोन सत्यापन", "action": "संदेश में दिए गए नंबर पर कभी कॉल न करें। कंपनी की आधिकारिक डायरेक्टरी से नंबर लेकर स्वतंत्र रूप से पुष्टि करें।"},
            {"step": 4, "title": "सुरक्षा दल (SOC) को रिपोर्ट", "action": "संदेश को आंतरिक सुरक्षा टीम (SOC) को अग्रेषित करें और वित्तीय धोखाधड़ी की स्थिति में तुरंत 1930 पर संपर्क करें।"}
        ]
    else:
        practical_investigation = [
            {"step": 1, "title": "Origin & Header Audit", "action": "Inspect the RFC 5322 Received headers, Return-Path, and envelope domain against the display name to identify third-party relays."},
            {"step": 2, "title": "Payload & Hyperlink Scrutiny", "action": "Never click directly. Hover to inspect destination URLs, check for typosquatting, and verify file extensions against macro-enabled signatures."},
            {"step": 3, "title": "Out-of-Band Channel Verification", "action": "Never reply or call numbers supplied inside the suspect communication. Use verified corporate PBX extensions or internal intranet directories."},
            {"step": 4, "title": "Containment & SOC Escalation", "action": "Quarantine the artifact, capture full network headers, alert the Security Operations Center, and dial 1930 for financial incidents."}
        ]

    # Module F: Analyst Notes
    if is_hi:
        analyst_notes = [
            "नियम 1 (जल्दबाजी ही संकेत है): हमलावर का सबसे बड़ा हथियार घबराहट पैदा करना है। जब भी अत्यधिक तात्कालिकता दिखाई जाए, तुरंत रुकें।",
            "नियम 2 (आधिकारिक माध्यम ही प्रमाण है): कभी भी संदिग्ध ईमेल या कॉल में दी गई संपर्क जानकारी पर भरोसा न करें।",
            "नियम 3 (सबूत सुरक्षित रखें): फ़ाइल या ईमेल को डिलीट करने से पहले उसका स्क्रीनशॉट और हेडर SOC जांच के लिए सुरक्षित रखें।"
        ]
    else:
        analyst_notes = [
            "Rule 1 (Urgency is the Primary Anomaly): Attackers fabricate artificial deadlines to induce cognitive panic. When rushed, pause immediately.",
            "Rule 2 (Inbound Data is Never Verification): Never trust contact details, telephone numbers, or URLs supplied inside the suspicious message itself.",
            "Rule 3 (Preserve Forensic Evidence): Capture unadulterated email headers, full URLs, and SHA-256 hashes before submitting for containment."
        ]

    # Module G: Common Mistakes
    if is_hi:
        common_mistakes = [
            "गलती 1: संदिग्ध प्रेषक को उसी ईमेल पर 'क्या यह आपने भेजा है?' लिखकर पूछना (हमलावर खुद ही हां में जवाब दे देगा)।",
            "गलती 2: यह मान लेना कि बड़े अधिकारी का नाम या फोटो दिख रहा है तो संदेश सच ही होगा (पहचान बदलना बहुत आसान है)।",
            "गलती 3: नौकरी जाने या डांट के डर से मानक सुरक्षा नियमों और दोहरे सत्यापन को छोड़ देना।"
        ]
    else:
        common_mistakes = [
            "Mistake 1: Replying directly to the suspect sender asking 'Did you send this?' (the threat actor will simply confirm).",
            "Mistake 2: Assuming that a high-ranking executive's title, photo, or signature proves authenticity (display metadata is trivial to spoof).",
            "Mistake 3: Allowing fear of reprimand to bypass mandatory dual-custody verification and standard authorization protocols."
        ]

    # Module H: Knowledge Check Questions (3 focused compact theory questions)
    if is_hi:
        knowledge_check = [
            {
                "question": f"{title} में हमलावर का प्राथमिक मनोवैज्ञानिक हथियार क्या होता है?",
                "options": [
                    "सोचने का समय न देना और कृत्रिम तात्कालिकता (Urgency) पैदा करना",
                    "कंप्यूटर में अत्यधिक जटिल गणितीय पासवर्ड डालना",
                    "हमेशा ईमेल में केवल सादा टेक्स्ट लिखना",
                    "केवल रात के समय ही संदेश भेजना"
                ],
                "correct_index": 0,
                "explanation": "हमलावर जानबूझकर घबराहट और जल्दबाजी पैदा करते हैं ताकि पीड़ित बिना सोचे-समझे कदम उठा ले।"
            },
            {
                "question": "किसी संदिग्ध वित्तीय या प्रशासनिक संदेश की पुष्टि करने का सबसे सुरक्षित तरीका क्या है?",
                "options": [
                    "उसी ईमेल में दिए गए नंबर पर तुरंत कॉल करना",
                    "कंपनी की आधिकारिक डायरेक्टरी से फोन नंबर लेकर अलग माध्यम से बात करना (Out-of-Band)",
                    "संदेश में दिए गए लिंक पर क्लिक करके पासवर्ड बदलना",
                    "अपने सहकर्मी से संदेश को फॉरवर्ड करने के लिए कहना"
                ],
                "correct_index": 1,
                "explanation": "संदेश के बाहर पूर्व-सत्यापित फोन नंबर या आंतरिक माध्यम से संपर्क करना ही आउट-ऑफ-बैंड सत्यापन कहलाता है।"
            },
            {
                "question": "भारतीय रिज़र्व बैंक (RBI) के अनुसार अनधिकृत वित्तीय लेनदेन की सूचना 3 दिन में देने पर आपकी क्या देनदारी होती है?",
                "options": [
                    "शून्य देनदारी (Zero Liability) — ग्राहक को कोई नुकसान नहीं होता",
                    "चुराई गई राशि का 50 प्रतिशत",
                    "पूरा नुकसान ग्राहक को सहना पड़ता है",
                    "बैंक केवल आधा पैसा लौटाता है"
                ],
                "correct_index": 0,
                "explanation": "आरबीआई सर्कुलर के तहत 3 कार्य दिवसों के भीतर अनधिकृत डिजिटल धोखाधड़ी की सूचना देने पर ग्राहक की देनदारी पूर्णतः शून्य होती है।"
            }
        ]
    else:
        knowledge_check = [
            {
                "question": f"What is the primary cognitive lever exploited by adversaries during {title}?",
                "options": [
                    "Manufactured urgency to trigger impulsive action and bypass rational verification",
                    "Cracking complex 256-bit AES encryption keys directly on client endpoints",
                    "Relying exclusively on plaintext messages without links or attachments",
                    "Waiting several weeks before requesting any action from the target"
                ],
                "correct_index": 0,
                "explanation": "Threat actors manufacture artificial urgency (e.g. account suspension, executive anger) to suppress the prefrontal cortex's analytical reasoning."
            },
            {
                "question": "What constitutes a valid Out-of-Band (OOB) verification when an unexpected urgent demand is received?",
                "options": [
                    "Contacting the requester using a pre-established number from the official corporate directory",
                    "Replying to the email asking if the sender is legitimate",
                    "Calling the telephone number provided in the signature of the suspect email",
                    "Clicking the verification link provided in the message to check its SSL certificate"
                ],
                "correct_index": 0,
                "explanation": "Out-of-band verification requires contacting the sender via a completely independent, verified channel outside the suspect message's control."
            },
            {
                "question": "Under the RBI Customer Protection framework, what is the customer's financial liability if an unauthorized transaction is reported within 3 working days?",
                "options": [
                    "Zero Liability — the customer bears no financial loss",
                    "50% of the total defrauded amount",
                    "Full liability rests entirely with the account holder",
                    "Liability is determined by the customer's credit score"
                ],
                "correct_index": 0,
                "explanation": "RBI directives mandate zero customer liability for unauthorized third-party electronic fraud reported within 3 working days."
            }
        ]

    return {
        "objectives": objectives,
        "concept_explanation": concept_explanation,
        "real_world_scenario": real_world_scenario,
        "technical_breakdown": technical_breakdown,
        "practical_investigation": practical_investigation,
        "analyst_notes": analyst_notes,
        "common_mistakes": common_mistakes,
        "knowledge_check": knowledge_check
    }


def get_synchronized_room_content(video: Any, lesson: Any) -> dict[str, Any]:
    """Assemble all 5 synchronized components for the Defense Room."""
    try:
        locale = current_locale()
    except Exception:
        locale = "en"

    # 1. Reliable lesson resolution: match by lesson slug first, then direct lesson id / video lesson id
    slug = getattr(lesson, "slug", "")
    data = None
    if slug:
        data = get_lesson_by_id_or_slug(None, slug)

    if not data:
        lid = getattr(lesson, "id", None) or getattr(video, "lesson_id", None) or getattr(video, "order_index", None) or getattr(video, "id", None)
        if isinstance(lid, int):
            mapped_id = ((lid - 1) % len(CURATED_LESSONS)) + 1
            data = CURATED_LESSONS.get(mapped_id)
        else:
            mapped_id = 1
            data = CURATED_LESSONS.get(1)
    else:
        mapped_id = data.get("id", 1)

    # 2. Build Synchronized Video Animation & Narration Scenes
    # 4 calibrated intervals of 20 seconds each: [0-20s], [20-40s], [40-60s], [60-80s]
    def make_scenes(lang: str) -> list[dict[str, Any]]:
        is_hi = lang == "hi"
        title_key = "title_hi" if is_hi else "title_en"
        lesson_title = data.get(title_key, data.get("title_en", "Cyber Defense"))

        s1_b = data["s1_badge"][1] if is_hi else data["s1_badge"][0]
        s2_b = data["s2_badge"][1] if is_hi else data["s2_badge"][0]
        s3_b = data["s3_badge"][1] if is_hi else data["s3_badge"][0]
        s4_b = data["s4_badge"][1] if is_hi else data["s4_badge"][0]

        s1_n = data["s1_narr"][1] if is_hi else data["s1_narr"][0]
        s2_n = data["s2_narr"][1] if is_hi else data["s2_narr"][0]
        s3_n = data["s3_narr"][1] if is_hi else data["s3_narr"][0]
        s4_n = data["s4_narr"][1] if is_hi else data["s4_narr"][0]

        # Extract pure unmixed language lines:
        # In curated_lessons.json: index 0=EN line1, 1=HI line1, 2=EN line2, 3=HI line2
        if is_hi:
            s1_l = [
                data["s1_lines"][1] if len(data["s1_lines"]) > 1 else "",
                data["s1_lines"][3] if len(data["s1_lines"]) > 3 else (data["s1_lines"][1] if len(data["s1_lines"]) > 1 else ""),
            ]
            s2_l = [
                data["s2_lines"][1] if len(data["s2_lines"]) > 1 else "",
                data["s2_lines"][3] if len(data["s2_lines"]) > 3 else (data["s2_lines"][1] if len(data["s2_lines"]) > 1 else ""),
            ]
            s3_l = [
                data["s3_lines"][1] if len(data["s3_lines"]) > 1 else "",
                data["s3_lines"][3] if len(data["s3_lines"]) > 3 else (data["s3_lines"][1] if len(data["s3_lines"]) > 1 else ""),
            ]
            s4_l = [
                data["s4_lines"][1] if len(data["s4_lines"]) > 1 else "",
                data["s4_lines"][3] if len(data["s4_lines"]) > 3 else (data["s4_lines"][1] if len(data["s4_lines"]) > 1 else ""),
            ]
        else:
            s1_l = [
                data["s1_lines"][0] if len(data["s1_lines"]) > 0 else "",
                data["s1_lines"][2] if len(data["s1_lines"]) > 2 else (data["s1_lines"][0] if len(data["s1_lines"]) > 0 else ""),
            ]
            s2_l = [
                data["s2_lines"][0] if len(data["s2_lines"]) > 0 else "",
                data["s2_lines"][2] if len(data["s2_lines"]) > 2 else (data["s2_lines"][0] if len(data["s2_lines"]) > 0 else ""),
            ]
            s3_l = [
                data["s3_lines"][0] if len(data["s3_lines"]) > 0 else "",
                data["s3_lines"][2] if len(data["s3_lines"]) > 2 else (data["s3_lines"][0] if len(data["s3_lines"]) > 0 else ""),
            ]
            s4_l = [
                data["s4_lines"][0] if len(data["s4_lines"]) > 0 else "",
                data["s4_lines"][2] if len(data["s4_lines"]) > 2 else (data["s4_lines"][0] if len(data["s4_lines"]) > 0 else ""),
            ]

        # Conversational masterclass teacher lecture (distinct from written slide bullets)
        if is_hi:
            t_script_1 = f"नमस्ते क्लास! क्या आपने कभी सोचा है कि आधुनिक सुरक्षा कवच होने के बावजूद कंपनियां कैसे हैक हो जाती हैं? क्योंकि हमलावर कंप्यूटर को नहीं, इंसानी फैसलों को निशाना बनाते हैं। आज के पाठ '{lesson_title}' में स्मार्टबोर्ड पर ध्यान दें: {s1_l[0]}। हमलावर सिस्टम तोड़ने के बजाय मानवीय भरोसे का फायदा उठाते हैं: {s1_l[1]}। हर अप्रत्याशित संदेश को पहले जांचना जरूरी है।"
            t_script_2 = f"छात्रों, इस खतरे के पीछे छिपे तकनीकी संकेतों को समझिए। हमलावर का मुख्य दांव है {s2_b}: {s2_l[0]}। सुरक्षा संचालन (SOC) में कृत्रिम जल्दबाजी ही धोखे की सबसे बड़ी पहचान होती है। जब भी कोई तत्काल कार्रवाई या बात को गुप्त रखने का दबाव बनाए, तो समझ जाइए कि यह सुरक्षा नियमों को तोड़ने की चाल है।"
            t_script_3 = f"यह है हमारा मुख्य रक्षा नियम: साठ सेकंड का ठहराव लें। पहला कदम: {s3_l[0]}। दूसरा कदम: {s3_l[1]}। कॉर्पोरेट सुरक्षा का नियम है कि वास्तविक अधिकारी और सहयोगी स्वतंत्र फोन सत्यापन का हमेशा स्वागत और सम्मान करते हैं।"
            t_script_4 = "कक्षा ध्यान दें, हमेशा याद रखें कि सरकारी नियम और कॉर्पोरेट नीतियां आपकी पूरी रक्षा करती हैं। बैंकिंग दिशा-निर्देशों और आईटी अधिनियम के तहत तीन दिन के भीतर सूचना देने पर आपकी वित्तीय देनदारी शून्य होती है। किसी भी खतरे पर तुरंत आंतरिक सुरक्षा दल को सूचित करें और राष्ट्रीय साइबर हेल्पलाइन उन्नीस-तीस पर कॉल करें।"
        else:
            t_script_1 = f"Hello class! Have you ever wondered why top corporations with multimillion-dollar firewalls still get breached? Adversaries rarely smash through technical firewalls when they can manipulate human judgment. In today's session on {lesson_title}, notice our smartboard: {s1_l[0]}. In this attack vector, {s1_l[1]}. Every unexpected message or call is an unverified entry point into your organization."
            t_script_2 = f"Notice the tactical red flags in this threat pattern. The attacker relies heavily on {s2_b}: {s2_l[0]}. In actual SOC incident response, manufactured urgency is the single biggest giveaway. When someone pressures you with sudden consequences or insists on secrecy, they are attempting an emotional bypass of standard security protocols."
            t_script_3 = f"Here is our Human Firewall defense countermeasure. When an irregular demand strikes, implement an intentional sixty-second pause to let rational thinking take over. Step one: {s3_l[0]}. Step two: {s3_l[1]}. In real cybersecurity operations, authentic colleagues will always commend you for verifying through approved corporate channels."
            t_script_4 = "Class, always remember that corporate policy and statutory law stand firmly behind you. Under RBI customer protection directives and the IT Act, reporting within seventy-two hours provides complete zero-liability protection. Immediately notify your security team and dial the national emergency helpline nineteen-thirty."

        return [
            {
                "idx": 0,
                "start_s": 0,
                "end_s": 20,
                "badge": s1_b,
                "board_title": f"{lesson_title} · {'हमला परिदृश्य' if is_hi else 'Attack Anatomy'}",
                "title": f"{lesson_title} - {'चरण 1: हमला परिदृश्य' if is_hi else 'Phase 1: Real Attack Scenario'}",
                "line1": s1_l[0],
                "line2": s1_l[1] if len(s1_l) > 1 else "",
                "narration": t_script_1,
                "teacher_script": t_script_1,
                "raw_narration": s1_n,
                "study_bullets": [
                    s1_b,
                    s1_l[0],
                    s1_l[1] if len(s1_l) > 1 else s1_n,
                ],
                "kind": "threat",
                "character_action": "welcome",
            },
            {
                "idx": 1,
                "start_s": 20,
                "end_s": 40,
                "badge": s2_b,
                "board_title": f"{lesson_title} · {'खतरे के संकेत व दबाव' if is_hi else 'Tactical Red Flags'}",
                "title": f"{lesson_title} - {'चरण 2: मनोवैज्ञानिक दबाव व संकेत' if is_hi else 'Phase 2: Tactical Red Flags'}",
                "line1": s2_l[0],
                "line2": s2_l[1] if len(s2_l) > 1 else "",
                "narration": t_script_2,
                "teacher_script": t_script_2,
                "raw_narration": s2_n,
                "study_bullets": [
                    s2_b,
                    s2_l[0],
                    s2_l[1] if len(s2_l) > 1 else s2_n,
                ],
                "kind": "alert",
                "character_action": "warn",
            },
            {
                "idx": 2,
                "start_s": 40,
                "end_s": 60,
                "badge": s3_b,
                "board_title": f"{lesson_title} · {'ह्यूमन फ़ायरवॉल सुरक्षा कदम' if is_hi else 'Human Firewall Protocol'}",
                "title": f"{lesson_title} - {'चरण 3: मानवीय सुरक्षा कदम' if is_hi else 'Phase 3: Human Firewall Defense'}",
                "line1": s3_l[0],
                "line2": s3_l[1] if len(s3_l) > 1 else "",
                "narration": t_script_3,
                "teacher_script": t_script_3,
                "raw_narration": s3_n,
                "study_bullets": [
                    s3_b,
                    s3_l[0],
                    s3_l[1] if len(s3_l) > 1 else s3_n,
                ],
                "kind": "defense",
                "character_action": "shield",
            },
            {
                "idx": 3,
                "start_s": 60,
                "end_s": 80,
                "badge": s4_b,
                "board_title": f"{lesson_title} · {'कानूनी अधिकार व 1930' if is_hi else 'Statutory Rights & Helpline'}",
                "title": f"{lesson_title} - {'चरण 4: कानूनी अधिकार व सरकारी नियम' if is_hi else 'Phase 4: Statutory Rights & Laws'}",
                "line1": s4_l[0],
                "line2": s4_l[1] if len(s4_l) > 1 else "",
                "narration": t_script_4,
                "teacher_script": t_script_4,
                "raw_narration": s4_n,
                "study_bullets": [
                    s4_b,
                    s4_l[0],
                    s4_l[1] if len(s4_l) > 1 else s4_n,
                    "राष्ट्रीय हेल्पलाइन: 1930 (72 घंटे में शून्य देनदारी)" if is_hi else "National Cyber Helpline: 1930 (Zero Liability within 72 hrs)",
                ],
                "kind": "legal",
                "character_action": "legal",
            },
        ]

    video_scenes = {"en": make_scenes("en"), "hi": make_scenes("hi")}

    # 3. Build Topic-Matched Incident Dialogue & Comic
    raw_c = data["comic"]
    comic = {
        "target_persona": raw_c["target_persona_hi"]
        if locale == "hi"
        else raw_c["target_persona_en"],
        "target_persona_en": raw_c["target_persona_en"],
        "target_persona_hi": raw_c["target_persona_hi"],
        "situation": raw_c["situation_hi"] if locale == "hi" else raw_c["situation_en"],
        "situation_en": raw_c["situation_en"],
        "situation_hi": raw_c["situation_hi"],
        "attacker_role": raw_c["attacker_role_hi"]
        if locale == "hi"
        else raw_c["attacker_role_en"],
        "attacker_role_en": raw_c["attacker_role_en"],
        "attacker_role_hi": raw_c["attacker_role_hi"],
        "problem": raw_c["problem_hi"] if locale == "hi" else raw_c["problem_en"],
        "problem_en": raw_c["problem_en"],
        "problem_hi": raw_c["problem_hi"],
        "resolution": raw_c["resolution_hi"]
        if locale == "hi"
        else raw_c["resolution_en"],
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
        lab_opts.append(
            {
                "id": opt["id"],
                "text": opt["text_hi"] if locale == "hi" else opt["text_en"],
                "text_en": opt["text_en"],
                "text_hi": opt["text_hi"],
                "is_correct": opt.get("is_correct", False),
            }
        )
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

    # 5. Build TryHackMe-Style Compact Theory & Threat Laws
    raw_r = data["reading"]
    theory_en = build_compact_theory(data, "en")
    theory_hi = build_compact_theory(data, "hi")
    active_theory = theory_hi if locale == "hi" else theory_en

    reading = {
        "overview": raw_r["overview_hi"] if locale == "hi" else raw_r["overview_en"],
        "overview_en": raw_r["overview_en"],
        "overview_hi": raw_r["overview_hi"],
        "red_flags": raw_r["red_flags_hi"] if locale == "hi" else raw_r["red_flags_en"],
        "red_flags_en": raw_r["red_flags_en"],
        "red_flags_hi": raw_r["red_flags_hi"],
        "regulations": raw_r["regulations"],
        # TryHackMe Room Compact Modules:
        "objectives": active_theory["objectives"],
        "objectives_en": theory_en["objectives"],
        "objectives_hi": theory_hi["objectives"],
        "concept_explanation": active_theory["concept_explanation"],
        "concept_explanation_en": theory_en["concept_explanation"],
        "concept_explanation_hi": theory_hi["concept_explanation"],
        "real_world_scenario": active_theory["real_world_scenario"],
        "real_world_scenario_en": theory_en["real_world_scenario"],
        "real_world_scenario_hi": theory_hi["real_world_scenario"],
        "technical_breakdown": active_theory["technical_breakdown"],
        "technical_breakdown_en": theory_en["technical_breakdown"],
        "technical_breakdown_hi": theory_hi["technical_breakdown"],
        "practical_investigation": active_theory["practical_investigation"],
        "practical_investigation_en": theory_en["practical_investigation"],
        "practical_investigation_hi": theory_hi["practical_investigation"],
        "analyst_notes": active_theory["analyst_notes"],
        "analyst_notes_en": theory_en["analyst_notes"],
        "analyst_notes_hi": theory_hi["analyst_notes"],
        "common_mistakes": active_theory["common_mistakes"],
        "common_mistakes_en": theory_en["common_mistakes"],
        "common_mistakes_hi": theory_hi["common_mistakes"],
        "knowledge_check": active_theory["knowledge_check"],
        "knowledge_check_en": theory_en["knowledge_check"],
        "knowledge_check_hi": theory_hi["knowledge_check"],
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
        "explanation": q1_raw["explanation_hi"]
        if locale == "hi"
        else q1_raw["explanation_en"],
        "explanation_en": q1_raw["explanation_en"],
        "explanation_hi": q1_raw["explanation_hi"],
    }

    # Q2 (ID 9001): RBI Zero Liability & Standard Banking/Operational Verification Defense
    q2 = {
        "id": 9001,
        "text": "भारतीय रिजर्व बैंक (RBI) के सुरक्षा सर्कुलर के अनुसार, अनधिकृत डिजिटल लेनदेन की सूचना तुरंत बैंक को देने पर ग्राहक की देयता क्या होती है?"
        if locale == "hi"
        else "Under Reserve Bank of India (RBI) customer protection directives, what is your liability if an unauthorized digital transaction is reported to the bank within 3 working days?",
        "text_en": "Under Reserve Bank of India (RBI) customer protection directives, what is your liability if an unauthorized digital transaction is reported to the bank within 3 working days?",
        "text_hi": "भारतीय रिजर्व बैंक (RBI) के सुरक्षा सर्कुलर के अनुसार, अनधिकृत डिजिटल लेनदेन की सूचना तुरंत बैंक को देने पर ग्राहक की देयता क्या होती है?",
        "options": [
            "आपको चुराई गई राशि का 50% वहन करना होगा",
            "शून्य देयता (Zero Liability) — ग्राहक को कोई वित्तीय नुकसान नहीं उठाना पड़ता",
            "पूरी जिम्मेदारी खाताधारक पर होती है",
            "जिम्मेदारी आपके क्रेडिट स्कोर पर निर्भर करती है",
        ]
        if locale == "hi"
        else [
            "You must pay 50% of the stolen amount",
            "Zero Liability — the customer bears no financial loss",
            "Full liability rests with the account holder",
            "Liability depends on your credit score",
        ],
        "options_en": [
            "You must pay 50% of the stolen amount",
            "Zero Liability — the customer bears no financial loss",
            "Full liability rests with the account holder",
            "Liability depends on your credit score",
        ],
        "options_hi": [
            "आपको चुराई गई राशि का 50% वहन करना होगा",
            "शून्य देयता (Zero Liability) — ग्राहक को कोई वित्तीय नुकसान नहीं उठाना पड़ता",
            "पूरी जिम्मेदारी खाताधारक पर होती है",
            "जिम्मेदारी आपके क्रेडिट स्कोर पर निर्भर करती है",
        ],
        "correct_index": 1,
        "explanation": "RBI के सर्कुलर DBR.No.Leg.BC.78/09.07.005/2017-18 के अनुसार, अनधिकृत लेनदेन की सूचना 3 कार्य दिवसों के भीतर देने पर ग्राहक की देयता शून्य होती है।"
        if locale == "hi"
        else "Under RBI Circular DBR.No.Leg.BC.78/09.07.005/2017-18, customers have ZERO liability if an unauthorized transaction is reported within 3 working days.",
        "explanation_en": "Under RBI Circular DBR.No.Leg.BC.78/09.07.005/2017-18, customers have ZERO liability if an unauthorized transaction is reported within 3 working days.",
        "explanation_hi": "RBI के सर्कुलर DBR.No.Leg.BC.78/09.07.005/2017-18 के अनुसार, अनधिकृत लेनदेन की सूचना 3 कार्य दिवसों के भीतर देने पर ग्राहक की देयता शून्य होती है।",
    }

    # Q3 (ID 9002): IT Act Section 66D Cheating by Impersonation & Digital Fraud Legal Recourse
    q3 = {
        "id": 9002,
        "text": "सूचना प्रौद्योगिकी (IT) अधिनियम 2000 की धारा 66D के तहत, कंप्यूटर या मोबाइल के माध्यम से पहचान बदलकर धोखाधड़ी करने पर क्या कानूनी सजा है?"
        if locale == "hi"
        else "Under Section 66D of the Information Technology (IT) Act 2000, what is the legal penalty for cheating by impersonation using a computer or mobile device?",
        "text_en": "Under Section 66D of the Information Technology (IT) Act 2000, what is the legal penalty for cheating by impersonation using a computer or mobile device?",
        "text_hi": "सूचना प्रौद्योगिकी (IT) अधिनियम 2000 की धारा 66D के तहत, कंप्यूटर या मोबाइल के माध्यम से पहचान बदलकर धोखाधड़ी करने पर क्या कानूनी सजा है?",
        "options": [
            "बिना आपराधिक रिकॉर्ड के केवल चेतावनी",
            "3 वर्ष तक का कारावास और ₹1,00,000 तक का जुर्माना",
            "केवल जमानत जब्त होना",
            "30 दिनों की सामुदायिक सेवा",
        ]
        if locale == "hi"
        else [
            "Warning letter with no criminal record",
            "Imprisonment up to 3 years and a fine up to ₹1,00,000",
            "Bail forfeiture only",
            "Community service for 30 days",
        ],
        "options_en": [
            "Warning letter with no criminal record",
            "Imprisonment up to 3 years and a fine up to ₹1,00,000",
            "Bail forfeiture only",
            "Community service for 30 days",
        ],
        "options_hi": [
            "बिना आपराधिक रिकॉर्ड के केवल चेतावनी",
            "3 वर्ष तक का कारावास और ₹1,00,000 तक का जुर्माना",
            "केवल जमानत जब्त होना",
            "30 दिनों की सामुदायिक सेवा",
        ],
        "correct_index": 1,
        "explanation": "IT एक्ट 2000 की धारा 66D के तहत कंप्यूटर या फोन से फर्जी प्रतिरूप बनाकर धोखाधड़ी करने पर 3 साल तक की जेल और ₹1 लाख तक का जुर्माना हो सकता है।"
        if locale == "hi"
        else "Section 66D of the IT Act penalizes cheating by personation by using any communication device or computer resource with imprisonment up to 3 years and fine up to ₹1 Lakh.",
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
