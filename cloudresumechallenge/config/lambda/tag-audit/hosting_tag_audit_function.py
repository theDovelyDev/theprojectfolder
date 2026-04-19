import boto3
import os
from datetime import datetime

sns = boto3.client('sns')
tagging = boto3.client('resourcegroupstaggingapi')

SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

REQUIRED_TAGS = ['Project', 'CostCenter', 'Environment', 'Component']

SKIP_RESOURCES = [
    'arn:aws:organizations',
    'arn:aws:budgets',
    'arn:aws:acm',
    'arn:aws:iam::102587257710:oidc-provider',
    'arn:aws:payments'
]

def lambda_handler(event, context):
    print("Starting hosting account tag audit...")

    paginator = tagging.get_paginator('get_resources')
    all_resources = []

    for page in paginator.paginate():
        all_resources.extend(page['ResourceTagMappingList'])

    # Filter out resources we intentionally skip
    resources = [
        r for r in all_resources
        if not any(r['ResourceARN'].startswith(skip) for skip in SKIP_RESOURCES)
    ]

    fully_tagged = []
    missing_tags = []
    untagged = []

    for resource in resources:
        arn = resource['ResourceARN']
        tags = {t['Key']: t['Value'] for t in resource.get('Tags', [])}

        missing = [tag for tag in REQUIRED_TAGS if tag not in tags]

        if not missing:
            fully_tagged.append(arn)
        elif len(missing) == len(REQUIRED_TAGS):
            untagged.append(arn)
        else:
            missing_tags.append({
                'arn': arn,
                'missing': missing
            })

    # Build report
    report = []
    report.append("AWS TAG COMPLIANCE AUDIT REPORT — HOSTING ACCOUNT")
    report.append("=" * 50)
    report.append(f"Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    report.append("")
    report.append("SUMMARY")
    report.append("-" * 20)
    report.append(f"Fully tagged    : {len(fully_tagged)}")
    report.append(f"Missing tags    : {len(missing_tags)}")
    report.append(f"Completely untagged : {len(untagged)}")
    report.append(f"Required tags   : {', '.join(REQUIRED_TAGS)}")
    report.append("")

    # Fully tagged
    report.append("✅ FULLY TAGGED")
    report.append("-" * 20)
    if fully_tagged:
        for arn in fully_tagged:
            short = arn.split(':')[-1]
            report.append(f"  • {short}")
    else:
        report.append("  None")
    report.append("")

    # Missing specific tags
    report.append("⚠️  MISSING TAGS")
    report.append("-" * 20)
    if missing_tags:
        for r in missing_tags:
            short = r['arn'].split(':')[-1]
            report.append(f"  • {short}")
            report.append(f"    Missing: {', '.join(r['missing'])}")
    else:
        report.append("  None — all tagged resources are compliant!")
    report.append("")

    # Completely untagged
    report.append("❌ COMPLETELY UNTAGGED")
    report.append("-" * 20)
    if untagged:
        for arn in untagged:
            short = arn.split(':')[-1]
            report.append(f"  • {short}")
    else:
        report.append("  None")
    report.append("")

    report.append("Next audit: 1 week from now")

    message = "\n".join(report)
    print(message)

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f"Hosting Account Tag Audit — {datetime.utcnow().strftime('%Y-%m-%d')}",
        Message=message
    )

    return {
        'status': 'complete',
        'fully_tagged': len(fully_tagged),
        'missing_tags': len(missing_tags),
        'untagged': len(untagged)
    }