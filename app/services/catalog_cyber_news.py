"""Curated Dataset of Major Cyber and Corporate Attacks (Past ~1.5 Years: 2023–2026).

Each attack is structured with multi-domain breakdowns:
- Executive & Plain English Overview (easy to study for non-technical readers)
- Corporate & Financial Market Impact (SEC filings, dollar losses, downtime)
- Technical Anatomy (CVEs, exploit vectors, protocols, MITRE ATT&CK)
- Behavioral & Human Factors (social engineering, urgency, cognitive bias)
- Actionable Human Firewall Checklist (remediation & prevention)
"""

from __future__ import annotations

from datetime import datetime, timedelta
from app.models.user import utcnow

def _days_ago(days: int) -> datetime:
    return utcnow() - timedelta(days=days)

CURATED_CYBER_ATTACKS: list[dict] = [
    # 1. CrowdStrike Falcon Global Outage
    {
        "title": "CrowdStrike Falcon Global Outage: Logic Error in Kernel Update Paralyzes 8.5M Systems Worldwide",
        "url": "https://www.cisa.gov/news-events/alerts/2024/07/19/widespread-it-outage-due-crowdstrike-update",
        "published_at": _days_ago(25),
        "category": "Supply Chain",
        "severity": "Critical",
        "financial_impact": "$5.4 Billion+ across Fortune 500",
        "summary_en": "A defective channel configuration update deployed by cybersecurity vendor CrowdStrike caused an unexpected memory read error in its Falcon sensor kernel driver, triggering Blue Screen of Death (BSOD) crashes across 8.5 million Microsoft Windows computers globally.",
        "summary_hi": "साइबर सुरक्षा कंपनी क्राउडस्ट्राइक के एक दोषपूर्ण अपडेट के कारण दुनिया भर में 85 लाख विंडोज़ कंप्यूटर क्रैश हो गए, जिससे वैश्विक स्तर पर उड़ानें, अस्पताल और बैंक ठप पड़ गए।",
        "what_happened_en": "On July 19, 2024, at 04:09 UTC, CrowdStrike pushed Rapid Response Content Channel File 291 to Windows systems running sensor 7.11+. The file was designed to evaluate named pipe execution, but contained 21 input fields when the internal validation sensor expected 20. This triggered an out-of-bounds memory read in CSagent.sys, causing infinite crash loops (PAGE_FAULT_IN_NONPAGED_AREA). Resolution required manual intervention: booting into Safe Mode or Windows Recovery Environment and deleting the file.",
        "what_happened_hi": "क्राउडस्ट्राइक ने एक अपडेट जारी किया जिसमें मेमोरी रीड एरर था। इससे कंप्यूटर बूट लूप में फंस गए और मैन्युअल रूप से सेफ मोड में जाकर फाइल हटाने पर ही ठीक हुए।",
        "who_is_affected_en": "Delta Airlines (disrupted for 6 days, canceling 5,500+ flights and losing $500M+), thousands of healthcare clinics and hospitals canceling surgeries, banks, 911 emergency services, and point-of-sale retail terminals worldwide.",
        "who_is_affected_hi": "डेल्टा एयरलाइंस, वैश्विक बैंक, अस्पताल और आपातकालीन 911 सेवाएं गंभीर रूप से प्रभावित हुईं।",
        "why_it_matters_en": "The largest IT outage in world history demonstrated the immense concentration risk in endpoint security architectures. When security software operates in Ring 0 (Windows kernel) and deploys simultaneous global updates without phased canary rollouts, a single software defect can collapse global critical infrastructure.",
        "why_it_matters_hi": "यह इतिहास का सबसे बड़ा आईटी संकट था, जिसने दिखाया कि बिना चरणबद्ध परीक्षण के सीधे अपडेट भेजना कितना खतरनाक हो सकता है।",
        "what_to_do_en": "1. Enforce phased, multi-ring deployment (Canary -> Pilot -> Production) for all endpoint agent updates.\n2. Maintain secure, offline, multi-party access to BitLocker recovery keys.\n3. Implement business continuity plans with non-digital manual operating procedures for critical services.",
        "what_to_do_hi": "1. सभी सॉफ्टवेयर अपडेट के लिए चरणबद्ध रोलआउट अनिवार्य करें।\n2. बिटलॉकर रिकवरी कीज का सुरक्षित ऑफलाइन बैकअप रखें।\n3. आपातकालीन मैनुअल संचालन योजना तैयार रखें।",
        "meta": {
            "category": "Supply Chain",
            "severity": "Critical",
            "financial_impact": "$5.4 Billion+",
            "technical_analysis": {
                "attack_vector": "Kernel-mode sensor configuration update (Channel File 291).",
                "cve_list": ["CWE-125: Out-of-bounds Read"],
                "mitre_tactics": ["Software Supply Chain (T1195)", "Impacting System Availability (T1489)"],
                "root_cause": "Mismatch between Content Validator and Content Interpreter in Ring 0 Windows kernel driver (CSagent.sys)."
            },
            "behavioral_analysis": {
                "human_factor": "Implicit Trust & Automation Bias.",
                "psychological_hooks": ["Assumption that vendor security updates are always safe", "Speed-to-market prioritization over staging"],
                "organizational_gap": "Organizations allowed automated vendor auto-updates on mission-critical servers without testing in isolated lab environments."
            },
            "key_takeaways": [
                "Never allow endpoint protection agents to update mission-critical production servers simultaneously.",
                "Kernel-level security software requires staged canary rings just like operating system updates.",
                "Maintain physical access runbooks and offline BitLocker keys for rapid recovery."
            ]
        }
    },

    # 2. Change Healthcare Ransomware Catastrophe
    {
        "title": "Change Healthcare Ransomware Attack: Single-Factor Citrix Portal Causes $2.5B US Medical Crisis",
        "url": "https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-060a",
        "published_at": _days_ago(60),
        "category": "Ransomware",
        "severity": "Critical",
        "financial_impact": "$2.5 Billion+ Cost; $22 Million Ransom Paid",
        "summary_en": "ALPHV/BlackCat ransomware cybercriminals compromised Change Healthcare (UnitedHealth Group) through an unmonitored remote access gateway lacking Multi-Factor Authentication (MFA), halting prescription billing across one-third of the entire US healthcare system.",
        "summary_hi": "मल्टी-फैक्टर ऑथेंटिकेशन (MFA) न होने के कारण हैकर्स ने चेंज हेल्थकेयर के सर्वरों को रैनसमवेयर से एन्क्रिप्ट कर दिया, जिससे लाखों मरीजों की दवाइयां और अस्पताल बिलिंग रुक गई।",
        "what_happened_en": "On February 12, 2024, attackers logged into a legacy Citrix remote application portal using compromised credentials. The portal did not enforce MFA. Attackers lingered undetected for 9 days, moving laterally across the corporate network, exfiltrating 6 terabytes of patient medical data, and deploying BlackCat ransomware encrypting primary servers and backups on February 21.",
        "what_happened_hi": "हमलावरों ने चुराए गए पासवर्ड से बिना ओटीपी वाले पोर्टल में लॉगिन किया, 9 दिनों तक डेटा चुराया और फिर रैनसमवेयर चलाकर पूरे सिस्टम को लॉक कर दिया।",
        "who_is_affected_en": "Over 100 million patients (one-third of all Americans) whose PII/PHI was stolen; tens of thousands of physician practices and retail pharmacies facing insolvency due to delayed claim payments.",
        "who_is_affected_hi": "10 करोड़ से अधिक मरीज और हजारों अस्पताल और दवा दुकानें वित्तीय संकट में फंस गए।",
        "why_it_matters_en": "Demonstrated that a single forgotten remote access server lacking MFA can compromise critical national healthcare infrastructure. It highlighted how mergers and acquisitions create dangerous blindspots when legacy systems are not integrated into modern security baselines.",
        "why_it_matters_hi": "यह साबित करता है कि केवल एक बिना एमएफए वाला सर्वर पूरे देश के स्वास्थ्य तंत्र को पंगु बना सकता है।",
        "what_to_do_en": "1. Mandate Multi-Factor Authentication (MFA) across 100% of external-facing portals with zero exceptions.\n2. Implement network segmentation isolating healthcare claims processing from general corporate Active Directory.\n3. Maintain immutable, air-gapped backup vaults that cannot be deleted by compromised domain administrators.",
        "what_to_do_hi": "1. सभी रिमोट पोर्टल पर एमएफए अनिवार्य करें।\n2. संवेदनशील सर्वरों को अलग नेटवर्क में रखें।\n3. ऑफलाइन इम्यूटिएबल बैकअप रखें।",
        "meta": {
            "category": "Ransomware",
            "severity": "Critical",
            "financial_impact": "$2.5 Billion+",
            "technical_analysis": {
                "attack_vector": "Credential stuffing on an un-MFA'd Citrix Application Delivery Controller.",
                "cve_list": [],
                "mitre_tactics": ["Initial Access: Valid Accounts (T1078)", "Data Encrypted for Impact (T1486)", "Exfiltration Over C2 (T1048)"],
                "root_cause": "Legacy Citrix portal omitted from modern corporate Single Sign-On (SSO) MFA policy."
            },
            "behavioral_analysis": {
                "human_factor": "M&A Integration Neglect & False Security Assumptions.",
                "psychological_hooks": ["Assumption that internal servers are safe behind the firewall", "Lack of credential hygiene verification"],
                "organizational_gap": "Failure of IT asset management to decommission or enforce security policies on inherited infrastructure."
            },
            "key_takeaways": [
                "Zero exceptions for MFA: Every external portal must require multi-factor authentication.",
                "Audit all legacy assets immediately following any corporate merger or acquisition.",
                "Air-gap recovery infrastructure to eliminate extortion leverage."
            ]
        }
    },

    # 3. Snowflake Multi-Enterprise Credential Theft
    {
        "title": "Snowflake Cloud Campaign: Infostealers Harvest Credentials to Breach 165+ Major Corporations",
        "url": "https://www.cisa.gov/news-events/alerts/2024/06/05/cisa-and-partners-release-advisory-unc5537-targeting-snowflake-customer-database-environments",
        "published_at": _days_ago(95),
        "category": "Cloud & Identity",
        "severity": "Critical",
        "financial_impact": "Hundreds of Millions in Extortion and Class Action Lawsuits",
        "summary_en": "Cybercriminal syndicate UNC5537 targeted Snowflake cloud data warehouse customers whose accounts lacked Multi-Factor Authentication (MFA) and IP allowlisting, exfiltrating billions of consumer records from Ticketmaster, Santander Bank, Advance Auto Parts, and AT&T.",
        "summary_hi": "हैकर्स ने कर्मचारियों के कंप्यूटर से चुराए गए पासवर्ड का इस्तेमाल करके स्नोफ्लेक क्लाउड पर मौजूद 165 से ज्यादा बड़ी कंपनियों का अरबों रिकॉर्ड डेटा चुरा लिया।",
        "what_happened_en": "Attackers obtained credentials previously stolen by infostealer malware (Lumma, Redline, Vidar) from contractor personal devices. Between April and June 2024, they used an automated command-line tool ('frosty_go') to query the Snowflake API. For tenants that did not enforce MFA and had no IP network restrictions, the stolen passwords granted direct access to run SQL staging queries and export database tables.",
        "what_happened_hi": "हमलावरों ने इन्फोस्टीलर मैलवेयर द्वारा चुराए गए पासवर्ड का उपयोग किया। जिन कंपनियों ने एमएफए और आईपी रिस्ट्रिक्शन चालू नहीं किए थे, उनका सारा डेटा डाउनलोड कर लिया गया।",
        "who_is_affected_en": "Live Nation / Ticketmaster (560M customer tickets/barcodes), Santander Bank (30M customers/employees across 3 countries), Advance Auto Parts (380M customer profiles), and Neiman Marcus.",
        "who_is_affected_hi": "टिकटमास्टर (56 करोड़ ग्राहक), सैंटेंडर बैंक (3 करोड़ खाते) और एडवांस ऑटो पार्ट्स जैसी कंपनियां।",
        "why_it_matters_en": "Demonstrated the Cloud Shared Responsibility Model in action. Snowflake's underlying platform was not hacked; rather, client organizations failed to enforce basic identity hygiene (MFA and network policies) on high-value analytics databases.",
        "why_it_matters_hi": "क्लाउड सुरक्षा में कंपनी की जिम्मेदारी होती है कि वह अपने खातों पर एमएफए और आईपी सुरक्षा चालू रखे।",
        "what_to_do_en": "1. Enforce tenant-wide mandatory MFA across all Snowflake users without exception.\n2. Configure Network Policies (IP Allowlisting) restricting access strictly to corporate VPN IPs.\n3. Integrate Dark Web credential monitoring to detect compromised employee passwords proactively.",
        "what_to_do_hi": "1. सभी क्लाउड खातों पर एमएफए अनिवार्य करें।\n2. केवल कंपनी के अधिकृत आईपी से ही एक्सेस की अनुमति दें।\n3. डार्क वेब पर पासवर्ड लीक की नियमित निगरानी करें।",
        "meta": {
            "category": "Cloud & Identity",
            "severity": "Critical",
            "financial_impact": "$300 Million+ Estimated",
            "technical_analysis": {
                "attack_vector": "Credential stuffing using infostealer dumps via custom CLI utility ('frosty_go').",
                "cve_list": [],
                "mitre_tactics": ["Credential Stuffing (T1110.004)", "Cloud Data Staging (T1074.002)", "Exfiltration (T1567)"],
                "root_cause": "Absence of tenant-enforced MFA and absence of Network Policies (IP allowlisting)."
            },
            "behavioral_analysis": {
                "human_factor": "BYOD / Personal Computer Infostealer Infection.",
                "psychological_hooks": ["Convenience over security", "Password reuse between personal gaming/entertainment PCs and work accounts"],
                "organizational_gap": "Treating cloud databases as secure by default without configuring tenant-level access controls."
            },
            "key_takeaways": [
                "Cloud security is a shared responsibility: default settings are rarely sufficient.",
                "Personal devices used for remote work must never store corporate credentials without endpoint isolation.",
                "Network policies restricting IP ranges prevent credential theft from working from attacker machines."
            ]
        }
    },

    # 4. AT&T 110M Subscriber Call/Text Metadata Exfiltration
    {
        "title": "AT&T Data Exfiltration: Call and Text Records of 110M Customers Downloaded in Snowflake Breach",
        "url": "https://www.reuters.com/technology/cybersecurity/att-says-data-about-109-million-customer-accounts-downloaded-2024-07-12/",
        "published_at": _days_ago(120),
        "category": "Cloud & Identity",
        "severity": "Critical",
        "financial_impact": "$370,000 Ransom Paid to Delete Data; High Regulatory Fines",
        "summary_en": "Telecom giant AT&T disclosed that cybercriminals illegally downloaded customer call and text records covering virtually all of its 109 million wireless subscribers from an unsecured cloud database workspace.",
        "summary_hi": "टेलीकॉम कंपनी एटीएंडटी के 10.9 करोड़ ग्राहकों के कॉल और मैसेज रिकॉर्ड हैकर्स ने क्लाउड डेटाबेस से चुरा लिए।",
        "what_happened_en": "Attackers used stolen credentials obtained through infostealer malware to access an AT&T analytics workspace hosted on a third-party cloud platform. Between May 1 and May 5, 2024, the attackers exfiltrated historical call detail records (CDRs) from mid-2022 containing telephone numbers, interaction counts, and call durations. AT&T subsequently paid an extortionist 5.7 Bitcoin (~$370,000) to delete the stolen cache.",
        "what_happened_hi": "हैकर्स ने क्लाउड से 6 महीने का पूरा कॉल डेटा डाउनलोड कर लिया। कंपनी ने डेटा डिलीट करवाने के लिए फिरौती दी।",
        "who_is_affected_en": "109 million AT&T wireless customers, MVNO subscribers using AT&T's network, and high-profile government and law enforcement contacts.",
        "who_is_affected_hi": "लगभग सभी एटीएंडटी मोबाइल उपभोक्ता और सरकारी अधिकारी।",
        "why_it_matters_en": "Metadata reveals social graphs, relationships, and operational connections even without call audio. Foreign adversaries can use CDR metadata to identify covert operatives, confidential sources, and executive movements.",
        "why_it_matters_hi": "कॉल रिकॉर्ड्स से यह पता लगाया जा सकता है कि कौन किससे कब और कितनी देर बात करता है, जो राष्ट्रीय सुरक्षा के लिए बड़ा खतरा है।",
        "what_to_do_en": "1. Pseudonymize and tokenize call records in cloud analytics environments.\n2. Enforce strict egress limits on data analytics queries.\n3. Mandate FIDO2 hardware security keys for all database administrators.",
        "what_to_do_hi": "1. क्लाउड में संवेदनशील डेटा को हमेशा एन्क्रिप्ट और टोकनाइज़ करें।\n2. डेटा डाउनलोड करने की सीमाएं तय करें।\n3. हार्डवेयर सिक्योरिटी कीज (FIDO2) का उपयोग करें।",
        "meta": {
            "category": "Cloud & Identity",
            "severity": "Critical",
            "financial_impact": "High Strategic & Regulatory Impact",
            "technical_analysis": {
                "attack_vector": "Compromised cloud service account credentials.",
                "cve_list": [],
                "mitre_tactics": ["Valid Accounts (T1078)", "Automated Exfiltration (T1020)"],
                "root_cause": "Unrestricted bulk data extraction from active analytics workspace."
            },
            "behavioral_analysis": {
                "human_factor": "Data Over-Retention & Complacency.",
                "psychological_hooks": ["Assuming analytics staging data is low risk"],
                "organizational_gap": "Retaining massive unencrypted historical telecommunications metadata in active query tiers."
            },
            "key_takeaways": [
                "Metadata is as sensitive as payload content: protect call logs with the same rigor as passwords.",
                "Enforce anomaly detection on SQL query volume and export file sizes.",
                "Apply the principle of data minimization: delete historical staging tables when queries complete."
            ]
        }
    },

    # 5. CDK Global Auto Dealership Ransomware Crisis
    {
        "title": "CDK Global Ransomware Attack: BlackSuit Freezes 15,000 Car Dealerships Nationwide",
        "url": "https://www.bleepingcomputer.com/news/security/cdk-global-cyberattack-what-we-know-and-impact-on-car-dealers/",
        "published_at": _days_ago(150),
        "category": "Ransomware",
        "severity": "Critical",
        "financial_impact": "$1.0+ Billion Economic Impact; $25 Million Ransom Paid",
        "summary_en": "BlackSuit ransomware paralyzed CDK Global, the dominant SaaS provider for auto dealerships across North America, forcing 15,000 dealerships to halt digital sales, service schedules, and financing for nearly two weeks.",
        "summary_hi": "रैनसमवेयर हमले ने अमेरिका और कनाडा की 15,000 कार डीलरशिप्स के सॉफ्टवेयर को बंद कर दिया, जिससे दो हफ्ते तक गाड़ियों की बिक्री और सर्विसिंग ठप रही।",
        "what_happened_en": "On June 19, 2024, attackers gained access to CDK's internal infrastructure and VMware ESXi hypervisors. When CDK attempted to restore operations, the attackers struck a second time, forcing CDK to completely shut down its data centers. Dealership staff were forced to write sales contracts with pen and paper. CDK reportedly paid a $25 million cryptocurrency ransom to obtain the decryptor tool.",
        "what_happened_hi": "हैकर्स ने सर्वरों को लॉक कर दिया। डीलरशिप्स को हाथ से पेन और कागज पर गाड़ियां बेचनी पड़ीं। अंततः 2.5 करोड़ डॉलर की फिरौती दी गई।",
        "who_is_affected_en": "15,000 auto dealerships, publicly traded dealership groups (AutoNation, Sonic, Penske, Group 1), and millions of car buyers unable to register vehicles or repair cars.",
        "who_is_affected_hi": "15,000 कार डीलरशिप्स और लाखों ग्राहक।",
        "why_it_matters_en": "Illustrates the systemic supply chain risk posed by single-vendor vertical monopolies. When an entire retail sector relies on a single proprietary cloud SaaS vendor, a single ransomware incident causes industry-wide gridlock.",
        "why_it_matters_hi": "जब पूरा उद्योग सिर्फ एक सॉफ्टवेयर पर निर्भर होता है, तो एक हमला पूरे बाजार को रोक सकता है।",
        "what_to_do_en": "1. Isolate and harden virtual hypervisors (VMware ESXi / Proxmox) behind separate management subnets.\n2. Maintain offline business continuity playbooks for paper/manual operational resilience.\n3. Conduct comprehensive incident eradication before attempting to reconnect systems.",
        "what_to_do_hi": "1. वर्चुअल सर्वरों को मजबूत सुरक्षा में रखें।\n2. बिना कंप्यूटर के काम करने की ऑफलाइन प्रक्रियाएं तैयार रखें।\n3. सिस्टम को दोबारा चालू करने से पहले वायरस की पूरी जांच करें।",
        "meta": {
            "category": "Ransomware",
            "severity": "Critical",
            "financial_impact": "$1.0 Billion+ (Combined Dealership Revenue Loss)",
            "technical_analysis": {
                "attack_vector": "Compromised administrative credentials targeting ESXi hypervisors.",
                "cve_list": [],
                "mitre_tactics": ["Inhibit System Recovery (T1490)", "Data Encrypted for Impact (T1486)"],
                "root_cause": "Broad lateral access to hypervisor hosts without out-of-band management isolation."
            },
            "behavioral_analysis": {
                "human_factor": "Panic & Premature Restoration.",
                "psychological_hooks": ["Urgency to restore service leading to reinfection"],
                "organizational_gap": "Prematurely bringing services back online before establishing full containment."
            },
            "key_takeaways": [
                "Never rush restoration: eradicating the adversary's persistence mechanisms is mandatory.",
                "Hypervisors holding critical tenant virtual machines must be strictly segmented from enterprise networks.",
                "Every business must maintain manual failover processes for cloud outages."
            ]
        }
    },

    # 6. MGM Resorts & Caesars Social Engineering Heist
    {
        "title": "MGM Resorts $100M Hack: 10-Minute Phone Call to IT Helpdesk Bypasses Multi-Million Dollar Defenses",
        "url": "https://www.reuters.com/business/mgm-resorts-estimates-100-mln-hit-cybersecurity-issue-las-vegas-2023-10-05/",
        "published_at": _days_ago(380),
        "category": "Social Engineering",
        "severity": "Critical",
        "financial_impact": "$100M+ Operating Loss for MGM; $15M Ransom Paid by Caesars",
        "summary_en": "Cybercriminal group Scattered Spider breached MGM Resorts International using voice phishing (vishing) against the internal IT helpdesk, disabling hotel digital keys, casino slot machines, and reservations across Las Vegas.",
        "summary_hi": "हैकर्स ने केवल 10 मिनट के फोन कॉल में आईटी हेल्पडेस्क को बेवकूफ बनाकर लास वेगास के सबसे बड़े होटलों और कैसीनो को पूरी तरह बंद करवा दिया।",
        "what_happened_en": "Attackers identified an MGM employee on LinkedIn. They phoned the corporate IT helpdesk claiming to be that employee with a broken phone, requested an Okta password and MFA reset, and registered an attacker-controlled device. With administrator access, they pivoted across Microsoft Azure, compromised ESXi hypervisors, and deployed BlackCat ransomware. MGM refused to pay, enduring 10 days of total system downtime costing $100M.",
        "what_happened_hi": "हैकर्स ने लिंक्डइन से कर्मचारी का नाम पता किया, हेल्पडेस्क पर फोन करके झूठ बोला कि फोन टूट गया है और नया पासवर्ड ले लिया। इसके बाद पूरे नेटवर्क को हैक कर लिया।",
        "who_is_affected_en": "Hotel guests at Bellagio, MGM Grand, Mandalay Bay locked out of rooms; thousands of electronic casino games disabled; confidential PII of millions of guests exposed.",
        "who_is_affected_hi": "हजारों होटल मेहमान और कैसीनो खिलाड़ी प्रभावित हुए।",
        "why_it_matters_en": "The premier example of why the Human Firewall is the most critical layer in cybersecurity. Multi-million dollar firewalls and EDR agents were bypassed completely by a simple, persuasive phone conversation with a helpful IT helpdesk technician.",
        "why_it_matters_hi": "यह साबित करता है कि दुनिया का सबसे महंगा एंटीवायरस भी बेकार हो जाता है अगर इंसान फोन पर झांसे में आ जाए।",
        "what_to_do_en": "1. Mandate strict out-of-band video or in-person verification before resetting employee MFA tokens.\n2. Train helpdesk staff specifically against urgency and authority pretexting tactics.\n3. Implement dual-administrator authorization for identity provider privilege changes.",
        "what_to_do_hi": "1. पासवर्ड या एमएफए रीसेट करने से पहले वीडियो कॉल पर पहचान सत्यापन अनिवार्य करें।\n2. हेल्पडेस्क कर्मचारियों को फोन फ्रॉड के खिलाफ कड़ा प्रशिक्षण दें।\n3. एडमिन अधिकारों के लिए दोहरे अनुमोदन की व्यवस्था करें।",
        "meta": {
            "category": "Social Engineering",
            "severity": "Critical",
            "financial_impact": "$100 Million+ MGM / $15 Million Caesars",
            "technical_analysis": {
                "attack_vector": "Voice Phishing (Vishing) targeting internal IT Helpdesk.",
                "cve_list": [],
                "mitre_tactics": ["Spearphishing Voice (T1566.004)", "Account Manipulation (T1098)", "Hypervisor Encryption (T1486)"],
                "root_cause": "Helpdesk technician allowed password and MFA reset without secondary out-of-band identity verification."
            },
            "behavioral_analysis": {
                "human_factor": "Helpfulness Bias & Authority Pretexting.",
                "psychological_hooks": ["Pretexting a frustrating technical issue ('my phone is broken')", "Relying on public LinkedIn profile data to establish identity"],
                "organizational_gap": "Absence of a zero-trust identity verification protocol for IT support tickets."
            },
            "key_takeaways": [
                "The human element is the primary entry point: protect identity reset workflows above all else.",
                "Never accept public social media details as proof of identity.",
                "Enforce multi-party verification for high-risk identity modifications."
            ]
        }
    },

    # 7. Microsoft Corporate Midnight Blizzard Breach
    {
        "title": "Microsoft Midnight Blizzard Breach: Russian SVR Password Sprays Legacy Tenant to Spy on Executive Emails",
        "url": "https://www.cisa.gov/news-events/alerts/2024/04/11/cisa-releases-emergency-directive-mitigating-significant-risk-nation-state-compromise-microsoft",
        "published_at": _days_ago(320),
        "category": "Cloud & Identity",
        "severity": "Critical",
        "financial_impact": "High Strategic Espionage; Source Code Repositories Accessed",
        "summary_en": "Russian state espionage group Midnight Blizzard (SVR / APT29) breached Microsoft's internal corporate systems via a password spray attack on a non-MFA legacy test tenant, accessing executive email mailboxes and internal source code repositories.",
        "summary_hi": "रूसी सरकारी हैकर्स ने माइक्रोसॉफ्ट के पुराने टेस्ट सर्वर पर पासवर्ड स्प्रे हमला करके वरिष्ठ अधिकारियों के ईमेल और सोर्स कोड चुरा लिए।",
        "what_happened_en": "Beginning in late November 2023, attackers conducted a low-and-slow password spray attack against a legacy non-production test tenant that lacked MFA. After compromising a test account, the attackers created a malicious OAuth application with full Exchange Web Services (EWS) permissions and pivoted into Microsoft's primary corporate tenant, exfiltrating emails between Microsoft leadership and cybersecurity government liaisons.",
        "what_happened_hi": "हैकर्स ने पुराने सर्वर से शुरुआत की जहां एमएफए नहीं था, और वहां से कंपनी के मुख्य ईमेल सिस्टम में घुसपैठ कर ली।",
        "who_is_affected_en": "Microsoft senior leadership, cybersecurity researchers, and government agencies whose sensitive communications were stored in executive mailboxes.",
        "who_is_affected_hi": "माइक्रोसॉफ्ट के शीर्ष अधिकारी और कई सरकारी एजेंसियां।",
        "why_it_matters_en": "Illustrates that development, test, and legacy environments must be defended with the exact same rigor as production networks. Attackers consistently identify and exploit orphaned test tenants to bypass primary perimeter controls.",
        "why_it_matters_hi": "यह दिखाता है कि टेस्ट और पुराने सर्वर भी उतने ही सुरक्षित होने चाहिए जितने मुख्य सर्वर।",
        "what_to_do_en": "1. Enforce universal MFA across ALL tenants including sandbox, dev, and legacy environments.\n2. Regularly audit and eliminate broad OAuth app permissions (`full_access_as_app`).\n3. Decommission abandoned test environments and rotate service principal credentials quarterly.",
        "what_to_do_hi": "1. सभी टेस्ट और देव सर्वरों पर भी एमएफए लागू करें।\n2. ऐप अनुमतियों की नियमित समीक्षा करें।\n3. पुराने अप्रयुक्त खातों को तुरंत बंद करें।",
        "meta": {
            "category": "Cloud & Identity",
            "severity": "Critical",
            "financial_impact": "Strategic Cyber Espionage",
            "technical_analysis": {
                "attack_vector": "Low-and-slow Password Spraying against legacy OAuth-enabled tenant.",
                "cve_list": [],
                "mitre_tactics": ["Password Spraying (T1110.003)", "Additional Cloud Credentials (T1098.001)", "Email Collection (T1114)"],
                "root_cause": "Legacy test tenant excluded from tenant-wide Conditional Access MFA policy."
            },
            "behavioral_analysis": {
                "human_factor": "Dev/Test Security Complacency.",
                "psychological_hooks": ["Assuming non-production assets carry zero security risk"],
                "organizational_gap": "Siloed management allowing test environments to exist outside enterprise identity governance."
            },
            "key_takeaways": [
                "Attackers don't distinguish between dev and prod: every tenant must be protected.",
                "Password spraying bypasses lockout thresholds if executed slowly across multiple accounts.",
                "OAuth application permissions must be scrutinized and restricted to least privilege."
            ]
        }
    },

    # 8. MOVEit Transfer Global Mass SQL Injection Exploitation
    {
        "title": "MOVEit Transfer Mass Zero-Day Exploitation: Cl0p Hacks 2,700+ Organizations via SQL Injection",
        "url": "https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-158a",
        "published_at": _days_ago(440),
        "category": "Supply Chain",
        "severity": "Critical",
        "financial_impact": "Hundreds of Millions in Extortion Demands; 93M+ Individuals Impacted",
        "summary_en": "Ransomware group Cl0p weaponized an unauthenticated SQL injection zero-day (CVE-2023-34362) in Progress Software's MOVEit Transfer managed file transfer tool, stealing data from over 2,700 corporations and government agencies worldwide.",
        "summary_hi": "हैकिंग ग्रुप ने MOVEit सॉफ्टवेयर की एक कमी का फायदा उठाकर दुनिया भर की 2,700 से ज्यादा कंपनियों और 9 करोड़ लोगों का डेटा चुरा लिया।",
        "what_happened_en": "Over the US Memorial Day weekend, attackers executed automated SQL injection against internet-exposed MOVEit Transfer web interfaces. The injection allowed them to deploy a custom webshell ('LEMURLOOT') that extracted Azure Blob Storage credentials, bypassed authentication, and exfiltrated terabytes of sensitive payroll, pension, and customer databases.",
        "what_happened_hi": "छुट्टियों के सप्ताहांत में हमलावरों ने इंटरनेट से जुड़े सर्वरों पर एसक्यूएल इंजेक्शन हमला किया और वेबशेल डालकर सारा डेटा डाउनलोड कर लिया।",
        "who_is_affected_en": "2,700+ global entities including US Department of Energy, Siemens, Shell, BBC, British Airways, Sony, EY, and 93 million individuals.",
        "who_is_affected_hi": "बीबीसी, ब्रिटिश एयरवेज़, सीमेंस और दुनिया भर की 2,700 से ज्यादा कंपनियां।",
        "why_it_matters_en": "The largest mass data extortion event in cyber history. It proved that exposing managed file transfer (MFT) tools directly to the public internet creates existential supply chain vulnerability.",
        "why_it_matters_hi": "यह इतिहास का सबसे बड़ा डेटा चोरी हमला था जिसने दिखाया कि फाइल ट्रांसफर सॉफ्टवेयर को सीधे इंटरनेट पर खुला नहीं छोड़ना चाहिए।",
        "what_to_do_en": "1. Remove file transfer web interfaces from public internet exposure; place behind Zero Trust Network Access (ZTNA).\n2. Enforce automated file retention policies that purge data after transfer completion.\n3. Implement Web Application Firewall (WAF) rules blocking SQL injection payloads.",
        "what_to_do_hi": "1. फाइल ट्रांसफर सर्वरों को केवल वीपीएन के पीछे रखें।\n2. काम पूरा होते ही पुरानी फाइलों को ऑटोमैटिक डिलीट करें।\n3. वेब एप्लीकेशन फ़ायरवॉल (WAF) का उपयोग करें।",
        "meta": {
            "category": "Supply Chain",
            "severity": "Critical",
            "financial_impact": "Hundreds of Millions",
            "technical_analysis": {
                "attack_vector": "Unauthenticated SQL injection leading to remote webshell drop.",
                "cve_list": ["CVE-2023-34362 (CVSS 9.8)"],
                "mitre_tactics": ["Exploit Public-Facing Application (T1190)", "Server Software Component: Web Shell (T1505.003)"],
                "root_cause": "Improper input sanitization in web application SQL queries."
            },
            "behavioral_analysis": {
                "human_factor": "Vendor Appliance Blindspot.",
                "psychological_hooks": ["Belief that commercial COTS appliances are impenetrable"],
                "organizational_gap": "Treating file transfer servers as permanent storage repositories rather than temporary transit caches."
            },
            "key_takeaways": [
                "File transfer servers are transit pipes, not permanent storage: delete files after delivery.",
                "Never expose management appliances directly to the internet without a WAF and ZTNA barrier.",
                "Zero-day attacks frequently strike over holiday weekends to maximize response delays."
            ]
        }
    },

    # 9. Salt Typhoon Telecom Espionage Infiltration
    {
        "title": "Salt Typhoon Cyber Espionage: Chinese State Hackers Infiltrate US Telecom Wiretap Infrastructure",
        "url": "https://www.cisa.gov/news-events/news/cisa-and-fbi-release-joint-statement-peoples-republic-china-targeting-commercial-telecommunications-infrastructure",
        "published_at": _days_ago(180),
        "category": "Critical Infrastructure",
        "severity": "Critical",
        "financial_impact": "Critical National Security Breach; Core Router Infrastructure Compromised",
        "summary_en": "Chinese state-sponsored espionage group Salt Typhoon infiltrated the core network infrastructure of major US telecom providers (AT&T, Verizon, Lumen Technologies), targeting systems used for court-authorized federal wiretaps.",
        "summary_hi": "विदेशी सरकारी हैकर्स ने अमेरिका की सबसे बड़ी टेलीकॉम कंपनियों के मुख्य नेटवर्क में सेंध लगाकर फोन टैपिंग सिस्टम को हैक कर लिया।",
        "what_happened_en": "The threat actors compromised commercial edge routers (Cisco, Juniper) by exploiting unpatched firmware vulnerabilities and using stolen administrative credentials. They established persistent presence inside carrier core networks, accessing private communications and systems utilized by the federal government under CALEA (Communications Assistance for Law Enforcement Act).",
        "what_happened_hi": "हैकर्स ने कोर राउटर्स में बैकडोर बनाकर सरकारी अधिकारियों और नेताओं की बातचीत और कॉल डेटा को इंटरसेप्ट किया।",
        "who_is_affected_en": "Senior political figures, national security officials, telecommunications carriers, and millions of mobile users whose call routing paths traversed compromised carrier backbones.",
        "who_is_affected_hi": "शीर्ष राजनीतिक नेता, राष्ट्रीय सुरक्षा अधिकारी और टेलीकॉम कंपनियां।",
        "why_it_matters_en": "Demonstrated the strategic vulnerability of core networking infrastructure. Threat actors who control the routing layer can intercept, manipulate, and monitor communications without touching endpoint devices.",
        "why_it_matters_hi": "यदि हैकर्स मुख्य नेटवर्क राउटर को हैक कर लें, तो वे किसी भी फोन या कंप्यूटर की बातचीत सुन सकते हैं।",
        "what_to_do_en": "1. Regularly audit and verify cryptographic checksums on router firmware against vendor baselines.\n2. Place lawful interception and wiretap compliance platforms on physically isolated out-of-band management networks.\n3. Replace end-of-life edge network hardware and enforce centralized AAA access logging.",
        "what_to_do_hi": "1. राउटर्स के फर्मवेयर की नियमित जांच करें।\n2. संवेदनशील सिस्टम्स को अलग नेटवर्क पर रखें।\n3. पुराने नेटवर्क उपकरणों को तुरंत बदलें।",
        "meta": {
            "category": "Critical Infrastructure",
            "severity": "Critical",
            "financial_impact": "Critical National Security Threat",
            "technical_analysis": {
                "attack_vector": "Edge router firmware exploitation and credential theft.",
                "cve_list": [],
                "mitre_tactics": ["Exploit Public-Facing Application (T1190)", "Modify Authentication (T1556)", "Network Sniffing (T1040)"],
                "root_cause": "Long-term unpatched firmware vulnerabilities in edge routing infrastructure."
            },
            "behavioral_analysis": {
                "human_factor": "Edge Infrastructure Neglect.",
                "psychological_hooks": ["Reluctance to reboot or patch critical routing hardware due to service downtime fears"],
                "organizational_gap": "Treating core routing hardware as 'set and forget' rather than active zero-trust endpoints."
            },
            "key_takeaways": [
                "Network routers and firewalls are prime targets for nation-state espionage: patch them proactively.",
                "Isolate compliance and wiretap platforms on dedicated air-gapped management planes.",
                "Monitor routing tables for anomalous BGP and internal gateway protocol modifications."
            ]
        }
    },

    # 10. Synnovis NHS Hospitals Pathology Ransomware Crisis
    {
        "title": "Synnovis NHS Ransomware Attack: Qilin Halts 10,000+ Surgeries and Blood Tests in London Hospitals",
        "url": "https://www.england.nhs.uk/synnovis-cyber-incident/",
        "published_at": _days_ago(210),
        "category": "Ransomware",
        "severity": "Critical",
        "financial_impact": "Severe Clinical Impact; Over 10,000 Outpatient Surgeries Delayed",
        "summary_en": "Russian-speaking ransomware syndicate Qilin attacked Synnovis, the critical pathology provider for King's College Hospital and Guy's and St Thomas' NHS Trust in London, crippling blood testing, cancer operations, and emergency care.",
        "summary_hi": "लंदन के प्रमुख अस्पतालों को रक्त जांच सेवा देने वाली कंपनी पर रैनसमवेयर हमले के कारण 10,000 से अधिक सर्जरी और इलाज टालने पड़े।",
        "what_happened_en": "Qilin ransomware operators penetrated Synnovis's corporate network through vulnerable remote access software. They encrypted laboratory information management systems (LIMS) and exfiltrated 400 GB of confidential patient data, demanding $50 million. The encryption prevented blood transfusions and automated pathology matching, forcing hospitals to appeal for emergency O-type blood donors and operate manually.",
        "what_happened_hi": "हैकर्स ने लैब सिस्टम को लॉक कर दिया। ब्लड मैचिंग न होने के कारण जीवन रक्षक ऑपरेशन और कैंसर इलाज रोकने पड़े।",
        "who_is_affected_en": "King's College Hospital, Guy's and St Thomas' Hospital, Royal Brompton, Harefield Hospital, primary care GP clinics, and thousands of cancer/transplant patients.",
        "who_is_affected_hi": "हजारों गंभीर मरीज, कैंसर रोगी और लंदन के बड़े अस्पताल।",
        "why_it_matters_en": "Demonstrated that cyber attacks directly endanger human lives. Criminal cartels deliberately target healthcare suppliers because the life-or-death pressure maximizes extortion leverage.",
        "why_it_matters_hi": "यह साबित करता है कि साइबर हमले सिर्फ डेटा चोरी नहीं बल्कि इंसानी जान के लिए सीधा खतरा बन चुके हैं।",
        "what_to_do_en": "1. Enforce strict network isolation between laboratory medical devices and corporate office networks.\n2. Maintain paper and manual clinical continuity procedures tested through realistic emergency drills.\n3. Implement 24/7 endpoint detection with rapid automated network quarantine capabilities.",
        "what_to_do_hi": "1. मेडिकल मशीनों को सामान्य ऑफिस नेटवर्क से बिल्कुल अलग रखें।\n2. बिना कंप्यूटर के काम करने के लिए आपातकालीन ड्रिल करें।\n3. 24 घंटे सुरक्षा निगरानी और ऑटोमैटिक अलगाव की व्यवस्था रखें।",
        "meta": {
            "category": "Ransomware",
            "severity": "Critical",
            "financial_impact": "Critical Human Life Impact",
            "technical_analysis": {
                "attack_vector": "Compromised remote access credentials and unpatched gateway appliances.",
                "cve_list": [],
                "mitre_tactics": ["Data Encrypted for Impact (T1486)", "Exfiltration to Cloud (T1567)"],
                "root_cause": "Critical pathology infrastructure hosted on shared unsegmented corporate network."
            },
            "behavioral_analysis": {
                "human_factor": "Supply Chain Vulnerability Blindspot.",
                "psychological_hooks": ["Extortionists exploiting human life pressure for financial ransom"],
                "organizational_gap": "Hospitals outsourcing critical diagnostic infrastructure without auditing vendor security controls."
            },
            "key_takeaways": [
                "Healthcare supply chains require rigorous third-party cyber risk assessment.",
                "Clinical teams must be trained to transition seamlessly to manual paper procedures during cyber outages.",
                "Ransomware gangs do not care about human life: defense and resilience are the only safety."
            ]
        }
    },

    # 11. WazirX Crypto Exchange Multi-Sig Breach
    {
        "title": "WazirX Crypto Hack: $235M Stolen in Multi-Sig Smart Contract Blind Signing Breach",
        "url": "https://www.reuters.com/technology/cybersecurity/indias-wazirx-cyber-attack-leads-theft-digital-assets-worth-235-mln-2024-07-18/",
        "published_at": _days_ago(240),
        "category": "Corporate & Financial",
        "severity": "Critical",
        "financial_impact": "$234.9 Million (Over 45% of Platform Reserves)",
        "summary_en": "Indian cryptocurrency exchange WazirX suffered a major cyber heist losing $235 million in digital assets when attackers compromised a 4-of-6 multi-signature custody wallet through transaction payload manipulation and blind signing.",
        "summary_hi": "भारत के प्रमुख क्रिप्टो एक्सचेंज वज़ीरएक्स से हैकर्स ने 23.5 करोड़ डॉलर (लगभग 2,000 करोड़ रुपये) के डिजिटल एसेट्स चुरा लिए।",
        "what_happened_en": "The attack targeted a multi-signature wallet co-managed between WazirX and third-party custody provider Liminal. Attackers manipulated the transaction payload displayed on the hardware signer interfaces. While the screen showed normal operations, the underlying cryptographic data upgraded a Gnosis Safe implementation contract to an attacker-controlled smart contract that drained Ethereum, Shiba Inu, and Polygon tokens.",
        "what_happened_hi": "हैकर्स ने ट्रांजैक्शन डेटा में हेरफेर किया। स्क्रीन पर सामान्य काम दिख रहा था, लेकिन अंदरूनी कोड ने वॉलेट का पूरा नियंत्रण हैकर को सौंप दिया।",
        "who_is_affected_en": "Over 4 million Indian cryptocurrency investors whose accounts and withdrawals were frozen indefinitely.",
        "who_is_affected_hi": "40 लाख से ज्यादा भारतीय निवेशक जिनके पैसे अटक गए।",
        "why_it_matters_en": "Highlights the danger of Blind Signing in digital asset custody. Even with multi-signature hardware tokens, if key signers cannot independently verify the raw transaction byte code, the entire approval workflow fails.",
        "why_it_matters_hi": "यह दिखाता है कि बिना असली कोड को समझे सिर्फ स्क्रीन देखकर 'ओके' कर देना करोड़ों का नुकसान करवा सकता है।",
        "what_to_do_en": "1. Mandate Clear Signing: Never approve cryptographic transactions without verifying the human-readable destination address and function call.\n2. Implement rate limits and time locks on treasury withdrawals exceeding preset thresholds.\n3. Conduct regular independent penetration testing on multi-sig orchestration platforms.",
        "what_to_do_hi": "1. कोड और पते की पूरी जांच किए बिना कभी भी डिजिटल हस्ताक्षर न करें।\n2. बड़े वित्तीय भुगतानों पर टाइम-लॉक और निकासी सीमा लगाएं।\n3. नियमित सुरक्षा ऑडिट करवाएं।",
        "meta": {
            "category": "Corporate & Financial",
            "severity": "Critical",
            "financial_impact": "$234.9 Million",
            "technical_analysis": {
                "attack_vector": "Smart contract payload manipulation and blind signing compromise.",
                "cve_list": [],
                "mitre_tactics": ["Compromise Software Dependencies (T1195.002)", "Financial Theft"],
                "root_cause": "Mismatch between displayed transaction metadata and raw payload executed on the blockchain."
            },
            "behavioral_analysis": {
                "human_factor": "Blind Signing Complacency.",
                "psychological_hooks": ["Routine administrative signing without independent byte verification", "Over-reliance on UI display accuracy"],
                "organizational_gap": "Lack of time-delay locks on multi-million dollar treasury transfers."
            },
            "key_takeaways": [
                "Clear signing is essential: never sign what your hardware wallet cannot independently parse and verify.",
                "Multi-signature security fails if the orchestrating interface is untrusted or compromised.",
                "Enforce timelocks on major corporate treasury withdrawals to allow defense intervention."
            ]
        }
    },

    # 12. Halliburton Energy Operations Ransomware
    {
        "title": "Halliburton Energy Systems Severed: RansomHub Attack Forces Global Oilfield Giant Offline",
        "url": "https://www.reuters.com/business/energy/us-energy-firm-halliburton-hit-by-cyberattack-2024-08-21/",
        "published_at": _days_ago(270),
        "category": "Critical Infrastructure",
        "severity": "High",
        "financial_impact": "Operational Disruptions Across Global Oilfield Services",
        "summary_en": "Oilfield services giant Halliburton was struck by a cyber attack attributed to the RansomHub syndicate, forcing the company to sever external network connections and take systems offline at its primary Houston campus.",
        "summary_hi": "वैश्विक ऊर्जा दिग्गज हैलिबर्टन पर रैनसमवेयर हमले के कारण कंपनी को अपने सभी कंप्यूटर और नेटवर्क को तुरंत इंटरनेट से काटना पड़ा।",
        "what_happened_en": "On August 21, 2024, attackers gained access to Halliburton's corporate networks. Upon detecting anomalous activity, the company activated its incident response plan, severed external connections, and notified law enforcement, filing an 8-K disclosure with the US SEC. The proactive network disconnection prevented lateral spread into critical industrial operational technology (OT) oil drilling systems.",
        "what_happened_hi": "हैकर्स के घुसते ही कंपनी ने तुरंत सारे नेटवर्क कनेक्शन काट दिए, जिससे हमला तेल ड्रिलिंग मशीनों तक नहीं पहुंच पाया।",
        "who_is_affected_en": "Global oilfield exploration clients, international operations across 70+ countries, and corporate IT operations.",
        "who_is_affected_hi": "दुनिया भर की तेल कंपनियां और आंतरिक ऑपरेशंस।",
        "why_it_matters_en": "Demonstrates the effectiveness of rapid, decisive network containment. While business operations suffered temporary disruption, swift disconnection prevented ransomware from impacting industrial SCADA and OT equipment.",
        "why_it_matters_hi": "यह दिखाता है कि समय रहते तुरंत नेटवर्क अलग करने से कितना बड़ा नुकसान होने से बच सकता है।",
        "what_to_do_en": "1. Maintain strict physical and logical air-gaps between IT corporate networks and OT industrial systems.\n2. Conduct regular tabletop exercises testing emergency network severance procedures.\n3. Implement 24/7 EDR monitoring capable of detecting unauthorized command execution.",
        "what_to_do_hi": "1. कॉर्पोरेट ऑफिस और औद्योगिक मशीनों के नेटवर्क को हमेशा अलग रखें।\n2. इमरजेंसी में नेटवर्क काटने के लिए नियमित मॉक ड्रिल करें।\n3. चौबीसों घंटे निगरानी रखें।",
        "meta": {
            "category": "Critical Infrastructure",
            "severity": "High",
            "financial_impact": "Significant Operational Disruption",
            "technical_analysis": {
                "attack_vector": "Enterprise network intrusion attributed to RansomHub cartel.",
                "cve_list": [],
                "mitre_tactics": ["Initial Access (T1190)", "Data Encrypted for Impact (T1486)"],
                "root_cause": "Attempted enterprise encryption thwarted by rapid network severance."
            },
            "behavioral_analysis": {
                "human_factor": "Decisive Incident Leadership.",
                "psychological_hooks": ["Fear of operational downtime causing hesitation"],
                "organizational_gap": "Overcoming organizational hesitation to sever external connectivity during active incidents."
            },
            "key_takeaways": [
                "Decisive containment saves the core business: never hesitate to sever network links during active intrusion.",
                "Air-gapping between IT and OT systems is non-negotiable for critical infrastructure.",
                "Pre-approved emergency containment protocols empower responders to act without executive delays."
            ]
        }
    }
]

