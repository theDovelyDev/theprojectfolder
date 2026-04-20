# Tagging Dictionary — Budget Research Agent

## Project 2 Tag Values

| Tag Key       | Value                    |
|---------------|--------------------------|
| `Project`     | `budget-research-agent`  |
| `CostCenter`  | `Project2`               |
| `Environment` | `dev`                    |
| `Owner`       | `theDovelyDev`           |
| `CreatedDate` | `2026-04-07`             |
| `ManagedBy`   | `manual`                 |
| `Component`   | varies (see below)       |

## Component Values by Resource

| Resource              | Component Value  |
|-----------------------|------------------|
| ECS/Fargate service `cara-service`  | `container`      |
| ECR repository `cara` | `container`      |
| API Gateway           | `api`            |
| CloudWatch logs       | `monitoring`     |
| IAM role `CaraAutoStopLambdaRole` | `monitoring` |
| IAM user `budget-research-agent-dev` | `iam` |
| Secrets Manager       | `config`         |
| ECS cluster `cara-cluster` | `container` |
| Fargate task definition `cara-task` | `container` |
| Security group `cara-sg` | `container` |
| Lambda `CaraAutoStopFunction` | `monitoring` |
| SNS `CaraAutoStopNotifications` | `monitoring` |
| CloudWatch alarm `CARA-Idle-CPU-AutoStop` | `monitoring` |
| CloudWatch alarm `CARA-2Hour-AutoStop` | `monitoring` |
