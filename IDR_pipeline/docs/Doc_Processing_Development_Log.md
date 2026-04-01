# Building an AI-Powered Document Processing Pipeline on AWS

## A Developer's Journey from Concept to Production

---

## 📝 Development Log

**Project:** Intelligent Document Processing Pipeline (DocFlow)
**Duration:** January 16, 2026 - March 24, 2026
**Total Hours:** ~35 hours
**Final Cost:** $6.90

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Why I Built This](#why-i-built-this)
3. [Development Log](#development-log)
4. [Key Learnings](#key-learnings)
5. [Results & Impact](#results)
6. [What's Next](#whats-next)

---

## Project Overview

**The Problem:** Manual document processing takes 3 minutes per document and costs $1.25 in staff time.

**The Solution:** An AWS serverless pipeline that processes documents in 30 seconds at $0.034 per document.

**Tech Stack:**

- AWS Services: S3, Lambda, Textract, Comprehend, API Gateway, DynamoDB, SNS, CloudWatch, EventBridge
- Languages: Python 3.11, JavaScript (ES6+)
- Tools: AWS CLI, Boto3, Git

**Key Metrics:**

- 100% success rate on 150-document live batch test
- 80.88% average extraction confidence
- 97% cost reduction per document vs. manual processing
- $6.90 total build cost
- ROI: 3,558% annually at 500 docs/month

---

## Why I Built This

My partner used to own three businesses at the same time — not three locations, three different businesses. For all three, he maintained invoicing manually. Spreadsheets, paper trails, hours of work every month that existed purely because no one had built him a better option.

That's the SMB reality that gets skipped in most AI conversations. I wanted to build something that made sense for a business like his.

The other honest reason: I had just passed my AWS AI Practitioner exam with barely-basic Python skills, and I wanted to know if I could build something real — not follow a tutorial, but actually build something — using what I knew and AI as a thought partner from conception to production.

---

## Development Log

### Pre-Development Setup

**Date:** January 16, 2026
**Time Spent:** 1 hour
**Status:** ✅ Complete

#### What I Did:

- [x] Created AWS account (ensured Free Tier eligibility)
- [x] Set up IAM user with proper permissions
- [x] Enabled MFA for security
- [x] Created CLI access keys
- [x] Configured AWS CLI in VSCode (switched from PowerShell to Bash)
- [x] Created cost budget alerts ($25 threshold)
- [x] Set up environment variables (PROJECT_NAME, REGION, ACCOUNT_ID)
- [x] Created setup.sh script for easy environment loading
- [x] Tested CLI with test S3 bucket creation/deletion
- [x] Set up GitHub repository
- [x] Created `dev` branch for active development
- [x] Added comprehensive `.gitignore`

#### Cost Tracker:

- AWS charges so far: $0.00
- Budget remaining: $25.00

---

### Phase 1: S3 Bucket Configuration

**Date:** January 16, 2026
**Time Spent:** 2 hours
**Status:** ✅ Complete

#### What I Did:

- [x] Implemented comprehensive tagging strategy (TAGGING_STRATEGY.md)
- [x] Updated setup.sh with tag variables for cost tracking
- [x] Created 3 S3 buckets with proper tags:
  - doc-processing-demo-uploads-848747536965
  - doc-processing-demo-processed-848747536965
  - doc-processing-demo-frontend-848747536965
- [x] Enabled versioning on uploads bucket
- [x] Configured Lambda access policy for uploads bucket
- [x] Created lifecycle policy (90 days → Glacier, applied via console)
- [x] Tested upload/download functionality
- [x] Committed all configuration files to Git

#### Cost Tracker:

- Running total: $0.00
- Budget remaining: $25.00

#### Challenges Faced:

```
Challenge: Lifecycle policy CLI command failed
- Solution: Applied via AWS Console instead
- Lesson: Don't be dogmatic about CLI only — sometimes the console is faster
```

---

### Side Quest: Automated Tag Governance

**Date:** January 16, 2026
**Time Spent:** 1 hour
**Status:** ✅ Complete

#### What I Did:

- [x] Evaluated AWS Config ($1/year) vs Lambda automation ($0.00)
- [x] Created SNS topic for email notifications (TagAuditNotifications)
- [x] Created IAM role for Lambda (TagAuditLambdaRole)
- [x] Wrote Python Lambda function (tag_audit_function.py — 120 lines)
- [x] Deployed Lambda to AWS (TagAuditFunction)
- [x] Created EventBridge rule for weekly schedule (Mondays 9 AM UTC)
- [x] Tested manually — 100% compliance on first audit (6 resources)
- [x] Created fix-tags.sh script for on-demand remediation

#### Architecture:

```
EventBridge (Weekly: Mon 9AM UTC)
    ↓
Lambda Function (TagAuditFunction)
    ↓
ResourceGroupsTaggingAPI
    ↓
SNS Topic (TagAuditNotifications)
    ↓
Your Inbox 📧
```

#### Cost Tracker:

- All within Free Tier
- Savings vs AWS Config: $1.00/year
- Running total: $0.00

---

### Phase 2: Lambda Function Development

**Date:** January 17, 2026
**Time Spent:** 3 hours
**Status:** ✅ Complete

#### What I Did:

- [x] Created IAM role (DocProcessingLambdaRole) with S3, Textract, Comprehend permissions
- [x] Wrote document_processor.py (200+ lines)
- [x] Packaged and deployed Lambda (DocumentProcessor)
- [x] Configured S3 trigger on uploads bucket
- [x] Created test invoice image using Python PIL
- [x] Tested end-to-end: upload → extract → analyze → save results
- [x] Verified CloudWatch logs and processed JSON output

#### Cost Tracker:

- Phase 2 total: $0.00
- Running total: $0.00

#### Challenges Faced:

```
Challenge: zip command not found on Windows Git Bash
- Solution: Used PowerShell Compress-Archive instead of debugging automation
- Lesson: Ship first, optimize later — the goal was a deployed Lambda, not perfect scripts
```

---

### Phase 3: Textract Integration Deep Dive

**Date:** January 31, 2026
**Time Spent:** 3 hours
**Status:** ✅ Complete

#### Testing Results:

- Documents tested: 15 (9 invoices, 6 receipts)
- Success rate: 80% (12/15)
- Failures: 3 complex PDFs — UnsupportedDocumentException
- Average confidence: 94.9%
- Cost per document: $0.003170

#### Cost Tracker:

- Comprehend: $0.038
- Running total: $0.038
- Budget remaining: $24.96

---

### Phase 4: Lambda Optimization & PDF Preprocessing

**Date:** March 4, 2026
**Time Spent:** 2 hours
**Status:** ✅ Complete

#### What I Did:

- [x] Built PyPDF2 Lambda layer (python3.11, 715KB)
- [x] Deployed layer (pypdf2-layer:1, ARN: arn:aws:lambda:us-east-1:848747536965:layer:pypdf2-layer:1)
- [x] Attached layer to DocumentProcessor
- [x] Wrote PDF validation and normalization logic in document_processor.py
- [x] Re-tested 3 failed documents — preprocessing worked, Textract still rejected them
- [x] Deliberate decision: ship at 80% with documented remediation path (pdf2image + poppler)
- [x] Full regression test — 12 previously passing documents still pass

#### Architecture Change:

```
BEFORE: S3 Upload → Lambda → Textract (20% failure)
AFTER:  S3 Upload → Lambda → PyPDF2 Preprocessing → Textract (80% — preprocessing foundation in place)
```

#### Challenges Faced:

```
Challenge: PyPDF2 preprocessing worked perfectly — Textract still rejected the same 3 PDFs
- Root cause: Problem was deeper than normalization — fundamental PDF encoding incompatibility
- Decision: Document limitation, define remediation path (pdf2image + poppler), ship at 80%
- Lesson: Not every test has to come back 100%. 80% with a documented path to 100% is honest.
```

#### Cost Tracker:

- Phase 4 total: $0.00
- Running total: $0.038

---

### Phase 5: Frontend Development

**Date:** March 6, 2026
**Time Spent:** ~2 hours
**Status:** ✅ Complete

#### What I Did:

- [x] Built DocFlow static frontend (index.html, styles.css, app.js)
- [x] Drag-and-drop upload with file validation (PDF/JPG/PNG, 10MB limit)
- [x] Animated progress ring with 4 pipeline step indicators
- [x] Result cards showing extracted fields, entities, sentiment, S3 key
- [x] Stats bar: docs processed, avg time, success rate, estimated cost
- [x] CONFIG.SIMULATE = true (Phase 6 API stubs pre-wired)
- [x] Deployed to S3 static website hosting
- [x] Recorded 1-minute Loom demo video

#### Cost Tracker:

- Phase 5 total: $0.00
- Running total: $0.038

---

### Phase 6: API Gateway Integration

**Date:** 2026-03-18 / 2026-03-19
**Time Spent:** ~2.5 hours
**Status:** ✅ Complete

#### What I Did:

- [x] Created REST API (doc-processing-api, REGIONAL, ID: 0r8p6ap199)
- [x] POST /upload → APIUploadHandler Lambda
- [x] GET /results → APIResultsHandler Lambda
- [x] CORS configured on both resources (API Gateway + Lambda response headers)
- [x] Deployed to production stage
- [x] Flipped CONFIG.SIMULATE to false
- [x] Frontend redeployed with live API endpoint
- [x] Tags applied to all new resources
- [x] Smoke tested via CLI and UI — 94.74% confidence on first real document
- [x] Verified in S3 and CloudTrail

#### API Smoke Test:

```bash
curl -X POST https://0r8p6ap199.execute-api.us-east-1.amazonaws.com/prod/upload \
  -H "Content-Type: application/json" \
  -d '{"fileName": "invoice_069_INV-2025-9308.pdf", "fileContent": "[base64]", "contentType": "application/pdf"}'

Response: {"message": "File uploaded successfully", "documentId": "3e618659-8fc7-4f2c-81b3-2428b64732b6", "s3Key": "uploads/3e618659-8fc7-4f2c-81b3-2428b64732b6_invoice_069_INV-2025-9308.pdf"}
```

#### Cost Tracker:

- API Gateway: <$0.01
- Running total: ~$0.52

#### Challenges Faced:

```
Challenge: Lambda zip packaged wrong handler file + nested zip
- Fix: Rebuilt zips using zipfile module, explicitly targeting each handler file
- Lesson: Always verify zip contents with zipfile.namelist() before deploying

Challenge: Syntax error in api_upload_handler.py line 1
- Root cause: Filename header from context file formatting copied into the file
- Fix: Removed the errant header line

Challenge: CloudWatch logs failing in Git Bash
- Fix: Use MSYS_NO_PATHCONV=1 or check logs via console
```

---

### Phase 7: End-to-End Testing

**Date:** 2026-03-19
**Time Spent:** ~1 hour
**Status:** ✅ Complete

#### What I Did:

- [x] Implemented rate limiting via API Gateway Usage Plan (DocFlowKey)
- [x] Rate: 5 req/s, burst 10, daily quota 100 requests
- [x] Ran batch test — all 150 mock documents against live API
- [x] 150/150 passed, 0 failures, 0 errors

#### Testing Results:

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Success rate | >95% | 100% | ✅ |
| Documents passed | 150 | 150/150 | ✅ |
| Failures | <5% | 0 | ✅ |
| Errors | 0 | 0 | ✅ |
| Avg Confidence | >90% | 80.88% | ⚠️ |

> Confidence note: 80.88% is consistent with Phase 3. Complex PDFs pull the average down but all documents processed successfully.

#### Cost Tracker:

- Textract AnalyzeDocTables overage: $3.55 (hit 100 page/month free tier in single batch test)
- Previous running total: ~$0.52
- **Running total: ~$4.07**

#### Key Lesson:

```
Rate limiting protects against per-second abuse — not monthly free tier consumption.
Two different problems. Now I know both.
```

---

### Phase 8: Optimization & Cost Reduction

**Date:** 2026-03-21
**Time Spent:** ~30 minutes
**Status:** ✅ Complete

#### What I Did:

- [x] Right-sized DocumentProcessor Lambda: 512MB → 256MB (max memory used was 43MB)
- [x] Increased APIResultsHandler timeout: 3s → 10s (reliability improvement)
- [x] Smoke tested post-optimization — 94.74% confidence, status: success
- [x] S3 lifecycle policies: already implemented in Phase 1 ✅
- [x] Batch processing: already implemented via batch_test.py ✅

#### Before/After Optimization:

| Metric | Before | After | Savings |
|--------|--------|-------|---------|
| DocumentProcessor memory | 512MB | 256MB | 50% compute cost reduction |
| APIResultsHandler timeout | 3s | 10s | Reliability improvement |

#### Cost Tracker:

- Phase 8 total: $0.00
- Running total: ~$4.07

---

### Phase 9: Documentation & Portfolio Prep

**Date:** 2026-03-21 / 2026-03-24
**Time Spent:** ~3 hours
**Status:** ✅ Complete

#### What I Did:

- [x] Created comprehensive README (updated through Phase 10)
- [x] Wrote Architecture_DataFlow_Documentation.md
- [x] Built three LucidChart architecture diagrams (overview + 2 flow diagrams)
- [x] Captured phase-by-phase screenshots (Phases 1–8 + Phase 10)
- [x] Recorded demo video (Loom — DocFlow pipeline walkthrough)
- [x] Updated portfolio site card (theprojectfolder.com)
- [x] Updated main repo README with Phase 10 additions
- [x] Wrote Substack article v4 (dataflow as backbone)
- [x] Updated AWS_Project_Cost_Tracker.xlsx with final actuals

#### Portfolio Assets Created:

- [x] README.md — full project arc, architecture diagram, cost analysis, margin analysis
- [x] Architecture_DataFlow_Documentation.md — technical reference with data formats
- [x] architecture_diagram.mermaid — version-controlled diagram
- [x] Three LucidChart PNGs — overview, Upload & Process flow, Dashboard & Export flow
- [x] Demo video — Loom recording of live pipeline
- [x] Screenshots — 14 assets covering all phases
- [x] AWS_Project_Cost_Tracker.xlsx — final actuals: $6.90 total
- [x] Substack article draft — v4 pending final edit and publish

#### GitHub Repository:

- URL: https://github.com/theDovelyDev/theprojectfolder/tree/main/IDR_pipeline

---

### Phase 10: Persistence & Output Layer

**Date:** 2026-03-24
**Time Spent:** ~3 hours
**Status:** ✅ Complete

#### What I Did:

- [x] Created DynamoDB table: DocFlowRecords (PAY_PER_REQUEST billing)
- [x] Updated DocumentProcessor to parse documentId from S3 key (fixed UUID mismatch bug)
- [x] Updated DocumentProcessor to write extracted record to DynamoDB after processing
- [x] Created DocFlowNotifications SNS topic — dedicated topic separate from tag audit
- [x] Updated DocumentProcessor to send SNS email notification on successful processing
- [x] Built APIRecordsHandler Lambda — GET /records and GET /export endpoints
- [x] Wired /records and /export to API Gateway with CORS
- [x] Built dashboard.html — records table, stats cards, search, CSV export, detail modal
- [x] Updated app.js — runRealPipeline fully wired, View in Dashboard link on result cards
- [x] Added nav links between index.html and dashboard.html
- [x] Tagged all new resources
- [x] Fixed Decimal serialization error (DynamoDB → JSON)
- [x] Added AWS_DEFAULT_REGION to config/setup.sh

#### Why Phase 10 Existed:

The pipeline was technically complete after Phase 7 — but not practically complete. Data extracted and displayed on a page with nowhere to go is a demo, not a workflow. An SMB owner using this in practice would still be manually cataloging everything. Phase 10 added the output layer that makes the pipeline actually useful: persistent queryable records, email notifications, a dashboard, and CSV export.

#### Cost Tracker:

- DynamoDB: ~$0.00 (PAY_PER_REQUEST, within free tier)
- SNS: ~$0.00 (within free tier)
- Phase 10 total: ~$0.00
- **True project total: ~$6.90**

#### Challenges Faced:

```
Challenge: documentId mismatch — dashboard showing 0 records
- Root cause: DocumentProcessor was generating a new uuid instead of
  parsing the documentId from the S3 key filename
- Fix: Extract documentId from key.split('/')[-1].split('_')[0]
- Lesson: Lambda functions triggered by S3 events must parse identifiers
  from the S3 key — not generate new ones

Challenge: Decimal serialization error
- Error: Object of type Decimal is not JSON serializable
- Root cause: DynamoDB returns numeric types as Python Decimal objects
- Fix: Custom DecimalEncoder class passed to json.dumps in APIRecordsHandler
- Lesson: Always add DecimalEncoder when serializing DynamoDB results to JSON

Challenge: IAM role permissions — SNS and DynamoDB
- Pattern: Role missing permissions for each new service Lambda calls
- Fix: Added DocFlowSNSPolicy and updated DocFlowDynamoDBPolicy inline policies
- Lesson: Every new AWS service call = check the role first, not just the user

Challenge: AWS_DEFAULT_REGION not set
- Error: NoRegion — You must specify a region
- Root cause: setup.sh exported REGION but AWS CLI reads AWS_DEFAULT_REGION
- Fix: Added export AWS_DEFAULT_REGION="us-east-1" to config/setup.sh
```

#### Screenshots Captured:

- [x] Dashboard with records populated
- [x] Detail modal showing extracted data
- [x] CSV export downloaded
- [x] SNS notification email
- [x] DynamoDB table with items

---

## Key Learnings

### Technical Skills Gained

- [x] AWS Lambda serverless architecture
- [x] S3 event-driven triggers
- [x] API Gateway REST API design
- [x] IAM roles and permissions (least-privilege)
- [x] AWS Textract OCR integration
- [x] AWS Comprehend NLP integration
- [x] DynamoDB schema design and serialization
- [x] SNS notification patterns
- [x] CloudWatch monitoring and logging
- [x] Cost optimization and FinOps guardrails

### Biggest Aha Moments

```
1. Ship what works, document what doesn't (Phase 4)
   PyPDF2 preprocessing worked perfectly — Textract still rejected the same
   3 PDFs. The real fix (pdf2image + poppler) would take another 1-2 hours.
   End of week deadline. I stopped. Documented the limitation, defined the
   remediation path, shipped the preprocessing foundation.
   Not every test has to come back 100% to be a passing score.

2. Rate limiting ≠ cost protection (Phase 7)
   Rate limiting protects against per-second abuse. It does not protect against
   monthly free tier consumption. Hit the Textract AnalyzeDocTables free tier
   ceiling in a single batch test — $3.55 overage. Two different problems,
   two different solutions. Now I know both.

3. A pipeline that extracts data but has nowhere to send it isn't complete (Phase 10)
   Almost shipped without the persistence and output layer. The data landed
   in S3 as JSON and displayed on a page — still a manual cataloging problem.
   Phase 10 is the difference between a demo and a product.

4. Every new AWS service call = check the role (Phase 10)
   Users feel tangible because you log in as them. Roles feel abstract.
   But every Lambda calling a new service needs the role permission updated —
   not the user. SNS and DynamoDB both caught me on this in the same phase.

5. CONFIG.SIMULATE is a FinOps pattern, not just a dev convenience (Phase 5/6)
   Build and demo the full frontend experience without burning real API budget.
   Only flip the switch after rate limiting is in place. This order matters.
```

---

## Results & Impact

### Final Metrics

| Metric | Result |
|--------|--------|
| Documents tested | 150 |
| Success rate | 100% |
| Avg extraction confidence | 80.88% |
| Avg processing time | ~30 seconds |
| Cost per document | $0.034 |
| Total build cost | $6.90 |
| vs. manual processing | 97% cheaper |

### ROI Analysis

```
Manual Processing (500 docs/month):
├─ Time: 3 min/doc × 500 = 25 hours/month
├─ Cost: $25/hour × 25 hours = $625/month
└─ Annual: $7,500

Automated Processing (500 docs/month):
├─ AWS Cost: ~$18/month
└─ Annual: $216

Annual Savings: $7,284
ROI: 3,558%
```

### Margin Analysis (If Sold)

| Model | Monthly Revenue | Monthly Cost | Margin |
|-------|----------------|--------------|--------|
| SaaS — SMB tier ($99/month) | $99 | $18 | $81 |
| Managed service ($299/month) | $299 | $18 | $281 |
| Consulting implementation | $2,500–$5,000 one-time | $6.90 build | — |

---

## What's Next

### Future Enhancements

- [ ] OCR fallback: pdf2image + poppler for complex PDFs (Phase 4 remediation path)
- [ ] SQS queue for batch processing at scale
- [ ] Cognito authentication for multi-user access
- [ ] QuickSight dashboard upgrade (~$18/user/month)
- [ ] Dedicated SNS topic per customer
- [ ] Document classification (invoice vs. receipt vs. contract)
- [ ] Handwritten document support via Textract custom models
- [ ] Webhook integration for QuickBooks, Xero, accounting software

### Projects Queue

1. Budget Research Agent — LangGraph, human-in-the-loop cost controls
2. DNS Failover with Route 53 — build, validate ~60s RTO, tear down, document
3. BI/Analytics portfolio — PostgreSQL, Looker Studio, AWS data pipeline

---

## Changelog

**January 16, 2026** — Pre-development setup complete
**January 16, 2026** — Phase 1 complete (S3 buckets, tagging, lifecycle policies)
**January 16, 2026** — Side Quest complete (automated tag governance — Lambda, EventBridge, SNS)
**January 17, 2026** — Phase 2 complete (Lambda + DocumentProcessor)
**January 31, 2026** — Phase 3 complete (Textract testing — 80% success rate, 12/15 docs)
**March 4, 2026** — Phase 4 complete (PyPDF2 preprocessing layer, 80% maintained, limitation documented)
**March 6, 2026** — Phase 5 complete (DocFlow frontend deployed to S3, Loom demo recorded)
**March 18–19, 2026** — Phase 6 complete (API Gateway, live endpoints, CONFIG.SIMULATE flipped)
**March 19, 2026** — Phase 7 complete (150-doc batch test, 100% success, $3.55 Textract overage)
**March 21, 2026** — Phase 8 complete (Lambda right-sized 512MB → 256MB)
**March 21–24, 2026** — Phase 9 complete (README, architecture docs, LucidChart diagrams, Substack draft)
**March 24, 2026** — Phase 10 complete (DynamoDB, SNS, dashboard, CSV export)
**March 24, 2026** — Project complete. Total cost: $6.90. Total time: ~35 hours.