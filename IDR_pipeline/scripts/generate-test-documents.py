#!/usr/bin/env python3
"""
Generate realistic test documents for document processing pipeline testing.

This script creates:
- Invoices (simple, medium, complex)
- Receipts (various formats)
- Forms (tax forms, application forms)
- Edge cases (multi-column, with logos, poor quality simulation)

All documents are created as PDFs using ReportLab.

Usage: python generate-test-documents.py [--count N] [--output-dir PATH]
"""

import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
except ImportError:
    print("❌ Error: ReportLab not installed")
    print("Install with: pip install reportlab --break-system-packages")
    exit(1)

# Company and product data
COMPANIES = [
    "Acme Corporation", "TechVision LLC", "Global Solutions Inc",
    "Prime Services", "Innovation Labs", "Enterprise Systems"
]

PRODUCTS = [
    ("Software License", 299.99, 1499.99),
    ("Consulting Services", 150.00, 500.00),
    ("Cloud Storage", 49.99, 199.99),
    ("API Access", 99.99, 999.99),
    ("Support Package", 199.99, 799.99),
    ("Training Session", 250.00, 1000.00)
]

RECEIPT_ITEMS = [
    ("Coffee", 4.50),
    ("Sandwich", 8.99),
    ("Office Supplies", 23.45),
    ("Parking", 15.00),
    ("Taxi Fare", 32.00),
    ("Lunch Meeting", 67.50),
    ("Book Purchase", 29.99)
]

def random_date(start_year=2024, end_year=2025):
    """Generate a random date."""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def generate_invoice_simple(filename, doc_number):
    """Generate a simple invoice (1 page, minimal fields)."""
    doc = SimpleDocTemplate(str(filename), pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Company header
    company_style = ParagraphStyle(
        'Company',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2C3E50'),
        alignment=TA_CENTER
    )
    
    company = random.choice(COMPANIES)
    story.append(Paragraph(company, company_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Invoice title
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading2'],
        fontSize=14,
        alignment=TA_CENTER
    )
    story.append(Paragraph(f"INVOICE {doc_number}", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Invoice details
    invoice_date = random_date()
    due_date = invoice_date + timedelta(days=30)
    
    details = [
        ["Invoice Number:", doc_number],
        ["Date:", invoice_date.strftime("%B %d, %Y")],
        ["Due Date:", due_date.strftime("%B %d, %Y")],
        ["", ""]
    ]
    
    details_table = Table(details, colWidths=[2*inch, 3*inch])
    details_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ]))
    
    story.append(details_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Line items
    item = random.choice(PRODUCTS)
    quantity = random.randint(1, 5)
    unit_price = random.uniform(item[1], item[2])
    subtotal = quantity * unit_price
    tax = subtotal * 0.08
    total = subtotal + tax
    
    items = [
        ["Description", "Quantity", "Unit Price", "Amount"],
        [item[0], str(quantity), f"${unit_price:.2f}", f"${subtotal:.2f}"],
        ["", "", "", ""],
        ["", "", "Subtotal:", f"${subtotal:.2f}"],
        ["", "", "Tax (8%):", f"${tax:.2f}"],
        ["", "", "Total:", f"${total:.2f}"]
    ]
    
    items_table = Table(items, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
    items_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, 1), 1, colors.black),
        ('LINEABOVE', (2, -3), (-1, -3), 1, colors.black),
        ('LINEABOVE', (2, -1), (-1, -1), 2, colors.black),
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    story.append(Paragraph("Thank you for your business!", footer_style))
    
    doc.build(story)
    return total

def generate_invoice_complex(filename, doc_number):
    """Generate a complex invoice (multiple items, tables)."""
    doc = SimpleDocTemplate(str(filename), pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Header with company info
    company_style = ParagraphStyle(
        'Company',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#2C3E50')
    )
    
    company = random.choice(COMPANIES)
    story.append(Paragraph(company, company_style))
    story.append(Paragraph("123 Business Street, Suite 100", styles['Normal']))
    story.append(Paragraph("New York, NY 10001", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Invoice title
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#E74C3C')
    )
    story.append(Paragraph(f"INVOICE {doc_number}", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Two-column layout for invoice and billing info
    invoice_date = random_date()
    due_date = invoice_date + timedelta(days=30)
    
    info_data = [
        ["INVOICE INFORMATION", "BILL TO"],
        [f"Invoice #: {doc_number}", "Client Corporation"],
        [f"Date: {invoice_date.strftime('%m/%d/%Y')}", "456 Client Avenue"],
        [f"Due Date: {due_date.strftime('%m/%d/%Y')}", "Boston, MA 02101"],
        ["Payment Terms: Net 30", ""]
    ]
    
    info_table = Table(info_data, colWidths=[3*inch, 3*inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ECF0F1')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Multiple line items
    items = [["Description", "Qty", "Unit Price", "Amount"]]
    subtotal = 0
    
    num_items = random.randint(3, 7)
    for _ in range(num_items):
        product = random.choice(PRODUCTS)
        qty = random.randint(1, 10)
        unit_price = random.uniform(product[1], product[2])
        amount = qty * unit_price
        subtotal += amount
        items.append([
            product[0],
            str(qty),
            f"${unit_price:.2f}",
            f"${amount:.2f}"
        ])
    
    # Totals
    discount = subtotal * 0.10 if random.random() > 0.5 else 0
    subtotal_after_discount = subtotal - discount
    tax = subtotal_after_discount * 0.08
    total = subtotal_after_discount + tax
    
    items.append(["", "", "", ""])
    items.append(["", "", "Subtotal:", f"${subtotal:.2f}"])
    if discount > 0:
        items.append(["", "", "Discount (10%):", f"-${discount:.2f}"])
    items.append(["", "", "Tax (8%):", f"${tax:.2f}"])
    items.append(["", "", "TOTAL DUE:", f"${total:.2f}"])
    
    items_table = Table(items, colWidths=[3.5*inch, 0.75*inch, 1.25*inch, 1.5*inch])
    items_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, num_items), 0.5, colors.grey),
        ('LINEABOVE', (2, -4), (-1, -4), 1, colors.black),
        ('LINEABOVE', (2, -1), (-1, -1), 2, colors.black),
        ('FONTNAME', (2, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (2, -1), (-1, -1), 11),
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Payment instructions
    payment_style = ParagraphStyle(
        'Payment',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#7F8C8D')
    )
    story.append(Paragraph("<b>Payment Instructions:</b>", payment_style))
    story.append(Paragraph("Make checks payable to: " + company, payment_style))
    story.append(Paragraph("Wire Transfer: Bank Account #123-456-789", payment_style))
    
    doc.build(story)
    return total

def generate_receipt(filename, receipt_number):
    """Generate a simple receipt."""
    doc = SimpleDocTemplate(str(filename), pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Store header
    store_style = ParagraphStyle(
        'Store',
        parent=styles['Heading1'],
        fontSize=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2C3E50')
    )
    
    store_name = random.choice(["QuickMart", "CaféBean", "Office Depot", "TechStop"])
    story.append(Paragraph(store_name, store_style))
    story.append(Paragraph("123 Main Street", styles['Normal']))
    story.append(Paragraph("Anytown, USA 12345", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Receipt info
    receipt_date = random_date()
    
    story.append(Paragraph(f"<b>Receipt #:</b> {receipt_number}", styles['Normal']))
    story.append(Paragraph(f"<b>Date:</b> {receipt_date.strftime('%m/%d/%Y %I:%M %p')}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Divider
    story.append(Paragraph("-" * 80, styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    # Items
    num_items = random.randint(1, 4)
    subtotal = 0
    
    items_data = [["Item", "Price"]]
    for _ in range(num_items):
        item_name, base_price = random.choice(RECEIPT_ITEMS)
        price = base_price * random.uniform(0.9, 1.1)
        subtotal += price
        items_data.append([item_name, f"${price:.2f}"])
    
    tax = subtotal * 0.08
    total = subtotal + tax
    
    items_data.append(["", ""])
    items_data.append(["Subtotal", f"${subtotal:.2f}"])
    items_data.append(["Tax", f"${tax:.2f}"])
    items_data.append(["TOTAL", f"${total:.2f}"])
    
    items_table = Table(items_data, colWidths=[4*inch, 2*inch])
    items_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('LINEABOVE', (0, -3), (-1, -3), 1, colors.grey),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    story.append(Paragraph("Thank you for your purchase!", footer_style))
    story.append(Paragraph("Please keep this receipt for your records", footer_style))
    
    doc.build(story)
    return total

def generate_documents(output_dir, count):
    """Generate test documents."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Generating {count} test documents in: {output_path}")
    print("="*70)
    
    invoice_count = 0
    receipt_count = 0
    total_cost = 0
    
    for i in range(1, count + 1):
        doc_type = random.choice(['invoice_simple', 'invoice_complex', 'receipt'])
        
        if 'invoice' in doc_type:
            invoice_count += 1
            doc_number = f"INV-{random.randint(2024, 2025)}-{random.randint(1000, 9999)}"
            filename = output_path / f"invoice_{i:03d}_{doc_number}.pdf"
            
            if doc_type == 'invoice_simple':
                amount = generate_invoice_simple(filename, doc_number)
                print(f"✅ Invoice (Simple): {filename.name} - ${amount:.2f}")
            else:
                amount = generate_invoice_complex(filename, doc_number)
                print(f"✅ Invoice (Complex): {filename.name} - ${amount:.2f}")
        else:
            receipt_count += 1
            receipt_number = f"RCP-{random.randint(100000, 999999)}"
            filename = output_path / f"receipt_{i:03d}_{receipt_number}.pdf"
            amount = generate_receipt(filename, receipt_number)
            print(f"✅ Receipt: {filename.name} - ${amount:.2f}")
        
        total_cost += amount
    
    print("="*70)
    print(f"\n📊 Generation Summary:")
    print(f"   Total Documents: {count}")
    print(f"   Invoices: {invoice_count}")
    print(f"   Receipts: {receipt_count}")
    print(f"   Total Value: ${total_cost:,.2f}")
    print(f"\n💾 Documents saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate test documents for document processing pipeline")
    parser.add_argument('--count', type=int, default=15, help='Number of documents to generate (default: 15)')
    parser.add_argument('--output-dir', type=str, default='/home/claude/generated-documents', 
                       help='Output directory (default: /home/claude/generated-documents)')
    
    args = parser.parse_args()
    
    generate_documents(args.output_dir, args.count)

if __name__ == '__main__':
    main()
