import boto3
import os
from datetime import datetime

sns = boto3.client('sns')
tagging = boto3.client('resourcegroupstaggingapi')

SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

REQUIRED_TAGS = ['Project', 'CostCenter', 'Environment', 'CreatedDate', 'ManagedBy']

KNOWN_PROJECTS = [
    'doc-processing-pipeline',
    'budget-research-agent',
]

def lambda_handler(event, context):
    print("Starting tag audit...")

    paginator = tagging.get_paginator('get_resources')
    all_resources = []

    for page in paginator.paginate():
        all_resources.extend(page['ResourceTagMappingList'])

    print(f"Total resources found: {len(all_resources)}")

    # Bucket resources by project
    buckets = {project: [] for project in KNOWN_PROJECTS}
    buckets['untagged_or_unknown'] = []

    for resource in all_resources:
        tags = {t['Key']: t['Value'] for t in resource.get('Tags', [])}
        project = tags.get('Project', None)

        missing = [tag for tag in REQUIRED_TAGS if tag not in tags]

        entry = {
            'arn': resource['ResourceARN'],
            'tags': tags,
            'missing': missing,
            'compliant': len(missing) == 0
        }

        if project in buckets:
            buckets[project].append(entry)
        else:
            buckets['untagged_or_unknown'].append(entry)

    # Build report
    total = len(all_resources)
    compliant = sum(1 for r in all_resources
                    if all(t['Key'] in [tag['Key'] for tag in r.get('Tags', [])]
                           for t in [{'Key': k} for k in REQUIRED_TAGS]))

    report = []
    report.append("AWS TAG COMPLIANCE AUDIT REPORT")
    report.append("=" * 40)
    report.append(f"Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    report.append("")
    report.append("SUMMARY")
    report.append("-" * 20)
    report.append(f"Total Resources : {total}")
    report.append(f"Compliant       : {sum(1 for r in all_resources if all(tag in {t['Key']: t['Value'] for t in r.get('Tags', [])} for tag in REQUIRED_TAGS))}")
    report.append(f"Non-Compliant   : {total - sum(1 for r in all_resources if all(tag in {t['Key']: t['Value'] for t in r.get('Tags', [])} for tag in REQUIRED_TAGS))}")
    report.append(f"Required Tags   : {', '.join(REQUIRED_TAGS)}")
    report.append("")

    for project in KNOWN_PROJECTS:
        resources = buckets[project]
        if not resources:
            continue

        non_compliant = [r for r in resources if not r['compliant']]
        status = "✅ COMPLIANT" if not non_compliant else f"⚠️  {len(non_compliant)} NON-COMPLIANT"

        report.append(f"PROJECT: {project.upper()}")
        report.append("-" * 20)
        report.append(f"Resources : {len(resources)}")
        report.append(f"Status    : {status}")

        if non_compliant:
            report.append("Non-compliant resources:")
            for r in non_compliant:
                short_arn = r['arn'].split(':')[-1]
                report.append(f"  - {short_arn}")
                report.append(f"    Missing: {', '.join(r['missing'])}")
        report.append("")

    # Catch anything unrecognized
    unknown = buckets['untagged_or_unknown']
    if unknown:
        report.append("UNTAGGED / UNKNOWN PROJECT")
        report.append("-" * 20)
        report.append(f"Resources : {len(unknown)}")
        for r in unknown:
            short_arn = r['arn'].split(':')[-1]
            report.append(f"  - {short_arn}")
            if r['missing']:
                report.append(f"    Missing: {', '.join(r['missing'])}")
        report.append("")

    report.append("Next audit: 1 week from now")

    message = "\n".join(report)
    print(message)

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f"AWS Tag Audit Report — {datetime.utcnow().strftime('%Y-%m-%d')}",
        Message=message
    )

    return {'status': 'complete', 'total_resources': total}