import json
import boto3
import os
from datetime import datetime

# Set allowed CORS origin from env (fallback to production domain)
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "https://www.theprojectfolder.com")

def lambda_handler(event, context):
    # Initialize DynamoDB inside the function
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ.get('DYNAMODB_TABLE', 'VisitorCountTable')
    table = dynamodb.Table('VisitorCountTable')
    
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

    cors_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    # Handle CORS preflight
    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps({"message": "CORS preflight allowed"})
        }

    if method == "POST":
        try:
            response = table.update_item(
                Key={"visitor_count_id": "global"},
                UpdateExpression="SET visitorCount = if_not_exists(visitorCount, :start) + :inc, #ts = :ts",
                ExpressionAttributeValues={
                    ":inc": 1,
                    ":start": 0,
                    ":ts": str(datetime.utcnow())
                },
                ExpressionAttributeNames={
                    "#ts": "timestamp"
                },
                ReturnValues="UPDATED_NEW"
            )
            new_count = response["Attributes"]["visitorCount"]
            print(f"[POST] Visitor count incremented to {new_count}")

            return {
                "statusCode": 200,
                "headers": cors_headers,
                "body": json.dumps({"visitorCount": int(new_count)})
            }

        except Exception as e:
            print(f"[ERROR] POST failed: {str(e)}")
            return {
                "statusCode": 500,
                "headers": cors_headers,
                "body": json.dumps({"error": "Could not update visitor count"})
            }

    elif method == "GET":
        try:
            response = table.get_item(Key={"visitor_count_id": "global"})
            item = response.get("Item", {})
            count = item.get("visitorCount", 0)
            print(f"[GET] Current visitor count: {count}")

            return {
                "statusCode": 200,
                "headers": cors_headers,
                "body": json.dumps({"visitorCount": int(count)})
            }

        except Exception as e:
            print(f"[ERROR] GET failed: {str(e)}")
            return {
                "statusCode": 500,
                "headers": cors_headers,
                "body": json.dumps({"error": "Could not retrieve visitor count"})
            }

    else:
        print(f"[ERROR] Method {method} not allowed")
        return {
            "statusCode": 405,
            "headers": cors_headers,
            "body": json.dumps({"error": "Method Not Allowed"})
        }