import boto3
import os
from datetime import datetime

sns = boto3.client('sns')
tagging = boto3.client('resourcegroupstaggingapi')

SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

REQUIRED_TAGS = ['Project', 'CostCenter', 'Environment', 'Component', 'ManagedBy']

KNOWN_PROJECTS = [
    'doc-processing-pipeline',
    'budget-research-agent',
]

SKIP_RESOURCES = [
    'arn:aws:organizations',
    'arn:aws:budgets',
    'arn:aws:acm',
    'arn:aws:iam::848747536965:oidc-provider',
    'arn:aws:payments'
]

def lambda_handler(event, context):
    print("Starting sandbox account tag audit...")

    try:
        paginator = tagging.get_paginator('get_resources')
        all_resources = []

        for page in paginator.paginate():
            all_resources.extend(page['ResourceTagMappingList'])
        
        print(f"Total resources found: {len(all_resources)}")

    except Exception as e:
        print(f"ERROR during resource scan: {str(e)}")
        raise

    # Filter out resources we intentionally skip
    resources = [
        r for r in all_resources
        if not any(r['ResourceARN'].startswith(skip) for skip in SKIP_RESOURCES)
    ]

    # Bucket by project
    buckets = {project: {'fully_tagged': [], 'missing_tags': [], 'untagged': []} 
               for project in KNOWN_PROJECTS}
    buckets['unknown'] = {'fully_tagged': [], 'missing_tags': [], 'untagged': []}

    for resource in resources:
        arn = resource['ResourceARN']
        tags = {t['Key']: t['Value'] for t in resource.get('Tags', [])}
        project = tags.get('Project', None)
        missing = [tag for tag in REQUIRED_TAGS if tag not in tags]

        entry = {'arn': arn, 'missing': missing}

        if project in buckets:
            bucket = buckets[project]
        else:
            bucket = buckets['unknown']

        if not missing:
            bucket['fully_tagged'].append(arn)
        elif len(missing) == len(REQUIRED_TAGS):
            bucket['untagged'].append(arn)
        else:
            bucket['missing_tags'].append(entry)
   
    # Global counts
    all_fully_tagged = sum(len(b['fully_tagged']) for b in buckets.values())
    all_missing = sum(len(b['missing_tags']) for b in buckets.values())
    all_untagged = sum(len(b['untagged']) for b in buckets.values())

    # Build report
    report = []
    report.append("AWS TAG COMPLIANCE AUDIT REPORT — SANDBOX ACCOUNT")
    report.append("=" * 50)
    report.append(f"Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    report.append("")
    report.append("SUMMARY")
    report.append("-" * 20)
    report.append(f"Fully tagged         : {all_fully_tagged}")
    report.append(f"Missing specific tags : {all_missing}")
    report.append(f"Completely untagged  : {all_untagged}")
    report.append(f"Required tags        : {', '.join(REQUIRED_TAGS)}")
    report.append("")

    for project in KNOWN_PROJECTS:
        b = buckets[project]
        total = len(b['fully_tagged']) + len(b['missing_tags']) + len(b['untagged'])
        if total == 0:
            continue

        report.append("=" * 50)
        report.append(f"PROJECT: {project.upper()}")
        report.append("=" * 50)
        report.append(f"Fully tagged         : {len(b['fully_tagged'])}")
        report.append(f"Missing specific tags : {len(b['missing_tags'])}")
        report.append(f"Completely untagged  : {len(b['untagged'])}")
        report.append("")

        report.append("✅ FULLY TAGGED")
        report.append("-" * 20)
        if b['fully_tagged']:
            for arn in b['fully_tagged']:
                short = arn.split(':')[-1]
                report.append(f"  • {short}")
        else:
            report.append("  None")
        report.append("")

        report.append("⚠️  MISSING TAGS")
        report.append("-" * 20)
        if b['missing_tags']:
            for r in b['missing_tags']:
                short = r['arn'].split(':')[-1]
                report.append(f"  • {short}")
                report.append(f"    Missing: {', '.join(r['missing'])}")
        else:
            report.append("  None — all tagged resources are compliant!")
        report.append("")

        report.append("❌ COMPLETELY UNTAGGED")
        report.append("-" * 20)
        if b['untagged']:
            for arn in b['untagged']:
                short = arn.split(':')[-1]
                report.append(f"  • {short}")
        else:
            report.append("  None")
        report.append("")

    # Unknown project resources
    u = buckets['unknown']
    if any([u['fully_tagged'], u['missing_tags'], u['untagged']]):
        report.append("=" * 50)
        report.append("UNKNOWN / UNTAGGED PROJECT")
        report.append("=" * 50)

        if u['fully_tagged']:
            report.append("✅ FULLY TAGGED")
            report.append("-" * 20)
            for arn in u['fully_tagged']:
                report.append(f"  • {arn.split(':')[-1]}")
            report.append("")

        if u['missing_tags']:
            report.append("⚠️  MISSING TAGS")
            report.append("-" * 20)
            for r in u['missing_tags']:
                report.append(f"  • {r['arn'].split(':')[-1]}")
                report.append(f"    Missing: {', '.join(r['missing'])}")
            report.append("")

        if u['untagged']:
            report.append("❌ COMPLETELY UNTAGGED")
            report.append("-" * 20)
            for arn in u['untagged']:
                report.append(f"  • {arn.split(':')[-1]}")
            report.append("")

    report.append("Next audit: 1 week from now")

    message = "\n".join(report)
    print(message)

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f"Sandbox Tag Audit — {datetime.utcnow().strftime('%Y-%m-%d')}",
        Message=message
    )

    return {
        'status': 'complete',
        'fully_tagged': all_fully_tagged,
        'missing_tags': all_missing,
        'untagged': all_untagged
    }
