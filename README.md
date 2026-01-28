# Amazon Invoice Data Extractor & Analytics Dashboard

A complete solution for extracting data from Amazon invoice PDFs and visualizing business insights through an interactive web dashboard.

## 🌐 Live Demo

**Analytics Dashboard**: [https://invoice-data-pdf-extractor.streamlit.app/](https://invoice-data-pdf-extractor.streamlit.app/)

Try the live dashboard with sample data or upload your own extracted invoice CSV!

## 📊 What It Does

This project transforms Amazon order invoice PDFs into actionable business insights through a two-part workflow:

### 1. PDF Invoice Extractor (Python Scripts)
Processes Amazon invoice PDFs in batch and extracts structured data including:
- Order Number, Invoice Number, Invoice Value
- Product Description, HSN Code, ASIN, SKU
- Payment Details (Transaction ID, Mode, Date & Time)
- Shipping Address and Place of Delivery

### 2. Analytics Dashboard (Web App)
Upload the extracted CSV to visualize:
- **Overview Metrics**: Total orders, revenue, data quality
- **Geographic Analysis**: State-wise revenue with interactive charts (Bar/Pie/Treemap)
- **Temporal Trends**: Monthly order volume and revenue tracking
- **Interactive Visualizations**: Powered by Plotly with hover, zoom, and pan controls

## 🚀 Quick Start

### Extract Invoice Data

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. For a **single PDF**:
```bash
python extract_invoice.py
```

3. For **batch processing** (multiple PDFs):
```bash
python extract_invoice_batch.py
```

### View Analytics

**Option 1: Use the Live Dashboard**
- Visit [https://invoice-data-pdf-extractor.streamlit.app/](https://invoice-data-pdf-extractor.streamlit.app/)
- Upload your `all_invoices.csv` file
- Explore interactive visualizations

**Option 2: Run Locally**
```bash
streamlit run app.py
```

## 📋 Features

### PDF Extraction
- Extracts 13+ fields from Amazon invoices
- Handles batch processing of multiple PDFs
- Intelligent description parsing (removes serial numbers, ASIN, SKU)
- Supports various date/time formats
- Debug mode for troubleshooting

### Analytics Dashboard
- **Professional UI**: Custom-designed interface with Inter font family
- **Interactive Charts**: Plotly-powered visualizations
- **Sample Data**: Built-in demo dataset for testing
- **Responsive Design**: Works on desktop and mobile
- **Light Mode**: Optimized for readability

## 📈 Profit & Shipping Calculation Logic

The dashboard implements a sophisticated profitability engine that accounts for variable product costs and non-linear shipping rates.

### 1. Dynamic Shipping Cost Calculation
Shipping is calculated based on the **Total Order Weight** using a tiered fee structure:

1.  **Weight Extraction**: The system automatically scans product descriptions for weight markers (e.g., `(350g)`, `500 g`, `1kg`).
2.  **Total Weight Calculation**: `Item Weight * Quantity (Qty)`.
3.  **Tiered Pricing Application**:
    | Weight Tier | Cost | Formula Details |
    | :--- | :--- | :--- |
    | **0 - 500g** | ₹76 | Flat rate |
    | **500g - 1kg** | ₹100 | Flat rate |
    | **1kg - 2kg** | ₹143 | Flat rate |
    | **2kg - 5kg** | ₹143 + (₹40/kg) | `143 + ceil(Weight - 2.0) * 40` |
    | **Above 5kg** | ₹263 + (₹26/kg) | `263 + ceil(Weight - 5.0) * 26` |

*Note: The script uses `math.ceil()` on additional weight, so partial kilograms are rounded up (e.g., 2.2kg is charged as 3kg).*

### 2. Profit Margin Calculation
Profit is calculated for each order by matching product descriptions against a master cost matrix (`df_data`).

**The Multi-Step Formula:**
1.  **Product Matching**: The system identifies the specific product and retrieves its specific **Purchase**, **Referral**, and **Packing** costs.
2.  **Multi-Item Support**: If a description contains multiple distinct products, the system sums the margins for all unique matches.
3.  **Revenue Generation**: `SP (before GST) * Quantity`.
4.  **Base Cost Calculation**: `(Purchase + Referral + Packing) * Quantity`.
5.  **Final Net Profit**:
    ```text
    Profit = Revenue - (Base Costs + Dynamic Shipping Cost)
    ```

---

## 📁 Output Format

The extractor generates CSV files with these columns:

| Column | Description | Example |
|--------|-------------|---------|
| PDF Filename | Source PDF file | invoice_001.pdf |
| Order Number | Amazon order ID | 407-1234567-8901234 |
| Order Date | Date of order | 02.11.2025 |
| Place of Delivery | Delivery state | TAMIL NADU |
| Invoice Number | Invoice ID | IN-BLR1-1234567 |
| Invoice Value | Total amount | 1299.00 |
| Description | Product description | Amudham Naturals 100% Pure Ragi Flour... |
| HSN Code | Tax classification | 11029090 |
| ASIN | Amazon product ID | B0FW7291VR |
| SKU | Seller SKU | MS-H2GY-GWJX |
| Payment Transaction ID | Payment reference | 1234567890 |
| Mode of Payment | Payment method | NetBanking |
| Date & Time | Transaction timestamp | 02/11/2025,12:58:05 hrs |
| Shipping Address | Full delivery address | Name, Street, City... |

## 🛠️ Configuration

### Extraction Scripts

**Change PDF directory** (in `extract_invoice_batch.py`):
```python
directory_path = "/path/to/your/invoices"
```

**Change page number** (default is page 2):
```python
page_number = 2  # Adjust as needed
```

**Enable debug mode**:
```python
debug_mode = True  # Shows raw text and extraction details
```

### Dashboard

The dashboard automatically processes uploaded CSV files. Configuration is handled via `.streamlit/config.toml` for theme settings.

## 📊 Use Cases

Perfect for Amazon sellers and business analysts who need to:
- Track sales performance across different states/regions
- Identify seasonal trends in orders
- Monitor revenue growth month-over-month
- Analyze product performance by ASIN/SKU
- Generate reports for accounting and tax purposes
- Make data-driven inventory and marketing decisions

## 🔧 Troubleshooting

### Extraction Issues

**Fields not extracting?**
1. Enable debug mode: `debug_mode = True`
2. Check the "RAW TEXT FROM PAGE" output
3. Verify the page number (default is page 2)
4. Adjust regex patterns if your PDF format differs

**Description incomplete?**
- The extractor is optimized for Amazon's table format
- Check the "DESCRIPTION EXTRACTION DEBUG" section
- Modify `stop_keywords` if needed

**Scanned/Image PDFs?**
- PyMuPDF only works with text-based PDFs
- For scanned PDFs, you'll need OCR (pytesseract)

### Dashboard Issues

**CSV upload fails?**
- Ensure CSV has the expected column names
- Check that dates are in DD.MM.YYYY format
- Verify Invoice Value is numeric (no currency symbols in the CSV)

## 📦 Dependencies

**Extraction Scripts:**
- PyMuPDF >= 1.23.0 (PDF text extraction)
- Standard library: csv, re, os, glob

**Analytics Dashboard:**
- streamlit >= 1.41.0
- pandas >= 2.1.0
- plotly >= 5.18.0
- matplotlib >= 3.8.0
- seaborn >= 0.13.0

## 📂 Project Structure

```
.
├── extract_invoice.py          # Single PDF extraction
├── extract_invoice_batch.py    # Batch processing
├── app.py                      # Analytics dashboard
├── analysis.py                 # Data analysis script
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # Dashboard theme config
└── README.md                   # This file
```

## 🌟 Workflow

1. **Download** Amazon invoice PDFs
2. **Extract** data using `extract_invoice_batch.py`
3. **Upload** the generated CSV to the dashboard
4. **Analyze** your business metrics and trends
5. **Export** insights for reporting

## 📝 Notes

- Designed specifically for Amazon invoice format
- Extracts from page 2 by default (most Amazon invoices)
- Regex patterns may need adjustment for different formats
- Dashboard runs on Streamlit Cloud for easy access
- All data processing happens client-side (secure)

## 🔗 Links

- **Live Dashboard**: [https://invoice-data-pdf-extractor.streamlit.app/](https://invoice-data-pdf-extractor.streamlit.app/)
- **GitHub Repository**: [Your repo URL]

## 📄 License

This project is provided as-is for invoice data extraction and analysis purposes.

---

**Made for Amudham Naturals** 📊
