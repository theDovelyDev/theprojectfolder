# DocFlow — AI Governance Assessment
## NIST AI RMF Alignment Report
**System:** Intelligent Document Processing Pipeline (DocFlow)
**Version:** Phase 10 Complete
**Assessed:** March 2026
**Assessor:** Carlandra Williams, Sr. FinOps Practitioner

---

## Executive Summary

DocFlow is a serverless AWS pipeline that extracts and analyzes structured data from invoices and receipts using AWS Textract (OCR) and AWS Comprehend (NLP). This assessment maps the current state of DocFlow's governance controls against the NIST AI Risk Management Framework (AI RMF 1.0) across four functions: Govern, Map, Measure, and Manage.

**Assessment Scoring Rubric**

Alignment status for each NIST AI RMF function is determined by the following criteria:

| Status | Definition| DocFlow Threshold|
|--------|-----------| -----------------|
|🟢 Aligned | All core controls for this function are implemented and documented. Gaps are minor or cosmetic. | ≥80% of controls present with no High-risk gaps
|🟡 Partial | Core controls are partially implemented. At least one Medium-risk gap exists with no remediation in place. | 40–79% of controls present, or ≥1 unmitigated Medium gap
|🔴 Not Aligned | Few or no controls implemented. High-risk gaps present with no remediation path defined. |<40% of controls present, or ≥1 unmitigated High gap

**Notes on scoring:**

- Scoring reflects current state at time of assessment — March 2026
- Risk ratings (Low, Medium, High) reflect potential impact in a general enterprise deployment context, not current single-tenant portfolio use
- A "Partial" rating does not indicate failure — it indicates a known gap with a documented remediation path
- This is a self-assessment. Independent third-party scoring may differ.

**Overall Assessment: Partially Aligned**

DocFlow demonstrates strong operational governance practices derived from FinOps discipline — cost controls, resource tagging, audit trails, and documented limitations. It has material gaps in areas specific to AI governance: bias evaluation, data provenance, explainability documentation, and formal risk categorization.

| NIST Function | Status | Notes |
|---------------|--------|-------|
| Govern | 🟡 Partial | Accountability and tagging in place; no formal AI governance policy |
| Map | 🟡 Partial | Use case and limitations documented; no formal risk categorization |
| Measure | 🟡 Partial | Performance metrics tracked; no bias or fairness evaluation |
| Manage | 🟢 Mostly Aligned | Controls, guardrails, and remediation paths in place |

---

## System Context

**System Type:** AI-assisted decision support (document extraction)
**Risk Tier (NIST):** Limited risk — outputs are structured data requiring human review before action
**Deployment:** Single-tenant, AWS serverless, developer-owned
**Data Processed:** Business invoices and receipts (no PII beyond vendor/customer names and financial data)
**Users:** SMB owners, operations managers, bookkeeping staff
**Decision Authority:** Human — DocFlow extracts and presents; humans act on outputs

---

## GOVERN Function

*Establish accountability structures, policies, and culture for AI risk management.*

### What's In Place

**Resource Ownership**
All AWS resources are tagged with `Project`, `CostCenter`, `Environment`, and `ManagedBy`. Weekly automated tag compliance audits (Lambda + EventBridge + SNS) confirm ownership attribution. Every resource has an identifiable owner.

**Access Controls**
- IAM least-privilege per function — each Lambda has scoped permissions
- API Gateway rate limiting: 5 req/s, burst 10, 100 req/day
- No public write access to any data store
- S3 bucket policies restrict access by function

**Cost Governance**
- Per-document cost tracked: $0.034
- Budget alerts configured
- Rate limiting as financial guardrail pre-deployment
- CONFIG.SIMULATE pattern — no production API calls during development

**Documented Decision Trail**
Phase-by-phase development log captures every architectural decision, trade-off, and known limitation. Decisions are traceable to specific dates and reasoning.

### Gaps

| ID | Gap | Risk | Remediation |
|-----|-----|------|-------------|
| GOV-01 | No formal AI governance policy | Medium | Define acceptable use, prohibited use cases, escalation path |
| GOV-02 | No designated AI risk owner separate from developer | Medium | For enterprise: assign governance role distinct from builder role |
|GOV-03 | No user communication about AI involvement | Low-Medium | Disclose that outputs are AI-generated and require verification |
| GOV-04 | No incident response plan for AI failures | Medium | Define what constitutes a failure, who is notified, and how |

---

## MAP Function

*Identify and categorize AI risks in context of intended use.*

### What's In Place

**Use Case Documentation**
DocFlow's intended use is clearly scoped: extract structured data from invoices and receipts. The system is not used for decisions with legal, employment, credit, or health consequences.

**Known Limitations Register**
Phase 4 documents the 20% PDF failure rate with:
- Root cause (deep Textract incompatibility with certain PDF encodings)
- Confidence correlation (failures correlate with document complexity)
- Remediation path (pdf2image + poppler image conversion fallback)
- Deliberate ship decision with documented reasoning

This is a functional known limitations register — the artifact AI governance frameworks require.

**Third-Party AI Dependencies**
DocFlow uses two AWS managed AI services:
- AWS Textract — OCR and form extraction
- AWS Comprehend — entity detection, sentiment analysis, key phrases

Both are black-box managed services. Input/output behavior is observable. Internal model architecture and training data are not disclosed by AWS.

### Gaps

| ID | Gap | Risk | Remediation |
|------|------|------|-------------|
| MAP-01 | No formal risk categorization by NIST AI RMF tier | Low (current scale) | Classify as Limited Risk; document basis for classification |
| MAP-02 | No training data provenance for Textract or Comprehend | Medium | Review AWS model cards and service documentation; document known data characteristics |
| MAP-03 | No stakeholder impact assessment | Low-Medium | Identify all parties affected by DocFlow outputs (staff, vendors, auditors) |
| MAP-04 | No prohibited use documentation | Low | Define explicitly what DocFlow should not be used for |

---

## MEASURE Function

*Analyze and assess AI risks quantitatively and qualitatively.*

### What's In Place

**Performance Metrics**
| Metric | Value | Tracking |
|--------|-------|----------|
| Success rate | 100% (150-doc batch test) | batch_test.py output |
| Avg extraction confidence | 80.88% | DynamoDB DocFlowRecords |
| Processing time | ~30 seconds | CloudWatch metrics |
| Cost per document | $0.034 | Cost tracker |
| Known failure rate | ~20% (complex PDFs) | Phase 3/4 documentation |

**Audit Trail**
Every processed document is stored in DynamoDB with:
- `documentId` — unique identifier
- `processedAt` — ISO timestamp
- `status` — success/failed
- `extractionConfidence` — numeric score
- `fullText` — complete extracted content
- `keyValuePairs` — structured field extraction
- `entities` — detected entities
- `sentiment` — overall sentiment classification

This constitutes a queryable audit log of all AI system outputs.

**Confidence Scoring**
Textract returns per-block confidence scores. DocFlow calculates and stores average extraction confidence per document. Low-confidence results are visible to users.

### Gaps

| ID | Gap | Risk | Remediation |
|------|-----|------|-------------|
| MEA-01 | No bias evaluation on Textract or Comprehend outputs | Medium | Test against diverse document samples; document performance variance by document type, language, and formatting |
| MEA-02 | No confidence calibration analysis | Medium | Validate that confidence scores correlate with actual accuracy |
| MEA-03 | No drift monitoring | Low (static model) | AWS managed models update without notice; implement periodic regression testing |
| MEA-04 | Sentiment analysis not validated for document processing context | Low | All 150 test documents returned NEUTRAL — validate this is expected, not a model limitation |
| MEA-05 | No adversarial testing | Medium | Test with malformed, adversarial, or edge-case documents |

---

## MANAGE Function

*Prioritize and address identified AI risks.*

### What's In Place

**Operational Guardrails**
- Rate limiting (velocity control): 5 req/s, burst 10
- Daily quota (volume control): 100 req/day
- CONFIG.SIMULATE flag: prevents production API calls during development
- Graceful failure handling: failed documents return error status, not silent failures

**Incident Visibility**
- CloudWatch logs all Lambda invocations
- SNS email notification per processed document
- DynamoDB records document status (success/failed)
- CloudTrail captures all API calls

**Remediation Paths**
All known limitations have documented remediation paths:
- Complex PDF failures → pdf2image + poppler image conversion
- Confidence below threshold → human review queue (architectural recommendation)
- API quota exceeded → alert via AWS Budgets + CloudWatch alarm

**Continuous Compliance**
Weekly tag audit Lambda confirms resource ownership and governance metadata compliance across all DocFlow resources.

### Gaps

| ID | Gap | Risk | Remediation |
|-----|-----|------|-------------|
| MAN-01 | No human review queue for low-confidence extractions | Medium | Implement confidence threshold (e.g., <85%) that routes to human review |
| MAN-02 | No feedback loop for incorrect extractions | Medium | Allow users to flag incorrect results; use to monitor model performance over time |
| MAN-03 | No formal SLA or uptime commitment | Low (portfolio) | For enterprise: define acceptable downtime, recovery time objective |
| MAN-04 | No data retention or deletion policy | Medium | Define how long extracted data is retained in DynamoDB and S3; implement lifecycle rules |
| MAN-05 | Multi-tenancy not implemented | High (for SaaS) | Customer data isolation required before any multi-customer deployment |

---

## Enterprise Deployment Requirements

Before DocFlow could be deployed in a general enterprise context, the following would be required:

### Must Have
- [ ] **MAN-05** — Multi-tenancy — tenant isolation at DynamoDB and S3 layer
- [ ] **GOV-02** — Authentication — Cognito or equivalent; no anonymous API access
- [ ] **MAN-04** — Data retention policy — define and implement automated deletion
- [ ] **MAN-01** — Human review queue — confidence threshold routing
- [ ] **MAP-01** — Formal risk classification document (NIST AI RMF tier)
- [ ] **GOV-03** — AI use disclosure to end users
- [ ] **GOV-04** — Incident response runbook

### Should Have
- [ ] **MEA-01** — Bias evaluation across document types and demographics
- [ ] **MAP-02** — Training data provenance documentation for Textract and Comprehend
- [ ] **MEA-02** — Confidence calibration analysis
- [ ] **MEA-03** — Periodic regression testing against held-out document set
- [ ] **MAN-02** — Feedback mechanism for incorrect extractions
- [ ] **MAN-03** — Formal SLA

### Nice to Have
- [ ] **MEA-05** — Adversarial testing protocol
- [ ] **GOV-05** — Third-party audit of AI system outputs
- [ ] **MEA-03** — Model drift monitoring
- [ ] **MEA-06** — Explainability documentation for Comprehend entity classifications

---
## Remediation Path

Gaps identified in this assessment are prioritized into three horizons based on risk level and effort required for enterprise deployment.

### Immediate (~2 weeks · $0 infrastructure impact)

These items are blockers — DocFlow cannot be responsibly deployed to a multi-customer or regulated enterprise environment without them.

| ID | Item | Effort | Cost Impact |
|----|------|--------|-------------|
| MAN-05 | Multi-tenancy — tenant isolation at S3 and DynamoDB | 2–3 days | +$0 |
| GOV-02 | Cognito authentication — no anonymous API access | 1 day | +$0.0055/MAU |
| MAN-04 | Data retention policy + automated deletion | 1 day | Reduces S3/DynamoDB cost |
| MAN-01 | Human review queue for low-confidence extractions | 1–2 days | +$0 |
| MAP-01 | Formal NIST AI RMF risk classification document | 4 hours | $0 |
| GOV-03 | AI use disclosure to end users | 2 hours | $0 |
| GOV-04 | Incident response runbook | 4 hours | $0 |

**Total immediate remediation: ~2 weeks, negligible infrastructure cost increase**

### Short-Term (30–60 Days · ~$5/month ongoing)

These items reduce ongoing risk and build the evidence base for model trustworthiness.

| ID | Item | Effort | Cost Impact |
|----|------|--------|-------------|
| MEA-01 | Bias evaluation across document types | 1 week | +$0 (testing cost only) |
| MAP-02 | Training data provenance (Textract + Comprehend) | 3–4 days research | $0 |
| MEA-02 | Confidence calibration analysis | 3–4 days | +$0 |
| MEA-03 | Monthly regression testing protocol | 2 days setup | +~$5/month |
| MAN-02 | Feedback mechanism for incorrect extractions | 2–3 days | +$0 |
| MAN-03 | Formal SLA definition | 1 day | $0 |

**Total short-term remediation: ~3 weeks engineering, ~$5/month ongoing**

### Long-Term (90+ Days · $5K–$15K audit)

These items reflect mature AI governance practice and are appropriate once the system has production usage data to analyze.

| ID | Item | Effort | Cost Impact |
|----|------|--------|-------------|
| GOV-05 | Third-party independent AI system audit | External engagement | $5,000–$15,000 one-time |
| MEA-03 | Automated model drift monitoring | 1 week | +~$10/month (CloudWatch) |
| MEA-06 | Explainability documentation for Comprehend | 1–2 weeks research | $0 |
| MEA-05 | Adversarial testing protocol | 1 week | $0 |

**Total long-term: external audit is the largest investment; infrastructure additions are minimal**

### Remediation Summary

| Horizon | Effort | Cost | Risk Reduction |
|---------|--------|------|----------------|
| Immediate | ~2 weeks | ~$0 | High — resolves all deployment blockers |
| Short-term | ~3 weeks | ~$5/month | Medium — builds evidence base |
| Long-term | Ongoing | $5K–$15K (audit) | Low — mature governance practice |

---

## Summary: What FinOps Transfers, What Doesn't

| Governance Domain | FinOps Transfer | New Skill Required |
|------------------|----------------|-------------------|
| Cost controls | ✅ Direct | — |
| Resource ownership | ✅ Direct (tagging) | — |
| Audit trails | ✅ Direct | — |
| Documented limitations | ✅ Direct | — |
| Access controls | ✅ Direct (IAM/rate limiting) | — |
| Risk categorization | 🟡 Partial (cost risk) | AI risk tiers, harm types |
| Bias evaluation | ❌ Not transferable | Statistical fairness methods |
| Data provenance | 🟡 Partial (vendor management) | Training data audit methodology |
| Explainability | ❌ Not transferable | XAI techniques, documentation standards |
| Incident response | 🟡 Partial (cost anomalies) | AI-specific failure modes |

---

## Assessor Notes

This assessment was conducted by the system's builder, not an independent third party. For enterprise deployment, an independent governance review would be required. This document serves as a self-assessment and interview artifact demonstrating applied knowledge of the NIST AI RMF against a production system.

The most significant governance gap in DocFlow is not technical — it's organizational. The same person who built the system, owns the infrastructure, and interprets the outputs is also the person who conducted this assessment. In any production deployment, those roles must be separated.

That's not a DocFlow-specific problem. It's the central challenge of AI governance at scale: the people closest to the system are least positioned to govern it objectively.

---

*Companion article: "What FinOps Taught Me About AI Governance" — carlandrainthecloud.substack.com*
*System repository: github.com/theDovelyDev/theprojectfolder/tree/main/IDR_pipeline*
