import json, boto3

s3_client = boto3.client('s3')
PROCESSED_BUCKET = 'doc-processing-demo-processed-848747536965'

def lambda_handler(event, context):
    try:
        doc_id = event['queryStringParameters']['documentId']
        response = s3_client.list_objects_v2(Bucket=PROCESSED_BUCKET,
                                              Prefix=f"processed/{doc_id}")
        if 'Contents' not in response or len(response['Contents']) == 0:
            return {'statusCode': 404, 'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'error': 'Results not found'})}
        result_object = s3_client.get_object(Bucket=PROCESSED_BUCKET,
                                              Key=response['Contents'][0]['Key'])
        results = json.loads(result_object['Body'].read().decode('utf-8'))
        return {'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Headers': 'Content-Type',
                            'Access-Control-Allow-Methods': 'GET, OPTIONS'},
                'body': json.dumps(results)}
    except Exception as e:
        return {'statusCode': 500, 'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': str(e)})}