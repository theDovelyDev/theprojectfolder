#!/bin/bash
# Verify tags on all Project 2 resources
# Usage: bash verify-tag-audit.sh

source setup.sh

echo ""
echo "🔍 Scanning resources tagged Project=${PROJECT_TAG}..."
echo ""

aws resourcegroupstaggingapi get-resources \
  --tag-filters "Key=Project,Values=${PROJECT_TAG}" \
  --region "${REGION}" \
  --profile "${AWS_PROFILE}" \
  --query 'ResourceTagMappingList[].{ARN:ResourceARN,Tags:Tags}' \
  --output table

echo ""
echo "🔍 Checking for untagged resources in region ${REGION}..."
echo ""

UNTAGGED=$(aws resourcegroupstaggingapi get-resources \
  --region "${REGION}" \
  --profile "${AWS_PROFILE}" \
  --query '[ResourceTagMappingList[] | length(@)]' \
  --output text)

echo "Total resources found: ${UNTAGGED}"
echo ""
echo "✅ Audit complete. Review table above for missing tags."