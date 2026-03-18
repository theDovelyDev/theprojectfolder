#!/bin/bash

# upload-document.sh - Upload a single document to S3 for processing
# Usage: ./upload-document.sh <filename>
# Example: ./upload-document.sh invoice_001_DOC-2025-2288.pdf

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TEST_DOCS_DIR="./test-documents/phase3"
UPLOAD_LOG="./phase3-results/upload_log.txt"

# Check if environment variables are loaded
if [ -z "$PROJECT_NAME" ] || [ -z "$ACCOUNT_ID" ] || [ -z "$REGION" ]; then
    echo -e "${RED}❌ Error: Environment variables not loaded${NC}"
    echo "Please run: source setup.sh"
    exit 1
fi

# Check if filename provided
if [ $# -eq 0 ]; then
    echo -e "${RED}❌ Error: No filename provided${NC}"
    echo ""
    echo "Usage: ./upload-document.sh <filename>"
    echo ""
    echo "Available test documents:"
    ls -1 "$TEST_DOCS_DIR" | grep .pdf || echo "No documents found in $TEST_DOCS_DIR"
    exit 1
fi

FILENAME="$1"
FILE_PATH="$TEST_DOCS_DIR/$FILENAME"

# Check if file exists
if [ ! -f "$FILE_PATH" ]; then
    echo -e "${RED}❌ Error: File not found: $FILE_PATH${NC}"
    echo ""
    echo "Available test documents:"
    ls -1 "$TEST_DOCS_DIR" | grep .pdf || echo "No documents found in $TEST_DOCS_DIR"
    exit 1
fi

# S3 bucket and key
UPLOAD_BUCKET="${PROJECT_NAME}-uploads-${ACCOUNT_ID}"
TIMESTAMP=$(date +%s)
S3_KEY="uploads/phase3/${TIMESTAMP}_${FILENAME}"

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}📤 DOCUMENT UPLOAD${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo "Document: $FILENAME"
echo "File size: $(stat -f%z "$FILE_PATH" 2>/dev/null || stat -c%s "$FILE_PATH") bytes"
echo "S3 Bucket: $UPLOAD_BUCKET"
echo "S3 Key: $S3_KEY"
echo ""

# Record start time
START_TIME=$(date +%s)
START_DATETIME=$(date '+%Y-%m-%d %H:%M:%S')

# Upload to S3
echo -e "${YELLOW}⏳ Uploading...${NC}"
if aws s3 cp "$FILE_PATH" "s3://${UPLOAD_BUCKET}/${S3_KEY}" --region "$REGION"; then
    END_TIME=$(date +%s)
    UPLOAD_DURATION=$((END_TIME - START_TIME))
    
    echo ""
    echo -e "${GREEN}✅ Upload successful!${NC}"
    echo ""
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}📊 UPLOAD DETAILS${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo "Upload time: ${UPLOAD_DURATION}s"
    echo "S3 URI: s3://${UPLOAD_BUCKET}/${S3_KEY}"
    echo "Start time: $START_DATETIME"
    echo ""
    
    # Log the upload
    mkdir -p "$(dirname "$UPLOAD_LOG")"
    echo "${START_DATETIME},${FILENAME},${S3_KEY},${UPLOAD_DURATION}s" >> "$UPLOAD_LOG"
    
    echo -e "${YELLOW}⏳ Lambda processing triggered...${NC}"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "1. Wait 30-60 seconds for Lambda to process"
    echo "2. Check results with: python scripts/check-results.py $FILENAME"
    echo ""
    echo -e "${BLUE}======================================${NC}"
else
    echo ""
    echo -e "${RED}❌ Upload failed!${NC}"
    echo "Check your AWS credentials and bucket permissions."
    exit 1
fi
