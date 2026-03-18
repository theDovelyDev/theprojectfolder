# 🤖 Intelligent Document Processing Pipeline

AI-powered document extraction and analysis built on AWS serverless architecture.

[![AWS](https://img.shields.io/badge/AWS-Serverless-orange?logo=amazon-aws)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Status:** 🚧 In Development — Phase 5 Complete
> **Cost So Far:** $0.038 / $25.00 budget  
> **Success Rate:** 80% (12/15 documents) — DocFlow frontend deployed
> **Last Updated:** March 6, 2026

---

## What It Does

Automates document processing for invoices, receipts, and forms — replacing 3 minutes of manual work with 30 seconds of serverless processing at $0.034 per document.

**Input:** Upload a PDF, JPG, or PNG to S3
**Output:** Structured JSON with extracted text, key-value pairs, entities, and sentiment

---

## Architecture

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Frontend (S3)      │  ← Upload interface
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  API Gateway        │  ← REST API
└──────┬──────────────┘
       │
       ▼
┌─────────────────────────────┐
│  Lambda Functions           │  ← Processing logic
│  + PyPDF2 Layer             │  ← PDF preprocessing (Phase 4)
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  PDF Preprocessing (PyPDF2) │  ← Validate, decrypt, normalize
└──────┬──────────────────────┘  ← Non-PDF files skip this step
       │
       ├──────────────────────
       ▼                      ▼
┌──────────────────┐   ┌──────────────────┐
│  S3 Buckets      │   │  AI Services     │
│  • Uploads       │   │  • Textract      │
│  • Processed     │   │  • Comprehend    │
│  • Preprocessed  │   │                  │
└──────────────────┘   └──────────────────┘
       │
       ▼
┌─────────────────────┐
│  CloudWatch         │  ← Monitoring & logging
└─────────────────────┘
```

**Data Flow:**

1. User uploads document → S3 triggers Lambda
2. PyPDF2 preprocesses PDFs (validates, decrypts, normalizes)
3. Textract extracts text, forms, and tables
4. Comprehend identifies entities, sentiment, and key phrases
5. Results saved as structured JSON to processed bucket

> ⚠️ **Known Limitation:** Some complex PDFs remain incompatible with Textract after normalization. Remediation path: pdf2image + poppler fallback. Tracked in the dev log.

---

## Tech Stack

**AWS:** S3, Lambda, Textract, Comprehend, API Gateway, CloudWatch, EventBridge, SNS, IAM
**Languages:** Python 3.11, JavaScript (ES6+)
**Tools:** AWS CLI, Boto3, PyPDF2, Git

---

## Project Structure

```
idr_pipeline/
├── lambda/
│   ├── document-processor/    ← Main processing function
│   ├── tag-audit/             ← Automated tag governance
│   └── layers/
│       └── pypdf2/            ← PDF preprocessing layer
├── config/                    ← Tags, policies, environment config
├── docs/                      ← Development log, implementation guide
├── scripts/                   ← Deployment and audit scripts
├── src/                       ← Frontend
└── test-documents/            ← 150 mock documents for testing
```

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/YOUR-USERNAME/idr_pipeline.git
cd idr_pipeline

# Load environment variables
cp setup.sh.example setup.sh
# Edit setup.sh with your AWS account details
source setup.sh

# Verify AWS connection
aws sts get-caller-identity
```

See the Implementation Guide in /docs for full setup instructions.

---

## Cost

| Phase                          | Running Total |
| ------------------------------ | ------------- |
| Phase 1 — S3 Infrastructure    | $0.00         |
| Phase 2 — Lambda Development   | $0.00         |
| Phase 3 — Textract Integration | $0.038        |
| Phase 4 — Lambda Optimization  | $0.038        |
| Phase 5 — Frontend (S3 Deploy) | $0.038        |

**Estimated production cost:** ~$17/month for 500 documents
**vs manual processing:** $625/month — 97% cost reduction

---

## Progress

- ✅ Phase 0 — Pre-Development Setup
- ✅ Phase 1 — S3 Infrastructure + Tag Governance
- ✅ Phase 2 — Lambda Function Development
- ✅ Phase 3 — Textract & Comprehend Integration
- ✅ Phase 4 — Lambda Optimization & PDF Preprocessing
- ✅ Phase 5 — Frontend Development (DocFlow static site deployed to S3)
- 🚧 Phase 6 — API Gateway Integration
- ⬜ Phase 7 — End-to-End Testing
- ⬜ Phase 8 — Optimization & Cost Reduction
- ⬜ Phase 9 — Documentation & Portfolio Prep

---

## Dev Log & Writing

## Dev Log & Writing

Full development log: docs/Doc_Processing_Development_Log.md

Substack: [Carlandra in the Cloud](https://carlandrainthecloud.substack.com)
Live demo: http://doc-processing-demo-frontend-848747536965.s3-website-us-east-1.amazonaws.com

---

## License

MIT — see LICENSE file

---

_Built with AWS and Python_
_Started January 16, 2026 · Total time invested: 12 hours_
