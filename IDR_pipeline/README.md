# 🤖 DocFlow — Intelligent Document Processing Pipeline

AI-powered document extraction and analysis system built on AWS serverless architecture. Drop in an invoice or receipt, get back structured data in under 30 seconds.

[![AWS](https://img.shields.io/badge/AWS-Serverless-orange?logo=amazon-aws)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen)]()
[![Cost](https://img.shields.io/badge/Total%20Cost-$6.90-yellow)]()

> **Project Status:** ✅ Complete — All 10 Phases  
> **Total Cost:** $6.90 / $25.00 Budget  
> **Timeline:** January 16 – March 24, 2026  
> **Live Demo:** [DocFlow Pipeline](https://doc-processing-demo-frontend-848747536965.s3-website-us-east-1.amazonaws.com)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Results](#results)
- [Cost Analysis](#cost-analysis)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Development Progress](#development-progress)
- [Key Learnings](#key-learnings)
- [Future Enhancements](#future-enhancements)
- [Contact](#contact)

---

## 🎯 Overview

### The Problem
Manual document processing takes 3 minutes per document and costs $1.25 in staff time — tedious, error-prone, and doesn't scale.

### The Solution
A fully serverless AWS pipeline that:
- ⚡ Processes documents in **30 seconds**
- 💵 Costs **$0.034 per document**
- 🎯 Achieved **100% success rate** on 150-document batch test
- 📊 Extracts text, key-value pairs, entities, and sentiment automatically

---

## 🏗️ Architecture

```
User
  │
  ▼
Frontend (S3 Static Hosting)
  │  drag-and-drop upload · records dashboard
  ▼
API Gateway (REST API)
  │  POST /upload  │  GET /results  │  GET /records  │  GET /export
  ▼                ▼                ▼                ▼
APIUploadHandler  APIResultsHandler  APIRecordsHandler  APIRecordsHandler
(Lambda)          (Lambda)           (Lambda)           (Lambda)
  │
  ▼
S3 Uploads Bucket
  │  S3 event trigger
  ▼
DocumentProcessor (Lambda)
  │
  ├──────────────────────┐
  ▼                      ▼
AWS Textract         AWS Comprehend
(text extraction,    (entity detection,
 key-value pairs,     sentiment analysis,
 table data)          key phrases)
  │
  ├─────────────────────────────┐
  ▼                             ▼
S3 Processed Bucket         DynamoDB (DocFlowRecords)
(results JSON)               (persistent record store)
  │                             │
  ▼                             ▼
CloudWatch                   SNS → Email Notification
(logging + monitoring)       (DocFlowNotifications)
```

### Data Flow
1. **Upload** → User drops document into web UI
2. **Store** → File saved to S3 uploads bucket via API Gateway
3. **Trigger** → S3 event fires DocumentProcessor Lambda
4. **Extract** → Textract pulls text, forms, tables
5. **Analyze** → Comprehend detects entities, sentiment, key phrases
6. **Save** → Structured JSON written to processed bucket
7. **Persist** → Record written to DynamoDB DocFlowRecords
8. **Notify** → SNS email sent via DocFlowNotifications
9. **Retrieve** → Frontend polls results via GET /results
10. **Display** → Results rendered with "View in Dashboard →" link
11. **Dashboard** → GET /records → APIRecordsHandler → DynamoDB scan
12. **Export** → GET /export → APIRecordsHandler → CSV download

---

## ✨ Key Features

**Core Pipeline**
- 📄 PDF document processing with PyPDF2 preprocessing layer
- 🔍 OCR text extraction via AWS Textract
- 📊 Key-value pair extraction (invoice numbers, totals, dates)
- 🏷️ Entity recognition (organizations, locations, dates, amounts)
- 😐 Sentiment analysis on document content
- 💡 Key phrase extraction

**Persistence & Output (Phase 10)**
- 🗄️ DynamoDB record store — every processed document queryable
- 📧 SNS email notification per document processed
- 📋 Records dashboard — sortable, searchable, with detail modal
- 📥 CSV export — one-click download of all records
- 🔗 "View in Dashboard →" link on every result card

**Infrastructure**
- ☁️ Fully serverless — no servers to manage
- 🔄 Event-driven processing via S3 triggers
- 🔒 Rate limiting: 5 req/s, burst 10, 100 req/day (FinOps guardrail)
- 🏷️ Comprehensive resource tagging with automated weekly compliance audits
- 📈 Auto-scaling under variable load

**FinOps**
- Rate limiting implemented before going live (prevents runaway costs)
- CONFIG.SIMULATE flag for safe frontend development without hitting real APIs
- Weekly tag audit Lambda (EventBridge + SNS) for cost allocation governance
- True project cost: $6.90 — $3.55 of which came from a single 150-doc batch test

---

## 🛠️ Technology Stack

| Category | Services / Tools |
|----------|-----------------|
| Compute | AWS Lambda (Python 3.11) |
| Storage | AWS S3 (3 buckets: uploads, processed, frontend) |
| Database | AWS DynamoDB (DocFlowRecords) |
| AI/ML | AWS Textract, AWS Comprehend |
| API | AWS API Gateway (REST, REGIONAL) |
| Notifications | AWS SNS (DocFlowNotifications) |
| Monitoring | AWS CloudWatch, AWS CloudTrail |
| Automation | AWS EventBridge, AWS SNS |
| Security | AWS IAM |
| Frontend | HTML5, CSS3, JavaScript ES6+ |
| Tooling | AWS CLI, Python, Bash, Git |

---

## 📊 Results

| Metric | Result |
|--------|--------|
| Documents tested | 150 |
| Success rate | 100% |
| Avg extraction confidence | 80.88% |
| Avg processing time | <30 seconds |
| Cost per document | $0.034 |
| vs. manual processing | 97% cheaper |
| Total project cost | $6.90 |

> **Confidence note:** 80.88% average reflects complex PDFs pulling the score down. Simple/medium documents consistently hit 94%+. Deep incompatibilities with complex PDFs are documented with a remediation path (pdf2image + poppler) in Phase 4.

---

## 💰 Cost Analysis

### Development Cost (Actual)

| Phase | Activity | Cost |
|-------|----------|------|
| 1–6 | S3, Lambda, API Gateway, testing | ~$0.52 |
| 7 | 150-document batch test (Textract AnalyzeDocTables) | $3.55 |
| 8 | Optimization smoke test | $0.00 |
| 9–10 | Dashboard, DynamoDB, SNS, records handler | ~$2.83 |
| **Total** | | **$6.90** |

> The $3.55 Textract overage came from hitting the 100-page/month free tier limit for AnalyzeDocTables in a single batch test. Rate limiting (100 req/day cap) prevents this in ongoing use.

### Production Cost Model (500 docs/month)

| Service | Monthly Cost |
|---------|-------------|
| S3 Storage | $1.15 |
| S3 Requests | $0.01 |
| Lambda | $1.25 |
| Textract | $1.50 |
| Comprehend | $10.00 |
| API Gateway | $0.01 |
| DynamoDB | $0.50 |
| SNS | $0.50 |
| CloudWatch | $2.00 |
| Data Transfer | $0.90 |
| **Total** | **~$18/month** |

**Annual production cost:** ~$216  
**vs. manual processing (500 docs/month):** $625/month  
**Annual savings:** $6,036 (80% reduction)  
**ROI:** 3,558%

### Margin Analysis

| Model | Monthly Revenue | Monthly Cost | Margin |
|-------|----------------|--------------|--------|
| SaaS — SMB tier ($99/month) | $99 | $18 | $81 |
| Managed service ($299/month) | $299 | $18 | $281 |
| Consulting implementation | $2,500–$5,000 one-time | $6.90 build | — |

---

## 📁 Project Structure

```
IDR_pipeline/
├── config/
│   ├── setup.sh                    ← Environment variables + tagging config
│   └── resource-tags.json          ← Standard tag definitions
├── docs/
│   ├── screenshots/                ← Phase-by-phase screenshots
│   ├── Architecture_DataFlow_Documentation.md
│   ├── Architecture_Diagram_Visual.html
│   ├── AWS_Project_Cost_Tracker.xlsx
│   ├── Doc_Processing_Development_Log.md
│   ├── Document_Processing_Implementation_Guide.md
│   └── TAGGING_STRATEGY.md
├── lambda/
│   ├── api-upload-handler/         ← POST /upload handler
│   ├── api-results-handler/        ← GET /results handler
│   ├── api-records-handler/        ← GET /records + GET /export handler
│   ├── document-processor/         ← Core Textract + Comprehend + DynamoDB + SNS
│   ├── layers/                     ← PyPDF2 Lambda layer
│   └── tag-audit/                  ← Weekly tag compliance function
├── policies/
│   ├── bucket-policy-uploads.json
│   ├── lambda-audit-trust-policy.json
│   ├── lambda-trust-policy.json
│   ├── lifecycle-policy.json
│   ├── s3-notification.json
│   └── tag-audit-policy.json
├── scripts/
│   ├── batch_test.py               ← 150-document batch test runner
│   ├── check-results.py
│   ├── fix-tags.sh                 ← Apply standard tags to any resource ARN
│   ├── generate-test-documents.py
│   ├── monitor-lambda.sh
│   ├── select-test-documents.py
│   ├── upload-document.sh
│   ├── verify-phase1.sh
│   └── verify-tag-audit.sh
├── src/
│   └── frontend/
│       ├── index.html              ← Upload UI + pipeline visualization
│       ├── dashboard.html          ← Records table, stats, CSV export
│       ├── styles.css
│       └── app.js                  ← Live API pipeline, dashboard link
├── test-results/
│   ├── phase3-results/             ← 15-document Textract testing results
│   └── test-results-phase7.json   ← 150-document batch test output
├── .env
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- AWS account with free tier active
- AWS CLI configured
- Python 3.11
- Git Bash (Windows) or Terminal (Mac/Linux)

### Setup

```bash
# Clone the repo
git clone https://github.com/theDovelyDev/theprojectfolder.git
cd theprojectfolder/IDR_pipeline

# Copy and configure environment
cp config/setup.sh.example config/setup.sh
# Edit setup.sh with your AWS account ID and preferences

# Load environment
source config/setup.sh
```

### Deploy

Follow the [Implementation Guide](docs/Document_Processing_Implementation_Guide.md) for full phase-by-phase deployment instructions.

---

## 📈 Development Progress

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | S3 Setup + Tag Governance | ✅ Complete |
| Phase 2 | Lambda + Document Processor | ✅ Complete |
| Phase 3 | Textract Integration + Testing | ✅ Complete |
| Phase 4 | PDF Preprocessing + Lambda Optimization | ✅ Complete |
| Phase 5 | Frontend Development | ✅ Complete |
| Phase 6 | API Gateway Integration | ✅ Complete |
| Phase 7 | End-to-End Testing (150 docs) | ✅ Complete |
| Phase 8 | Optimization & Cost Reduction | ✅ Complete |
| Phase 9 | Documentation & Portfolio Prep | ✅ Complete |
| Phase 10 | Persistence & Output Layer | ✅ Complete |

---

## 💡 Key Learnings

**Engineering**
- Preprocessing has limits — PyPDF2 normalization improved Textract compatibility but couldn't fix deep encoding incompatibilities in complex PDFs. Ship with documented limitations and a remediation path.
- Rate limiting is a FinOps concern, not just a security one — implement it before going live, not after.
- `CONFIG.SIMULATE` flags let you build and demo frontends without burning API budget.
- DynamoDB returns numeric types as Python `Decimal` objects — always add a custom `DecimalEncoder` when serializing to JSON.
- Every new AWS service a Lambda calls requires a role permission update — not just the user, the role.

**AWS-Specific**
- CORS must be configured in two places for Lambda proxy integration: API Gateway AND Lambda response headers.
- Lambda zip packaging requires explicit file targeting — `shutil.make_archive()` will pick up everything in the directory including nested zips.
- CloudWatch log group names cause path conversion errors in Git Bash on Windows — use `MSYS_NO_PATHCONV=1`.
- `AWS_DEFAULT_REGION` is the environment variable the AWS CLI reads — exporting `REGION` alone isn't enough.

**FinOps**
- The $3.55 Textract overage from batch testing revealed that rate limiting protects against per-second abuse but not monthly free tier consumption — two different problems, two different solutions.
- Build-and-test at scale is what surfaces real cost behavior. That's the point.
- A pipeline that extracts data but has nowhere to send it isn't a complete solution — the output layer is the difference between a demo and a product.

---

## 📎 Additional Artifacts

| Artifact | Description |
|----------|-------------|
| [Governance Assessment](docs/DocFlow_Governance_Assessment.md) | NIST AI RMF alignment report — what's in place, gaps, and enterprise remediation path |
| [Pitch Deck](docs/DocFlow_Pitch_Deck.html) | Interactive product pitch — unit economics, pricing tiers, complete product roadmap |
| [Substack Article](https://carlandrainthecloud.substack.com/p/ship-what-works-document-what-doesnt) | Full build story — 10 phases, $6.90, every engineering decision |
| [AI Governance Article](https://carlandrainthecloud.substack.com) | What FinOps taught me about AI governance — the practitioner pivot piece |

---

## 🚀 Future Enhancements

- [ ] OCR fallback pipeline: pdf2image + poppler for complex PDFs (remediation for 20% failure case)
- [ ] SQS queue for batch processing at scale
- [ ] Cognito authentication for multi-user access
- [ ] QuickSight dashboard upgrade (~$18/user/month) for managed BI and sharing
- [ ] Dedicated SNS topic per customer (currently shared DocFlowNotifications)
- [ ] Document classification (invoice vs. receipt vs. contract)
- [ ] Support for handwritten documents via Textract custom models
- [ ] Multi-language support via Comprehend
- [ ] Webhook integration for pushing results to QuickBooks, Xero, or accounting software

---

## 📬 Contact & Links

- **GitHub:** [theDovelyDev](https://github.com/theDovelyDev)
- **LinkedIn:** [Carlandra Williams](https://linkedin.com/in/carlandra-williams)
- **Portfolio:** [theprojectfolder.com](https://theprojectfolder.com)
- **Substack:** [Carlandra in the Cloud](https://carlandrainthecloud.substack.com)

---

*Built with ☁️ AWS, 🐍 Python, and the honest acknowledgment that $3.55 of the $6.90 total came from proving it actually works at scale.*

*Last Updated: March 24, 2026*