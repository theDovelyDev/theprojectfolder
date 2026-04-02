# S3 Lifecycle Policy Configuration

## Policy Applied: Archive Old Documents

**Bucket:** doc-processing-demo-processed-[ACCOUNT_ID]

**Configuration Method:** AWS Console (CLI command failed)

**Policy Details:**
- **Rule Name:** ArchiveOldDocuments
- **Status:** Enabled
- **Transition:** After 90 days → GLACIER storage class
- **Prefix Filter:** `processed/`

**Purpose:**
Reduces storage costs by moving processed document results to cheaper Glacier storage after 90 days. Documents remain accessible but with longer retrieval times.

**Cost Savings:**
- Standard S3: $0.023 per GB/month
- Glacier: $0.004 per GB/month
- Savings: ~83% on storage costs for old documents

**Applied:** January 16, 2026

## Steps to Apply via Console:

1. Go to S3 Console → Select processed bucket
2. Click "Management" tab
3. Click "Create lifecycle rule"
4. Rule name: `ArchiveOldDocuments`
5. Choose rule scope: "Limit the scope using filters"
6. Prefix: `processed/`
7. Lifecycle rule actions: "Transition current versions of objects between storage classes"
8. Transition to Glacier: 90 days after object creation
9. Review and create

## CLI Command (for reference - had issues):
```bash
aws s3api put-bucket-lifecycle-configuration \
  --bucket ${PROJECT_NAME}-processed-${ACCOUNT_ID} \
  --lifecycle-configuration file://lifecycle-policy.json
```

Note: Applied via console due to CLI configuration issues.
