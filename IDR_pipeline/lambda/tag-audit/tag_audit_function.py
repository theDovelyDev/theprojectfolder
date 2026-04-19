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

    paginator = tagging.get_paginator('get_resources')
    all_resources = []

    for page in paginator.paginate():
        all_resources.extend(page['ResourceTagMappingList'])

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