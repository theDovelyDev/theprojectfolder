# Tagging Dictionary — DocFlow IDP Pipeline

## Project 1 Tag Values

| Tag Key       | Value                      |
|---------------|---------------------------|
| `Project`     | `doc-processing-pipeline`  |
| `CostCenter`  | `Project1`                 |
| `Environment` | `dev`                      |
| `ManagedBy`   | `manual`                   |
| `Component`   | varies (see below)         |

## Component Values by Resource

| Resource | Component |
|----------|-----------|
| S3 upload bucket | `storage` |
| S3 processed bucket | `storage` |
| S3 frontend bucket | `storage` |
| Lambda — DocumentProcessor | `processing` |
| Lambda — APIUploadHandler | `api` |
| Lambda — APIResultsHandler | `api` |
| Lambda — APIRecordsHandler | `api` |
| Lambda — TagAuditFunction | `monitoring` |
| API Gateway | `api` |
| DynamoDB — DocFlowRecords | `processing` |
| SNS — DocFlowNotifications | `monitoring` |
| SNS — TagAuditNotifications | `monitoring` |
| EventBridge — TagAuditWeeklySchedule | `monitoring` |
| CloudWatch logs | `monitoring` |
| IAM — TagAuditLambdaRole | `monitoring` |
| IAM roles/policies    | `iam`            |