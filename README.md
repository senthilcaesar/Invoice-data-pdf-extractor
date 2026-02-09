# Sales Performance Dashboard

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

### 2. Sales Performance Dashboard (Web App)
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

The dashboard implements a sophisticated profitability engine. Profit is calculated using the following primary formula:

```text
Profit = Total Revenue - (Total Base Costs + Dynamic Shipping Cost)
```

### 1. How Each Variable is Computed

#### **A. Total Revenue**
Revenue is calculated based on the **Selling Price (SP) before GST** for all products identified in the order description, multiplied by the quantity.
*   **Formula**: `(Sum of Unit SP before GST) * Quantity (Qty)`
*   **Source**: SP values are retrieved from the internal master data based on product name matching.

#### **B. Total Base Costs**
This includes all fixed costs associated with the physical product and the sale transaction.
*   **Formula**: `(Purchase Cost + Referral Fee + Packing Cost) * Quantity (Qty)`
*   **Components**: 
    *   **Purchase Cost**: The cost at which the item was bought/manufactured.
    *   **Referral Fee**: Marketplace commission (e.g., Amazon referral fees).
    *   **Packing Cost**: Cost of materials and labor for packaging.

#### **C. Dynamic Shipping Cost**
Shipping is **not** a simple flat fee per item. It is calculated dynamically based on the **Total Weight** of the entire order.
*   **Weight Extraction**: The system scans product descriptions for weight markers (e.g., `1kg`, `500g`).
*   **Total weight**: `Unit Weight * Quantity (Qty)`.
*   **Shipping Tiers**:
    | Total Order Weight | Shipping Cost | Calculation Logic |
    | :--- | :--- | :--- |
    | **0 - 500g** | ₹76 | Flat rate |
    | **500g - 1kg** | ₹100 | Flat rate |
    | **1kg - 2kg** | ₹143 | Flat rate |
    | **2kg - 5kg** | ₹143 + (₹40/kg) | `143 + ceil(Weight - 2.0) * 40` |
    | **Above 5kg** | ₹263 + (₹26/kg) | `263 + ceil(Weight - 5.0) * 26` |

---

### 3. Detailed Analytics Guide
For a deeper understanding of the statistical visualizations (Box Plots, Histograms, etc.) and the outlier filtering logic (IQR Method) used in the dashboard, please refer to the **[Analytics & Visualization Guide](ANALYTICS_GUIDE.md)**.

---

Let's calculate the profit for an order of **2 units** of **"Amudham Naturals Raw Peanuts, 1kg Pack"**.

**1. Product Data (per unit):**
- **SP before GST**: ₹286
- **Purchase Cost**: ₹130
- **Referral Fee**: ₹7.08
- **Packing Cost**: ₹20
- **Unit Weight**: 1.0 kg

**2. Variable Calculations:**
- **Total Revenue**: `₹286 * 2` = **₹572.00**
- **Total Base Costs**: `(₹130 + ₹7.08 + ₹20) * 2` = `₹157.08 * 2` = **₹314.16**
- **Total Weight**: `1.0kg * 2` = **2.0 kg**
- **Dynamic Shipping Cost**: (For 2.0kg tier) = **₹143.00**

**3. Final Profit Calculation:**
- `Profit = ₹572.00 - (₹314.16 + ₹143.00)`
- `Profit = ₹572.00 - ₹457.16`
- **Resulting Profit = ₹114.84**

---

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
