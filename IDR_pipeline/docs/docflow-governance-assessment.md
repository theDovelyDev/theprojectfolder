# DocFlow — AI Governance Assessment
## NIST AI RMF Alignment Report
**System:** Intelligent Document Processing Pipeline (DocFlow)
**Version:** Phase 10 Complete
**Assessed:** March 2026
**Assessor:** Carlandra Williams, Sr. FinOps Practitioner

---

## Executive Summary

DocFlow is a serverless AWS pipeline that extracts and analyzes structured data from invoices and receipts using AWS Textract (OCR) and AWS Comprehend (NLP). This assessment maps the current state of DocFlow's governance controls against the NIST AI Risk Management Framework (AI RMF 1.0) across four functions: Govern, Map, Measure, and Manage.

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

| Gap | Risk | Remediation |
|-----|------|-------------|
| No formal AI governance policy | Medium | Define acceptable use, prohibited use cases, escalation path |
| No designated AI risk owner separate from developer | Medium | For enterprise: assign governance role distinct from builder role |
| No user communication about AI involvement | Low-Medium | Disclose that outputs are AI-generated and require verification |
| No incident response plan for AI failures | Medium | Define what constitutes a failure, who is notified, and how |

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

| Gap | Risk | Remediation |
|-----|------|-------------|
| No formal risk categorization by NIST AI RMF tier | Low (current scale) | Classify as Limited Risk; document basis for classification |
| No training data provenance for Textract or Comprehend | Medium | Review AWS model cards and service documentation; document known data characteristics |
| No stakeholder impact assessment | Low-Medium | Identify all parties affected by DocFlow outputs (staff, vendors, auditors) |
| No prohibited use documentation | Low | Define explicitly what DocFlow should not be used for |

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

| Gap | Risk | Remediation |
|-----|------|-------------|
| No bias evaluation on Textract or Comprehend outputs | Medium | Test against diverse document samples; document performance variance by document type, language, and formatting |
| No confidence calibration analysis | Medium | Validate that confidence scores correlate with actual accuracy |
| No drift monitoring | Low (static model) | AWS managed models update without notice; implement periodic regression testing |
| Sentiment analysis not validated for document processing context | Low | All 150 test documents returned NEUTRAL — validate this is expected, not a model limitation |
| No adversarial testing | Medium | Test with malformed, adversarial, or edge-case documents |

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

| Gap | Risk | Remediation |
|-----|------|-------------|
| No human review queue for low-confidence extractions | Medium | Implement confidence threshold (e.g., <85%) that routes to human review |
| No feedback loop for incorrect extractions | Medium | Allow users to flag incorrect results; use to monitor model performance over time |
| No formal SLA or uptime commitment | Low (portfolio) | For enterprise: define acceptable downtime, recovery time objective |
| No data retention or deletion policy | Medium | Define how long extracted data is retained in DynamoDB and S3; implement lifecycle rules |
| Multi-tenancy not implemented | High (for SaaS) | Customer data isolation required before any multi-customer deployment |

---

## Enterprise Deployment Requirements

Before DocFlow could be deployed in a general enterprise context, the following would be required:

### Must Have
- [ ] Multi-tenancy — tenant isolation at DynamoDB and S3 layer
- [ ] Authentication — Cognito or equivalent; no anonymous API access
- [ ] Data retention policy — define and implement automated deletion
- [ ] Human review queue — confidence threshold routing
- [ ] Formal risk classification document (NIST AI RMF tier)
- [ ] AI use disclosure to end users
- [ ] Incident response runbook

### Should Have
- [ ] Bias evaluation across document types and demographics
- [ ] Training data provenance documentation for Textract and Comprehend
- [ ] Confidence calibration analysis
- [ ] Periodic regression testing against held-out document set
- [ ] Feedback mechanism for incorrect extractions
- [ ] Formal SLA

### Nice to Have
- [ ] Adversarial testing protocol
- [ ] Third-party audit of AI system outputs
- [ ] Model drift monitoring
- [ ] Explainability documentation for Comprehend entity classifications

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
