#!/bin/bash

# Usage: ./fix-tags.sh <resource-arn>

RESOURCE_ARN=$1

if [ -z "$RESOURCE_ARN" ]; then
    echo "Usage: ./fix-tags.sh <resource-arn>"
    exit 1
fi

# Load standard tags
source setup.sh

echo "Applying standard tags to: $RESOURCE_ARN"

# Apply all required tags
aws resourcegroupstaggingapi tag-resources \
    --resource-arn-list "$RESOURCE_ARN" \
    --tags \
        Project=${PROJECT_TAG} \
        CostCenter=${COST_CENTER} \
        Environment=${ENVIRONMENT} \
        CreatedDate=${CREATED_DATE} \
        ManagedBy=${MANAGED_BY}

if [ $? -eq 0 ]; then
    echo "✅ Tags applied successfully"
else
    echo "❌ Failed to apply tags"
fi
