#!/usr/bin/env python3
"""
Check processing results for a test document.

This script:
1. Checks if processing is complete
2. Downloads the JSON results from S3
3. Parses and displays key metrics
4. Calculates performance statistics

Usage: python check-results.py <filename>
Example: python check-results.py invoice_001_DOC-2025-2288.pdf
"""

import sys
import json
import os
import time
from pathlib import Path
from datetime import datetime

try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    print("❌ Error: boto3 not installed")
    print("Install with: pip install boto3 --break-system-packages")
    sys.exit(1)

# Configuration
PROJECT_NAME = os.environ.get('PROJECT_NAME', 'doc-processing-demo')
ACCOUNT_ID = os.environ.get('ACCOUNT_ID', '')
REGION = os.environ.get('REGION', 'us-east-1')
RESULTS_DIR = Path('./phase3-results')

# Check environment
if not ACCOUNT_ID:
    print("❌ Error: ACCOUNT_ID environment variable not set")
    print("Please run: source setup.sh")
    sys.exit(1)

PROCESSED_BUCKET = f"{PROJECT_NAME}-processed-{ACCOUNT_ID}"

# AWS clients
s3 = boto3.client('s3', region_name=REGION)

def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(text)
    print("="*70)

def check_processing_status(filename):
    """Check if the document has been processed."""
    # Results are saved as: processed/<timestamp>_<filename>.json
    prefix = "processed/"
    
    try:
        response = s3.list_objects_v2(
            Bucket=PROCESSED_BUCKET,
            Prefix=prefix
        )
        
        if 'Contents' not in response:
            return None, "No processed documents found"
        
        # Find matching results (look for filename in the key)
        base_filename = filename.replace('.pdf', '')
        matching_results = []
        
        for obj in response['Contents']:
            key = obj['Key']
            if base_filename in key and key.endswith('.json'):
                matching_results.append({
                    'key': key,
                    'last_modified': obj['LastModified'],
                    'size': obj['Size']
                })
        
        if not matching_results:
            return None, f"No results found for {filename}"
        
        # Get the most recent result
        latest = sorted(matching_results, key=lambda x: x['last_modified'], reverse=True)[0]
        return latest, None
        
    except ClientError as e:
        return None, f"Error checking S3: {e}"

def download_results(s3_key):
    """Download and parse the results JSON."""
    try:
        response = s3.get_object(Bucket=PROCESSED_BUCKET, Key=s3_key)
        results_json = response['Body'].read().decode('utf-8')
        return json.loads(results_json), None
    except ClientError as e:
        return None, f"Error downloading results: {e}"
    except json.JSONDecodeError as e:
        return None, f"Error parsing JSON: {e}"

def calculate_metrics(results):
    """Calculate key metrics from results."""
    metrics = {
        'document_name': results.get('document_name', 'Unknown'),
        'processed_at': results.get('processed_at', 'Unknown'),
        'status': results.get('status', 'Unknown')
    }
    
    # Extraction metrics
    extraction = results.get('extraction', {})
    metrics['full_text_length'] = len(extraction.get('full_text', ''))
    metrics['key_value_pairs'] = len(extraction.get('key_value_pairs', {}))
    metrics['page_count'] = extraction.get('page_count', 0)
    
    # Analysis metrics
    analysis = results.get('analysis', {})
    entities = analysis.get('entities', [])
    metrics['entities_found'] = len(entities)
    
    if entities:
        avg_confidence = sum(e.get('score', 0) for e in entities) / len(entities)
        metrics['avg_entity_confidence'] = round(avg_confidence * 100, 1)
    else:
        metrics['avg_entity_confidence'] = 0
    
    # Entity breakdown
    entity_types = {}
    for entity in entities:
        entity_type = entity.get('type', 'Unknown')
        entity_types[entity_type] = entity_types.get(entity_type, 0) + 1
    metrics['entity_types'] = entity_types
    
    # Sentiment
    sentiment = analysis.get('sentiment', {})
    metrics['sentiment'] = sentiment.get('overall', 'Unknown')
    sentiment_scores = sentiment.get('scores', {})
    if sentiment_scores:
        metrics['sentiment_confidence'] = round(
            sentiment_scores.get(sentiment.get('overall', '').lower(), 0) * 100, 1
        )
    else:
        metrics['sentiment_confidence'] = 0
    
    # Key phrases
    key_phrases = analysis.get('key_phrases', [])
    metrics['key_phrases_count'] = len(key_phrases)
    metrics['top_key_phrases'] = [p.get('text', '') for p in key_phrases[:5]]
    
    return metrics

def display_metrics(metrics):
    """Display metrics in a readable format."""
    print_header("📊 PROCESSING RESULTS")
    
    print(f"\nDocument: {metrics['document_name']}")
    print(f"Processed: {metrics['processed_at']}")
    print(f"Status: {metrics['status']}")
    
    print_header("📄 TEXT EXTRACTION METRICS")
    print(f"Text Length: {metrics['full_text_length']:,} characters")
    print(f"Key-Value Pairs: {metrics['key_value_pairs']}")
    print(f"Page Count: {metrics['page_count']}")
    
    print_header("🏷️  ENTITY DETECTION")
    print(f"Total Entities: {metrics['entities_found']}")
    print(f"Average Confidence: {metrics['avg_entity_confidence']}%")
    
    if metrics['entity_types']:
        print("\nEntity Types Detected:")
        for entity_type, count in sorted(metrics['entity_types'].items()):
            print(f"  • {entity_type}: {count}")
    
    print_header("😊 SENTIMENT ANALYSIS")
    print(f"Sentiment: {metrics['sentiment']}")
    print(f"Confidence: {metrics['sentiment_confidence']}%")
    
    print_header("💡 KEY PHRASES")
    print(f"Total Key Phrases: {metrics['key_phrases_count']}")
    if metrics['top_key_phrases']:
        print("\nTop 5 Key Phrases:")
        for i, phrase in enumerate(metrics['top_key_phrases'], 1):
            print(f"  {i}. {phrase}")
    
    print("\n" + "="*70)

def estimate_cost(metrics):
    """Estimate the processing cost."""
    pages = metrics['page_count']
    
    # Textract: $1.50 per 1,000 pages (after free tier)
    textract_cost = (pages / 1000) * 1.50
    
    # Comprehend: $0.0001 per unit (100 characters)
    # Entity detection, sentiment, key phrases = 3 features
    text_units = metrics['full_text_length'] / 100
    comprehend_cost = (text_units / 10000) * 1.00 * 3  # 3 features
    
    # Lambda: ~$0.0000002 per invocation (negligible)
    lambda_cost = 0.0000002
    
    total_cost = textract_cost + comprehend_cost + lambda_cost
    
    print_header("💰 ESTIMATED COST")
    print(f"Textract: ${textract_cost:.6f}")
    print(f"Comprehend: ${comprehend_cost:.6f}")
    print(f"Lambda: ${lambda_cost:.6f}")
    print(f"Total: ${total_cost:.6f}")
    print("\n(Note: First 1,000 Textract pages/month are free for 3 months)")
    print("=" * 70 + "\n")

def save_results_locally(filename, results, metrics):
    """Save results to local directory for offline analysis."""
    RESULTS_DIR.mkdir(exist_ok=True)
    
    # Save full JSON
    json_file = RESULTS_DIR / f"{filename.replace('.pdf', '')}_results.json"
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Save metrics summary
    metrics_file = RESULTS_DIR / f"{filename.replace('.pdf', '')}_metrics.json"
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"📁 Results saved to: {RESULTS_DIR}")
    print(f"  • Full results: {json_file.name}")
    print(f"  • Metrics: {metrics_file.name}\n")

def main():
    if len(sys.argv) < 2:
        print("❌ Error: No filename provided")
        print("\nUsage: python check-results.py <filename>")
        print("Example: python check-results.py invoice_001_DOC-2025-2288.pdf")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    print_header(f"🔍 CHECKING RESULTS FOR: {filename}")
    print("\n⏳ Searching for processed results...\n")
    
    # Check processing status
    result_info, error = check_processing_status(filename)
    
    if error:
        print(f"❌ {error}")
        print("\nPossible reasons:")
        print("  • Document hasn't been uploaded yet")
        print("  • Lambda is still processing (wait 30-60 seconds)")
        print("  • Processing failed (check CloudWatch logs)")
        sys.exit(1)
    
    print(f"✅ Found results!")
    print(f"   S3 Key: {result_info['key']}")
    print(f"   Last Modified: {result_info['last_modified']}")
    print(f"   Size: {result_info['size']:,} bytes")
    
    # Download results
    print("\n⏳ Downloading and parsing results...\n")
    results, error = download_results(result_info['key'])
    
    if error:
        print(f"❌ {error}")
        sys.exit(1)
    
    # Calculate and display metrics
    metrics = calculate_metrics(results)
    display_metrics(metrics)
    estimate_cost(metrics)
    
    # Save locally
    save_results_locally(filename, results, metrics)
    
    print("✅ Analysis complete!")

if __name__ == '__main__':
    main()
