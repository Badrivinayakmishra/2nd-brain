"""
Automated Security Training Content Delivery
Provides security training content for employees

SOC 2 Requirements:
- CC1.4: Security awareness training content
- CC1.5: Ongoing training programs
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class TrainingLesson:
    """Training lesson content"""
    lesson_id: str
    title: str
    content: str
    duration_minutes: int
    quiz_questions: List[Dict[str, Any]]
    learning_objectives: List[str]


class SecurityTrainingContent:
    """
    Security training content library

    Features:
    - Comprehensive security training modules
    - Interactive quizzes
    - Progress tracking
    - Certification generation
    """

    def __init__(self):
        """Initialize training content"""
        self.modules = self._initialize_training_modules()
        print(f"✓ Security Training Content initialized")
        print(f"  - Training modules: {len(self.modules)}")

    def _initialize_training_modules(self) -> Dict[str, Dict]:
        """Initialize comprehensive training modules"""
        modules = {}

        # ===== Module 1: Security Basics =====
        modules['security_basics'] = {
            "module_id": "security_basics",
            "title": "Security Basics & Best Practices",
            "description": "Foundational security awareness training",
            "duration_minutes": 30,
            "required": True,
            "lessons": [
                self._create_password_security_lesson(),
                self._create_phishing_awareness_lesson(),
                self._create_device_security_lesson(),
            ]
        }

        # ===== Module 2: Data Protection =====
        modules['data_protection'] = {
            "module_id": "data_protection",
            "title": "Data Protection & Privacy",
            "description": "GDPR, data classification, and sensitive data handling",
            "duration_minutes": 45,
            "required": True,
            "lessons": [
                self._create_data_classification_lesson(),
                self._create_gdpr_lesson(),
                self._create_data_handling_lesson(),
            ]
        }

        # ===== Module 3: Incident Response =====
        modules['incident_response'] = {
            "module_id": "incident_response",
            "title": "Incident Response Procedures",
            "description": "How to recognize and report security incidents",
            "duration_minutes": 30,
            "required": True,
            "lessons": [
                self._create_incident_recognition_lesson(),
                self._create_incident_reporting_lesson(),
            ]
        }

        # ===== Module 4: Social Engineering =====
        modules['social_engineering'] = {
            "module_id": "social_engineering",
            "title": "Social Engineering Awareness",
            "description": "Recognizing and preventing social engineering attacks",
            "duration_minutes": 25,
            "required": True,
            "lessons": [
                self._create_social_engineering_lesson(),
                self._create_pretexting_lesson(),
            ]
        }

        # ===== Module 5: Secure Coding (Engineers) =====
        modules['secure_coding'] = {
            "module_id": "secure_coding",
            "title": "Secure Coding Practices",
            "description": "OWASP Top 10 and secure development practices",
            "duration_minutes": 60,
            "required": False,
            "lessons": [
                self._create_owasp_top10_lesson(),
                self._create_input_validation_lesson(),
                self._create_authentication_lesson(),
            ]
        }

        # ===== Module 6: SOC 2 Compliance =====
        modules['soc2_compliance'] = {
            "module_id": "soc2_compliance",
            "title": "SOC 2 & Compliance Overview",
            "description": "Understanding SOC 2 and employee responsibilities",
            "duration_minutes": 40,
            "required": True,
            "lessons": [
                self._create_soc2_overview_lesson(),
                self._create_employee_responsibilities_lesson(),
            ]
        }

        return modules

    def _create_password_security_lesson(self) -> TrainingLesson:
        """Create password security lesson"""
        return TrainingLesson(
            lesson_id="password_security",
            title="Password Security",
            content="""
# Password Security Best Practices

## Why Password Security Matters

Weak passwords are the #1 cause of security breaches. A strong password is your first line of defense.

## Creating Strong Passwords

✅ **DO:**
- Use at least 12 characters
- Include uppercase, lowercase, numbers, and symbols
- Use a passphrase: "Coffee!Laptop@Morning2024"
- Use a unique password for each account
- Use a password manager (LastPass, 1Password, Bitwarden)

❌ **DON'T:**
- Use dictionary words
- Use personal information (birthday, name, pet name)
- Reuse passwords across sites
- Share passwords with anyone
- Write passwords on sticky notes

## Multi-Factor Authentication (MFA)

**Always enable MFA when available!**

MFA adds a second layer of security:
1. Something you know (password)
2. Something you have (phone, security key)
3. Something you are (fingerprint, face)

Even if your password is compromised, MFA protects your account.

## Password Manager Best Practices

1. Use a strong master password
2. Enable MFA on your password manager
3. Regularly update critical passwords
4. Never share your master password

## What to Do If Compromised

If you suspect your password is compromised:
1. **Immediately** change the password
2. Enable MFA if not already enabled
3. Check for unauthorized access
4. Report to IT/Security team
5. Change passwords on any sites using the same password

## Company Policy

- Passwords must be changed every 90 days
- MFA is **required** for all company accounts
- Never share your password, even with IT
- Report suspicious login attempts immediately
            """,
            duration_minutes=10,
            quiz_questions=[
                {
                    "question": "What is the minimum recommended password length?",
                    "options": ["8 characters", "10 characters", "12 characters", "16 characters"],
                    "correct_answer": 2,
                    "explanation": "12 characters minimum provides adequate security against brute force attacks."
                },
                {
                    "question": "What does MFA stand for?",
                    "options": ["Multi-Factor Authentication", "My First Authentication", "Maximum Force Access", "Multiple File Access"],
                    "correct_answer": 0,
                    "explanation": "MFA (Multi-Factor Authentication) adds multiple layers of security."
                },
                {
                    "question": "Should you reuse passwords across different accounts?",
                    "options": ["Yes, for convenience", "No, never", "Only for unimportant sites", "Only if they're strong"],
                    "correct_answer": 1,
                    "explanation": "Never reuse passwords - if one site is breached, all your accounts are at risk."
                }
            ],
            learning_objectives=[
                "Understand password security principles",
                "Create strong, unique passwords",
                "Use multi-factor authentication",
                "Respond appropriately to password compromise"
            ]
        )

    def _create_phishing_awareness_lesson(self) -> TrainingLesson:
        """Create phishing awareness lesson"""
        return TrainingLesson(
            lesson_id="phishing_awareness",
            title="Phishing Attack Recognition",
            content="""
# Recognizing Phishing Attacks

## What is Phishing?

Phishing is a social engineering attack where attackers impersonate legitimate organizations to steal credentials, data, or money.

## Common Phishing Techniques

### 1. Email Phishing
**Red Flags:**
- Urgent language: "Your account will be closed!"
- Suspicious sender: ceo@compny.com (note the typo)
- Generic greetings: "Dear Customer"
- Requests for credentials or personal information
- Unexpected attachments or links
- Poor grammar and spelling

**Example:**
```
From: security@paypa1.com (note the "1" instead of "l")
Subject: Urgent: Verify Your Account Now!

Dear Customer,

Your account has been compromised. Click here immediately to verify:
http://paypal-security-verification.sketchy-site.com

Failure to verify within 24 hours will result in permanent account closure.

Security Team
```

### 2. Spear Phishing
Targeted attacks using personal information:
- Uses your name, job title, recent activities
- References real projects or colleagues
- Appears to come from someone you know

### 3. Whaling
Phishing targeting executives:
- CEO fraud: "Wire this money urgently"
- Board meeting invitations with malicious links
- Executive-level information requests

### 4. SMS Phishing (Smishing)
```
Your bank account has been locked.
Click: bit.ly/unlock-acct123 to restore access.
```

### 5. Voice Phishing (Vishing)
Phone calls claiming to be:
- IT support needing your password
- IRS demanding payment
- Tech support detecting viruses

## How to Protect Yourself

✅ **DO:**
1. Verify sender email addresses carefully
2. Hover over links before clicking (check URL)
3. Go directly to websites instead of clicking links
4. Call the sender using a known number to verify
5. Report suspicious emails to security@company.com

❌ **DON'T:**
1. Click links in unexpected emails
2. Download unexpected attachments
3. Provide credentials via email/phone
4. Trust urgency - legitimate companies won't threaten you

## Reporting Phishing

**If you receive a phishing email:**
1. Don't click anything
2. Forward to security@company.com
3. Mark as phishing/spam
4. Delete the email

**If you clicked a phishing link:**
1. Immediately change your password
2. Enable MFA if not already enabled
3. Report to IT/Security immediately
4. Scan your device for malware

## Real-World Example

✅ **Legitimate:**
```
From: billing@company.com
Subject: Monthly Invoice #12345

Hi John,

Your monthly invoice is available in your account dashboard.

Log in at: https://company.com/dashboard

Thanks,
Billing Team
```

❌ **Phishing:**
```
From: billing@company-invoice.com
Subject: URGENT: Invoice Payment Required

Dear Customer,

Your invoice is OVERDUE. Click here immediately:
http://company-billing-payment.suspicious.com

Failure to pay will result in service termination.

Billing Department
```
            """,
            duration_minutes=15,
            quiz_questions=[
                {
                    "question": "What is a red flag in a phishing email?",
                    "options": [
                        "Professional formatting",
                        "Urgent language and threats",
                        "Personalized greeting",
                        "Company logo"
                    ],
                    "correct_answer": 1,
                    "explanation": "Phishing emails often use urgent language to pressure you into acting quickly without thinking."
                },
                {
                    "question": "What should you do if you receive a suspicious email?",
                    "options": [
                        "Click the link to investigate",
                        "Forward it to security@company.com",
                        "Reply asking if it's legitimate",
                        "Ignore it"
                    ],
                    "correct_answer": 1,
                    "explanation": "Always report suspicious emails to your security team so they can investigate and protect others."
                },
                {
                    "question": "How can you verify if a link is safe?",
                    "options": [
                        "Click it to see where it goes",
                        "Hover over it to see the actual URL",
                        "Trust the sender",
                        "Check if it has HTTPS"
                    ],
                    "correct_answer": 1,
                    "explanation": "Hovering over a link shows the actual destination URL before clicking."
                }
            ],
            learning_objectives=[
                "Recognize common phishing techniques",
                "Identify red flags in emails",
                "Respond appropriately to suspected phishing",
                "Report phishing attempts to security team"
            ]
        )

    def _create_device_security_lesson(self) -> TrainingLesson:
        """Create device security lesson"""
        return TrainingLesson(
            lesson_id="device_security",
            title="Device & Endpoint Security",
            content="""
# Device Security Best Practices

## Laptop/Computer Security

### Physical Security
✅ **DO:**
- Lock your screen when stepping away (Windows: Win+L, Mac: Cmd+Ctrl+Q)
- Use a privacy screen in public places
- Keep devices physically secure
- Enable "Find My Device"
- Encrypt your hard drive (BitLocker, FileVault)

❌ **DON'T:**
- Leave devices unattended in public
- Loan your work device to others
- Leave sensitive documents visible on screen
- Connect to unknown USB devices

### Software Security
✅ **DO:**
- Keep operating system updated
- Install security updates immediately
- Use company-approved antivirus
- Enable firewall
- Only install approved software

❌ **DON'T:**
- Ignore update notifications
- Disable antivirus
- Install pirated software
- Use unauthorized cloud storage

## Mobile Device Security

### Smartphone Security
✅ **DO:**
- Use strong passcode (not 1234!)
- Enable biometric auth (fingerprint/face)
- Install MDM profile if required
- Keep OS and apps updated
- Only install apps from official stores
- Enable remote wipe capability

❌ **DON'T:**
- Jailbreak or root your device
- Install apps from unknown sources
- Connect to untrusted devices
- Disable security features

### Public Wi-Fi Safety
**NEVER use public Wi-Fi for:**
- Accessing company systems
- Banking or financial transactions
- Entering passwords
- Accessing sensitive data

**If you must use public Wi-Fi:**
1. Use company VPN
2. Verify network name with staff
3. Disable auto-connect to Wi-Fi
4. Use mobile hotspot instead when possible

## Home Network Security

✅ **DO:**
- Change default router password
- Use WPA3 encryption
- Update router firmware
- Use a strong Wi-Fi password
- Separate guest network
- Disable WPS

## Lost or Stolen Device

**Immediately report to IT/Security if device is lost or stolen:**

1. Call IT/Security: [phone number]
2. We will remotely wipe the device
3. Change all passwords
4. Monitor for suspicious activity
5. File police report if stolen

## Bring Your Own Device (BYOD)

If using personal devices for work:
- Install company MDM profile
- Use separate work/personal data
- Agree to remote wipe for company data
- Follow same security policies
- Report loss/theft immediately
            """,
            duration_minutes=10,
            quiz_questions=[
                {
                    "question": "What should you do when stepping away from your computer?",
                    "options": [
                        "Leave it as is",
                        "Close all windows",
                        "Lock the screen",
                        "Shut it down"
                    ],
                    "correct_answer": 2,
                    "explanation": "Always lock your screen when stepping away to prevent unauthorized access."
                },
                {
                    "question": "Is it safe to use public Wi-Fi for work?",
                    "options": [
                        "Yes, always",
                        "Only with company VPN",
                        "Only for email",
                        "Never"
                    ],
                    "correct_answer": 1,
                    "explanation": "Public Wi-Fi can be monitored by attackers. Always use VPN to encrypt your connection."
                },
                {
                    "question": "What should you do if your work device is stolen?",
                    "options": [
                        "Wait to see if it's returned",
                        "Immediately report to IT/Security",
                        "Try to track it yourself",
                        "Buy a new one"
                    ],
                    "correct_answer": 1,
                    "explanation": "Immediate reporting allows IT to remotely wipe the device and protect company data."
                }
            ],
            learning_objectives=[
                "Secure work devices physically and digitally",
                "Use public Wi-Fi safely",
                "Respond to lost/stolen devices",
                "Maintain home network security"
            ]
        )

    def _create_data_classification_lesson(self) -> TrainingLesson:
        """Create data classification lesson"""
        return TrainingLesson(
            lesson_id="data_classification",
            title="Data Classification & Handling",
            content="""
# Data Classification & Handling

## Why Data Classification Matters

Not all data has the same sensitivity level. Proper classification ensures appropriate protection.

## Classification Levels

### 🌍 PUBLIC
**Definition:** Information that can be freely shared
**Examples:**
- Marketing materials
- Public website content
- Press releases
- Job postings

**Handling:**
- No special protection required
- Can be shared externally
- Can be posted on public websites

---

### 🏢 INTERNAL
**Definition:** Information for internal use only
**Examples:**
- Internal policies
- Employee directories
- Meeting notes
- Project plans (non-confidential)

**Handling:**
- Share only with employees
- Don't post publicly
- Use company email/systems
- No special encryption required

---

### 🔒 CONFIDENTIAL
**Definition:** Sensitive business information
**Examples:**
- Financial reports
- Business strategies
- Customer lists
- Source code
- Contracts

**Handling:**
- Share only with authorized personnel
- Encrypt when sending externally
- Use secure file sharing
- Mark documents "CONFIDENTIAL"
- Shred when disposing

---

### 🚨 RESTRICTED
**Definition:** Highly sensitive data requiring maximum protection
**Examples:**
- Customer PII (SSN, credit cards, health data)
- Authentication credentials
- Encryption keys
- Legal documents under NDA
- Trade secrets

**Handling:**
- Strict need-to-know access only
- Always encrypt (at rest and in transit)
- Log all access
- Sanitize before using in AI/analytics
- Secure disposal (DoD 5220.22-M standard)
- Report any breach immediately

## Data Handling Examples

### ✅ CORRECT Handling

**Scenario:** Sharing a customer report
**CONFIDENTIAL data:**
1. Verify recipient needs access
2. Send via encrypted email
3. Mark "CONFIDENTIAL"
4. Log the transmission

**Scenario:** Customer support case
**RESTRICTED data (SSN):**
1. Sanitize PII before logging
2. Access only in secure system
3. Don't include in tickets
4. Never send via email

### ❌ INCORRECT Handling

**DON'T:**
- ❌ Email passwords or SSNs
- ❌ Post CONFIDENTIAL data in public Slack
- ❌ Upload RESTRICTED data to personal cloud
- ❌ Discuss CONFIDENTIAL info in public
- ❌ Leave printed CONFIDENTIAL docs on desk
- ❌ Use customer PII in test data

## Data in Different Contexts

### Email
- RESTRICTED: Never send via email
- CONFIDENTIAL: Encrypted email only
- INTERNAL: Company email OK
- PUBLIC: Any email OK

### Cloud Storage
- RESTRICTED: Company-approved encrypted storage only
- CONFIDENTIAL: Company-approved storage only
- INTERNAL: Company storage
- PUBLIC: Any storage

### AI/LLM Processing
- RESTRICTED: MUST sanitize PII first
- CONFIDENTIAL: Use zero-retention AI (Azure OpenAI Enterprise)
- INTERNAL: Company-approved AI only
- PUBLIC: Any AI OK

### Printing
- RESTRICTED: Minimize printing, shred immediately after use
- CONFIDENTIAL: Print only when necessary, shred when done
- INTERNAL: Normal printing
- PUBLIC: Normal printing

## Data Disposal

### Digital Disposal
- RESTRICTED/CONFIDENTIAL: Secure deletion (3-pass overwrite)
- INTERNAL: Normal deletion
- PUBLIC: Normal deletion

### Physical Disposal
- RESTRICTED/CONFIDENTIAL: Cross-cut shred or burn
- INTERNAL: Shred or recycle
- PUBLIC: Recycle

## Questions to Ask

Before handling any data, ask:
1. What classification level is this?
2. Am I authorized to access it?
3. How should I protect it?
4. How should I share it (if at all)?
5. How should I dispose of it?

## Violations

**Report immediately if you:**
- Accidentally send RESTRICTED/CONFIDENTIAL data to wrong person
- Find unprotected sensitive data
- Suspect a data breach
- Receive data you shouldn't have access to

**Contact:** security@company.com or call [number]
            """,
            duration_minutes=15,
            quiz_questions=[
                {
                    "question": "Which classification requires encryption?",
                    "options": ["PUBLIC", "INTERNAL", "CONFIDENTIAL and RESTRICTED", "Only RESTRICTED"],
                    "correct_answer": 2,
                    "explanation": "Both CONFIDENTIAL and RESTRICTED data require encryption, with RESTRICTED requiring the strictest controls."
                },
                {
                    "question": "Can you email a customer's Social Security Number?",
                    "options": ["Yes, if work-related", "Yes, if encrypted", "No, never", "Yes, internally only"],
                    "correct_answer": 2,
                    "explanation": "RESTRICTED data like SSNs should NEVER be sent via email, even if encrypted."
                },
                {
                    "question": "What should you do with CONFIDENTIAL documents when finished?",
                    "options": ["Recycle them", "Throw in trash", "Shred them", "Leave on desk"],
                    "correct_answer": 2,
                    "explanation": "CONFIDENTIAL documents must be cross-cut shredded to prevent reconstruction."
                }
            ],
            learning_objectives=[
                "Understand data classification levels",
                "Apply appropriate handling procedures",
                "Protect sensitive data properly",
                "Dispose of data securely"
            ]
        )

    def _create_gdpr_lesson(self) -> TrainingLesson:
        """Create GDPR lesson"""
        return TrainingLesson(
            lesson_id="gdpr_overview",
            title="GDPR & Privacy Compliance",
            content="""
# GDPR & Privacy Compliance

## What is GDPR?

**General Data Protection Regulation (GDPR)**
EU law protecting personal data and privacy

**Applies to:**
- Any company processing EU residents' data
- Regardless of where company is located
- Even a single EU customer = GDPR applies

**Penalties for violations:**
- Up to €20 million OR 4% of global revenue
- Whichever is higher!

## What is Personal Data?

**Personal Data:** Any information about an identified or identifiable person

**Examples:**
- Name, email, phone number
- IP address, cookie IDs
- Location data
- Photos, voice recordings
- Social Security numbers
- Health information
- Racial/ethnic origin
- Political opinions

**Special Categories (Extra Protected):**
- Health data
- Genetic/biometric data
- Sexual orientation
- Religious beliefs
- Trade union membership

## Data Subject Rights

Under GDPR, individuals have these rights:

### 1. Right to Access (Article 15)
**What:** See what data you have about them
**Timeline:** 30 days
**Our system:** `privacy/gdpr_compliance.py` - export_user_data()

### 2. Right to Rectification (Article 16)
**What:** Correct inaccurate data
**Timeline:** 30 days
**Our system:** `privacy/gdpr_compliance.py` - update_user_data()

### 3. Right to Erasure (Article 17)
**What:** Delete their data ("Right to be forgotten")
**Timeline:** 30 days
**Exceptions:** Legal obligations, public interest
**Our system:** `privacy/gdpr_compliance.py` - delete_user_data()

### 4. Right to Data Portability (Article 20)
**What:** Get data in portable format (JSON, CSV)
**Timeline:** 30 days
**Our system:** Automated export to JSON/ZIP

### 5. Right to Object (Article 21)
**What:** Object to processing (e.g., marketing)
**Timeline:** Must stop immediately

### 6. Right to Restrict Processing (Article 18)
**What:** Limit how data is used
**Timeline:** Immediately

## Privacy Principles

### 1. Lawfulness
Must have a legal basis to process data:
- Consent
- Contract
- Legal obligation
- Vital interests
- Public task
- Legitimate interests

### 2. Purpose Limitation
Only use data for stated purpose

❌ WRONG: "We collected email for invoicing, now using for marketing"
✅ RIGHT: "Email used only for stated purpose in privacy policy"

### 3. Data Minimization
Only collect what you need

❌ WRONG: "Collect SSN for newsletter signup"
✅ RIGHT: "Collect only email for newsletter"

### 4. Accuracy
Keep data accurate and up to date

### 5. Storage Limitation
Don't keep data longer than necessary

**Our retention:**
- RESTRICTED data: 7 years (audit requirement)
- CONFIDENTIAL: Per classification policy
- User data: Deleted within 30 days of request

### 6. Integrity & Confidentiality
Protect data with security measures:
- ✅ Encryption (at rest and in transit)
- ✅ Access controls
- ✅ Audit logging
- ✅ Incident detection

### 7. Accountability
Must demonstrate compliance:
- ✅ Privacy policy
- ✅ Data protection impact assessments
- ✅ Records of processing
- ✅ Data breach procedures

## Data Breach Requirements

**What is a breach:** Unauthorized access, loss, or disclosure of personal data

**72-Hour Rule:**
Must notify supervisory authority within **72 hours** of becoming aware of breach

**Must notify individuals if:**
- High risk to their rights and freedoms
- Could result in discrimination, identity theft, financial loss

**Our procedure:**
1. Discover breach → Immediately report to security@company.com
2. Security team investigates
3. If confirmed, notify within 72 hours
4. Document everything

## Employee Responsibilities

### ✅ DO:
- Minimize personal data collection
- Delete data when no longer needed
- Respond to data subject requests within 30 days
- Report data breaches immediately
- Protect personal data with encryption
- Only access data you need for your job

### ❌ DON'T:
- Collect unnecessary personal data
- Use personal data for unauthorized purposes
- Share personal data externally without permission
- Ignore data subject requests
- Delay breach reporting

## GDPR Violations to Avoid

**Real-world examples:**

1. **Amazon (€746M):** Excessive data processing
2. **WhatsApp (€225M):** Unclear privacy policy
3. **Google (€90M):** No clear consent for ads
4. **H&M (€35M):** Excessive employee monitoring

## How to Handle Data Subject Requests

**Request received:**
1. Forward to: privacy@company.com
2. Our automated system processes it
3. Response generated within 30 days
4. You don't need to do anything!

**Example email:**
```
From: customer@example.com
Subject: GDPR Data Access Request

I would like to request a copy of all my personal data.

[Automatic system response]:
Your request has been received. Data export will be
available within 30 days at: [secure download link]
```
            """,
            duration_minutes=20,
            quiz_questions=[
                {
                    "question": "How long do you have to respond to a GDPR data access request?",
                    "options": ["7 days", "15 days", "30 days", "90 days"],
                    "correct_answer": 2,
                    "explanation": "GDPR requires response to data subject requests within 30 days."
                },
                {
                    "question": "How long do you have to report a data breach to authorities?",
                    "options": ["24 hours", "48 hours", "72 hours", "1 week"],
                    "correct_answer": 2,
                    "explanation": "GDPR requires data breach notification to authorities within 72 hours."
                },
                {
                    "question": "What is 'Right to be Forgotten'?",
                    "options": [
                        "Right to anonymous browsing",
                        "Right to delete search history",
                        "Right to have personal data deleted",
                        "Right to opt-out of emails"
                    ],
                    "correct_answer": 2,
                    "explanation": "Right to erasure (Article 17) allows individuals to request deletion of their personal data."
                }
            ],
            learning_objectives=[
                "Understand GDPR requirements",
                "Recognize data subject rights",
                "Handle personal data compliantly",
                "Respond to data breaches properly"
            ]
        )

    # Additional lesson creation methods would go here...
    def _create_data_handling_lesson(self) -> TrainingLesson:
        return TrainingLesson(
            lesson_id="data_handling",
            title="Secure Data Handling Practices",
            content="[Data handling content...]",
            duration_minutes=10,
            quiz_questions=[],
            learning_objectives=[]
        )

    def _create_incident_recognition_lesson(self) -> TrainingLesson:
        return TrainingLesson(
            lesson_id="incident_recognition",
            title="Recognizing Security Incidents",
            content="[Incident recognition content...]",
            duration_minutes=15,
            quiz_questions=[],
            learning_objectives=[]
        )

    def _create_incident_reporting_lesson(self) -> TrainingLesson:
        return TrainingLesson(
            lesson_id="incident_reporting",
            title="Reporting Security Incidents",
            content="[Incident reporting content...]",
            duration_minutes=15,
            quiz_questions=[],
            learning_objectives=[]
        )

    def _create_social_engineering_lesson(self) -> TrainingLesson:
        return TrainingLesson(
            lesson_id="social_engineering",
            title="Social Engineering Tactics",
            content="[Social engineering content...]",
            duration_minutes=15,
            quiz_questions=[],
            learning_objectives=[]
        )

    def _create_pretexting_lesson(self) -> TrainingLesson:
        return TrainingLesson(
            lesson_id="pretexting",
            title="Pretexting & Manipulation",
            content="[Pretexting content...]",
            duration_minutes=10,
            quiz_questions=[],
            learning_objectives=[]
        )

    def _create_owasp_top10_lesson(self) -> TrainingLesson:
        return TrainingLesson(
            lesson_id="owasp_top10",
            title="OWASP Top 10 Security Risks",
            content="[OWASP content...]",
            duration_minutes=30,
            quiz_questions=[],
            learning_objectives=[]
        )

    def _create_input_validation_lesson(self) -> TrainingLesson:
        return TrainingLesson(
            lesson_id="input_validation",
            title="Input Validation & Sanitization",
            content="[Input validation content...]",
            duration_minutes=15,
            quiz_questions=[],
            learning_objectives=[]
        )

    def _create_authentication_lesson(self) -> TrainingLesson:
        return TrainingLesson(
            lesson_id="authentication",
            title="Secure Authentication Implementation",
            content="[Authentication content...]",
            duration_minutes=15,
            quiz_questions=[],
            learning_objectives=[]
        )

    def _create_soc2_overview_lesson(self) -> TrainingLesson:
        return TrainingLesson(
            lesson_id="soc2_overview",
            title="SOC 2 Overview",
            content="[SOC 2 overview content...]",
            duration_minutes=20,
            quiz_questions=[],
            learning_objectives=[]
        )

    def _create_employee_responsibilities_lesson(self) -> TrainingLesson:
        return TrainingLesson(
            lesson_id="employee_responsibilities",
            title="Employee Security Responsibilities",
            content="[Employee responsibilities content...]",
            duration_minutes=20,
            quiz_questions=[],
            learning_objectives=[]
        )

    def get_module(self, module_id: str) -> Optional[Dict]:
        """Get training module by ID"""
        return self.modules.get(module_id)

    def export_module(self, module_id: str, output_dir: str = "data/training_content"):
        """Export module to files"""
        module = self.get_module(module_id)
        if not module:
            print(f"❌ Module not found: {module_id}")
            return

        output_path = Path(output_dir) / module_id
        output_path.mkdir(parents=True, exist_ok=True)

        # Save module metadata
        module_data = {
            "module_id": module["module_id"],
            "title": module["title"],
            "description": module["description"],
            "duration_minutes": module["duration_minutes"],
            "required": module["required"],
            "lesson_count": len(module["lessons"])
        }

        with open(output_path / "module.json", 'w') as f:
            json.dump(module_data, f, indent=2)

        # Save each lesson
        for lesson in module["lessons"]:
            lesson_file = output_path / f"{lesson.lesson_id}.json"
            with open(lesson_file, 'w') as f:
                json.dump(asdict(lesson), f, indent=2)

        print(f"✓ Module exported: {output_path}")


if __name__ == "__main__":
    print("=" * 70)
    print("SECURITY TRAINING CONTENT SYSTEM")
    print("=" * 70)

    content = SecurityTrainingContent()

    print("\n📚 Available Training Modules:")
    for module_id, module in content.modules.items():
        print(f"\n  {module['title']}")
        print(f"  Duration: {module['duration_minutes']} minutes")
        print(f"  Required: {module['required']}")
        print(f"  Lessons: {len(module['lessons'])}")

    # Export all modules
    print("\n📁 Exporting training content...")
    for module_id in content.modules:
        content.export_module(module_id)

    print("\n" + "=" * 70)
    print("✅ TRAINING CONTENT READY!")
    print("=" * 70)
