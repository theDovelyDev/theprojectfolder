# AWS Resource Tagging Strategy

cat > TAGGING_STRATEGY.md << 'EOF'

# AWS Resource Tagging Strategy

## 🎯 Purpose

This tagging strategy enables:

- **Cost tracking** across multiple projects in one AWS account
- **Resource organization** (find all resources for a specific project)
- **Year-end cost analysis** (which project cost how much?)
- **Automation** (identify resources for backup, cleanup, etc.)

---

## 📋 Standard Tags (Apply to ALL resources)

| Tag Key       | Required?   | Format                 | Example                   | Purpose                        |
| ------------- | ----------- | ---------------------- | ------------------------- | ------------------------------ |
| `Project`     | ✅ Yes      | lowercase-with-hyphens | `doc-processing-pipeline` | Group all resources by project |
| `CostCenter`  | ✅ Yes      | ProjectN               | `Project1`                | Cost allocation bucket         |
| `Environment` | ✅ Yes      | dev/staging/prod       | `dev`                     | Separate dev/test/prod costs   |
| `Owner`       | ⚠️ Optional | FirstLast or username  | `JohnDoe`                 | Who manages this resource      |
| `CreatedDate` | ✅ Yes      | YYYY-MM-DD             | `2026-01-16`              | Track resource age             |
| `ManagedBy`   | ✅ Yes      | tool-name              | `manual`                  | How is it managed              |
| `Component`   | ✅ Yes      | descriptive-name       | `uploads`                 | Specific resource function     |

---

## 🏗️ Project Naming Convention

**Format:** `{descriptive-name}-pipeline` or `{descriptive-name}-app`

**Examples:**

- ✅ `doc-processing-pipeline`
- ✅ `image-classification-app`
- ✅ `sentiment-analysis-api`
- ❌ `project1` (not descriptive)
- ❌ `my-aws-project` (too generic)

---

## 💰 Cost Center Naming Convention

**Format:** `ProjectN` where N = 1, 2, 3, etc.

**Why this format?**

- Simple and predictable
- Easy to remember
- Works well in cost reports
- Consistent across all projects

**Example mapping:**

- Project 1 (Document Processing) → `Project1`
- Project 2 (Image Classifier) → `Project2`
- Project 3 (Sentiment Analysis) → `Project3`

---

## 📊 Current Projects

### Project 1: Intelligent Document Processing Pipeline

- **Project Tag:** `doc-processing-pipeline`
- **CostCenter:** `Project1`
- **Start Date:** January 16, 2026
- **Environment:** `dev`
- **Services Used:** S3, Lambda, Textract, Comprehend, API Gateway, CloudWatch, EventBridge, SNS
- **Description:** AI-powered document extraction and analysis system
- **Estimated Monthly Cost:** $17 (500 documents)
- **Status:** ✅ Complete

### Project 2: Budget-Conscious Research Agent
- **Project Tag:** `budget-research-agent`
- **CostCenter:** `Project2`
- **Start Date:** April 7, 2026
- **Environment:** `dev`
- **Services Used:** Fargate, ECR, API Gateway, CloudWatch, IAM
- **Description:** LangGraph agent with budget kill switch and human-in-the-loop interrupt
- **Estimated Monthly Cost:** ~$0.50/day (Fargate, dev only)
- **Status:** 🚧 In Development (Phase 1)

### Project 3: [Future Project]

- **Project Tag:** `[project-name-here]`
- **CostCenter:** `Project3`
- **Start Date:** TBD
- **Environment:** `dev`
- **Services Used:** TBD
- **Description:** TBD
- **Estimated Monthly Cost:** TBD

---

## 🔧 Component Tag Examples

Use the `Component` tag to identify specific resource types within a project:

| Resource Type       | Component Value | Example Resource                           |
| ------------------- | --------------- | ------------------------------------------ |
| S3 upload bucket    | `uploads`       | doc-processing-demo-uploads-123456789012   |
| S3 processed bucket | `processed`     | doc-processing-demo-processed-123456789012 |
| S3 frontend bucket  | `frontend`      | doc-processing-demo-frontend-123456789012  |
| Lambda processor    | `processing`    | DocumentProcessor                          |
| Lambda API handler  | `api`           | APIUploadHandler                           |
| Lambda tag audit    | `monitoring`    | TagAuditFunction                           |
| API Gateway         | `api`           | DocumentProcessingAPI                      |
| CloudWatch logs     | `monitoring`    | /aws/lambda/DocumentProcessor              |
| SNS topic           | `monitoring`    | TagAuditNotifications                      |

---

## 🚀 How to Apply Tags

### S3 Buckets

```bash
aws s3api put-bucket-tagging \
  --bucket ${PROJECT_NAME}-uploads-${ACCOUNT_ID} \
  --tagging "TagSet=[
    {Key=Project,Value=${PROJECT_TAG}},
    {Key=CostCenter,Value=${COST_CENTER}},
    {Key=Environment,Value=${ENVIRONMENT}},
    {Key=Owner,Value=${OWNER}},
    {Key=Component,Value=uploads},
    {Key=CreatedDate,Value=${CREATED_DATE}},
    {Key=ManagedBy,Value=${MANAGED_BY}}
  ]"
```

### Lambda Functions

```bash
aws lambda create-function \
  --function-name DocumentProcessor \
  --tags Project=${PROJECT_TAG},CostCenter=${COST_CENTER},Environment=${ENVIRONMENT},Owner=${OWNER},Component=processing,CreatedDate=${CREATED_DATE},ManagedBy=${MANAGED_BY} \
  # ... other parameters

```

### SNS Topics

```bash
aws sns create-topic \
  --name TagAuditNotifications \
  --tags "Key=Project,Value=${PROJECT_TAG}" "Key=CostCenter,Value=${COST_CENTER}" "Key=Component,Value=monitoring"
```

### API Gateway

```bash
aws apigateway create-rest-api \
  --name "DocumentProcessingAPI" \
  --tags Project=${PROJECT_TAG},CostCenter=${COST_CENTER},Environment=${ENVIRONMENT},Owner=${OWNER},Component=api,CreatedDate=${CREATED_DATE},ManagedBy=${MANAGED_BY}
```

---

## 🔍 Tag Governance & Auditing

### ✅ Implemented: Automated Lambda Tag Audit

**Status:** Active and Running  
**Implementation Date:** January 16, 2026  
**Cost:** $0.00 (within Free Tier)

#### Architecture

```
EventBridge Rule (Weekly: Mon 9AM UTC)
    ↓
Lambda Function (TagAuditFunction)
    ↓ scans all AWS resources
ResourceGroupsTaggingAPI
    ↓ generates compliance report
SNS Topic (TagAuditNotifications)
    ↓ sends email notification
Your Inbox 📧
```

#### How It Works

1. **Every Monday at 9 AM UTC**, EventBridge triggers the Lambda function
2. Lambda scans **all AWS resources** using ResourceGroupsTaggingAPI
3. Checks each resource for **7 required tags** (Project, CostCenter, Environment, Owner, Component, CreatedDate, ManagedBy)
4. Generates a **compliance report** listing non-compliant resources
5. Sends **email report** via SNS with:
   - Total resources scanned
   - Compliance rate percentage
   - List of non-compliant resources grouped by type
   - Missing tags for each resource
   - Action items for remediation

#### Email Report Example

```
AWS TAG COMPLIANCE AUDIT REPORT
================================
Date: 2026-01-23 09:00:00 UTC

SUMMARY
-------
Total Resources: 6
Compliant: 6
Non-Compliant: 0
Compliance Rate: 100.0%

Required Tags: Project, CostCenter, Environment, Owner, CreatedDate, ManagedBy

✅ ALL RESOURCES ARE COMPLIANT!

Next audit: 1 week from now
```

#### Resources Created

- **Lambda Function:** `TagAuditFunction` (Python 3.11, 256MB, 60s timeout)
- **IAM Role:** `TagAuditLambdaRole` (with AWSLambdaBasicExecutionRole + custom TagAuditPolicy)
- **EventBridge Rule:** `TagAuditWeeklySchedule` (cron: 0 9 ? _ MON _)
- **SNS Topic:** `TagAuditNotifications` (email subscription confirmed)
- **CloudWatch Logs:** `/aws/lambda/TagAuditFunction` (automatic)

#### Cost Breakdown (Monthly)

| Component          | Usage         | Cost                           |
| ------------------ | ------------- | ------------------------------ |
| Lambda Invocations | 4/month       | $0.00 (Free Tier: 1M/month)    |
| Lambda Compute     | 10 GB-seconds | $0.00 (Free Tier: 400K GB-sec) |
| EventBridge Rule   | 1 rule        | $0.00 (First rule free)        |
| SNS Notifications  | 4 emails      | $0.00 (Free Tier: 1,000/month) |
| CloudWatch Logs    | ~5 MB         | $0.00 (Free Tier: 5 GB/month)  |
| **Total**          |               | **$0.00**                      |

**Annual Cost:** $0.00 (within Free Tier forever)  
**Savings vs AWS Config:** $1.00/year

---

### Regular Tag Audits

**Automated (Primary):**

- Weekly Lambda audits every Monday
- Email reports to your inbox
- No manual intervention required
- ✅ **Currently Active**

**Manual (Backup):**

```bash
# Run on-demand audit
./audit-tags.sh

# Fix non-compliant resource
./fix-tags.sh <resource-arn>
```

---

### Automated Compliance Checks - Options Comparison

| Solution                 | Monthly Cost | Frequency  | Setup Time | Maintenance | Best For                             | Status             |
| ------------------------ | ------------ | ---------- | ---------- | ----------- | ------------------------------------ | ------------------ |
| **Lambda + EventBridge** | $0.00        | Weekly     | 1 hour     | None        | Learning projects, personal accounts | ✅ **Implemented** |
| AWS Config               | $0.08        | Continuous | 10 min     | Low         | Production, teams, compliance        | ❌ Not used        |
| Manual Script            | $0.00        | On-demand  | 15 min     | Manual runs | One-off checks                       | ⚠️ Backup only     |

**Decision Rationale:**

- Lambda provides **professional-grade governance** at zero cost
- Learning opportunity: Built Lambda, EventBridge, SNS integration
- Automated weekly audits are sufficient for 15 resources
- Saved $1/year while gaining hands-on AWS experience
- Can scale to hundreds of resources without additional cost

---

### Tag Governance Best Practices

1. ✅ **Document your tagging strategy** (this file!)
2. ✅ **Audit tags automatically** (Lambda function running weekly)
3. ✅ **Email notifications** (immediate visibility of issues)
4. ✅ **Review cost allocation tags** (activated in AWS Billing)
5. ⚠️ **Clean up unused tags** (quarterly review)
6. ⚠️ **Train team members** (when working with others)

---

## 📈 Cost Analysis Queries

### Monthly Cost by Project

```bash
aws ce get-cost-and-usage \
  --time-period Start=2026-01-01,End=2026-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=TAG,Key=Project
```

### Monthly Cost by CostCenter

```bash
aws ce get-cost-and-usage \
  --time-period Start=2026-01-01,End=2026-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=TAG,Key=CostCenter
```

### Year-End Summary

```bash
# Use the provided script
./year-end-report.sh 2026

# Output example:
# Project1: $204.50
# Project2: $387.25
# Project3: $156.80
# Total: $748.55
```

---

## ⚠️ IMPORTANT: Activate Cost Allocation Tags

Tags won't appear in cost reports until activated!

**Steps:**

1. Go to AWS Console → Billing Dashboard
2. Click "Cost Allocation Tags" (left sidebar)
3. Find your custom tags: `Project`, `CostCenter`, `Environment`, `Owner`, `Component`
4. Select them and click **"Activate"**
5. Wait 24 hours for activation

**Note:** This step MUST be done in the console - cannot be done via CLI

---

## ✅ Tag Validation Checklist

Before creating any AWS resource, verify:

- [ ] Have you loaded your environment? `source setup.sh`
- [ ] Does your resource include the `Project` tag?
- [ ] Does your resource include the `CostCenter` tag?
- [ ] Does your resource include the `Environment` tag?
- [ ] Does your resource include the `Component` tag?
- [ ] Does your resource include the `CreatedDate` tag?
- [ ] Does your resource include the `ManagedBy` tag?
- [ ] Have you added an `Owner` tag if applicable?

**Use the helper script:**

```bash
# Tag any resource after creation
./tag-resource.sh <resource-arn> <component-name>
```

---

## 🎓 Tagging Best Practices

### ✅ DO:

- Tag EVERY resource you create
- Use consistent tag keys across all resources
- Use descriptive, meaningful tag values
- Document your tagging strategy (this file!)
- Activate cost allocation tags in AWS Billing
- Review tags quarterly to ensure compliance

### ❌ DON'T:

- Create resources without tags
- Use different spellings/cases for tag keys (Project vs project)
- Use spaces in tag values (use hyphens: `doc-processing` not `doc processing`)
- Forget to activate cost allocation tags
- Delete tags from existing resources

---

## 🔍 Audit Your Tags

Check which resources are missing tags:

```bash
# List all resources without a Project tag
aws resourcegroupstaggingapi get-resources \
  --tag-filters Key=Project,Values= \
  --region ${REGION}

# Count untagged resources
aws resourcegroupstaggingapi get-resources \
  --region ${REGION} \
  | jq '[.ResourceTagMappingList[] | select(.Tags | length == 0)] | length'
```

---

## 📚 Additional Resources

- AWS Tagging Best Practices: https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html
- AWS Cost Allocation Tags: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html
- Resource Groups Tagging API: https://docs.aws.amazon.com/resourcegroupstagging/latest/APIReference/Welcome.html

---

## 🎯 Success Metrics

At the end of 2026, you should be able to:

- ✅ Generate a year-end cost report in < 5 minutes
- ✅ See exact costs for each project (Project1, Project2, Project3)
- ✅ Identify which AWS services cost the most per project
- ✅ Track cost trends month-over-month
- ✅ Make data-driven decisions about project continuation

**Your Future Self Will Thank You!** 🙏
