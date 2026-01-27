# Invoice Data Extractor - Architecture & Flow

## 📊 System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    INVOICE DATA EXTRACTOR                        │
│                                                                  │
│  Purpose: Extract structured data from PDF invoices              │
│  Technology: Python + PyMuPDF                                   │
│  Output: CSV files with extracted invoice data                  │
└─────────────────────────────────────────────────────────────────┘
```

## 🏗️ Application Structure

```
invoice-data-extractor/
│
├── extract_invoice.py          # Single PDF processor
├── extract_invoice_batch.py    # Batch PDF processor
├── requirements.txt            # Dependencies
├── README.md                   # Documentation
│
├── input/                      # User's PDF files
│   ├── invoice1.pdf
│   ├── invoice2.pdf
│   └── invoice3.pdf
│
└── output/                     # Generated CSV files
    ├── invoice_data.csv        # Single PDF output
    └── all_invoices.csv        # Batch output
```

## 📋 High-Level Flow Diagram

```
┌──────────────┐
│   User Input │
│  (PDF Files) │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────┐
│   Choose Processing Mode:            │
│   • extract_invoice.py (Single)      │
│   • extract_invoice_batch.py (Batch) │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│   PDF Processing Engine               │
│   (PyMuPDF - fitz)                   │
│                                       │
│   1. Open PDF                        │
│   2. Navigate to Page 2              │
│   3. Extract Raw Text                │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│   Text Processing & Extraction       │
│   (Regular Expressions)              │
│                                       │
│   Extract 11 Fields:                 │
│   • Order Number                     │
│   • Order Date                       │
│   • Place of Delivery                │
│   • Invoice Number                   │
│   • Invoice Value                    │
│   • Description (from table)         │
│   • HSN Code (from description)      │
│   • Payment Transaction ID           │
│   • Mode of Payment                  │
│   • Date & Time                      │
│   • Shipping Address                 │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│   Data Structuring                   │
│   (Python Dictionary)                │
│                                       │
│   {                                   │
│     "Order Number": "...",           │
│     "Order Date": "...",             │
│     ...                              │
│   }                                  │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│   CSV Export                         │
│   (csv module)                       │
│                                       │
│   • Write headers                    │
│   • Write data rows                  │
│   • Save to disk                     │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────┐
│  CSV Output  │
│ (User's Data)│
└──────────────┘
```

## 🔄 Detailed Processing Flow

### Single PDF Processing (extract_invoice.py)

```
START
  │
  ├─→ Load Configuration
  │   ├─ pdf_file = "invoice.pdf"
  │   ├─ page_number = 2
  │   └─ debug_mode = True/False
  │
  ├─→ Open PDF with PyMuPDF
  │   └─ Check page count
  │
  ├─→ Extract Text from Page 2
  │   └─ page.get_text()
  │
  ├─→ [Optional] Display Raw Text (if debug=True)
  │
  ├─→ Extract Each Field Using Regex
  │   │
  │   ├─→ Order Number
  │   │   └─ Pattern: r'Order\s+(?:Number|No\.?|#)\s*:?\s*([A-Z0-9\-]+)'
  │   │
  │   ├─→ Order Date
  │   │   └─ Pattern: r'Order\s+Date\s*:?\s*(\d{2}\.\d{2}\.\d{4})'
  │   │
  │   ├─→ Place of Delivery
  │   │   └─ Pattern: r'Place\s+of\s+Delivery\s*:?\s*([^\n]+)'
  │   │
  │   ├─→ Invoice Number
  │   │   └─ Pattern: r'Invoice\s+(?:Number|No\.?|#)\s*:?\s*([A-Z0-9\-]+)'
  │   │
  │   ├─→ Invoice Value
  │   │   └─ Pattern: r'TOTAL\s*:?\s*[₹$€£]?\s*([\d,]+\.?\d*)'
  │   │
  │   ├─→ Description & HSN Code
  │   │   ├─ Find "Description" column header
  │   │   ├─ Extract lines until "TOTAL:"
  │   │   ├─ Separate HSN: r'HSN\s*:?\s*(\d+)'
  │   │   └─ Clean and combine text
  │   │
  │   ├─→ Payment Transaction ID
  │   │   └─ Pattern: r'Transaction\s+(?:ID|No\.?)\s*:?\s*([A-Z0-9\-]+)'
  │   │
  │   ├─→ Mode of Payment
  │   │   └─ Pattern: r'Mode\s+of\s+Payment\s*:?\s*([^\n]+)'
  │   │
  │   ├─→ Date & Time
  │   │   └─ Pattern: r'Date\s+&\s+Time\s*:?\s*(\d{2}/\d{2}/\d{4},\s*\d{2}:\d{2}:\d{2}\s*hrs?)'
  │   │
  │   └─→ Shipping Address
  │       └─ Pattern: r'Shipping\s+Address\s*:?\s*([^\n]+(?:\n...){0,5})'
  │
  ├─→ Store in Dictionary
  │   └─ invoice_data = {...}
  │
  ├─→ Display Extraction Summary
  │   ├─ Show all fields
  │   └─ Mark found (✓) vs missing (✗)
  │
  ├─→ Save to CSV
  │   ├─ Create invoice_data.csv
  │   ├─ Write header row
  │   └─ Write data row
  │
  └─→ Display Success Message
      └─ Show file path
END
```

### Batch Processing (extract_invoice_batch.py)

```
START
  │
  ├─→ Load Configuration
  │   ├─ directory = "."
  │   ├─ page_number = 2
  │   └─ debug_mode = True/False
  │
  ├─→ Find All PDFs in Directory
  │   └─ Path('.').glob('*.pdf')
  │
  ├─→ Display Found Files
  │   └─ List all PDF filenames
  │
  ├─→ Initialize Results List
  │   └─ all_data = []
  │
  ├─→ FOR EACH PDF FILE:
  │   │
  │   ├─→ Display Progress [1/3, 2/3, 3/3]
  │   │
  │   ├─→ Open PDF with PyMuPDF
  │   │
  │   ├─→ Extract Text from Page 2
  │   │
  │   ├─→ Extract All 11 Fields
  │   │   └─ (Same process as single PDF)
  │   │
  │   ├─→ Store in Dictionary
  │   │   └─ Add 'PDF Filename' field
  │   │
  │   ├─→ Append to Results List
  │   │   └─ all_data.append(invoice_data)
  │   │
  │   └─→ Display Brief Summary
  │       └─ Show extracted/total fields
  │
  ├─→ Save All Data to CSV
  │   ├─ Create all_invoices.csv
  │   ├─ Write header row
  │   └─ Write all data rows
  │
  ├─→ Calculate Statistics
  │   ├─ Total PDFs processed
  │   ├─ Fields per invoice
  │   └─ Extraction success rate per field
  │
  ├─→ Display Extraction Summary
  │   ├─ Overall statistics
  │   └─ Field-by-field success rates
  │       ├─ ✓ = >80% success
  │       ├─ ⚠ = 50-80% success
  │       └─ ✗ = <50% success
  │
  └─→ Display Success Message
      └─ Show output file path
END
```

## 🧩 Component Breakdown

### 1. PDF Reader Component
```
┌─────────────────────────────────┐
│   PyMuPDF (fitz) Library        │
├─────────────────────────────────┤
│                                 │
│  Functions:                     │
│  • fitz.open(pdf_path)          │
│  • doc[page_index]              │
│  • page.get_text()              │
│                                 │
│  Input:  PDF file path          │
│  Output: Raw text string        │
└─────────────────────────────────┘
```

### 2. Text Extraction Component
```
┌─────────────────────────────────┐
│   Regex Pattern Matcher         │
├─────────────────────────────────┤
│                                 │
│  Process:                       │
│  1. Define patterns for each    │
│     field                       │
│  2. Search text with re.search()│
│  3. Extract matched groups      │
│  4. Clean and format data       │
│                                 │
│  Input:  Raw text + patterns    │
│  Output: Extracted values       │
└─────────────────────────────────┘
```

### 3. Special: Description Extractor
```
┌─────────────────────────────────┐
│   Description & HSN Extractor   │
├─────────────────────────────────┤
│                                 │
│  Process:                       │
│  1. Find "Description" header   │
│  2. Collect subsequent lines    │
│  3. Stop at "TOTAL:" or similar │
│  4. Extract HSN code separately │
│  5. Clean and combine text      │
│                                 │
│  Special Logic:                 │
│  • Skip table headers           │
│  • Skip numeric-only lines      │
│  • Handle multi-line content    │
│                                 │
│  Input:  Full page text         │
│  Output: (description, hsn_code)│
└─────────────────────────────────┘
```

### 4. Data Storage Component
```
┌─────────────────────────────────┐
│   Python Dictionary             │
├─────────────────────────────────┤
│                                 │
│  Structure:                     │
│  {                              │
│    'Order Number': 'ABC123',    │
│    'Order Date': '02.11.2025',  │
│    'Place of Delivery': '...',  │
│    'Invoice Number': 'INV456',  │
│    'Invoice Value': '₹240.00',  │
│    'Description': '...',        │
│    'HSN Code': '11029090',      │
│    'Payment Transaction ID': '',│
│    'Mode of Payment': '...',    │
│    'Date & Time': '...',        │
│    'Shipping Address': '...'    │
│  }                              │
│                                 │
│  Features:                      │
│  • Key-value pairs              │
│  • Empty string for missing     │
│  • Easy to convert to CSV       │
└─────────────────────────────────┘
```

### 5. CSV Export Component
```
┌─────────────────────────────────┐
│   CSV Writer (csv.DictWriter)   │
├─────────────────────────────────┤
│                                 │
│  Process:                       │
│  1. Open file in write mode     │
│  2. Create DictWriter with keys │
│  3. Write header row            │
│  4. Write data row(s)           │
│  5. Close file                  │
│                                 │
│  Output Format:                 │
│  Order Number,Order Date,...    │
│  ABC123,02.11.2025,...          │
│                                 │
│  Features:                      │
│  • UTF-8 encoding               │
│  • Automatic escaping           │
│  • Comma-separated              │
└─────────────────────────────────┘
```

## 🎯 Extraction Strategy

### Pattern Matching Hierarchy

```
For Each Field:
│
├─→ Try Primary Pattern
│   └─ Most specific format
│
├─→ Try Alternative Pattern 1
│   └─ Common variation
│
├─→ Try Alternative Pattern 2
│   └─ Another variation
│
└─→ Return Empty String
    └─ If no match found
```

### Example: Order Date Extraction

```
Input Text: "Order Date: 02.11.2025"

Patterns Tried:
1. r'Order\s+Date\s*:?\s*(\d{2}\.\d{2}\.\d{4})'  ← MATCH! ✓
   Result: "02.11.2025"

2. r'Order\s+Date\s*:?\s*(\d{1,2}[./]\d{1,2}[./]\d{2,4})'
   (Not needed - already matched)

Output: "02.11.2025"
```

## 🐛 Debug Mode Flow

```
When debug_mode = True:

START
  │
  ├─→ Display Raw Text
  │   ├─ Shows entire page 2 content
  │   └─ Helps identify formatting
  │
  ├─→ For Each Field Extraction:
  │   ├─ Print field name
  │   ├─ Show pattern used
  │   ├─ Display extracted value
  │   └─ Mark as ✓ (found) or ✗ (missing)
  │
  ├─→ Special Debug for Description:
  │   ├─ Show header line location
  │   ├─ Display each extracted line
  │   ├─ Show stop condition
  │   └─ Display final combined result
  │
  └─→ Final Summary
      └─ Show all fields with status
END
```

## 📈 Performance Characteristics

```
┌─────────────────────────────────────────┐
│  Processing Speed (approximate)         │
├─────────────────────────────────────────┤
│                                         │
│  Single PDF:     ~0.5-2 seconds        │
│  10 PDFs:        ~5-20 seconds         │
│  100 PDFs:       ~50-200 seconds       │
│                                         │
│  Factors:                               │
│  • PDF file size                        │
│  • Text complexity                      │
│  • Debug mode (adds overhead)          │
│  • System performance                   │
└─────────────────────────────────────────┘
```

## 🔧 Configuration Points

```
User-Configurable Settings:

1. File Selection
   └─ pdf_file = "invoice.pdf"
   
2. Page Number
   └─ page_number = 2
   
3. Debug Mode
   └─ debug_mode = True/False
   
4. Directory (Batch)
   └─ directory = "."
   
5. Output Filename
   └─ 'invoice_data.csv' or 'all_invoices.csv'
```

## 🎨 Data Flow Visualization

```
PDF File(s)
    │
    │ PyMuPDF
    ▼
Raw Text
    │
    │ Regex Patterns
    ▼
Matched Data
    │
    │ Python Dictionary
    ▼
Structured Data
    │
    │ CSV Writer
    ▼
CSV File
```

## 🔍 Error Handling

```
┌─────────────────────────────────────┐
│  Error Detection & Handling         │
├─────────────────────────────────────┤
│                                     │
│  1. File Not Found                  │
│     └─ Check if PDF exists          │
│                                     │
│  2. Invalid Page Number             │
│     └─ Use last available page      │
│                                     │
│  3. No Text Extracted               │
│     └─ Return empty dictionary      │
│                                     │
│  4. Pattern Not Matched             │
│     └─ Store empty string           │
│                                     │
│  5. CSV Write Error                 │
│     └─ Display error message        │
└─────────────────────────────────────┘
```

## 📊 Success Metrics (Batch Mode)

```
Field Extraction Rate:

✓ >80%  = Excellent (Green)
⚠ 50-80% = Needs Review (Yellow)
✗ <50%  = Poor (Red)

Example Output:
─────────────────────────────────
✓ Order Number        : 95/100 (95.0%)
✓ Invoice Value       : 98/100 (98.0%)
⚠ Payment Transaction : 65/100 (65.0%)
✗ Place of Delivery   : 32/100 (32.0%)
─────────────────────────────────
```

## 🚀 Optimization Opportunities

```
Current:     Sequential Processing
Future:      Parallel Processing

Single Thread:
PDF 1 → PDF 2 → PDF 3 → PDF 4
(10 seconds total)

Multi-Thread:
PDF 1 ─┐
PDF 2 ─┼→ Process
PDF 3 ─┤
PDF 4 ─┘
(3 seconds total)
```

---

## Summary

This architecture provides:
- ✅ Clear separation of concerns
- ✅ Modular design for easy maintenance
- ✅ Flexible pattern matching
- ✅ Robust error handling
- ✅ User-friendly output
- ✅ Scalable batch processing
