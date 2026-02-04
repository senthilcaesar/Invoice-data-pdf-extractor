import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
CSV_FILE = "invoice_data_with_profit.csv"
SQL_FILE = "invoice_data_mysql.sql"
TABLE_NAME = "invoices"

# -----------------------------
# READ CSV
# -----------------------------
df = pd.read_csv(CSV_FILE)

# -----------------------------
# CLEAN DATA
# -----------------------------

# Invoice Value: ensure it's a float
df["Invoice Value"] = pd.to_numeric(df["Invoice Value"], errors="coerce")

# Profit: ensure it's a float
df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")

# Order Date: YYYY-MM-DD format (already appears to be in this format)
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%Y-%m-%d",
    errors="coerce"
).dt.strftime("%Y-%m-%d")

# Date & Time: Clean and convert
# Handle the format "DD/MM/YYYY, HH:MM:SS\nhrs" or "DD/MM/YYYY,\nHH:MM:SS hrs"
df["Date & Time"] = (
    df["Date & Time"]
    .astype(str)
    .str.replace("\n", " ", regex=False)
    .str.replace(" hrs", "", regex=False)
    .str.strip()
)

df["Date & Time"] = pd.to_datetime(
    df["Date & Time"],
    format="%d/%m/%Y, %H:%M:%S",
    errors="coerce"
).dt.strftime("%Y-%m-%d %H:%M:%S")

# Qty & HSN Code
df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce").fillna(0).astype(int)
df["HSN Code"] = pd.to_numeric(df["HSN Code"], errors="coerce").fillna(0).astype(int)

# Year, Month, Day, WeekOfYear
df["Year"] = pd.to_numeric(df["Year"], errors="coerce").fillna(0).astype(int)
df["Month"] = pd.to_numeric(df["Month"], errors="coerce").fillna(0).astype(int)
df["Day"] = pd.to_numeric(df["Day"], errors="coerce").fillna(0).astype(int)
df["WeekOfYear"] = pd.to_numeric(df["WeekOfYear"], errors="coerce").fillna(0).astype(int)

# Replace NaN with NULL marker
df = df.where(pd.notnull(df), None)

# -----------------------------
# WRITE MYSQL SQL FILE
# -----------------------------
with open(SQL_FILE, "w", encoding="utf-8") as f:

    # CREATE DATABASE (optional)
    f.write("CREATE DATABASE IF NOT EXISTS food_business;\n")
    f.write("USE food_business;\n\n")

    # DROP + CREATE TABLE
    f.write(f"DROP TABLE IF EXISTS `{TABLE_NAME}`;\n")
    f.write(f"""
CREATE TABLE `{TABLE_NAME}` (
    pdf_filename VARCHAR(50),
    order_number VARCHAR(50),
    order_date DATE,
    place_of_delivery VARCHAR(50),
    invoice_number VARCHAR(50),
    invoice_value DECIMAL(12,2),
    description TEXT,
    qty INT,
    hsn_code INT,
    asin VARCHAR(20),
    sku VARCHAR(50),
    payment_transaction_id VARCHAR(100),
    mode_of_payment VARCHAR(30),
    date_time DATETIME,
    shipping_address TEXT,
    year INT,
    month INT,
    day INT,
    day_of_week VARCHAR(20),
    week_of_year INT,
    state VARCHAR(50),
    profit DECIMAL(12,2)
);
\n""")

    # INSERT STATEMENTS
    for _, row in df.iterrows():
        values = []
        for val in row:
            if val is None:
                values.append("NULL")
            elif isinstance(val, (int, float)):
                values.append(str(val))
            else:
                # Escape single quotes by doubling them
                escaped = str(val).replace("'", "''")
                values.append(f"'{escaped}'")

        f.write(
            f"INSERT INTO `{TABLE_NAME}` VALUES ({', '.join(values)});\n"
        )

print(f"MySQL SQL file created successfully: {SQL_FILE}")
print(f"Total records converted: {len(df)}")
