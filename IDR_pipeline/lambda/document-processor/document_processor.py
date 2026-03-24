import json
import boto3
import os
import io
import uuid
from datetime import datetime

# PyPDF2 is available via Lambda layer
import PyPDF2

s3_client = boto3.client('s3')
textract_client = boto3.client('textract')
comprehend_client = boto3.client('comprehend')
dynamodb = boto3.resource('dynamodb')
sns_client = boto3.client('sns')

PROCESSED_BUCKET = os.environ.get('PROCESSED_BUCKET', '')
DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE', 'DocFlowRecords')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', '')


def lambda_handler(event, context):
    """
    Main handler for document processing
    Triggered by S3 upload event
    """
    try:
        # Get bucket and key from S3 event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        print(f"Processing document: {key} from bucket: {bucket}")

        # Step 1: Preprocess document (Phase 4)
        processed_bucket, processed_key = preprocess_document(bucket, key)

        # Step 2: Extract text using Textract
        extracted_data = extract_text_from_document(processed_bucket, processed_key)

        # Step 3: Analyze text using Comprehend
        analysis_results = analyze_text(extracted_data['full_text'])

        # Step 4: Combine results
        # Extract documentId from S3 key — format: uploads/{documentId}_{fileName}
        key_filename = key.split('/')[-1]
        doc_id = key_filename.split('_')[0]
        final_result = {
            'documentId': doc_id,
            'document_name': key,
            'processed_at': datetime.now().isoformat(),
            'extraction': extracted_data,
            'analysis': analysis_results,
            'status': 'success'
        }

        # Step 5: Save results to processed bucket
        result_key = f"processed/{key.split('/')[-1]}.json"
        s3_client.put_object(
            Bucket=PROCESSED_BUCKET,
            Key=result_key,
            Body=json.dumps(final_result, indent=2),
            ContentType='application/json'
        )

        print(f"Successfully processed {key}")
        print(f"Results saved to: {result_key}")

        # Step 5a: Write record to DynamoDB (Phase 10)
        write_to_dynamodb(doc_id, key, extracted_data, analysis_results)

        # Step 5b: Send SNS notification (Phase 10)
        send_notification(key, extracted_data)

        return {
            'statusCode': 200,
            'body': json.dumps(final_result)
        }

    except Exception as e:
        print(f"Error processing document: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


# -------------------------------------------------------
# NEW IN PHASE 10: DynamoDB Write
# -------------------------------------------------------

def write_to_dynamodb(doc_id, key, extracted_data, analysis_results):
    """
    Write extracted record to DynamoDB after successful processing.
    Stores the full extraction and analysis results in a generic schema
    so any document type is supported.
    """
    try:
        table = dynamodb.Table(DYNAMODB_TABLE)

        # Pull top 3 key-value pairs for quick reference
        key_value_pairs = extracted_data.get('key_value_pairs', {})
        top_pairs = dict(list(key_value_pairs.items())[:3])

        table.put_item(Item={
            'documentId': doc_id,
            'documentName': key.split('/')[-1],
            'processedAt': datetime.now().isoformat(),
            'status': 'success',
            'extractionConfidence': str(extracted_data.get('extraction_confidence', 0)),
            'pageCount': extracted_data.get('page_count', 0),
            'fullText': extracted_data.get('full_text', ''),
            'keyValuePairs': key_value_pairs,
            'topKeyValues': top_pairs,
            'entities': [e['text'] for e in analysis_results.get('entities', [])[:5]],
            'sentiment': analysis_results.get('sentiment', {}).get('overall', 'NEUTRAL'),
            'keyPhrases': [p['text'] for p in analysis_results.get('key_phrases', [])[:5]]
        })

        print(f"Record written to DynamoDB: {doc_id}")

    except Exception as e:
        # Don't fail the whole pipeline if DynamoDB write fails
        print(f"DynamoDB write error: {str(e)}")


# -------------------------------------------------------
# NEW IN PHASE 10: SNS Notification
# -------------------------------------------------------

def send_notification(key, extracted_data):
    """
    Send SNS email notification after successful processing.
    Only fires if SNS_TOPIC_ARN is configured.
    """
    if not SNS_TOPIC_ARN:
        print("SNS_TOPIC_ARN not set, skipping notification")
        return

    try:
        doc_name = key.split('/')[-1]
        confidence = extracted_data.get('extraction_confidence', 0)
        key_value_pairs = extracted_data.get('key_value_pairs', {})
        top_pairs = list(key_value_pairs.items())[:3]

        top_pairs_text = '\n'.join([f"  {k}: {v}" for k, v in top_pairs]) if top_pairs else '  No key-value pairs extracted'

        message = f"""DocFlow — Document Processed Successfully

Document: {doc_name}
Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
Confidence: {confidence}%

Top extracted fields:
{top_pairs_text}
"""

        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"DocFlow — {doc_name} processed",
            Message=message
        )

        print(f"SNS notification sent for {doc_name}")

    except Exception as e:
        # Don't fail the pipeline if notification fails
        print(f"SNS notification error: {str(e)}")


# -------------------------------------------------------
# NEW IN PHASE 4: PDF Preprocessing
# -------------------------------------------------------

def preprocess_document(bucket, key):
    """
    Triage and normalize documents before sending to Textract.

    Why this exists:
    Textract is strict about PDF encoding. PDFs generated by older software,
    certain printers, or non-standard exporters can fail with
    UnsupportedDocumentException even though the file opens fine in Acrobat.
    PyPDF2 reads and rewrites the PDF, normalizing its structure so Textract
    can process it reliably.

    Returns the bucket and key to use for Textract — either the original
    (for non-PDFs or already-clean PDFs) or a normalized version.
    """

    if not key.lower().endswith('.pdf'):
        print(f"Non-PDF file detected ({key}), skipping preprocessing")
        return bucket, key

    print(f"PDF detected, starting preprocessing for {key}")

    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        pdf_bytes = response['Body'].read()

        normalized_bytes = validate_and_normalize_pdf(pdf_bytes, key)

        if normalized_bytes is None:
            print(f"Normalization failed for {key}, falling back to original")
            return bucket, key

        normalized_key = f"preprocessed/{key.split('/')[-1]}"
        s3_client.put_object(
            Bucket=bucket,
            Key=normalized_key,
            Body=normalized_bytes,
            ContentType='application/pdf'
        )

        print(f"Normalized PDF uploaded to: {normalized_key}")
        return bucket, normalized_key

    except Exception as e:
        print(f"Preprocessing error for {key}: {str(e)}, falling back to original")
        return bucket, key


def validate_and_normalize_pdf(pdf_bytes, key):
    """
    Inspect the PDF and rewrite it using PyPDF2.

    Three things this handles:
    1. Encrypted PDFs: Many PDFs have permissions encryption (can't print,
       can't copy) but no password. PyPDF2 can decrypt these with an empty
       string, making them accessible to Textract.

    2. Malformed structure: PDFs from older or non-standard software sometimes
       violate the PDF spec in subtle ways. Reading and rewriting with PyPDF2
       fixes most structural issues.

    3. Non-standard encoding: Some PDF generators use unusual character
       encoding. The rewrite normalizes this to standard encoding.

    Returns normalized PDF bytes, or None if normalization fails.
    """
    try:
        input_buffer = io.BytesIO(pdf_bytes)
        reader = PyPDF2.PdfReader(input_buffer)

        if reader.is_encrypted:
            print(f"Encrypted PDF detected: {key}, attempting decryption")
            decrypt_result = reader.decrypt('')
            if decrypt_result == 0:
                print(f"PDF {key} is password protected, cannot decrypt")
                return None
            print(f"PDF decrypted successfully: {key}")

        page_count = len(reader.pages)
        if page_count == 0:
            print(f"PDF {key} has no pages, skipping")
            return None

        print(f"PDF {key} has {page_count} page(s), normalizing...")

        writer = PyPDF2.PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        output_buffer = io.BytesIO()
        writer.write(output_buffer)
        output_buffer.seek(0)

        normalized_bytes = output_buffer.read()
        print(f"Normalization complete: {key} ({len(pdf_bytes)} → {len(normalized_bytes)} bytes)")

        return normalized_bytes

    except Exception as e:
        print(f"PDF normalization error for {key}: {str(e)}")
        return None


# -------------------------------------------------------
# UNCHANGED FROM PHASE 3 BELOW
# -------------------------------------------------------

def extract_text_from_document(bucket, key):
    """
    Extract text from document using AWS Textract
    """
    print(f"Starting Textract analysis on {key}")

    try:
        response = textract_client.analyze_document(
            Document={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            },
            FeatureTypes=['TABLES', 'FORMS']
        )

        full_text = []
        key_value_pairs = {}

        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                full_text.append(block['Text'])

            elif block['BlockType'] == 'KEY_VALUE_SET':
                if 'KEY' in block.get('EntityTypes', []):
                    key_text = extract_text_from_relationship(block, response['Blocks'])
                    value_text = extract_value_text(block, response['Blocks'])
                    if key_text and value_text:
                        key_value_pairs[key_text] = value_text

        return {
            'full_text': ' '.join(full_text),
            'key_value_pairs': key_value_pairs,
            'page_count': len(set(b.get('Page', 1) for b in response['Blocks'])),
            'extraction_confidence': calculate_average_confidence(response['Blocks'])
        }

    except Exception as e:
        print(f"Textract error: {str(e)}")
        return {
            'full_text': '',
            'key_value_pairs': {},
            'page_count': 0,
            'error': str(e)
        }


def extract_text_from_relationship(block, all_blocks):
    """Helper to extract text from relationships"""
    text = []
    if 'Relationships' in block:
        for relationship in block['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    child = next((b for b in all_blocks if b['Id'] == child_id), None)
                    if child and child['BlockType'] == 'WORD':
                        text.append(child['Text'])
    return ' '.join(text)


def extract_value_text(key_block, all_blocks):
    """Helper to extract value associated with key"""
    if 'Relationships' in key_block:
        for relationship in key_block['Relationships']:
            if relationship['Type'] == 'VALUE':
                for value_id in relationship['Ids']:
                    value_block = next((b for b in all_blocks if b['Id'] == value_id), None)
                    if value_block:
                        return extract_text_from_relationship(value_block, all_blocks)
    return None


def calculate_average_confidence(blocks):
    """Calculate average confidence score from Textract blocks"""
    confidences = [block.get('Confidence', 0) for block in blocks if 'Confidence' in block]
    return round(sum(confidences) / len(confidences), 2) if confidences else 0


def analyze_text(text):
    """
    Analyze text using AWS Comprehend
    """
    if not text or len(text.strip()) < 3:
        return {'error': 'Text too short for analysis'}

    text = text[:5000]
    results = {}

    try:
        entities_response = comprehend_client.detect_entities(
            Text=text,
            LanguageCode='en'
        )
        results['entities'] = [
            {
                'text': e['Text'],
                'type': e['Type'],
                'score': round(e['Score'], 2)
            }
            for e in entities_response['Entities']
        ]

        sentiment_response = comprehend_client.detect_sentiment(
            Text=text,
            LanguageCode='en'
        )
        results['sentiment'] = {
            'overall': sentiment_response['Sentiment'],
            'scores': {
                k: round(v, 2)
                for k, v in sentiment_response['SentimentScore'].items()
            }
        }

        phrases_response = comprehend_client.detect_key_phrases(
            Text=text,
            LanguageCode='en'
        )
        results['key_phrases'] = [
            {
                'text': p['Text'],
                'score': round(p['Score'], 2)
            }
            for p in phrases_response['KeyPhrases'][:10]
        ]

    except Exception as e:
        results['error'] = str(e)
        print(f"Comprehend error: {str(e)}")

    return results