#!/bin/bash

# Lambda Monitoring Script
# Real-time monitoring of document processing

echo "📊 Document Processor Monitoring Dashboard"
echo "=========================================="
echo ""

# Check if environment variables are loaded
if [ -z "$PROJECT_NAME" ]; then
    echo "❌ Error: Environment variables not loaded"
    echo "Please run: source setup.sh"
    exit 1
fi

FUNCTION_NAME="DocumentProcessor"

# Function metrics
echo "📈 Lambda Function Metrics (Last 24 hours):"
echo "-------------------------------------------"

# Get invocation count
INVOCATIONS=$(aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=${FUNCTION_NAME} \
  --start-time $(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 86400 \
  --statistics Sum \
  --query 'Datapoints[0].Sum' \
  --output text 2>/dev/null || echo "0")

# Get error count
ERRORS=$(aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=${FUNCTION_NAME} \
  --start-time $(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 86400 \
  --statistics Sum \
  --query 'Datapoints[0].Sum' \
  --output text 2>/dev/null || echo "0")

# Get average duration
AVG_DURATION=$(aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=${FUNCTION_NAME} \
  --start-time $(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 86400 \
  --statistics Average \
  --query 'Datapoints[0].Average' \
  --output text 2>/dev/null || echo "0")

echo "  Invocations: ${INVOCATIONS}"
echo "  Errors: ${ERRORS}"
echo "  Avg Duration: $(printf "%.0f" ${AVG_DURATION} 2>/dev/null || echo "0") ms"

# Calculate success rate
if [ "$INVOCATIONS" != "0" ] && [ "$INVOCATIONS" != "None" ]; then
    SUCCESS_RATE=$(echo "scale=1; (($INVOCATIONS - $ERRORS) / $INVOCATIONS) * 100" | bc 2>/dev/null || echo "100")
    echo "  Success Rate: ${SUCCESS_RATE}%"
else
    echo "  Success Rate: N/A (no invocations)"
fi

echo ""

# Recent logs
echo "📝 Recent Logs (Last 10 minutes):"
echo "--------------------------------"
aws logs tail /aws/lambda/${FUNCTION_NAME} --since 10m --format short 2>/dev/null | head -n 20 || echo "No logs available"

echo ""

# S3 bucket stats
UPLOAD_BUCKET="${PROJECT_NAME}-uploads-${ACCOUNT_ID}"
PROCESSED_BUCKET="${PROJECT_NAME}-processed-${ACCOUNT_ID}"

echo "📁 S3 Bucket Status:"
echo "-------------------"
UPLOAD_COUNT=$(aws s3 ls s3://${UPLOAD_BUCKET}/uploads/ --recursive 2>/dev/null | wc -l)
PROCESSED_COUNT=$(aws s3 ls s3://${PROCESSED_BUCKET}/processed/ --recursive 2>/dev/null | wc -l)

echo "  Upload bucket: ${UPLOAD_COUNT} files"
echo "  Processed bucket: ${PROCESSED_COUNT} files"

echo ""
echo "=========================================="
echo ""
echo "To follow logs in real-time:"
echo "  aws logs tail /aws/lambda/${FUNCTION_NAME} --follow"
echo ""
echo "To view function configuration:"
echo "  aws lambda get-function --function-name ${FUNCTION_NAME}"
echo ""
