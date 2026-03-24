import json
import boto3
import csv
import io
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'DocFlowRecords'

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def lambda_handler(event, context):
    try:
        path = event.get('path', '')
        if path.endswith('/export'):
            return handle_export()
        else:
            return handle_records()
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

def handle_records():
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    records = response.get('Items', [])
    records.sort(key=lambda x: x.get('processedAt', ''), reverse=True)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET, OPTIONS'
        },
        'body': json.dumps({'count': len(records), 'records': records}, cls=DecimalEncoder)
    }

def handle_export():
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    records = response.get('Items', [])
    records.sort(key=lambda x: x.get('processedAt', ''), reverse=True)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'documentId', 'documentName', 'processedAt', 'status',
        'extractionConfidence', 'pageCount', 'sentiment', 'entities', 'keyPhrases'
    ])
    for r in records:
        writer.writerow([
            r.get('documentId', ''),
            r.get('documentName', ''),
            r.get('processedAt', ''),
            r.get('status', ''),
            r.get('extractionConfidence', ''),
            r.get('pageCount', ''),
            r.get('sentiment', ''),
            ', '.join(r.get('entities', [])),
            ', '.join(r.get('keyPhrases', []))
        ])

    filename = f"docflow-export-{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv"
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/csv',
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Access-Control-Allow-Origin': '*'
        },
        'body': output.getvalue()
    }