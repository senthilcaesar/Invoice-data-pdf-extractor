# Invoice Data Pdf Extractor

A Python script to extract specific attributes from PDF invoices using PyMuPDF and save them to CSV format.

## Features

Extracts the following attributes from a PDF invoice:

1. Order Number
2. Order Date
3. Place of Delivery
4. Invoice Number
5. Invoice Value
6. Description (from table column)
7. HSN Code (separated from description)
8. Payment Transaction ID
9. Mode of Payment
10. Date & Time
11. Shipping Address

## Installation

1. Install the required dependency:

```bash
pip install -r requirements.txt
```

Or install PyMuPDF directly:

```bash
pip install PyMuPDF
```

## Usage

### Single PDF File

To extract data from a **single PDF file**, use:

```bash
python extract_invoice.py
```

**Configuration:**

- Open `extract_invoice.py` and modify the `pdf_file` variable to point to your PDF:
  ```python
  pdf_file = "invoice.pdf"  # Change to your PDF filename
  ```
- The script will extract data from page 2 by default
- Output will be saved to `invoice_data.csv`

### Multiple PDF Files (Batch Processing)

To extract data from **all PDF files in a directory**, use:

```bash
python extract_invoice_batch.py
```

**Configuration:**

- The script will automatically find all `.pdf` files in the current directory
- Output will be saved to `all_invoices.csv` with one row per PDF
- You can modify the script to specify a custom directory or list of files

## Output Format

The script generates a CSV file with the following columns:

- Order Number
- Order Date
- Place of Delivery
- Invoice Number
- Invoice Value
- Description
- HSN Code
- Payment Transaction ID
- Mode of Payment
- Date & Time
- Shipping Address

## Supported Date/Time Formats

The extractor is optimized for these specific formats:

- **Order Date**: `DD.MM.YYYY` (e.g., 02.11.2025)
- **Date & Time**: `DD/MM/YYYY,HH:MM:SS hrs` (e.g., 02/11/2025,12:58:05 hrs)
- **Mode of Payment**: NetBanking, Credit Card, etc.

## Description and HSN Code Extraction

The script intelligently extracts product descriptions from table columns:

- **Example**: "Amudham Naturals 100% Pure Ragi Flour, Traditional Indian Finger Millet Flour, No Added Preservatives, Gluten-Free, 1 kg | B0FW7291VR ( MS-H2GY-GWJX )"
- **HSN Code**: Automatically separated from description (e.g., 11029090)

## Customization

### Change Page Number

To extract from a different page, modify the `page_number` parameter:

```python
invoice_data = extract_invoice_data(pdf_file, page_number=3)  # Extract from page 3
```

### Enable/Disable Debug Mode

Debug mode shows the raw extracted text and extraction details:

```python
debug_mode = True   # Enable debug output
debug_mode = False  # Disable debug output
```

### Adjust Extraction Patterns

If your PDF has a different format, you can modify the regex patterns in the script. Each field has multiple patterns to handle variations:

```python
# Example: Add a new pattern for Order Number
order_patterns = [
    r'Order\s+(?:Number|No\.?|#)\s*:?\s*([A-Z0-9\-]+)',
    r'Order\s+ID\s*:?\s*([A-Z0-9\-]+)',
    r'Your\s+Custom\s+Pattern\s*:?\s*([A-Z0-9\-]+)',  # Add your pattern
]
```

## Troubleshooting

### Issue: Some fields are not extracted

**Solution 1:** Enable debug mode to see the raw text:

```python
debug_mode = True
```

Run the script and examine the "RAW TEXT FROM PAGE" section to see what text is available.

**Solution 2:** Check the page number. The script defaults to page 2. If your data is on a different page:

```python
page_number = 3  # Change to the correct page
```

### Issue: Description is incomplete or incorrect

**Solution:** The description extraction is optimized for table-based formats. If your PDF has a different layout:

1. Enable debug mode
2. Look at the "DESCRIPTION EXTRACTION DEBUG" section
3. Adjust the stop keywords if needed:

```python
stop_keywords = ['TOTAL:', 'Subtotal', 'YourKeyword']
```

### Issue: Text extraction fails

**Possible causes:**

- The PDF is scanned (image-based) - PyMuPDF only works with text-based PDFs
- The PDF is password-protected
- The PDF has unusual encoding

**Solution for scanned PDFs:** You would need OCR (Optical Character Recognition):

```bash
pip install pytesseract pdf2image
# Then use pytesseract to extract text from images
```

### Issue: Wrong HSN code extracted

**Solution:** The script looks for patterns like "HSN:XXXXXXXX". If your PDF uses a different format:

```python
# Modify the HSN extraction pattern
hsn_match = re.search(r'HSN\s*Code\s*:?\s*(\d+)', line, re.IGNORECASE)
```

## File Structure

```
.
├── extract_invoice.py          # Single PDF extraction
├── extract_invoice_batch.py    # Batch processing for multiple PDFs
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── invoice.pdf                 # Your input PDF (example)
└── invoice_data.csv            # Output file (generated)
```

## Advanced Usage

### Custom Output Filename

```python
save_to_csv(invoice_data, 'my_custom_output.csv')
```

### Process Specific Files

Edit `extract_invoice_batch.py` and specify your files:

```python
pdf_files = [
    "invoice_jan.pdf",
    "invoice_feb.pdf",
    "invoice_mar.pdf"
]
```

### Extract from First Page

```python
invoice_data = extract_invoice_data(pdf_file, page_number=1)
```

## Dependencies

- **PyMuPDF (fitz)**: PDF text extraction
- **csv**: CSV file writing (Python standard library)
- **re**: Regular expressions (Python standard library)

## Notes

- The script is designed for **text-based PDFs** only
- For scanned/image PDFs, OCR (pytesseract) is required
- The script extracts data from **page 2** by default
- Regex patterns may need adjustment based on your specific PDF format
- Debug mode helps identify extraction issues

## Support

If certain fields are not extracting correctly:

1. Enable debug mode: `debug_mode = True`
2. Check the raw text output
3. Verify the page number
4. Adjust regex patterns if needed

## License

This script is provided as-is for invoice data extraction purposes.
