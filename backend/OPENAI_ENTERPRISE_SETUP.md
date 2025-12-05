# OpenAI Enterprise Setup for Research Lab Pilot

## 🚨 CRITICAL: You MUST Use OpenAI Enterprise

**Standard OpenAI API is NOT ACCEPTABLE for research labs because:**
- ❌ Data retained for 30+ days
- ❌ Could be used for model training (unless opted out)
- ❌ No contractual guarantees
- ❌ Not HIPAA/IRB compliant by default

**OpenAI Enterprise provides:**
- ✅ **Zero data retention** - Deleted immediately after processing
- ✅ **No training on your data** - Contractual guarantee
- ✅ **SOC 2 Type 2 certified**
- ✅ **GDPR compliant**
- ✅ **HIPAA compliant** (with BAA)
- ✅ **Enterprise SLA** - 99.9% uptime

---

## How to Get OpenAI Enterprise

### Step 1: Contact OpenAI Sales

**Option A: Online Form**
1. Go to https://openai.com/enterprise
2. Click "Contact Sales"
3. Fill out form:
   - Company: [Your startup name]
   - Use case: "Healthcare research lab knowledge management"
   - Requirements: "Zero data retention, HIPAA compliance"

**Option B: Direct Email**
Email: `enterprise@openai.com`

```
Subject: Enterprise API for Healthcare Research Lab

Hi OpenAI Team,

We're building a knowledge management system for research labs and need
Enterprise API access with zero data retention.

Requirements:
- Zero data retention (immediate deletion)
- No training on our data
- HIPAA compliance (BAA if possible)
- SOC 2 compliance documentation

Current usage:
- Model: GPT-4o-mini
- Estimated tokens/month: ~1M
- Customer type: Healthcare/research labs

Can you help us get set up?

Best,
[Your name]
```

### Step 2: Provide Information

They'll ask for:
- Company information
- Use case details
- Expected usage volume
- Security requirements

### Step 3: Sign Agreement

You'll receive:
- Enterprise Terms of Service
- Data Processing Agreement (DPA)
- Zero Retention Addendum
- (Optional) Business Associate Agreement (BAA) for HIPAA

### Step 4: Get Credentials

Once approved, you'll receive:
- Enterprise API key (looks like: `sk-proj-...` or `sk-enterprise-...`)
- Organization ID (looks like: `org-...`)
- Access to enterprise dashboard

---

## Configure Your Backend

### Update .env file:

```bash
# Copy template
cp .env.template .env

# Edit .env
nano .env
```

```env
# REQUIRED: Your enterprise API key
OPENAI_API_KEY=sk-proj-YOUR-ENTERPRISE-KEY-HERE

# REQUIRED: Your organization ID
OPENAI_ORGANIZATION=org-YOUR-ORG-ID-HERE

# Confirm zero retention
OPENAI_ZERO_RETENTION=true
```

### Verify Zero Retention is Active

The backend automatically uses enterprise settings when you have the org ID configured.

---

## Pricing

**OpenAI Enterprise pricing is typically:**
- Same per-token pricing as standard API
- OR volume discounts if usage is high
- No minimum commitment (usually)

**GPT-4o-mini pricing:**
- Input: $0.15 / 1M tokens
- Output: $0.60 / 1M tokens

**Estimated cost for research lab pilot:**
- 1000 documents processed: ~$0.50
- 100 RAG queries/day: ~$1.50/month

**Total: < $10/month for pilot** ✅

---

## What to Tell Research Lab

> "We use OpenAI's Enterprise API with contractual zero data retention.
> Your data is processed in real-time and immediately deleted - it's never
> stored or used for training. OpenAI Enterprise is SOC 2 Type 2 and
> GDPR compliant, meeting the highest security standards for healthcare
> and research institutions."

Provide them:
1. Copy of your OpenAI Enterprise agreement (redact pricing)
2. OpenAI's SOC 2 report (request from OpenAI)
3. Data Processing Agreement (DPA)

---

## Timeline

**How long does it take?**
- Sales response: 1-2 business days
- Agreement signing: 2-3 days
- Access provisioned: Same day after signing

**URGENT:** If your pilot is Wednesday, contact them TODAY (Thursday).
- They can expedite for urgent needs
- Mention it's for a healthcare research lab pilot

---

## Fallback: Temporary Standard API with Opt-Out

**If Enterprise isn't approved by Wednesday:**

1. Use standard API BUT:
   - Opt out of training: https://platform.openai.com/account/data-controls
   - Enable "Zero data retention" option (if available)
   - Note: Still retained for 30 days (vs immediate deletion)

2. Disclose to research lab:
   - "We use OpenAI API with training opt-out"
   - "Data retained for 30 days (OpenAI policy), then permanently deleted"
   - "Enterprise upgrade pending for immediate deletion"

3. Upgrade to Enterprise ASAP after pilot

---

## Questions?

**Common Questions:**

**Q: Do we need a minimum commitment?**
A: Usually no, but they may offer discounts for commitments

**Q: Can we switch from standard to enterprise?**
A: Yes, instantly - just update the API key

**Q: Does it cost more?**
A: Usually same pricing, sometimes discounts for volume

**Q: How do we prove zero retention to research lab?**
A: Share the enterprise agreement and DPA

---

**Next Step:** Contact OpenAI Enterprise sales TODAY!

**Email template above ↑**
