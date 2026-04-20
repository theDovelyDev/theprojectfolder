import boto3
import os
from datetime import datetime

ecs = boto3.client('ecs')
sns = boto3.client('sns')

CLUSTER = os.environ['ECS_CLUSTER']
SERVICE = os.environ['ECS_SERVICE']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    print(f"Auto-stop triggered at {datetime.utcnow()}")
    print(f"Trigger: {event.get('source', 'unknown')}")

    # Set desired count to 0
    response = ecs.update_service(
        cluster=CLUSTER,
        service=SERVICE,
        desiredCount=0
    )

    status = response['service']['desiredCount']
    print(f"Service desired count set to: {status}")

    # Notify via SNS
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f"CARA Auto-Stop Triggered — {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC",
        Message=(
            f"CARA Fargate service has been automatically stopped.\n\n"
            f"Reason: CloudWatch alarm triggered (idle CPU or 2-hour runtime limit)\n"
            f"Cluster: {CLUSTER}\n"
            f"Service: {SERVICE}\n"
            f"Desired count set to: 0\n\n"
            f"To restart CARA, set desired count back to 1 in ECS console or run:\n"
            f"aws ecs update-service --cluster {CLUSTER} --service {SERVICE} --desired-count 1"
        )
    )

    return {
        'status': 'stopped',
        'desired_count': status,
        'timestamp': datetime.utcnow().isoformat()
    }