import json
import boto3
import os
from datetime import datetime

# Initialize AWS clients
tagging_client = boto3.client('resourcegroupstaggingapi')
sns_client = boto3.client('sns')

# Environment variables
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
REQUIRED_TAGS = ['Project', 'CostCenter', 'Environment','CreatedDate', 'ManagedBy']

def lambda_handler(event, context):
    """
    Audit all AWS resources for required tags
    Send email report via SNS
    """
    print(f"Starting tag audit at {datetime.now().isoformat()}")
    
    # Get all resources with pagination
    all_resources = []
    paginator = tagging_client.get_paginator('get_resources')
    
    for page in paginator.paginate():
        all_resources.extend(page['ResourceTagMappingList'])
    
    print(f"Found {len(all_resources)} total resources")
    
    # Check each resource for missing tags
    non_compliant_resources = []
    
    for resource in all_resources:
        resource_arn = resource['ResourceARN']
        existing_tags = {tag['Key']: tag['Value'] for tag in resource.get('Tags', [])}
        
        missing_tags = []
        for required_tag in REQUIRED_TAGS:
            if required_tag not in existing_tags:
                missing_tags.append(required_tag)
        
        if missing_tags:
            non_compliant_resources.append({
                'arn': resource_arn,
                'type': extract_resource_type(resource_arn),
                'missing_tags': missing_tags,
                'existing_tags': existing_tags
            })
    
    # Generate report
    report = generate_report(all_resources, non_compliant_resources)
    
    # Send via SNS
    send_notification(report)
    
    # Return summary
    return {
        'statusCode': 200,
        'body': json.dumps({
            'total_resources': len(all_resources),
            'compliant': len(all_resources) - len(non_compliant_resources),
            'non_compliant': len(non_compliant_resources),
            'compliance_rate': f"{((len(all_resources) - len(non_compliant_resources)) / len(all_resources) * 100):.1f}%"
        })
    }

def extract_resource_type(arn):
    """Extract readable resource type from ARN"""
    parts = arn.split(':')
    if len(parts) >= 3:
        service = parts[2]
        if len(parts) >= 6:
            resource = parts[5].split('/')[0]
            return f"{service}:{resource}"
        return service
    return "unknown"

def generate_report(all_resources, non_compliant):
    """Generate human-readable email report"""
    total = len(all_resources)
    compliant = total - len(non_compliant)
    compliance_rate = (compliant / total * 100) if total > 0 else 0
    
    report = f"""
AWS TAG COMPLIANCE AUDIT REPORT
================================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

SUMMARY
-------
Total Resources: {total}
Compliant: {compliant}
Non-Compliant: {len(non_compliant)}
Compliance Rate: {compliance_rate:.1f}%

Required Tags: {', '.join(REQUIRED_TAGS)}

"""
    
    if not non_compliant:
        report += "✅ ALL RESOURCES ARE COMPLIANT!\n"
    else:
        report += f"❌ NON-COMPLIANT RESOURCES ({len(non_compliant)})\n"
        report += "=" * 60 + "\n\n"
        
        # Group by resource type
        by_type = {}
        for resource in non_compliant:
            rtype = resource['type']
            if rtype not in by_type:
                by_type[rtype] = []
            by_type[rtype].append(resource)
        
        for rtype, resources in sorted(by_type.items()):
            report += f"\n{rtype} ({len(resources)} resources)\n"
            report += "-" * 60 + "\n"
            
            for resource in resources[:5]:  # Limit to first 5 per type
                report += f"\nARN: {resource['arn']}\n"
                report += f"Missing Tags: {', '.join(resource['missing_tags'])}\n"
                if resource['existing_tags']:
                    report += f"Existing Tags: {json.dumps(resource['existing_tags'], indent=2)}\n"
            
            if len(resources) > 5:
                report += f"\n... and {len(resources) - 5} more {rtype} resources\n"
    
    report += "\n" + "=" * 60 + "\n"
    report += "\nACTION ITEMS:\n"
    report += "1. Review non-compliant resources above\n"
    report += "2. Apply missing tags using: ./fix-tags.sh <resource-arn>\n"
    report += "3. Update TAGGING_STRATEGY.md if needed\n"
    report += "\nNext audit: 1 week from now\n"
    
    return report

def send_notification(report):
    """Send report via SNS"""
    subject = f"AWS Tag Audit Report - {datetime.now().strftime('%Y-%m-%d')}"
    
    try:
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=report
        )
        print(f"Notification sent successfully. MessageId: {response['MessageId']}")
    except Exception as e:
        print(f"Error sending notification: {str(e)}")
        raise
