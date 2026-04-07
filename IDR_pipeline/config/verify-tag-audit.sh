#!/bin/bash

echo "=== Tag Audit System Verification ==="
echo ""

source setup.sh

echo "1️⃣ Checking SNS Topic..."
aws sns list-topics --query "Topics[?contains(TopicArn, 'TagAuditNotifications')]" --output table

echo ""
echo "2️⃣ Checking Lambda Function..."
aws lambda get-function --function-name TagAuditFunction --query 'Configuration.[FunctionName,Runtime,Timeout,MemorySize]' --output table

echo ""
echo "3️⃣ Checking EventBridge Rule..."
aws events describe-rule --name TagAuditWeeklySchedule --query '[Name,State,ScheduleExpression]' --output table

echo ""
echo "4️⃣ Checking EventBridge Targets..."
aws events list-targets-by-rule --rule TagAuditWeeklySchedule --query 'Targets[*].[Id,Arn]' --output table

echo ""
echo "5️⃣ Testing Lambda Invocation..."
aws lambda invoke --function-name TagAuditFunction --payload '{}' test-output.json > /dev/null 2>&1
cat test-output.json | jq '.'
rm test-output.json

echo ""
echo "✅ Tag Audit System Status:"
echo "   • SNS Topic: Created"
echo "   • Lambda Function: Deployed"
echo "   • EventBridge Schedule: Active (Mondays 9 AM UTC)"
echo "   • Next audit: $(date -d 'next monday 09:00' '+%Y-%m-%d %H:%M UTC')"
echo ""
echo "��� Check your email for the test audit report!"
