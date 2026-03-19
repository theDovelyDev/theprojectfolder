import json, boto3, base64, uuid
from datetime import datetime

s3_client = boto3.client('s3')
UPLOAD_BUCKET = 'doc-processing-demo-uploads-848747536965'

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        file_content = base64.b64decode(body['fileContent'])
        file_name = body['fileName']
        doc_id = str(uuid.uuid4())
        s3_key = f"uploads/{doc_id}_{file_name}"
        s3_client.put_object(Bucket=UPLOAD_BUCKET, Key=s3_key, Body=file_content,
                             ContentType=body.get('contentType', 'application/pdf'))
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Methods': 'POST, OPTIONS'},
            'body': json.dumps({'message': 'File uploaded successfully',
                                'documentId': doc_id, 's3Key': s3_key})
        }
    except Exception as e:
        return {'statusCode': 500, 'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': str(e)})}