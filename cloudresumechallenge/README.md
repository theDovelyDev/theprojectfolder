# ☁️ The Cloud Resume Challenge

A full-stack serverless portfolio site built on AWS — the long way, on purpose.

[![AWS](https://img.shields.io/badge/AWS-Serverless-orange?logo=amazon-aws)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![IaC](https://img.shields.io/badge/IaC-CloudFormation-red?logo=amazon-aws)](https://aws.amazon.com/cloudformation/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-black?logo=github)](https://github.com/features/actions)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Project Status:** ✅ Live in Production  
> **Monthly Cost:** ~$0.50 (Route 53 hosted zone only)  
> **Started:** 2023  
> **Live Site:** [www.theprojectfolder.com](https://www.theprojectfolder.com)  
> **Read the Build Post:** [Substack — What I Actually Learned Building My Portfolio Site on AWS](https://open.substack.com/pub/carlandrainthecloud/p/i-almost-let-one-wrong-s3-bucket?utm_campaign=post-expanded-share&utm_medium=web)  
> **FinOps Analysis:** [I Built a Website on AWS and Then Did a FinOps Analysis on It](https://open.substack.com/pub/carlandrainthecloud/p/i-built-a-website-on-aws-and-then?utm_campaign=post-expanded-share&utm_medium=web)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Why This Project](#why-this-project)
- [Solution Architecture](#solution-architecture)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Cost Analysis](#cost-analysis)
- [CI/CD Pipeline](#cicd-pipeline)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Key Learnings](#key-learnings)
- [Future Enhancements](#future-enhancements)
- [Resources](#resources)

---

## 🎯 Overview

This project is my implementation of [The Cloud Resume Challenge](https://cloudresumechallenge.dev/docs/the-challenge/aws/) — a 16-step project that bridges cloud certification with real-world DevOps skills.

The result is a fully serverless, production-grade portfolio site with a live visitor counter, HTTPS, custom domain, infrastructure as code, and an automated CI/CD pipeline. No servers. No manual deployments. No hardcoded credentials.

**Why it matters for FinOps:** As a FinOps professional, hands-on cloud experience directly strengthens the conversations I have with Engineering and Product teams. You can only get so far advising on cloud costs from a spreadsheet. At some point, you have to build something.

---

## 💡 Why This Project

FinOps sits at the intersection of Finance and DevOps — maximizing the business value of cloud spend. That means working closely with engineering teams who are building the infrastructure that drives the bill.

This project was about closing the gap between the work I analyze and the work I advise on. Building it gave me:

- Firsthand experience with the architectural decisions that drive cloud costs
- A working understanding of serverless tradeoffs (Lambda Function URL vs. API Gateway — see cost analysis below)
- Practical IaC and CI/CD experience in a real production environment
- A foundation for every cloud project that follows

---

## 🏗️ Solution Architecture

```
┌─────────────────────────────────────────────────────┐
│                      User                           │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              Amazon Route 53                        │  ← DNS (custom domain)
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│             Amazon CloudFront                       │  ← CDN + HTTPS termination
│          + AWS Certificate Manager                  │  ← Free TLS certificate
└──────────┬───────────────────────────┬──────────────┘
           │                           │
           ▼                           ▼
┌─────────────────────┐    ┌────────────────────────────┐
│   Amazon S3         │    │  Lambda Function URL        │  ← Visitor counter API
│  (Static Assets)    │    │  (No API Gateway needed)    │
└─────────────────────┘    └────────────────┬───────────┘
                                            │
                                            ▼
                               ┌────────────────────────┐
                               │     Amazon DynamoDB     │  ← Visitor count store
                               └────────────────────────┘

┌─────────────────────────────────────────────────────┐
│              GitHub Actions (CI/CD)                 │  ← Auto-deploy on push
│              + OIDC (no stored credentials)         │
└─────────────────────────────────────────────────────┘
```

### Request Flow

1. **DNS** → User hits `theprojectfolder.com`, Route 53 resolves to CloudFront
2. **CDN** → CloudFront serves cached assets from nearest edge location
3. **HTTPS** → ACM certificate handles TLS — no manual cert management
4. **Static assets** → HTML, CSS, images served from S3 origin (CloudFront handles egress)
5. **Visitor counter** → JavaScript triggers POST to Lambda Function URL
6. **Backend** → Lambda atomically increments DynamoDB counter and returns count
7. **Display** → Frontend renders visitor count

---

## ✨ Key Features

**Built with ☁️ AWS, 🐍 Python, ☕ stubbornness, and the willingness to delete everything and start over.**

### Frontend

- 🌐 **Custom domain** with HTTPS via Route 53 + ACM
- ⚡ **Global CDN delivery** via CloudFront (100 GB/month free tier)
- 📊 **Live visitor counter** — real-time, serverless
- 📱 **Responsive design** — works on all devices

### Backend

- ⚡ **Lambda Function URL** — replaces API Gateway for single-endpoint use case
- 🗄️ **DynamoDB On-Demand** — elastic scaling, no capacity planning
- 🔒 **IAM least-privilege** — Lambda role scoped to specific table operations only
- 🌐 **CORS configured** — locked to production domain origin

### Infrastructure & DevOps

- 📦 **Infrastructure as Code** — CloudFormation templates for reproducible deploys
- 🔄 **CI/CD pipeline** — GitHub Actions auto-deploys on push to main
- 🔑 **OIDC authentication** — no long-lived AWS credentials stored in GitHub
- 🏷️ **Resource tagging** — all resources tagged `Project: CloudResume` for cost visibility

---

## 🛠️ Technology Stack

### AWS Services

| Service                     | Role                                                        |
| --------------------------- | ----------------------------------------------------------- |
| **S3**                      | Static website hosting (HTML, CSS, JS, images, resume PDF)  |
| **CloudFront**              | CDN, HTTPS termination, edge caching                        |
| **AWS Certificate Manager** | Free TLS certificate, auto-renewal                          |
| **Route 53**                | DNS management, custom domain                               |
| **Lambda**                  | Serverless visitor counter backend (Python)                 |
| **DynamoDB**                | Visitor count persistence (On-Demand, Standard table)       |
| **CloudFormation**          | Infrastructure as Code                                      |
| **IAM**                     | Roles and policies (OIDC for GitHub, Lambda execution role) |

### Languages & Tools

| Tool                      | Use                            |
| ------------------------- | ------------------------------ |
| **HTML5 / CSS3**          | Frontend site                  |
| **JavaScript (ES6+)**     | Visitor counter fetch calls    |
| **Python 3.x**            | Lambda function                |
| **CloudFormation (YAML)** | Infrastructure as Code         |
| **GitHub Actions**        | CI/CD pipeline                 |
| **AWS CLI**               | Local deployment and debugging |

---

## 💰 Cost Analysis

### The Real Monthly Cost

| Service                  | Free Tier                           | Monthly Cost |
| ------------------------ | ----------------------------------- | ------------ |
| S3 Storage               | 5 GB / 12 mo (then $0.023/GB)       | $0.00        |
| S3 GET Requests          | 20K/mo free                         | $0.00        |
| CloudFront Data Transfer | **100 GB/mo free (permanent†)**     | $0.00        |
| CloudFront Requests      | **1M req/mo free (permanent†)**     | $0.00        |
| ACM Certificate          | Always free                         | $0.00        |
| Lambda Requests          | 1M req/mo free (permanent)          | $0.00        |
| Lambda Compute           | 400K GB-seconds/mo free (permanent) | $0.00        |
| DynamoDB                 | 25 WCU/RCU provisioned free         | $0.00        |
| Route 53 Hosted Zone     | —                                   | **$0.50**    |
| Route 53 DNS Queries     | First 1B queries/mo: $0.40/million  | ~$0.00       |
| **Total Monthly**        |                                     | **~$0.50**   |

_† CloudFront Free tier updated November 2025 — permanent, not the 12-month trial_

**Domain registration:** ~$13/year (one-time annual cost via Route 53)  
**Effective annual cost:** ~$6 (hosted zone) + $13 (domain) = **~$19/year**

### Lambda Function URL vs. API Gateway

The challenge originally prescribes API Gateway. I replaced it with a Lambda Function URL. Here's why:

|                              | Lambda Function URL          | API Gateway (HTTP API)            |
| ---------------------------- | ---------------------------- | --------------------------------- |
| **Cost (10K visitors/mo)**   | $0.00                        | ~$0.01                            |
| **Cost (1M visitors/mo)**    | $0.00                        | ~$1.00                            |
| **Request pricing**          | Included in Lambda free tier | $1.00/million (after free tier)   |
| **Advanced features**        | IAM auth only                | Auth, throttling, stages, logging |
| **Setup complexity**         | Simple                       | Moderate                          |
| **Right for this use case?** | ✅ Yes                       | ❌ Overengineered                 |

**FinOps decision:** One endpoint. One operation. Lambda Function URL is the right-sized solution. API Gateway adds cost and complexity for features a visitor counter doesn't need. If I add multiple routes or need rate limiting, I'll revisit.

### Scaling Cost Projections

| Monthly Visitors | S3     | CloudFront | Lambda | DynamoDB | Route 53 | **Total**  |
| ---------------- | ------ | ---------- | ------ | -------- | -------- | ---------- |
| 1,000            | $0.00  | $0.00      | $0.00  | $0.00    | $0.50    | **$0.50**  |
| 10,000           | $0.00  | $0.00      | $0.00  | $0.00    | $0.50    | **$0.50**  |
| 50,000           | $0.00  | $0.00      | $0.00  | $0.00    | $0.50    | **$0.50**  |
| 100,000          | ~$0.01 | $0.00†     | $0.00  | $0.00    | $0.50    | **~$0.51** |

_† CloudFront Free tier covers 100 GB/month. At ~1 MB/visitor, 100 GB = ~100,000 visitors before any CloudFront charges._

**Budget alert configured at $5.00/month.** Anything above $1.00 signals a misconfiguration worth investigating.

---

## 🔄 CI/CD Pipeline

### Why OIDC Instead of Access Keys

Most CI/CD tutorials for S3 deploys tell you to store AWS access keys as GitHub secrets. I didn't do that.

From time spent in Vulnerability Management, I know what hardcoded credentials cost — in audit findings, in incident response time, in the quiet dread of wondering if something already leaked. GitHub's OIDC integration with AWS eliminates long-lived credentials entirely.

### How It Works

```
Push to main branch
        ↓
GitHub Actions triggered
        ↓
GitHub requests OIDC token from GitHub's identity provider
        ↓
AWS STS exchanges token for short-lived credentials
        ↓
IAM role assumed (scoped to S3 sync + CloudFront invalidation only)
        ↓
Site deployed — credentials expire automatically
```

**Result:** No stored AWS credentials anywhere. No rotation schedule. No risk of accidental key exposure in commit history.

### Pipeline Steps

```yaml
# Simplified flow
1. Checkout code
2. Configure AWS credentials via OIDC (no keys stored)
3. Sync HTML/CSS/JS/images to S3 bucket
4. Create CloudFront cache invalidation (/* path)
5. Verify deployment
```

---

## 📁 Project Structure

```
theprojectfolder/
├── README.md                        ← You are here
├── index.html                       ← Main portfolio page
├── images/                          ← Profile photo, cert badges, project images
│   ├── profile_pic.jpg
│   ├── aws-certified-cloud-practitioner.png
│   ├── finops-certified-practitioner.png
│   └── ...
├── content/                         ← Additional HTML pages
├── .github/
│   └── workflows/
│       └── deploy.yml               ← GitHub Actions CI/CD pipeline
└── infrastructure/                  ← CloudFormation templates
    ├── s3-cloudfront.yaml           ← Frontend infrastructure
    └── lambda-dynamodb.yaml         ← Backend infrastructure
```

---

## 🚀 Getting Started

Want to build your own version? Here's the honest path:

### Prerequisites

- AWS account (free tier works for this entire project)
- AWS CLI configured locally
- GitHub account
- Your own domain (Route 53 or external registrar)
- AWS Cloud Practitioner certification (Step 1 of the challenge — do it first)

### High-Level Steps

```bash
# 1. Create two S3 buckets (root domain + www redirect)
aws s3 mb s3://yourdomain.com
aws s3 mb s3://www.yourdomain.com

# 2. Enable static website hosting
aws s3 website s3://yourdomain.com --index-document index.html

# 3. Request ACM certificate (us-east-1 region required for CloudFront)
aws acm request-certificate \
  --domain-name yourdomain.com \
  --subject-alternative-names www.yourdomain.com \
  --validation-method DNS \
  --region us-east-1

# 4. Create CloudFront distribution pointing to S3 origin
# (Use the console for first time — easier to configure SSL cert binding)

# 5. Set up Route 53 hosted zone + A records pointing to CloudFront

# 6. Create DynamoDB table
aws dynamodb create-table \
  --table-name VisitorCounter \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --tags Key=Project,Value=CloudResume

# 7. Deploy Lambda function with Function URL enabled
# (See infrastructure/lambda-dynamodb.yaml for full IaC)

# 8. Configure GitHub Actions OIDC
# (See .github/workflows/deploy.yml)
```

### The One Mistake to Avoid

**Create two S3 buckets from the start** — one for your root domain (`yourdomain.com`), one for the www redirect (`www.yourdomain.com`). Trying to make one bucket work for both is a week of debugging you don't need. Start clean.

---

## 💡 Key Learnings

### 1. Starting Over Is Faster Than Defending a Bad Decision

Created one S3 bucket instead of two. Spent a week trying to patch around it. Deleted everything, started fresh, had a working HTTPS site in 20 minutes. The lesson applies at every scale of cloud architecture.

### 2. Implicit Setup ≠ Explicit Permission

Lambda auto-created its execution role — but that role had no DynamoDB permissions. A quick IAM update fixed it. The same principle governs cost visibility: just because a resource exists in your account doesn't mean you can see what it costs without explicit tagging.

### 3. Security Shortcuts Create Long-Term Liability

Every GitHub Actions tutorial said to store access keys. I spent extra time finding the OIDC solution. That time investment pays forward every time I don't have to rotate credentials or investigate a leaked key.

### 4. Pricing Models Change — Your Estimates Should Too

My original CloudFront cost estimates were accurate for 2024 pricing. CloudFront launched a new Free tier in November 2025 that changed the economics entirely. FinOps isn't a one-time analysis — it's a practice of continuous re-evaluation.

### 5. Right-Sizing Starts at Architecture Design

Lambda Function URL vs. API Gateway isn't just a cost question — it's an architectural question. Choosing the right service for the actual use case (one endpoint, one operation) is cheaper, simpler, and easier to maintain. That's the FinOps mindset applied at the infrastructure layer.

### 6. Tag Everything Before You Deploy Anything

All resources tagged with `Project: theprojectfolder` before first deployment. Filtering Cost Explorer by this tag gives me an exact dollar figure for this project at any time. At portfolio scale this seems trivial. At $200M enterprise scale, this discipline is how you generate $1.5M in cost avoidance.

---

## 🔭 Future Enhancements

- [ ] Add Terraform version of infrastructure (learning path item)
- [ ] Per-page visitor tracking (separate DynamoDB items per route)
- [ ] CloudWatch dashboard for traffic metrics
- [ ] Geographic visitor distribution via CloudFront access logs
- [ ] Automated 30-day cost forecast vs. actuals comparison (see FinOps analysis)
- [ ] Dark mode toggle

---

## 📚 Resources

### The Challenge

- [Cloud Resume Challenge — Official Site](https://cloudresumechallenge.dev/docs/the-challenge/aws/)
- [Original challenge created by Forrest Brazeal](https://forrestbrazeal.com/)

### My Write-Ups

- [What I Actually Learned Building My Portfolio Site on AWS](https://open.substack.com/pub/carlandrainthecloud/p/i-almost-let-one-wrong-s3-bucket?utm_campaign=post-expanded-share&utm_medium=web) — honest reflection on what went wrong and why
- [I Built a Website on AWS and Then Did a FinOps Analysis on It](https://substack.com/home) — cost model, pricing corrections, 30-day forecast

### AWS Documentation

- [S3 Static Website Hosting with Custom Domain](https://docs.aws.amazon.com/AmazonS3/latest/userguide/website-hosting-custom-domain-walkthrough.html)
- [CloudFront with S3 Origin](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/GettingStarted.SimpleDistribution.html)
- [Lambda Function URLs](https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls.html)
- [GitHub Actions OIDC with AWS](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [DynamoDB On-Demand Pricing](https://aws.amazon.com/dynamodb/pricing/on-demand/)

### FinOps

- [FinOps Foundation Framework](https://www.finops.org/framework/)
- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
- [AWS Budgets](https://aws.amazon.com/aws-cost-management/aws-budgets/)

---

## 📬 Connect

- **Live Site:** [theprojectfolder.com](https://www.theprojectfolder.com)
- **LinkedIn:** [Carlandra Williams](https://www.linkedin.com/in/carlandrawilliams)
- **Substack:** [Carlandra in the Cloud](https://substack.com/@carlandrainthecloud)
- **GitHub:** [@theDovelyDev](https://github.com/theDovelyDev)
- **Email:** carlandra.williams@gmail.com

---

## 📄 License

MIT License — fork it, build your own version, share what you learn.

---

_Part of [The Project Folder](https://www.theprojectfolder.com) — a working portfolio, not a highlight reel._

_Last Updated: March 2026_
