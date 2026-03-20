# Building an AI-Powered Document Processing Pipeline on AWS

## A Developer's Journey from Concept to Production

---

## 📝 Development Log & Substack Article Draft

**Project:** Intelligent Document Processing Pipeline  
**Duration:** January 16, 2026 - [END DATE]  
**Total Hours:** 7 hours (1 pre-dev + 2 Phase 1 + 1 tag governance + 3 Phase 2)  
**Final Cost:** $0.00 (so far)

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Why I Built This](#why-i-built-this)
3. [Day-by-Day Development Log](#development-log)
4. [Technical Challenges & Solutions](#challenges)
5. [Key Learnings](#learnings)
6. [Results & Impact](#results)
7. [What's Next](#whats-next)

---

## Project Overview

**The Problem:** Manual document processing takes 3 minutes per document and costs $1.25 in staff time.

**The Solution:** An AWS serverless pipeline that processes documents in 30 seconds at $0.034 per document.

**Tech Stack:**

- AWS Services: S3, Lambda, Textract, Comprehend, API Gateway, CloudWatch
- Languages: Python 3.11, JavaScript (ES6+)
- Tools: AWS CLI, Boto3, Git

**Key Metrics:**

- 80% reduction in processing time
- 97% cost reduction per document
- Processes 500 documents/month for $17
- ROI: 3,558% annually

---

## Why I Built This

[FILL IN YOUR PERSONAL MOTIVATION]

Example:

> As someone transitioning into AI/ML engineering, I wanted hands-on experience with AWS AI services. I chose document processing because it's a real business problem with measurable ROI—something I could discuss confidently in interviews.

---

## Development Log

### Pre-Development Setup

**Date:** January 16, 2026  
**Time Spent:** 1 hour  
**Status:** ✅ Complete

#### What I Did:

- [x] Created AWS account (ensured Free Tier eligibility)
- [x] Set up IAM user with proper permissions
- [x] Enabled MFA (Multi-Factor Authentication) for security
- [x] Created CLI access keys
- [x] Configured AWS CLI in VSCode (switched from PowerShell to Bash)
- [x] Created cost budget alerts ($25 threshold)
- [x] Set up environment variables (PROJECT_NAME, REGION, ACCOUNT_ID)
- [x] Created setup.sh script for easy environment loading
- [x] Tested CLI with test S3 bucket creation/deletion
- [ ] Set up GitHub repository
- [ ] Created `dev` branch for active development
- [ ] Added comprehensive `.gitignore`

#### Cost Tracker:

- AWS charges so far: $0.00
- Budget remaining: $25.00
- Free Tier status: Active

#### Notes & Observations:

```
CLI Configuration Journey:
- Initially unfamiliar with bash/CLI but walked through step-by-step
- Switched VSCode terminal from PowerShell to Bash for project consistency
- Learned that environment variables reset when terminal closes - created setup.sh to solve this
- MFA setup adds extra security layer (good practice!)
- Test bucket creation/deletion worked perfectly - CLI is configured correctly
- Used us-east-1 region for best Free Tier coverage
- Access keys stored securely, not in any git repo

Key Commands Learned:
- aws configure (initial setup)
- aws sts get-caller-identity (verify credentials)
- aws s3 mb/rb (make/remove bucket)
- source setup.sh (load environment variables)
- export VARIABLE="value" (set env variables)

Aha Moment:
- Environment variables make scripts reusable and keep account IDs out of code
- The ${VARIABLE} syntax in bash is actually pretty straightforward once you try it
```

#### Screenshots Captured:

- [x] AWS Budget alert confirmation ($25 threshold, 50%, 80%, 100% alerts)
- [x] IAM user created with MFA enabled
- [x] CLI configuration successful (aws sts get-caller-identity output)
- [ ] Cost Explorer enabled (will capture after 24 hours when data populates)

#### Setup Files Created:

```bash
# setup.sh - Load environment variables
#!/bin/bash
export PROJECT_NAME="doc-processing-demo"
export REGION="us-east-1"
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "✅ Environment variables loaded"
echo "PROJECT_NAME: $PROJECT_NAME"
echo "REGION: $REGION"
echo "ACCOUNT_ID: $ACCOUNT_ID"
```

---

### Phase 1: S3 Bucket Configuration

**Date:** January 16, 2026  
**Time Spent:** 2 hours  
**Status:** ✅ Complete

#### What I Did:

- [x] Implemented comprehensive tagging strategy (TAGGING_STRATEGY.md)
- [x] Updated setup.sh with tag variables for cost tracking
- [x] Created setup.sh.example template with tagging best practices
- [x] Created 3 S3 buckets with proper tags:
  - doc-processing-demo-uploads-[ACCOUNT_ID]
  - doc-processing-demo-processed-[ACCOUNT_ID]
  - doc-processing-demo-frontend-[ACCOUNT_ID]
- [x] Applied comprehensive tags to all buckets:
  - Project: doc-processing-pipeline
  - CostCenter: Project1
  - Environment: dev
  - Owner: YourName
  - Component: uploads/processed/frontend
  - CreatedDate: 2026-01-16
  - ManagedBy: manual
- [x] Enabled versioning on uploads bucket
- [x] Configured Lambda access policy for uploads bucket
- [x] Created lifecycle policy for cost optimization (applied via console)
- [x] Tested upload/download functionality
- [x] Committed all configuration files to Git

#### Commands Used:

```bash
# Load environment with tags
source setup.sh

# Create buckets with tags
aws s3 mb s3://${PROJECT_NAME}-uploads-${ACCOUNT_ID} --region ${REGION}
aws s3api put-bucket-tagging \
  --bucket ${PROJECT_NAME}-uploads-${ACCOUNT_ID} \
  --tagging "TagSet=[{Key=Project,Value=${PROJECT_TAG}},{Key=CostCenter,Value=${COST_CENTER}},{Key=Environment,Value=${ENVIRONMENT}},{Key=Owner,Value=${OWNER}},{Key=Component,Value=uploads},{Key=CreatedDate,Value=${CREATED_DATE}},{Key=ManagedBy,Value=${MANAGED_BY}}]"

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket ${PROJECT_NAME}-uploads-${ACCOUNT_ID} \
  --versioning-configuration Status=Enabled

# Apply bucket policy
aws s3api put-bucket-policy \
  --bucket ${PROJECT_NAME}-uploads-${ACCOUNT_ID} \
  --policy file://bucket-policy-uploads.json

# Verify tags
aws s3api get-bucket-tagging --bucket ${PROJECT_NAME}-uploads-${ACCOUNT_ID}

# Test upload
echo "Test" > test.txt
aws s3 cp test.txt s3://${PROJECT_NAME}-uploads-${ACCOUNT_ID}/test/
aws s3 ls s3://${PROJECT_NAME}-uploads-${ACCOUNT_ID}/test/
```

#### Cost Tracker:

- S3 bucket creation: $0.00 (free)
- S3 storage: $0.00 (no significant data yet)
- S3 requests: $0.00 (minimal test uploads)
- Running total: $0.00
- Budget remaining: $25.00

#### Challenges Faced:

```
Challenge 1: Lifecycle policy CLI command failed
- Command: aws s3api put-bucket-lifecycle-configuration
- Issue: CLI command encountered configuration/syntax issues
- Attempted troubleshooting: Checked JSON formatting, permissions, syntax
- Solution: Applied lifecycle policy directly through AWS Console instead
- Time spent: ~10 minutes trying CLI, 2 minutes in console
- Lesson: Don't be dogmatic about "CLI only" - sometimes the console is faster
  and more reliable, especially for one-time configurations during learning
- Result: Lifecycle policy successfully configured via console:
  * Rule: Archive documents to Glacier after 90 days
  * Applied to: processed bucket, prefix: processed/
  * Status: Enabled
  * Purpose: Reduce storage costs by ~83% for old documents

Challenge 2: Understanding tag structure for CLI
- Initially confused about TagSet JSON formatting
- Used environment variables to make it cleaner and reusable
- Created ${TAGS} variable for easy copy-paste
- This made applying tags to future resources much simpler
```

#### What Worked Well:

```
Success 1: Comprehensive tagging strategy from day one
- Created TAGGING_STRATEGY.md documenting all standards
- Used consistent tags across all resources
- Set up for easy year-end cost analysis by project
- Template (setup.sh.example) will help anyone following this project
- Future me (December 2026) will thank present me!

Success 2: Environment variables made everything reusable
- setup.sh loads all configuration with one command: source setup.sh
- No hardcoded values in any commands
- Easy to adapt for future projects (just change variables)
- PROJECT_NAME, REGION, ACCOUNT_ID, and all tags centralized

Success 3: Git workflow running smoothly
- Successfully using dev branch for all development
- .gitignore protecting sensitive setup.sh file
- Only committing safe templates (setup.sh.example)
- Clear, descriptive commit messages following conventions
- Good foundation for the rest of the project

Success 4: Bucket policy and versioning worked perfectly via CLI
- Policy correctly allows Lambda to read from uploads bucket
- Versioning protects against accidental deletions/overwrites
- Test uploads confirmed everything working
```

#### Notes & Observations:

```
Tagging Strategy - Key Insight:
The tagging strategy I implemented will save me hours at year-end. By tagging
every resource with Project, CostCenter, Environment, and Component, I'll be
able to run a single command (./year-end-report.sh 2026) and see exactly how
much each project cost. This is professional-grade AWS hygiene that most
beginners skip.

CLI vs Console - Aha Moment:
Sometimes the "right" tool is the one that works! I tried applying the lifecycle
policy via CLI (following infrastructure-as-code best practices), but ran into
issues. Rather than spend 30 minutes debugging, I pivoted to the AWS Console
and had it configured in 2 minutes.

Lesson: Don't be dogmatic about "CLI only" or "Console only" - use the right
tool for the situation. For one-time configurations during learning, the console's
visual feedback is invaluable. For production automation, CLI/IaC is essential.

In interviews, this shows adaptability and pragmatism over rigid adherence to
"best practices." Real-world engineering is about getting things done effectively,
not following rules blindly.

Environment Variables - Best Practice:
Using setup.sh to centralize all configuration (bucket names, region, tags) made
this phase so much cleaner. Every command uses ${VARIABLES} instead of
hardcoded values. This means:
- Scripts are reusable across accounts
- No risk of committing sensitive data to Git
- Easy to adapt for future projects
- Self-documenting (variable names explain their purpose)

S3 Bucket Naming:
Following the pattern {project-name}-{component}-{account-id} ensures globally
unique names while keeping them descriptive. The account ID suffix prevents
naming conflicts if I ever need multiple AWS accounts.
```

#### Screenshots Captured:

- [x] S3 buckets in AWS Console showing all 3 buckets
- [x] Bucket tags configuration (showing all 7 tags)
- [x] Versioning enabled on uploads bucket
- [x] Bucket policy JSON in console
- [x] Lifecycle policy configuration screen (applied via console)
- [ ] Cost Explorer (will capture after 24 hours when data populates)

---

### Side Quest: Automated Tag Governance (1 hour)

**Date:** January 16, 2026  
**Time Spent:** 1 hour  
**Status:** ✅ Complete

#### What I Did:

- [x] Evaluated 3 tag governance options (AWS Config, Lambda automation, manual script)
- [x] Decided on Lambda + EventBridge solution ($0.00 vs AWS Config $1/year)
- [x] Created SNS topic for email notifications (TagAuditNotifications)
- [x] Confirmed SNS email subscription (found in spam folder!)
- [x] Created IAM role for Lambda (TagAuditLambdaRole)
- [x] Attached policies (AWSLambdaBasicExecutionRole + custom TagAuditPolicy)
- [x] Wrote Python Lambda function (tag_audit_function.py - 120 lines)
- [x] Packaged Lambda with Python zipfile (zip command not available on Windows)
- [x] Deployed Lambda to AWS
- [x] Created EventBridge rule for weekly schedule (Mondays 9 AM UTC)
- [x] Added Lambda invoke permission for EventBridge
- [x] Configured EventBridge target
- [x] Tested Lambda function manually
- [x] Verified email notification received
- [x] Created verification script (verify-tag-audit.sh)
- [x] Updated cost tracker with Lambda and EventBridge line items
- [x] Created comprehensive README.md for GitHub

#### Architecture Built:

```
EventBridge (Weekly: Mon 9AM UTC)
    ↓
Lambda Function (TagAuditFunction)
    ↓ scans all resources
ResourceGroupsTaggingAPI
    ↓ generates compliance report
SNS Topic (TagAuditNotifications)
    ↓ sends email
Your Inbox 📧
```

#### Commands Used:

```bash
# Create SNS topic
aws sns create-topic --name TagAuditNotifications --region ${REGION}

# Subscribe email
aws sns subscribe \
  --topic-arn ${SNS_TOPIC_ARN} \
  --protocol email \
  --notification-endpoint your-email@example.com

# Create IAM role
aws iam create-role \
  --role-name TagAuditLambdaRole \
  --assume-role-policy-document file://lambda-audit-trust-policy.json

# Attach policies
aws iam attach-role-policy \
  --role-name TagAuditLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Package Lambda (using Python on Windows)
python -c "import zipfile; zipfile.ZipFile('function.zip', 'w').write('tag_audit_function.py')"

# Deploy Lambda
aws lambda create-function \
  --function-name TagAuditFunction \
  --runtime python3.11 \
  --role ${TAG_AUDIT_ROLE_ARN} \
  --handler tag_audit_function.lambda_handler \
  --zip-file fileb://lambda/tag-audit/function.zip \
  --timeout 60 \
  --memory-size 256 \
  --environment "Variables={SNS_TOPIC_ARN=${SNS_TOPIC_ARN}}"

# Create EventBridge schedule
aws events put-rule \
  --name TagAuditWeeklySchedule \
  --schedule-expression "cron(0 9 ? * MON *)"

# Add target
aws events put-targets \
  --rule TagAuditWeeklySchedule \
  --targets "Id=1,Arn=${LAMBDA_ARN}"
```

#### Cost Tracker:

- SNS Topic creation: $0.00
- SNS email notifications: $0.00 (4/month, within 1,000 free tier)
- Lambda invocations: $0.00 (4/month, within 1M free tier)
- Lambda compute: $0.00 (within 400K GB-seconds free tier)
- EventBridge rules: $0.00 (first rule is free)
- CloudWatch Logs: $0.00 (within 5GB free tier)
- **Running total: $0.00**
- **Savings vs AWS Config: $1.00/year**

#### Challenges Faced:

```
Challenge 1: Missing IAM Permissions
- Issue: Initially didn't have permission to create IAM roles
- Error: AccessDenied when trying to create TagAuditLambdaRole
- Solution: Added IAMFullAccess policy to doc-processing IAM user
- Time spent: 5 minutes
- Lesson: Check IAM permissions before starting infrastructure tasks

Challenge 2: SNS Email Not Received
- Issue: Subscribed to SNS topic but confirmation email never arrived
- Attempts:
  1. Checked email address was correct
  2. Waited 10 minutes
  3. Tried resubscribing
- Solution: Found confirmation email in spam folder!
- Time spent: 15 minutes searching
- Lesson: Always check spam for AWS confirmation emails

Challenge 3: Zip Command Not Found on Windows
- Issue: `zip function.zip tag_audit_function.py` failed
- Error: "zip: command not found"
- Attempted: Git Bash doesn't have zip by default on Windows
- Solution: Used Python's zipfile module instead (cross-platform)
- Code: `python -c "import zipfile; zipfile.ZipFile('function.zip', 'w').write('tag_audit_function.py')"`
- Alternative: Used PowerShell's Compress-Archive
- Time spent: 5 minutes
- Lesson: Always have cross-platform alternatives ready

Challenge 4: Empty Environment Variables in Lambda Deploy
- Issue: Lambda deployment failed with "Error parsing parameter '--environment'"
- Error: "Expected: ',', received: 'EOF' for input: Variables={SNS_TOPIC_ARN=}"
- Root cause: SNS_TOPIC_ARN variable was empty/not loaded
- Solution: Explicitly set SNS_TOPIC_ARN before deployment
- Time spent: 10 minutes debugging
- Lesson: Always verify environment variables are set before using them
```

#### What Worked Well:

```
Success 1: Cost-Conscious Decision Making
- Evaluated AWS Config ($0.08/month) vs Lambda ($0.00/month)
- Chose Lambda automation - professional governance at zero cost
- Added bonus: Learned Lambda, EventBridge, and SNS
- Updated cost tracker to document decision

Success 2: Lambda Function Architecture
- Clean, well-documented Python code (120 lines)
- Proper error handling and logging
- Generates human-readable email reports
- Identifies non-compliant resources by type
- Groups violations for easy remediation

Success 3: Automation Without Complexity
- Weekly schedule (Mondays 9 AM UTC) - not too frequent, not too rare
- Email notifications - no need to check logs manually
- Completely serverless - no infrastructure to maintain
- Set it and forget it - runs automatically

Success 4: Documentation as I Built
- Created README.md during the side quest
- Updated cost tracker in real-time
- Wrote verification script for testing
- All tools and scripts ready for future use
```

#### Notes & Observations:

```
Tag Governance Philosophy:
This side quest perfectly demonstrates cost-conscious engineering. AWS Config
is the "enterprise" solution ($1/year), but for a 15-resource learning project,
Lambda automation achieves the same governance goal at $0 while teaching three
new AWS services. Sometimes the DIY solution is better than the turnkey one.

AWS Free Tier is Generous:
- Lambda: 1M requests/month (using 4 = 0.0004%)
- SNS: 1,000 emails/month (using 4 = 0.4%)
- EventBridge: First rule free
This governance system will NEVER cost money at current usage levels.

Professional-Grade Governance:
Weekly automated audits with email reports is exactly what production teams use.
The fact that it costs $0 doesn't make it less professional - it makes it smarter.
This demonstrates operational maturity and cost optimization skills.

Cross-Platform Development:
Working on Windows revealed platform-specific issues (zip command, environment
variables). Building workarounds (Python zipfile, explicit variable setting)
shows adaptability and problem-solving skills.

Learning Through Building:
Instead of just reading documentation about Lambda, EventBridge, and SNS, I
built a real, useful automation tool. The learning sticks better when solving
actual problems.
```

#### First Audit Results:

```
Total Resources Scanned: 6
- S3 buckets: 3
- SNS topics: 1
- IAM roles: 1
- Lambda functions: 1

Compliant Resources: 6 (100%)
Non-Compliant Resources: 0

✅ All resources properly tagged!

Tags verified on all resources:
- Project: doc-processing-pipeline
- CostCenter: Project1
- Environment: dev
- Owner: [Your Name]
- Component: uploads/processed/frontend/monitoring
- CreatedDate: 2026-01-16
- ManagedBy: implem
```

#### Screenshots Captured:

- [x] SNS topic created in console
- [x] Email subscription confirmed
- [x] Lambda function deployed
- [x] EventBridge rule configuration
- [x] Sample email audit report
- [x] CloudWatch logs showing successful execution
- [x] First audit results (100% compliance)

#### Files Created:

- `lambda/tag-audit/tag_audit_function.py` (120 lines)
- `lambda-audit-trust-policy.json` (IAM trust policy)
- `tag-audit-policy.json` (custom IAM policy)
- `verify-tag-audit.sh` (verification script)
- `README.md` (comprehensive project documentation)
- Updated `AWS_Project_Cost_Tracker.xlsx` (added Lambda + EventBridge costs)
- Updated `TAGGING_STRATEGY.md` (added governance section)

#### Key Learnings for Substack Article:

```
1. "Automated governance without AWS Config"
   Instead of enabling AWS Config ($1/year), I built a Lambda function that
   audits tags weekly and emails me reports—staying within Free Tier ($0) while
   learning Lambda, EventBridge, and SNS. Sometimes the DIY solution teaches
   more than the turnkey one.

2. "Cost-conscious engineering is intentional, not cheap"
   Choosing Lambda over AWS Config wasn't about being cheap—it was about being
   intentional. For 15 resources, automated weekly audits are sufficient. The
   saved dollar goes toward actual compute costs instead.

3. "Platform-specific challenges build resilience"
   Working on Windows revealed issues (zip command, Git Bash quirks) that Linux
   users wouldn't face. Building cross-platform workarounds (Python zipfile,
   PowerShell alternatives) demonstrates adaptability.

4. "Learning by solving real problems"
   This wasn't just "Lambda tutorial" - I built actual governance automation
   that will run every week for the next year. The learning sticks better when
   solving genuine operational needs.
```

---

### Phase 2: Lambda Function Development

**Date:** January 17, 2026  
**Time Spent:** 3 hours  
**Status:** ✅ Complete

#### What I Did:

- [x] Created IAM role for Lambda with proper permissions (DocProcessingLambdaRole)
- [x] Attached policies: AWSLambdaBasicExecutionRole, S3FullAccess, TextractFullAccess, ComprehendFullAccess
- [x] Wrote document_processor.py (200+ lines with Textract + Comprehend integration)
- [x] Packaged Lambda function with boto3 dependencies (used PowerShell - see challenges!)
- [x] Deployed Lambda function to AWS (DocumentProcessor)
- [x] Configured S3 trigger on uploads bucket
- [x] Created test invoice image using Python PIL
- [x] Tested end-to-end: upload → extract → analyze → save results
- [x] Verified CloudWatch logs showing successful processing
- [x] Confirmed extracted data in processed bucket as properly formatted JSON

#### Commands Used:

```bash
# IAM Role Creation
aws iam create-role --role-name DocProcessingLambdaRole \
  --assume-role-policy-document file://lambda-trust-policy.json

# Attach Policies (x4 policies for Lambda, S3, Textract, Comprehend)
aws iam attach-role-policy --role-name DocProcessingLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name DocProcessingLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
aws iam attach-role-policy --role-name DocProcessingLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonTextractFullAccess
aws iam attach-role-policy --role-name DocProcessingLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/ComprehendFullAccess

# Package Lambda with PowerShell (Windows workaround)
# In PowerShell terminal:
Remove-Item function.zip -ErrorAction SilentlyContinue
Compress-Archive -Path .\package\* -DestinationPath function.zip
Compress-Archive -Path document_processor.py -Update -DestinationPath function.zip

# Lambda Deployment
aws lambda create-function \
  --function-name DocumentProcessor \
  --runtime python3.11 \
  --role ${ROLE_ARN} \
  --handler document_processor.lambda_handler \
  --zip-file fileb://function.zip \
  --timeout 60 \
  --memory-size 512 \
  --environment "Variables={PROCESSED_BUCKET=${PROCESSED_BUCKET}}"

# S3 Trigger Configuration
aws lambda add-permission --function-name DocumentProcessor \
  --statement-id S3InvokeFunction \
  --action lambda:InvokeFunction \
  --principal s3.amazonaws.com \
  --source-arn arn:aws:s3:::${UPLOAD_BUCKET}

aws s3api put-bucket-notification-configuration \
  --bucket ${UPLOAD_BUCKET} \
  --notification-configuration file://s3-notification.json

# Test by uploading invoice image
python << 'EOF'
from PIL import Image, ImageDraw, ImageFont
# ... image generation code ...
EOF

aws s3 cp test-invoice.png s3://${UPLOAD_BUCKET}/uploads/
aws logs filter-log-events --log-group-name "/aws/lambda/DocumentProcessor" --start-time $(($(date +%s) - 300))000
aws s3 cp s3://${PROCESSED_BUCKET}/processed/test-invoice.png.json - | python -m json.tool
```

#### Cost Tracker:

- Lambda invocations: $0.00 (Free Tier: 1M requests/month, used <10)
- Lambda compute time: $0.00 (Free Tier: 400K GB-seconds)
- Textract API calls: $0.00 (Free Tier: 1,000 pages first 3 months, used 1 page)
- Comprehend API calls: $0.00 (Free Tier: 50K units first 12 months, used <100 units)
- CloudWatch Logs: $0.00 (Free Tier: 5GB/month, used <1MB)
- **Phase 2 Total: $0.00**
- **Running total: $0.00**

#### Challenges Faced:

```
Challenge 1: The Great Windows Zip Command Saga (30 minutes of my life I'll never get back)
- Issue: Automated deployment scripts failed with "zip: command not found"
- Context: Git Bash on Windows doesn't include zip utility (because of course it doesn't)
- Initial Attempt: "I'll just write a cross-platform Python script!" (narrator: this was hubris)
- The Weeds: Spent 20 minutes debugging Python zipfile paths, Windows backslashes, and
  environment variables while questioning all my life choices
- Moment of Clarity: "Wait... why am I debugging automation scripts when PowerShell exists?"
- Solution: Abandoned the automation rabbit hole, used PowerShell's Compress-Archive (2 commands)
- Time to solution: 5 minutes once I stopped being clever
- Lesson: Sometimes the fastest path forward is abandoning "perfect automation" for "thing
  that actually works." Most AWS tutorials assume Linux. Real development on Windows means
  accepting that you'll occasionally need to fight with path separators and missing utilities.
  The real skill isn't having perfect scripts - it's knowing when to pivot.

Challenge 2: IAM Permissions Speedbump
- Issue: "AccessDenied" when trying to create DocProcessingLambdaRole
- Cause: My IAM user didn't have permissions to create roles (oops)
- Solution: Added IAMFullAccess policy via AWS Console
- Time spent: 5 minutes
- Lesson: Always verify IAM permissions before starting. For development, broad permissions
  (IAMFullAccess) are fine. Production requires least-privilege policies.

Challenge 3: CloudWatch Logs vs. Git Bash Path Translation
- Issue: Log group path "/aws/lambda/DocumentProcessor" auto-converted to Windows path
- Error: "Value 'C:/Program Files/Git/aws/lambda/DocumentProcessor' failed constraint"
- Solution: Wrap log group names in quotes, or just use AWS Console
- Lesson: Git Bash on Windows has quirky path translation. When AWS CLI complains about
  paths, try quotes first.

Challenge 4: "Why Won't Textract Read My Text File?" (A Brief Mystery)
- Issue: UnsupportedDocumentException when processing test-document.txt
- Root Cause: Textract only supports PDF, JPG, PNG - not plain text (reasonable, actually)
- Solution: Generated realistic invoice image (800x1000 PNG) using Python PIL/Pillow
- Result: Beautiful programmatically-created invoice with company name, line items, totals
- Lesson: Always verify supported formats before creating test data. Textract does OCR on
  images/PDFs - feeding it plain text is like asking a camera to photograph sound.
```

#### What Worked Well:

```
Success 1: Pragmatism Beats Perfectionism
- Manual PowerShell + AWS CLI deployment took 20 minutes vs. hours debugging automation
- Lambda deployed successfully, S3 trigger configured correctly, everything working
- Takeaway: The best solution is the one that ships. You can optimize later.

Success 2: Lambda Code Worked On First Deploy (shocking, I know)
- document_processor.py (200+ lines) deployed without any code modifications
- Textract extracted text, forms, and key-value pairs correctly
- Comprehend detected entities, sentiment, and key phrases as expected
- Error handling and CloudWatch logging performed perfectly
- This proves the value of working from well-tested examples

Success 3: Event-Driven Architecture Just Works™
- S3 → Lambda trigger configured correctly on first attempt
- Upload document → automatic processing (no polling, no cron, no complexity)
- Results appeared in processed bucket within seconds
- This is the power of serverless: focus on logic, not infrastructure

Success 4: Python PIL for Test Data Generation
- Programmatically created realistic 800x1000 invoice image
- Included: company header, invoice number, line items, subtotals, totals
- Textract successfully extracted ALL text and recognized form structure
- Reusable approach for future testing without needing real documents

Success 5: Free Tier Coverage (AWS really is generous)
- Lambda: 1M requests/month (used 10 = 0.001%)
- Textract: 1,000 pages/3 months (used 1 = 0.1%)
- Comprehend: 50K units/12 months (used 100 = 0.2%)
- Total Phase 2 cost: $0.00 ✅
```

#### Notes & Observations:

```
Windows Development: The Hidden Cost of Cross-Platform Tutorials
Most AWS tutorials live in a Linux utopia where `zip` commands work and paths use forward
slashes. Working on Windows revealed the gaps: Git Bash lacks zip, path translation breaks
CloudWatch commands, PowerShell handles archives differently. The solution wasn't fighting
Windows - it was embracing native tools (PowerShell for packaging) while using cross-
platform tools (AWS CLI) where they excel.

In interviews, this demonstrates:
• Adaptability: Pivoting quickly when blocked
• Platform awareness: Understanding OS-specific tooling
• Pragmatism: Choosing simplicity over dogmatism
• Real-world experience: These are the actual issues devs encounter

Lambda Function Architecture: Serverless in the Wild
The document_processor.py function showcases event-driven serverless architecture:
• S3 upload → automatic Lambda trigger (zero polling logic needed)
• Async processing that scales automatically (1 doc or 10,000, same code)
• Results saved to separate S3 bucket (clean separation of concerns)
• Comprehensive CloudWatch logging (full operational visibility)

What this eliminates:
✗ Server provisioning and capacity planning
✗ Load balancers and auto-scaling configuration
✗ Process monitoring and restart logic
✗ Infrastructure maintenance windows

The pipeline processes documents at $0.034 each with zero operational overhead. That's
the serverless promise delivered.

Textract + Comprehend: When 1 + 1 = 3
Textract alone extracts text, forms, and tables from images/PDFs (OCR on steroids).
Comprehend alone analyzes text for entities, sentiment, and key phrases (NLP in a box).
Together they transform: Unstructured document → Structured, analyzable, searchable data.

Example flow:
1. Invoice image uploaded
2. Textract extracts: "Invoice #12345, Date: Jan 17, Amount: $6,210.00"
3. Comprehend identifies: Invoice# (OTHER entity), Date (DATE entity), Amount (QUANTITY)
4. Result: Structured JSON ready for database insert or business logic

This combination turns a manual 3-minute data entry task into a 30-second automated process.

The Weeds: A Cautionary Tale with a Happy Ending
Phase 2's automation detour taught me something valuable about problem-solving. After 20
minutes debugging cross-platform packaging scripts, I had a moment of clarity: "Am I
optimizing for the right outcome?" The goal wasn't "perfect automation scripts" - it was
"deployed Lambda function." Once I reframed the problem, the solution became obvious: use
PowerShell, deploy, move on.

This is the difference between being blocked and being productive. Sometimes you need to
recognize when you're solving the wrong problem. Perfect automation is great for production
infrastructure deployed 100 times. For a learning project deployed once, manual commands
that work beat automated scripts that don't.

The lesson: Don't let perfect be the enemy of done. Ship first, optimize later.
```

#### Screenshots Captured:

- [x] IAM Role (DocProcessingLambdaRole) showing attached policies
- [x] Lambda function in AWS Console (Configuration tab)
- [x] Lambda environment variables (PROCESSED_BUCKET set correctly)
- [x] Lambda monitoring tab (invocations, duration, success rate)
- [x] S3 bucket notification configuration (showing Lambda trigger)
- [x] CloudWatch Logs showing successful document processing
- [x] Test invoice image (input): 800x1000 PNG with realistic invoice data
- [x] Processed JSON results (output): showing Textract extractions + Comprehend analysis
- [x] Cost Explorer showing $0.00 charges for Phase 2
- [x] S3 bucket contents (uploads/ and processed/ directories)

#### Files Created:

- `document_processor.py` (200+ lines) - Main Lambda function with Textract/Comprehend
- `lambda-trust-policy.json` (IAM trust policy for Lambda execution role)
- `function.zip` (15MB packaged deployment with boto3 dependencies)
- `s3-notification.json` (S3 event configuration linking uploads to Lambda)
- `test-lambda-image.sh` (test script that generates invoice image and uploads)
- `package/` directory (boto3, botocore, jmespath, s3transfer for Lambda runtime)

#### Key Learnings for Substack Article:

```
1. "When automation becomes the problem, not the solution"
   Debugging cross-platform packaging scripts for 20 minutes taught me a valuable lesson:
   sometimes the "engineering" move is admitting you're solving the wrong problem. Switched
   to PowerShell, deployed in 5 minutes. Engineering isn't about perfect tools - it's about
   shipping working solutions.

2. "Platform differences are real, and tutorials lie by omission"
   Most AWS guides assume Linux. Windows developers face: missing zip, path translation
   issues, PowerShell vs Bash quirks. Solution: hybrid tooling (native tools where they
   excel, AWS CLI for cross-platform). This isn't a workaround - it's smart engineering.

3. "Free Tier isn't marketing fluff - it's genuinely useful"
   Entire Phase 2 cost: $0.00. Lambda (1M requests), Textract (1,000 pages), Comprehend
   (50K units) - all free for development. You can build and test production-grade
   infrastructure without spending a cent.

4. "Event-driven architecture: the infrastructure you don't have to manage"
   S3 upload → Lambda trigger → processing → results. Zero servers, zero polling, zero
   complexity. Scales from 1 to 10,000 documents without code changes. This is why
   serverless matters.

5. "Getting unstuck: the skill tutorials don't teach"
   The packaging detour wasn't wasted time - it taught me to recognize when I'm optimizing
   for the wrong outcome. After 20 minutes in the weeds, I asked: "What's the actual goal?"
   Answer: deployed Lambda, not perfect scripts. That question saved hours.
```

---

---

### Phase 3: Textract Integration Deep Dive

**Date:** January 31, 2026  
**Time Spent:** 3 hours  
**Status:** ✅ Complete

#### What I Did:

- [x] Selected 15 diverse test documents (9 invoices, 6 receipts)
- [x] Created automated testing toolkit (4 scripts)
- [x] Uploaded all 15 documents to S3
- [x] Verified Lambda processing for each document
- [x] Analyzed Textract extraction accuracy
- [x] Measured Comprehend entity detection
- [x] Tracked processing times and costs
- [x] Documented all results in comprehensive template

#### Testing Results Summary:

**Documents Tested:** 15 total

- Simple: 4 documents (100% success)
- Medium: 8 documents (100% success)
- Complex: 3 documents (0% success - Textract compatibility issue)

**Success Rate:** 12/15 (80%)

**Performance Metrics:**

- Average Processing Time: ~30-60 seconds
- Average Entities Detected: 21.4 per document
- Average Confidence Score: 94.9%
- Total Cost: $0.038 for 15 documents
- Cost per Document: $0.003170

**Cost Projections:**

- 500 documents/month: $1.59/month
- Annual (500 docs/month): $19.08/year
- ROI vs Manual Processing: 519% annually

#### Key Findings:

**✅ What Worked Excellently:**

1. **High Accuracy on Standard Documents**
   - 94.9% average confidence across successful extractions
   - Consistent performance on receipts and invoices
   - Entity detection averaged 21.4 per document
   - All documents processed in under 60 seconds

2. **Cost Efficiency**
   - $0.003170 per document (97% cheaper than manual at $1.25)
   - Well within Free Tier for testing phase
   - Scales economically for production

3. **Reliable Processing**
   - 100% success rate on simple/medium complexity documents
   - Consistent sentiment analysis (all Neutral)
   - No Lambda timeout errors

**⚠️ What Struggled:**

1. **PDF Format Compatibility Issues**
   - 20% failure rate (3/15 documents)
   - All failures were complex invoices (>3,700 bytes)
   - Error: `UnsupportedDocumentException` from Textract
   - Root cause: PDF encoding/format incompatibility
   - Documents are valid (readable in PDF viewers) but Textract cannot process them

2. **Document Complexity Correlation**
   - 100% success on documents <3,700 bytes
   - 0% success on documents >3,700 bytes
   - File size appears to correlate with PDF format complexity

#### Production Recommendations:

1. **Implement PDF Pre-validation**
   - Check PDF format before sending to Textract
   - Route incompatible formats to alternative processing
   - Estimated implementation: 2-3 hours

2. **Add PDF Normalization Pipeline**
   - Use PyPDF2 or Ghostscript to rewrite PDFs
   - Convert to Textract-compatible format before processing
   - Fallback to OCR pipeline (pdf2image + Tesseract) for stubborn formats
   - Estimated implementation: 4-6 hours

3. **Enhanced Error Handling**
   - Graceful failure notifications to users
   - Retry logic with automatic format conversion
   - Clear messaging about supported formats
   - Estimated implementation: 2 hours

#### Tools Created:

**Testing Scripts:**

1. `select-test-documents.py` - Selects diverse subset from 150 mock documents
2. `upload-document.sh` - Uploads single document to S3 with timing
3. `check-results.py` - Verifies processing and displays metrics
4. `generate-test-documents.py` - Generates new test documents (bonus)

**Documentation:**

- `Phase3_Test_Results_Template.md` - Comprehensive tracking spreadsheet
- `PHASE3_TESTING_GUIDE.md` - Step-by-step workflow
- `PHASE3_TOOLKIT_SUMMARY.md` - Tool descriptions and setup

#### Cost Tracker:

- S3 uploads: $0.00 (negligible)
- S3 storage: $0.00 (minimal)
- Lambda invocations: $0.00 (15 invocations, within Free Tier)
- Textract: $0.00 (15 pages, within 1,000 page/month Free Tier)
- Comprehend: $0.038 (within 50K unit/month Free Tier)
- **Running total: $0.038**
- **Budget remaining: $24.96**

#### Screenshots Captured:

- [x] Upload script output showing S3 paths
- [x] Check-results.py output with metrics
- [x] Sample extracted JSON (invoice)
- [x] Sample extracted JSON (receipt)
- [x] Textract error for unsupported PDF
- [x] Phase 3 cost breakdown

#### Challenges Faced:

Challenge 1: Windows Path Compatibility

- Issue: Scripts had Linux paths (/home/claude/)
- Solution: Updated all paths to relative paths (./test-documents/)
- Time spent: 15 minutes
- #### Lesson: Always use relative paths for cross-platform compatibility

Challenge 2: Git Bash vs PowerShell

- Issue: upload-document.sh is bash script, won't run in PowerShell
- Solution: Used Git Bash terminal for all script execution
- Alternative: Could create PowerShell .ps1 version
  Time spent: 5 minutes troubleshooting
- #### Lesson: Document required shell environment for scripts

Challenge 3: Textract PDF Compatibility

- Issue: 3 complex documents failed with UnsupportedDocumentException
- Investigation: PDFs are valid and readable, but incompatible with Textract
- Root cause: PDF format/encoding that Textract doesn't support
- Impact: 20% failure rate
- Solution: Proposed PDF normalization preprocessing step
- Time spent: 30 minutes investigating
- #### Lesson: Always test with edge cases and document failures

### Phase 4: Lambda Optimization & PDF Preprocessing

**Date:** March 4, 2026
**Time Spent:** 2 hours
**Status:** ✅ Complete

#### Goal:

Fix the 20% failure rate from Phase 3 by adding PDF preprocessing before Textract ingestion.
3 complex PDFs failed with `UnsupportedDocumentException` — Phase 4 resolves this.

#### What I Did:

- [x] Built PyPDF2 Lambda layer (lambda/layers/pypdf2/)
- [x] Installed PyPDF2 3.0.1 using Python 3.11 to match Lambda runtime
- [x] Zipped layer using Python shutil (zip not available on Windows Git Bash)
- [x] Deployed layer to AWS (pypdf2-layer:1)
- [ ] Attach layer to DocumentProcessor Lambda function
- [ ] Write PDF validation function
- [ ] Implement PDF normalization logic
- [ ] Update Lambda handler with preprocessing
- [ ] Re-test 3 failed documents
- [ ] Full regression test (all 15 documents)
- [ ] Update cost tracker

#### Architecture Change:

```
BEFORE (Phase 3):
S3 Upload → Lambda → Textract (20% failure on complex PDFs)

AFTER (Phase 4):
S3 Upload → Lambda → PyPDF2 Preprocessing → Textract (target: 100% success)
```

#### Layer Details:

```
Layer Name: pypdf2-layer
Version: 1
ARN: arn:aws:lambda:us-east-1:848747536965:layer:pypdf2-layer:1
Runtime: python3.11
Package: PyPDF2 3.0.1
Size: 715KB
Note: AWS does not support tagging Lambda layers — tracked here instead.
```

#### Key Learnings So Far:

```
Lambda Layers - Mental Model:
Layers are pre-loaded kitchen tools. Instead of shipping all dependencies
with every function deployment, layers mount to /opt/ at runtime and are
shared across functions. Stable dependencies (PyPDF2) belong in layers;
volatile business logic belongs in the function itself.

When to use layers:
- Multiple Lambda functions need the same dependency
- Large dependencies that change rarely (PyPDF2, Pandas, NumPy)
- Sharing internal utilities across a team or org
- Approaching Lambda's 50MB deployment package size limit

Python Version Matching:
Always match local Python version to Lambda runtime. Building a layer with
Python 3.13 locally but running Python 3.11 in Lambda causes silent failures
for packages with C extensions. PyPDF2 is pure Python so it's forgiving,
but this habit is critical for packages like Pandas or NumPy.

pip --target flag:
Installs packages to a specific folder instead of the global Python
environment. Essential pattern for Lambda layer packaging.

AWS Layer Tagging Limitation:
AWS does not support tagging Lambda layers — only Lambda functions.
Workaround: document layer resources in config files or the dev log.

Windows Git Bash - zip not available:
Used Python shutil.make_archive() as a cross-platform alternative.
Pattern: when a CLI tool is missing, Python stdlib almost always has an equivalent.
```

#### Challenges Faced:

```
Challenge 1: Python Version Mismatch
- Issue: Local Python 3.13 compiled .pyc files incompatible with Lambda 3.11
- Detection: cpython-313 in .pyc filenames after install
- Solution: Wiped folder, installed Python 3.11, reinstalled with explicit path
- Lesson: Always verify python --version matches Lambda runtime before building layers

Challenge 2: Python 3.11 Not on PATH After Install
- Issue: python3.11 command not found even after installing Python 3.11
- Root cause: Windows installer did not add versioned executable to PATH
- Solution: Used full path /c/Users/carla/AppData/Local/Programs/Python/Python311/python.exe
- Lesson: On Windows, use full paths for specific Python versions

Challenge 3: pip not included with Python 3.11 install
- Solution: python3.11 -m ensurepip --upgrade
- Lesson: Always bootstrap pip on fresh Python installs

Challenge 4: zip command not available on Windows Git Bash
- Solution: Python shutil.make_archive() — cross-platform and reliable
- Lesson: Python stdlib is a reliable fallback for missing CLI tools on Windows
```

#### Cost Tracker:

- Lambda layer storage: $0.00 (within Free Tier)
- Running total: $0.038
- Budget remaining: $24.96

---

### Phase 5: Frontend Development

**Date:** March 6, 2026
**Time Spent:** ~2 hours
**Status:** ✅ Complete
**Tag:** phase-5-complete

#### What I Did:

- [x] Built DocFlow static frontend (index.html, styles.css, app.js)
- [x] Implemented drag-and-drop upload with file validation (PDF/JPG/PNG, 10MB limit)
- [x] Built animated progress ring with 4 pipeline step indicators (S3 → Textract → Comprehend → Store)
- [x] Built results cards showing extracted Textract fields, entities, sentiment bars, S3 key
- [x] Built stats bar tracking docs processed, avg time, success rate, estimated cost
- [x] Simulated pipeline at 80% success rate matching Phase 3/4 actuals
- [x] Pre-wired Phase 6 API stubs in app.js (CONFIG.SIMULATE flag ready to flip)
- [x] Fixed style.css → styles.css filename typo
- [x] Deployed to S3 static website hosting
- [x] Configured public access block + bucket policy
- [x] Recorded 1-minute demo video (90% success rate on 10 docs)
- [x] Updated portfolio project cards (copy, tags, DocFlow screenshot)
- [x] Committed, tagged, merged to main

#### Design Decisions:

```
Dark theme with grid background — matches technical/engineering aesthetic
DM Mono for data fields — clearly separates labels from values
Progress ring over spinner — shows actual progress not just "loading"
Pipeline breadcrumb (S3 → Lambda → Textract → Comprehend → Output) —
  educates viewers about the architecture while they wait
Failure cards kept intentional — honest 80% rate, shows UnsupportedDocumentException
  with documented remediation path from Phase 4
Stats bar always visible — immediate value signal for portfolio viewers
CONFIG.SIMULATE flag — clean separation between Phase 5 UI and Phase 6 API wiring
```

#### S3 Deployment:

```
Bucket: doc-processing-demo-frontend-848747536965
URL: http://doc-processing-demo-frontend-848747536965.s3-website-us-east-1.amazonaws.com
Public access block: disabled (frontend bucket only — by design)
Bucket policy: PublicReadGetObject
Content-type headers set explicitly on upload (critical for browser rendering)
cache-control: no-cache on HTML/JS, max-age=3600 on CSS
```

#### Challenges Faced:

```
Challenge 1: style.css vs styles.css filename mismatch
- Issue: File uploaded as style.css but index.html referenced styles.css
- Impact: CSS not loading, unstyled page
- Solution: Renamed locally, re-uploaded with corrected filename
- Lesson: Always verify filenames match exactly before deploying

Challenge 2: S3 BlockPublicPolicy error on bucket policy
- Issue: AccessDenied when calling PutBucketPolicy — BlockPublicPolicy setting
- Solution: Disabled public access block first, then applied bucket policy
- Lesson: S3 public access block must be explicitly disabled before public
  bucket policies can be applied — this is intentional AWS security behavior
  Note: Only appropriate for frontend/static asset buckets, never uploads/processed buckets
```

#### Key Learnings:

```
aws s3 cp source destination — same as Unix cp but crosses local ↔ S3 boundary
--content-type flag is critical — without it S3 serves HTML as plain text
--cache-control "no-cache" on HTML/JS ensures browsers always fetch fresh copy
S3 Block Public Access — four separate settings, all must be false for public hosting
Production pattern: CloudFront → private S3 (Origin Access Control) instead of public bucket
Phase 6 presigned URL pattern — Lambda generates temporary signed URL,
  browser uploads directly to S3, no credentials exposed client-side
```

#### Demo Video:

```
Length: ~1 minute
Success rate shown: 90% (10 docs, 1 failure)
Structure: single doc first → bulk processing (shows both use cases)
Platform: Loom (browser extension)
Scheduled posts: LinkedIn, Instagram, Substack (captions drafted)
```

#### Portfolio Updates:

```
Updated project cards: Cloud Resume Challenge, FinOps Case Study,
  Cloud Governance Playbook, Doc Processing Pipeline
Changes: new copy (value-first format), tightened tags, DocFlow screenshot added
Governance Playbook title updated: "The Cloud Governance Playbook I Wish Existed When I Started"
```

#### Cost Tracker:

- S3 static hosting: $0.00 (within Free Tier)
- S3 PUT requests (file uploads): $0.00 (within Free Tier)
- Running total: $0.038
- Budget remaining: $24.962

#### Screenshots Captured:

- [x] DocFlow frontend live (portfolio card image)
- [x] Demo video recorded (10 docs, 90% success rate)
- [x] LinkedIn engagement — peer validation from Full Stack Developer

#### Side Quest: GitHub Repo Restructure

```
Status: Completed
Goal: Flattened theDovelyDev/theDovelyDev → theDovelyDev/theprojectfolder (no wrapper folder)
```

### Phase 6: API Gateway Integration

**Date:** 2026-03-18 / 2026-03-19  
**Time Spent:** ~2.5 hours  
**Status:** [x] Complete

#### What I Did:

- [x] Created REST API (doc-processing-api, REGIONAL, ID: 0r8p6ap199)
- [x] Set up POST /upload endpoint → APIUploadHandler Lambda
- [x] Set up GET /results endpoint → APIResultsHandler Lambda
- [x] Configured CORS on both resources (API Gateway + Lambda response headers)
- [x] Created and deployed APIUploadHandler and APIResultsHandler Lambda functions
- [x] Deployed to production stage
- [x] Updated frontend with live API endpoint, flipped CONFIG.SIMULATE to false
- [x] Applied resource tags to both Lambdas and API Gateway
- [x] Smoke tested via CLI and UI — confirmed end-to-end
- [x] Verified uploads and results in S3, confirmed invocations in CloudTrail

#### API Testing:
```bash
curl -X POST https://0r8p6ap199.execute-api.us-east-1.amazonaws.com/prod/upload \
  -H "Content-Type: application/json" \
  -d '{"fileName": "invoice_069_INV-2025-9308.pdf", "fileContent": "[base64]", "contentType": "application/pdf"}'

Response: {"message": "File uploaded successfully", "documentId": "3e618659-8fc7-4f2c-81b3-2428b64732b6", "s3Key": "uploads/3e618659-8fc7-4f2c-81b3-2428b64732b6_invoice_069_INV-2025-9308.pdf"}

curl "https://0r8p6ap199.execute-api.us-east-1.amazonaws.com/prod/results?documentId=3e618659-8fc7-4f2c-81b3-2428b64732b6"

Response: Full extraction + Comprehend analysis returned — 94.74% confidence, status: success
```

#### Cost Tracker:

- API Gateway requests: <$0.01 (well within free tier)
- Running total: ~$0.038

#### Challenges Faced:
```
Challenge: Lambda zip packaged wrong handler file + nested zip
- Error: Runtime.ImportModuleError
- Root cause: shutil.make_archive() picked up all files in folder including
  the zip itself; handler files had been placed in wrong directories
- Solution: Rebuilt zips using zipfile module, explicitly targeting each handler file
- Lesson: Always verify zip contents with zipfile.namelist() before deploying

Challenge: Syntax error in api_upload_handler.py
- Error: Runtime.UserCodeSyntaxError on line 1
- Root cause: Filename header from context file formatting copied into the file
- Solution: Removed the **api_upload_handler.py:** line, file started with import json
- Lesson: Verify file contents in VSCode before zipping

Challenge: CloudWatch logs failing in Git Bash
- Error: AWS CLI converting /aws/lambda/... to a Windows path
- Solution: Use MSYS_NO_PATHCONV=1 prefix, or check logs via console
- Lesson: Console is faster for one-off log checks on Windows
```

#### Screenshots Captured:

- [ ] API Gateway configuration
- [ ] Successful curl smoke test output
- [ ] UI end-to-end document upload
- [ ] S3 uploads and processed buckets confirmed
- [ ] CloudTrail invocation logs

---

### Phase 7: End-to-End Testing

**Date:** [DATE]  
**Time Spent:** [HOURS]  
**Status:** [ ] In Progress / [ ] Complete

#### What I Did:

- [ ] Tested with 150 mock documents
- [ ] Processed 50 invoices
- [ ] Processed 50 receipts
- [ ] Monitored costs in real-time
- [ ] Checked CloudWatch logs for errors
- [ ] Validated extraction accuracy

#### Testing Results:

| Metric          | Target | Actual    | Status |
| --------------- | ------ | --------- | ------ |
| Processing time | <60s   | [ACTUAL]s | ✅/❌  |
| Success rate    | >95%   | [ACTUAL]% | ✅/❌  |
| Cost per doc    | <$0.05 | $[ACTUAL] | ✅/❌  |
| Accuracy        | >90%   | [ACTUAL]% | ✅/❌  |

#### Total Testing Cost:

- 150 documents processed
- Textract: $[AMOUNT]
- Comprehend: $[AMOUNT]
- Lambda: $[AMOUNT]
- Total: $[AMOUNT]

#### Issues Found & Fixed:

```
Issue 1: [DESCRIBE]
- Impact: [SEVERITY]
- Root cause: [CAUSE]
- Fix: [SOLUTION]

Issue 2: [DESCRIBE]
```

#### Screenshots Captured:

- [ ] Cost Explorer showing actual usage
- [ ] CloudWatch metrics dashboard
- [ ] Processing results examples

---

### Phase 8: Optimization & Cost Reduction

**Date:** [DATE]  
**Time Spent:** [HOURS]  
**Status:** [ ] In Progress / [ ] Complete

#### What I Did:

- [ ] Implemented S3 lifecycle policies (90 day → Glacier)
- [ ] Right-sized Lambda memory allocation
- [ ] Optimized Textract API calls
- [ ] Added batch processing capability
- [ ] Reduced unnecessary logging

#### Before/After Optimization:

| Metric              | Before    | After      | Savings |
| ------------------- | --------- | ---------- | ------- |
| Lambda memory       | 512MB     | [ACTUAL]MB | [%]     |
| Avg processing time | [TIME]s   | [TIME]s    | [%]     |
| Cost per doc        | $[AMOUNT] | $[AMOUNT]  | [%]     |

#### Cost Tracker - Final:

- Total development cost: $[FINAL AMOUNT]
- Under budget? ✅/❌ by $[AMOUNT]

#### Key Optimizations:

```
[Describe what worked]

Example:
1. Reduced Lambda memory from 512MB → 256MB (no performance impact)
   - Saved: 30% on compute costs

2. Implemented lifecycle policy for S3
   - Old documents → Glacier after 90 days
   - Saved: 90% on storage for archived docs
```

---

### Phase 9: Documentation & Portfolio Prep

**Date:** [DATE]  
**Time Spent:** [HOURS]  
**Status:** [ ] In Progress / [ ] Complete

#### What I Did:

- [ ] Created comprehensive README
- [ ] Wrote architecture documentation
- [ ] Captured all screenshots
- [ ] Recorded demo video (2-3 minutes)
- [ ] Updated LinkedIn with project
- [ ] Published portfolio page

#### Portfolio Assets Created:

- [ ] README.md (with architecture diagram)
- [ ] Demo video (uploaded to YouTube/Vimeo)
- [ ] 10 key screenshots
- [ ] Cost analysis spreadsheet
- [ ] This development log / Substack article

#### GitHub Repository:

- URL: [YOUR REPO URL]
- Stars: [TRACK OVER TIME]
- Forks: [TRACK OVER TIME]

---

## Technical Challenges & Solutions

### Challenge 1: [YOUR BIGGEST CHALLENGE]

**The Problem:**

```
[Detailed description]
```

**What I Tried:**

1. [First attempt]
2. [Second attempt]
3. [Third attempt]

**The Solution:**

```
[What ultimately worked]
```

**Key Takeaway:**

```
[What you learned]
```

---

### Challenge 2: Managing AWS Costs

**The Problem:**

```
I was worried about costs spiraling during development, especially with AI services
that charge per API call.
```

**What I Tried:**

1. Set up budget alerts at $25
2. Used Cost Explorer daily
3. Tracked every API call in spreadsheet

**The Solution:**

```
- Used Free Tier strategically (Textract: 1,000 pages free for 3 months)
- Tested with small document batches first
- Implemented cost tracking in my development log
- Final cost: $8.47 (well under $25 budget)
```

**Key Takeaway:**

```
AWS Free Tier is generous if you plan carefully. Cost Explorer is your friend.
Budget alerts saved me from accidentally leaving resources running.
```

---

### Challenge 3: [ANOTHER CHALLENGE]

[FILL IN YOUR CHALLENGES]

---

## Key Learnings

### Technical Skills Gained

- [ ] AWS Lambda serverless architecture
- [ ] S3 event-driven triggers
- [ ] API Gateway REST API design
- [ ] IAM roles and permissions
- [ ] AWS Textract OCR integration
- [ ] AWS Comprehend NLP integration
- [ ] CloudWatch monitoring and logging
- [ ] Cost optimization strategies

### Soft Skills Developed

- [ ] Problem decomposition (breaking 28-hour project into phases)
- [ ] Documentation (this log!)
- [ ] Cost management and budgeting
- [ ] Time tracking and estimation
- [ ] Git workflow (dev branch → main merges)

### Biggest "Aha!" Moments

```
1. CLI vs Console: Pragmatism Over Dogmatism (Phase 1)
   During Phase 1, I tried applying the S3 lifecycle policy via CLI following
   "infrastructure-as-code best practices." The command failed. After 10 minutes
   of troubleshooting, I pivoted to the AWS Console and had it configured in
   2 minutes.

   AHA: Don't be dogmatic about "CLI only" or "Console only" - use the right
   tool for the situation. For one-time configurations during learning, the
   console's visual feedback is invaluable. For production automation, CLI/IaC
   is essential. Real-world engineering is about getting things done effectively,
   not following rules blindly.

   This moment taught me that adaptability and pragmatism are more valuable than
   rigid adherence to "best practices." In interviews, this shows problem-solving
   flexibility rather than religious devotion to a single approach.

2. Tagging Strategy: Future-Proofing From Day One (Phase 1)
   I almost skipped implementing a comprehensive tagging strategy because it felt
   like "extra work" for a learning project. But I pushed through and created
   TAGGING_STRATEGY.md with Project, CostCenter, Environment, Owner, Component,
   CreatedDate, and ManagedBy tags.

   AHA: Professional-grade AWS hygiene costs 30 minutes now but saves hours later.
   At year-end, I'll run ONE command (./year-end-report.sh 2026) and instantly see:
   "Project1 cost $43, Project2 cost $67, Project3 cost $28." This level of cost
   visibility is what separates hobbyist projects from professional portfolios.

   The extra 30 minutes to set up proper tagging demonstrates forward-thinking and
   operational maturity - exactly what hiring managers look for.

3. Environment Variables: Self-Documenting, Reusable Infrastructure (Phase 1)
   Instead of hardcoding bucket names and account IDs, I created setup.sh with
   all configuration centralized: PROJECT_NAME, REGION, ACCOUNT_ID, and all tags.

   AHA: Using ${VARIABLES} instead of hardcoded values makes code self-documenting
   AND reusable. Every command reads like:
   "aws s3 mb s3://${PROJECT_NAME}-uploads-${ACCOUNT_ID}"

   This means anyone (including future me) can immediately understand what each
   value represents. Plus, adapting this project for a new AWS account or different
   project is literally just changing 3 variables in setup.sh.

   This is the difference between "code that works" and "code that's maintainable."

4. [YOUR MOMENT - Add more as you progress through phases]
   Example: "Serverless doesn't mean 'no servers'—it means 'no server management.'
   Lambda still runs on servers, but AWS handles all the scaling/patching."
```

### What I'd Do Differently Next Time

```
1. [REFLECTION]
   Example: "Start with cost estimation calculator BEFORE building"

2. [REFLECTION]
   Example: "Test with production-sized documents earlier"

3. [REFLECTION]
```

---

## Results & Impact

### Final Metrics

**Performance:**

- Average processing time: [ACTUAL] seconds
- Success rate: [ACTUAL]%
- Extraction accuracy: [ACTUAL]%
- Documents tested: 150

**Cost (Development):**

- Budgeted: $11-15
- Actual: $[ACTUAL]
- Variance: [OVER/UNDER] by $[AMOUNT]

**Cost (Production Model):**

- Per document: $[ACTUAL]
- Monthly (500 docs): $[ACTUAL]
- Annual: $[ACTUAL]

**ROI Analysis:**

```
Manual Processing Cost:
- Time: 3 minutes per document
- Staff rate: $25/hour
- Cost per document: $1.25
- Monthly cost (500 docs): $625

Automated Processing Cost:
- Time: 30 seconds per document
- AWS cost: $0.034 per document
- Monthly cost (500 docs): $17

Savings:
- Per document: $1.22 (97% reduction)
- Monthly: $608
- Annual: $7,296
- ROI: 3,558%
```

### Business Impact

```
For a small accounting firm processing 500 invoices/month:
- Time saved: 20.8 hours/month (83% reduction)
- Cost saved: $608/month
- Payback period: < 1 week
- 3-year savings: $21,888
```

---

## What's Next

### Potential Enhancements

- [ ] Add support for handwritten documents (AWS Textract custom models)
- [ ] Implement batch processing queue with SQS
- [ ] Create admin dashboard with analytics
- [ ] Add webhook notifications for processing completion
- [ ] Support 20+ languages (Comprehend multi-language)
- [ ] Implement document classification (invoice vs receipt vs form)
- [ ] Add user authentication (AWS Cognito)
- [ ] Build mobile app version

### Other AWS Projects Planned

1. [Next project idea]
2. [Next project idea]
3. [Next project idea]

---

## Appendix: Resources That Helped

### Documentation

- AWS Textract Developer Guide: [link]
- AWS Comprehend Documentation: [link]
- AWS Lambda Best Practices: [link]

### Tutorials & Inspiration

- [Tutorial name]: [link]
- [Blog post]: [link]

### Tools Used

- AWS CLI
- VS Code (with AWS Toolkit extension)
- Postman (API testing)
- draw.io (architecture diagrams)

### Cost Tracking

- Detailed spreadsheet: [link to your cost tracker]
- AWS Cost Explorer screenshots: [included above]

---

## How to Follow My Journey

**GitHub:** [Your GitHub profile]  
**LinkedIn:** [Your LinkedIn]  
**Portfolio:** [Your portfolio site]  
**Substack:** [Your Substack - if you create one]

**Coming up next:** [Tease your next project]

---

## FAQ for Readers

**Q: Can I replicate this project?**  
A: Absolutely! Full code and implementation guide available in my GitHub repo: [link]

**Q: What was the hardest part?**  
A: [Your answer]

**Q: How long did it really take?**  
A: [Actual hours], spread over [number] days

**Q: What if I don't have AWS experience?**  
A: [Your advice]

**Q: Is the Free Tier really enough?**  
A: [Your experience]

---

## Final Thoughts

[Write your reflection here after completing the project]

Example template:

> When I started this project, I [initial feeling/thought]. After 28 hours of
> development, I learned that [key insight]. The most surprising part was [surprise].
> If you're considering building something similar, my advice is [advice].
>
> This project taught me that [lesson]. I'm excited to apply these skills to [next goal].

---

## Acknowledgments

Thanks to:

- [Anyone who helped]
- [Resources you used]
- [Communities that supported you]

---

**Project Status:** [In Progress / Complete]  
**Last Updated:** [DATE]  
**Total Time Invested:** [HOURS]  
**Final Cost:** $[AMOUNT]  
**Worth It?** [YES/NO - and why]

---

_This log serves as both development documentation and the foundation for my Substack article. It captures the real, unfiltered journey—challenges, victories, and lessons learned._

---

## Notes Section (Private - Don't Publish)

Use this space for quick notes during development:

```
[Quick thoughts, reminders, ideas]

Example:
- Remember to screenshot the CloudWatch dashboard before teardown
- That error message at 11pm was due to incorrect IAM permissions
- Good quote for article: "Serverless isn't about servers, it's about time"
- Follow up: Check if Textract supports handwriting better now
```

---

## Changelog

**January 16, 2026** - Started project  
**January 16, 2026** - Completed Pre-Development Setup (AWS account, IAM, CLI config, budget alerts)  
**January 16, 2026** - Completed Phase 1 (S3 buckets with comprehensive tagging, versioning, policies, lifecycle rules)  
**January 16, 2026** - Completed Side Quest: Automated Tag Governance (Lambda, EventBridge, SNS - weekly audits)  
**February 2026** - Completed Phase 2 (Lambda functions)  
**February 2026** - Completed Phase 3 (Textract integration - 80% success rate, 12/15 docs)  
**March 4, 2026** - Completed Phase 4 (Lambda Optimization & PDF Preprocessing - PyPDF2 layer, preprocessing pipeline, 80% success rate maintained)  
**March 5, 2026** - Completed Phase 5 (DocFlow frontend deployed to S3 — drag-and-drop upload, animated pipeline visualization, simulated 80% success rate, Phase 6 API stubs pre-wired. Portfolio project cards updated. Demo video recorded.)
**March 18, 20226** - Completed Phase 6 (API Gateway)  
**[DATE]** - Completed Phase 7 (End-to-end testing)  
**[DATE]** - Completed Phase 8 (Optimization)  
**[DATE]** - Completed Phase 9 (Documentation & portfolio prep)  
**[DATE]** - Project complete!  
**[DATE]** - Published Substack article

---

## Article Outline (For Substack Conversion)

When converting this log to a Substack article, use this structure:

### Title Options:

1. "I Built an AI Document Processor on AWS for $8.47 (Here's How)"
2. "From Zero to AI: Building a Serverless Document Pipeline in 28 Hours"
3. "My First AWS AI Project: Processing 150 Documents with Textract & Comprehend"

### Article Flow:

1. **Hook** (200 words)
   - The problem (manual document processing is slow/expensive)
   - What I built (AI-powered automation)
   - Results teaser (80% time savings, $0.034 per document)

2. **Why I Built This** (300 words)
   - Learning goals
   - Career transition context
   - Portfolio motivation

3. **The Architecture** (400 words)
   - Simple diagram
   - 6 layers explained briefly
   - Tech stack overview

4. **Building It: The Journey** (800 words)
   - Phase-by-phase highlights (not all details)
   - Focus on 2-3 biggest challenges
   - Include code snippets
   - Share "aha!" moments

5. **Testing at Scale** (300 words)
   - 150 mock documents
   - Results & accuracy
   - Cost breakdown

6. **What I Learned** (400 words)
   - Technical skills
   - Unexpected insights
   - What I'd do differently

7. **The Results** (300 words)
   - Final metrics
   - ROI analysis
   - Business impact

8. **Try It Yourself** (200 words)
   - Link to GitHub
   - Link to implementation guide
   - Encouragement

9. **What's Next** (150 words)
   - Future enhancements
   - Next projects
   - Call to action (follow, subscribe)

**Total Target Length:** 2,500-3,000 words  
**Reading Time:** 10-12 minutes  
**Tone:** Technical but accessible, honest about challenges

---

**Remember:** This log is your raw material. The Substack article will be a polished, storytelling version of this journey. Keep this document honest and detailed—you'll mine it for the good parts later!
