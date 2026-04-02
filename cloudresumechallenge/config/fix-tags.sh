#!/bin/bash

# Usage: ./fix-tags.sh <resource-arn>

RESOURCE_ARN=$1

if [ -z "$RESOURCE_ARN" ]; then
    echo "Usage: ./fix-tags.sh <resource-arn>"
    exit 1
fi

# Load standard tags — pass no args so ENVIRONMENT stays as set
source config/setup.sh "${ENVIRONMENT:-prod}"

echo "Applying standard tags to: $RESOURCE_ARN"

# Apply all required tags
aws resourcegroupstaggingapi tag-resources \
    --resource-arn-list "$RESOURCE_ARN" \
    --tags "{\"Project\":\"${PROJECT_TAG}\",\"CostCenter\":\"${COST_CENTER}\",\"Environment\":\"${ENVIRONMENT}\",\"ManagedBy\":\"${MANAGED_BY}\"}" \
    --profile portfolio-admin

if [ $? -eq 0 ]; then
    echo "✅ Tags applied successfully"
else
    echo "❌ Failed to apply tags"
fi