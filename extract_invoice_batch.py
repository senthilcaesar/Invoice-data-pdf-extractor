"""
Invoice Data Extractor - Final Complete Version
Extracts clean Description (without serial number, ASIN, SKU), HSN Code, ASIN, and SKU.
Filters out serial numbers, table headers, and all numeric columns.
"""

import fitz  # PyMuPDF
import csv
import re
import os
import glob


def extract_description_hsn_asin_sku(text, debug=False):
    """
    Extract description, HSN code, ASIN, and SKU from table format.
    Filters out serial numbers, table column headers and labels.
    
    ASIN format: B0FW7291VR (starts with B0, followed by alphanumeric)
    SKU format: MS-H2GY-GWJX (alphanumeric with hyphens, in parentheses)
    
    Args:
        text (str): Full page text
        debug (bool): Print debug info
        
    Returns:
        tuple: (description, hsn_code, asin, sku)
    """
    description = ""
    hsn_code = ""
    asin = ""
    sku = ""
    
    if debug:
        print("\n" + "-"*80)
        print("DESCRIPTION EXTRACTION DEBUG:")
        print("-"*80)
    
    # Split text into lines
    lines = text.split('\n')
    
    # Find the Description column header
    desc_start_index = -1
    for i, line in enumerate(lines):
        if re.search(r'\bDescription\b', line, re.IGNORECASE):
            desc_start_index = i
            if debug:
                print(f"Found 'Description' header at line {i}: {line}")
            break
    
    if desc_start_index != -1:
        # Collect description lines (text only, no numbers or headers)
        desc_lines = []
        raw_text = []  # Keep raw text for ASIN/SKU extraction
        
        # Keywords that indicate we've moved past the description section
        stop_keywords = ['TOTAL:', 'Subtotal', 'Grand Total', 
                        'Mode of Payment', 'Date & Time', 'Transaction']
        
        # Start from the line after "Description" header
        for i in range(desc_start_index + 1, min(desc_start_index + 30, len(lines))):
            line = lines[i].strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Stop if we hit total or other sections
            if any(keyword in line for keyword in stop_keywords):
                if debug:
                    print(f"Stopping at line {i}: {line}")
                break
            
            # Keep raw text for ASIN/SKU extraction
            raw_text.append(line)
            
            # CRITICAL FILTERS - Skip all numeric/table data and headers:
            
            # 1. Skip lines that are just a single digit or small number (serial numbers like "1", "2", etc.)
            if re.match(r'^\d{1,3}$', line):
                if debug:
                    print(f"Skipping serial number {i}: {line}")
                continue
            
            # 2. Skip lines that are repetitions of "Amount" or similar column headers
            if re.match(r'^(Amount\s*){2,}', line, re.IGNORECASE):
                if debug:
                    print(f"Skipping repeated 'Amount' header {i}: {line}")
                continue
            
            # 3. Skip lines like "Amount Amount Amount 1" or similar table artifacts
            if re.match(r'^(Amount|Net|Tax|Total|Type|Rate|Qty|Price)\s+(Amount|Net|Tax|Total|Type|Rate|Qty|Price)', line, re.IGNORECASE):
                if debug:
                    print(f"Skipping table header line {i}: {line}")
                continue
            
            # 4. Skip pure numbers (prices, quantities, amounts)
            if re.match(r'^[\d,.\s₹$€£%]+$', line):
                if debug:
                    print(f"Skipping numeric line {i}: {line}")
                continue
            
            # 5. Skip currency amounts with symbols
            if re.match(r'^[₹$€£]\s*[\d,]+\.?\d*$', line):
                if debug:
                    print(f"Skipping currency amount {i}: {line}")
                continue
            
            # 6. Skip lines that are ONLY numbers, percentages, or currency
            if re.match(r'^(\d+%?|[\d,]+\.?\d*|[₹$€£][\d,]+\.?\d*)$', line):
                if debug:
                    print(f"Skipping number/percentage {i}: {line}")
                continue
            
            # 7. Skip tax type indicators
            if re.match(r'^(IGST|CGST|SGST|GST)$', line, re.IGNORECASE):
                if debug:
                    print(f"Skipping tax type {i}: {line}")
                continue
            
            # 8. Skip standard column headers
            if re.match(r'^(Sl\.?\s*No|Unit\s+Price|Qty|Net\s+Amount|Tax\s+Rate|Tax\s+Type|Tax\s+Amount|Total\s+Amount)$', line, re.IGNORECASE):
                if debug:
                    print(f"Skipping column header {i}: {line}")
                continue
            
            # 9. Skip lines with mostly numbers and currency symbols
            num_count = len(re.findall(r'[\d₹$€£,%.]', line))
            letter_count = len(re.findall(r'[a-zA-Z]', line))
            if num_count > letter_count and num_count > 5:
                if debug:
                    print(f"Skipping numeric-heavy line {i}: {line}")
                continue
            
            # 10. Skip lines that look like just "Amount 1" or "Net 1" etc.
            if re.match(r'^(Amount|Net|Tax|Total|Price|Rate)\s+\d+$', line, re.IGNORECASE):
                if debug:
                    print(f"Skipping column label with number {i}: {line}")
                continue
            
            # Check if this line contains HSN code
            hsn_match = re.search(r'HSN\s*:?\s*(\d+)', line, re.IGNORECASE)
            if hsn_match:
                hsn_code = hsn_match.group(1)
                # Extract description part before HSN (if any on same line)
                desc_part = re.sub(r'HSN\s*:?\s*\d+', '', line, flags=re.IGNORECASE).strip()
                if desc_part and len(desc_part) > 3:
                    # Only add if it doesn't look like a header or serial number
                    if not re.match(r'^(Amount|Net|Tax|Total|\d{1,3})$', desc_part, re.IGNORECASE):
                        desc_lines.append(desc_part)
                if debug:
                    print(f"Found HSN code at line {i}: {hsn_code}")
                    if desc_part:
                        print(f"  Description part: {desc_part}")
                continue
            
            # Add to description if it contains actual text (product description)
            # Must have at least some letters and be reasonably long
            if len(line) > 5 and re.search(r'[a-zA-Z]{3,}', line):
                # Additional check: make sure it's not just a serial number pattern
                if not re.match(r'^[A-Z0-9\-]{8,}$', line):
                    # Skip if it looks like a column header
                    if not re.match(r'^(Amount|Net|Tax|Total|Type|Rate|Qty|Price)', line, re.IGNORECASE):
                        desc_lines.append(line)
                        if debug:
                            print(f"✓ Adding description line {i}: {line}")
        
        # Combine description lines
        description = ' '.join(desc_lines).strip()
        
        # Extract ASIN and SKU from the raw text
        full_raw_text = ' '.join(raw_text)
        
        # Extract ASIN (format: B0 followed by alphanumeric characters, typically 10 chars total)
        asin_match = re.search(r'\b(B0[A-Z0-9]{8})\b', full_raw_text)
        if asin_match:
            asin = asin_match.group(1)
            if debug:
                print(f"Found ASIN: {asin}")
            # Remove ASIN from description
            description = description.replace(asin, '').strip()
        
        # Extract SKU (format: alphanumeric with hyphens, in parentheses)
        # Pattern: ( XXXXX-XXXXX-XXXXX ) or similar
        sku_match = re.search(r'\(\s*([A-Z0-9\-]+)\s*\)', full_raw_text)
        if sku_match:
            potential_sku = sku_match.group(1)
            # Make sure it's not the ASIN (ASIN doesn't have hyphens typically)
            if potential_sku != asin and '-' in potential_sku:
                sku = potential_sku
                if debug:
                    print(f"Found SKU: {sku}")
                # Remove SKU and parentheses from description
                description = re.sub(r'\(\s*' + re.escape(sku) + r'\s*\)', '', description).strip()
        
        # Clean up description
        if description:
            # Remove any leading serial numbers (single digits at the start)
            description = re.sub(r'^\d{1,3}\s+', '', description)
            
            # Remove extra whitespace
            description = ' '.join(description.split())
            
            # Remove trailing punctuation artifacts
            description = description.rstrip('|,;')
            
            # Remove any remaining numeric artifacts at the end
            description = re.sub(r'\s+[\d,]+\.?\d*\s*$', '', description)
            
            # Clean up extra pipes and spaces
            description = re.sub(r'\s*\|\s*$', '', description)
            description = re.sub(r'\s+', ' ', description)
            
            # Remove any remaining "Amount" or similar artifacts
            description = re.sub(r'\b(Amount|Net|Tax|Total|Type|Rate)\s+\d*\s*$', '', description, flags=re.IGNORECASE).strip()
    
    # Alternative method if table parsing didn't work
    if not description:
        if debug:
            print("\nTrying alternative description extraction...")
        
        # Look for product description pattern (after serial number)
        pattern = r'\d+\s+([A-Za-z][^₹\d\n]{20,}?)(?:\s*HSN\s*:?\s*(\d+)|\s*₹|\s+\d+\.\d{2})'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            description = match.group(1).strip()
            if match.lastindex >= 2 and match.group(2):
                hsn_code = match.group(2)
            # Clean up
            description = ' '.join(description.split())
            if debug:
                print(f"Alternative method found: {description}")
    
    # Extract HSN if not found yet
    if not hsn_code:
        hsn_match = re.search(r'HSN\s*:?\s*(\d{6,10})', text, re.IGNORECASE)
        if hsn_match:
            hsn_code = hsn_match.group(1)
            if debug:
                print(f"Found HSN code via alternative search: {hsn_code}")
    
    # Extract ASIN if not found yet
    if not asin:
        asin_match = re.search(r'\b(B0[A-Z0-9]{8})\b', text)
        if asin_match:
            asin = asin_match.group(1)
            if debug:
                print(f"Found ASIN via alternative search: {asin}")
    
    # Extract SKU if not found yet
    if not sku:
        sku_match = re.search(r'\(\s*([A-Z0-9]+-[A-Z0-9]+-[A-Z0-9]+)\s*\)', text)
        if sku_match:
            sku = sku_match.group(1)
            if debug:
                print(f"Found SKU via alternative search: {sku}")
    
    if debug:
        print("-"*80)
        print(f"FINAL Description: {description}")
        print(f"FINAL HSN Code: {hsn_code}")
        print(f"FINAL ASIN: {asin}")
        print(f"FINAL SKU: {sku}")
        print("-"*80 + "\n")
    
    return description, hsn_code, asin, sku


def extract_invoice_data(pdf_path, page_number=2, debug=False):
    """
    Extract invoice attributes from PDF.
    
    Args:
        pdf_path (str): Path to the PDF file
        page_number (int): Page number (1-indexed)
        debug (bool): Enable debug output
        
    Returns:
        dict: Extracted invoice data
    """
    invoice_data = {
        'PDF Filename': '',
        'Order Number': '',
        'Order Date': '',
        'Place of Delivery': '',
        'Invoice Number': '',
        'Invoice Value': '',
        'Description': '',
        'HSN Code': '',
        'ASIN': '',
        'SKU': '',
        'Payment Transaction ID': '',
        'Mode of Payment': '',
        'Date & Time': '',
        'Shipping Address': ''
    }
    
    try:
        doc = fitz.open(pdf_path)
        
        if len(doc) < page_number:
            print(f"Warning: PDF has only {len(doc)} page(s).")
            page_index = min(len(doc) - 1, 0)
        else:
            page_index = page_number - 1
        
        page = doc[page_index]
        text = page.get_text()
        doc.close()
        
        if debug:
            print("\n" + "="*80)
            print(f"RAW TEXT FROM PAGE {page_number}:")
            print("="*80)
            print(text)
            print("="*80 + "\n")
            print("EXTRACTING FIELDS...")
            print("="*80)
        
        # 1. Order Number
        patterns = [
            r'Order\s+(?:Number|No\.?|#)\s*:?\s*([A-Z0-9\-]+)',
            r'Order\s+ID\s*:?\s*([A-Z0-9\-]+)',
            r'Order\s*#?\s*:?\s*([A-Z0-9\-]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                invoice_data['Order Number'] = match.group(1).strip()
                if debug: print(f"✓ Order Number: {invoice_data['Order Number']}")
                break
        if debug and not invoice_data['Order Number']:
            print("✗ Order Number: Not found")
        
        # 2. Order Date (Format: DD.MM.YYYY like 02.11.2025)
        patterns = [
            r'Order\s+Date\s*:?\s*(\d{2}\.\d{2}\.\d{4})',
            r'Order\s+Date\s*:?\s*(\d{1,2}[./]\d{1,2}[./]\d{2,4})',
            r'Ordered\s+on\s*:?\s*(\d{1,2}[./]\d{1,2}[./]\d{2,4})',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                invoice_data['Order Date'] = match.group(1).strip()
                if debug: print(f"✓ Order Date: {invoice_data['Order Date']}")
                break
        if debug and not invoice_data['Order Date']:
            print("✗ Order Date: Not found")
        
        # 3. Place of Delivery
        patterns = [
            r'Place\s+of\s+Delivery\s*:?\s*([^\n]+)',
            r'Delivery\s+(?:Location|Place)\s*:?\s*([^\n]+)',
            r'Deliver\s+to\s*:?\s*([^\n]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                invoice_data['Place of Delivery'] = match.group(1).strip()
                if debug: print(f"✓ Place of Delivery: {invoice_data['Place of Delivery']}")
                break
        if debug and not invoice_data['Place of Delivery']:
            print("✗ Place of Delivery: Not found")
        
        # 4. Invoice Number
        patterns = [
            r'Invoice\s+(?:Number|No\.?|#)\s*:?\s*([A-Z0-9\-]+)',
            r'Invoice\s+ID\s*:?\s*([A-Z0-9\-]+)',
            r'Invoice\s*#?\s*:?\s*([A-Z0-9\-]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                invoice_data['Invoice Number'] = match.group(1).strip()
                if debug: print(f"✓ Invoice Number: {invoice_data['Invoice Number']}")
                break
        if debug and not invoice_data['Invoice Number']:
            print("✗ Invoice Number: Not found")
        
        # 5. Invoice Value / Total Amount
        patterns = [
            r'TOTAL\s*:?\s*[₹$€£]?\s*[\d,]+\.?\d*\s*[₹$€£]?\s*([\d,]+\.?\d*)',
            r'Grand\s+Total\s*:?\s*[₹$€£]?\s*([\d,]+\.?\d*)',
            r'Total\s+Amount\s*:?\s*[₹$€£]?\s*([\d,]+\.?\d*)',
            r'Invoice\s+(?:Value|Amount|Total)\s*:?\s*[₹$€£]?\s*([\d,]+\.?\d*)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                invoice_data['Invoice Value'] = '₹' + match.group(1).strip()
                if debug: print(f"✓ Invoice Value: {invoice_data['Invoice Value']}")
                break
        if debug and not invoice_data['Invoice Value']:
            print("✗ Invoice Value: Not found")
        
        # 6, 7, 8, 9. Description, HSN Code, ASIN, and SKU - Extract together
        description, hsn_code, asin, sku = extract_description_hsn_asin_sku(text, debug)
        invoice_data['Description'] = description
        invoice_data['HSN Code'] = hsn_code
        invoice_data['ASIN'] = asin
        invoice_data['SKU'] = sku
        
        if not debug:
            # Only print in non-debug mode
            if description:
                print(f"✓ Description: {description}")
            else:
                print("✗ Description: Not found")
            if hsn_code:
                print(f"✓ HSN Code: {hsn_code}")
            else:
                print("✗ HSN Code: Not found")
            if asin:
                print(f"✓ ASIN: {asin}")
            else:
                print("✗ ASIN: Not found")
            if sku:
                print(f"✓ SKU: {sku}")
            else:
                print("✗ SKU: Not found")
        
        # 10. Payment Transaction ID
        patterns = [
            r'(?:Payment\s+)?Transaction\s+(?:ID|No\.?|#)\s*:?\s*([A-Z0-9\-]+)',
            r'Transaction\s+Reference\s*:?\s*([A-Z0-9\-]+)',
            r'Payment\s+ID\s*:?\s*([A-Z0-9\-]+)',
            r'UTR\s*(?:Number|No\.?)?\s*:?\s*([A-Z0-9\-]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                invoice_data['Payment Transaction ID'] = match.group(1).strip()
                if debug: print(f"✓ Payment Transaction ID: {invoice_data['Payment Transaction ID']}")
                break
        if debug and not invoice_data['Payment Transaction ID']:
            print("✗ Payment Transaction ID: Not found")
        
        # 11. Mode of Payment (e.g., "NetBanking")
        patterns = [
            r'Mode\s+of\s+Payment\s*:?\s*([^\n]+)',
            r'Payment\s+(?:Mode|Method)\s*:?\s*([^\n]+)',
            r'Payment\s+Type\s*:?\s*([^\n]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                invoice_data['Mode of Payment'] = match.group(1).strip()
                if debug: print(f"✓ Mode of Payment: {invoice_data['Mode of Payment']}")
                break
        if debug and not invoice_data['Mode of Payment']:
            print("✗ Mode of Payment: Not found")
        
        # 12. Date & Time (Format: 02/11/2025,12:58:05 hrs)
        patterns = [
            r'Date\s+(?:&|and)\s+Time\s*:?\s*(\d{2}/\d{2}/\d{4},\s*\d{2}:\d{2}:\d{2}\s*hrs?)',
            r'Date\s+(?:&|and)\s+Time\s*:?\s*(\d{1,2}/\d{1,2}/\d{4},\s*\d{1,2}:\d{2}:\d{2}\s*hrs?)',
            r'Date\s*&\s*Time\s*:?\s*(\d{1,2}/\d{1,2}/\d{4},\s*\d{1,2}:\d{2}:\d{2})',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                invoice_data['Date & Time'] = match.group(1).strip()
                if debug: print(f"✓ Date & Time: {invoice_data['Date & Time']}")
                break
        if debug and not invoice_data['Date & Time']:
            print("✗ Date & Time: Not found")
        
        # 13. Shipping Address
        patterns = [
            r'Shipping\s+Address\s*:?\s*([^\n]+(?:\n(?!\s*(?:Order|Invoice|Payment|Mode|Date|TOTAL))[^\n]+){0,5})',
            r'Delivery\s+Address\s*:?\s*([^\n]+(?:\n(?!\s*(?:Order|Invoice|Payment|Mode|Date|TOTAL))[^\n]+){0,5})',
            r'Ship\s+To\s*:?\s*([^\n]+(?:\n(?!\s*(?:Order|Invoice|Payment|Mode|Date|TOTAL))[^\n]+){0,5})',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                address = match.group(1).strip()
                invoice_data['Shipping Address'] = ' '.join(address.split())
                if debug: print(f"✓ Shipping Address: {invoice_data['Shipping Address']}")
                break
        if debug and not invoice_data['Shipping Address']:
            print("✗ Shipping Address: Not found")
        
        return invoice_data
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return invoice_data


def save_to_csv(data, csv_path='invoice_data.csv'):
    """Save extracted data to CSV."""
    try:
        if isinstance(data, dict):
            data = [data]
        
        if not data:
            print("No data to save!")
            return
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
        print(f"\n{'='*80}")
        print(f"✓ SUCCESS: Data saved to {csv_path}")
        print(f"  Total records: {len(data)}")
        print(f"{'='*80}")
        
    except Exception as e:
        print(f"Error saving CSV: {str(e)}")


def process_multiple_pdfs(pdf_files, page_number=2, debug=False):
    """Process multiple PDF files."""
    results = []
    
    for i, pdf_file in enumerate(pdf_files, 1):
        filename = os.path.basename(pdf_file)
        print(f"\n{'='*80}")
        print(f"[{i}/{len(pdf_files)}] Processing: {filename}")
        print(f"{'='*80}")
        
        data = extract_invoice_data(pdf_file, page_number, debug)
        data['PDF Filename'] = filename
        results.append(data)
    
    return results


def main():
    """Main function."""
    # Configuration
    directory_path = "/Users/senthilpalanivelu/Desktop/amazon_invoice"  # Change to your directory path
    page_number = 2  # Page to extract from (1-indexed)
    debug_mode = False  # Set to True to see detailed extraction info for each PDF
    
    print("="*80)
    print("INVOICE DATA EXTRACTOR - BATCH PROCESSING")
    print("Extracts clean Description (without serial numbers), HSN, ASIN, and SKU")
    print("="*80)
    print(f"Directory: {directory_path}")
    print(f"Page: {page_number}")
    print(f"Debug: {debug_mode}")
    print("="*80)
    
    # Find all PDF files in the directory
    import glob
    pdf_files = glob.glob(os.path.join(directory_path, "*.pdf"))
    
    if not pdf_files:
        print(f"\nNo PDF files found in: {directory_path}")
        return
    
    print(f"\nFound {len(pdf_files)} PDF file(s)")
    print("="*80)
    
    # Process all PDFs
    all_data = process_multiple_pdfs(pdf_files, page_number, debug_mode)
    
    # Display summary for each file
    print("\n" + "="*80)
    print("EXTRACTION SUMMARY:")
    print("="*80)
    for i, data in enumerate(all_data, 1):
        print(f"\n[{i}/{len(all_data)}] {data.get('PDF Filename', 'Unknown')}")
        print("-"*80)
        
        # Show key fields
        fields_to_show = ['Order Number', 'Invoice Number', 'Invoice Value', 
                         'Description', 'ASIN', 'SKU', 'HSN Code']
        
        for key in fields_to_show:
            value = data.get(key, '')
            status = "✓" if value else "✗"
            display_value = value if value else "(not found)"
            
            # Truncate long descriptions
            if key == "Description" and len(display_value) > 60:
                display_value = display_value[:60] + "..."
            
            print(f"  {status} {key:20s}: {display_value}")
    
    # Save all data to CSV
    print("\n" + "="*80)
    output_file = 'all_invoices.csv'
    save_to_csv(all_data, output_file)
    print(f"\n✓ Processed {len(all_data)} invoice(s)")
    print(f"✓ Results saved to: {output_file}")


if __name__ == "__main__":
    main()