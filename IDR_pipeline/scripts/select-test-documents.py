#!/usr/bin/env python3
"""
Select 15 diverse test documents from the 150 mock documents for Phase 3 testing.

This script:
1. Analyzes all 150 documents
2. Selects a diverse subset based on:
   - Document type (invoices vs receipts)
   - File size (proxy for complexity)
   - Date ranges (from filenames)
3. Copies selected documents to test-documents/phase3/
4. Creates a manifest file with document details
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

# Paths
SOURCE_DIR = Path('./test-documents/mock_documents')
DEST_DIR = Path('./test-documents/phase3')
MANIFEST_FILE = DEST_DIR / 'test_manifest.json'

def analyze_documents():
    """Analyze all documents and gather metadata."""
    documents = []
    
    for pdf_file in sorted(SOURCE_DIR.glob('*.pdf')):
        file_stat = pdf_file.stat()
        filename = pdf_file.name
        
        # Parse filename: invoice_001_DOC-2025-2288.pdf or receipt_001_RCP-103406.pdf
        parts = filename.replace('.pdf', '').split('_')
        doc_type = parts[0]  # 'invoice' or 'receipt'
        doc_number = parts[1]  # '001', '002', etc.
        doc_id = '_'.join(parts[2:])  # 'DOC-2025-2288' or 'RCP-103406'
        
        documents.append({
            'filename': filename,
            'type': doc_type,
            'number': int(doc_number),
            'doc_id': doc_id,
            'size_bytes': file_stat.st_size,
            'path': str(pdf_file)
        })
    
    return documents

def select_diverse_subset(documents):
    """Select 15 diverse documents for testing."""
    invoices = [d for d in documents if d['type'] == 'invoice']
    receipts = [d for d in documents if d['type'] == 'receipt']
    
    # Sort by size to get variety
    invoices_small = sorted(invoices, key=lambda x: x['size_bytes'])[:3]
    invoices_medium = sorted(invoices, key=lambda x: x['size_bytes'])[48:51]  # Middle range
    invoices_large = sorted(invoices, key=lambda x: x['size_bytes'])[-3:]
    
    receipts_small = sorted(receipts, key=lambda x: x['size_bytes'])[:2]
    receipts_medium = sorted(receipts, key=lambda x: x['size_bytes'])[24:26]
    receipts_large = sorted(receipts, key=lambda x: x['size_bytes'])[-2:]
    
    selected = (
        invoices_small + invoices_medium + invoices_large +
        receipts_small + receipts_medium + receipts_large
    )
    
    return selected

def copy_documents(selected_docs):
    """Copy selected documents to test directory."""
    # Clear destination directory
    if DEST_DIR.exists():
        shutil.rmtree(DEST_DIR)
    DEST_DIR.mkdir(parents=True)
    
    copied = []
    for doc in selected_docs:
        src = Path(doc['path'])
        dst = DEST_DIR / doc['filename']
        shutil.copy2(src, dst)
        copied.append({
            'filename': doc['filename'],
            'type': doc['type'],
            'doc_id': doc['doc_id'],
            'size_bytes': doc['size_bytes'],
            'category': categorize_document(doc)
        })
        print(f"âœ… Copied: {doc['filename']} ({doc['size_bytes']:,} bytes)")
    
    return copied

def categorize_document(doc):
    """Categorize document based on size."""
    if doc['size_bytes'] < 2600:
        return 'simple'
    elif doc['size_bytes'] < 3200:
        return 'medium'
    else:
        return 'complex'

def create_manifest(selected_docs):
    """Create a manifest file with test document details."""
    manifest = {
        'created': datetime.now().isoformat(),
        'total_documents': len(selected_docs),
        'document_types': {
            'invoices': len([d for d in selected_docs if d['type'] == 'invoice']),
            'receipts': len([d for d in selected_docs if d['type'] == 'receipt'])
        },
        'documents': selected_docs
    }
    
    with open(MANIFEST_FILE, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n📄 Manifest created: {MANIFEST_FILE}")
    return manifest

def print_summary(manifest):
    """Print a summary of selected documents."""
    print("\n" + "="*70)
    print("PHASE 3 TEST DOCUMENT SELECTION SUMMARY")
    print("="*70)
    print(f"Total Documents Selected: {manifest['total_documents']}")
    print(f"  • Invoices: {manifest['document_types']['invoices']}")
    print(f"  • Receipts: {manifest['document_types']['receipts']}")
    print(f"\nDocuments saved to: {DEST_DIR}")
    print("\nBreakdown by Category:")
    
    categories = {}
    for doc in manifest['documents']:
        cat = doc['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in sorted(categories.items()):
        print(f"  • {cat.capitalize()}: {count}")
    
    print("\n" + "="*70)
    print("\nNext Steps:")
    print("1. Review the selected documents in: test-documents/phase3/")
    print("2. Use upload-document.sh to upload documents to S3")
    print("3. Use check-results.py to verify processing")
    print("4. Track results in Phase3_Test_Results_Template.md")
    print("="*70 + "\n")

def main():
    print("🔍 Analyzing 150 mock documents...")
    all_docs = analyze_documents()
    print(f"✅ Found {len(all_docs)} documents")
    print(f"   • Invoices: {len([d for d in all_docs if d['type'] == 'invoice'])}")
    print(f"   • Receipts: {len([d for d in all_docs if d['type'] == 'receipt'])}")
    
    print("\n📋 Selecting diverse subset of 15 documents...")
    selected = select_diverse_subset(all_docs)
    
    print(f"\n📁 Copying {len(selected)} documents to test directory...")
    copied_docs = copy_documents(selected)
    
    print("\n📝 Creating test manifest...")
    manifest = create_manifest(copied_docs)
    
    print_summary(manifest)

if __name__ == '__main__':
    main()
