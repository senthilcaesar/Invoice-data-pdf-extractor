# Invoice Data Conversion Scripts

## Overview

This folder contains two Python scripts that help you convert invoice data from CSV (Excel-like) files into SQL database format. Think of it as translating your invoice spreadsheet into a language that databases can understand and store.

---

## Files Included

1. **csv_to_mysql_sql.py** - Sample/template script
2. **convert_invoice_to_sql.py** - Your actual invoice converter
3. **invoice_data_mysql.sql** - The generated SQL file (ready to import into database)

---

## What Do These Scripts Do?

### Simple Explanation

Imagine you have all your invoice data in an Excel spreadsheet. You want to put this data into a proper database (like MySQL) so you can:
- Search through it quickly
- Run reports and analytics
- Keep it organized and secure
- Share it with other applications

These Python scripts automatically read your spreadsheet and create a SQL file that contains all the instructions needed to:
1. Create a database table
2. Insert all your invoice records into that table

It's like having a robot assistant that translates your spreadsheet into database language!

---

## Script 1: csv_to_mysql_sql.py

### What it does:
This is a **sample template script** that shows how to convert a different invoice CSV file called "all_invoices.csv" into SQL format.

### Main features:
- Reads invoice data from a CSV file
- Cleans up the data (removes commas from numbers, fixes date formats)
- Creates SQL statements to build a database table
- Generates INSERT statements to put all the data into the database

### The data it handles:
- PDF filenames
- Order numbers and dates
- Invoice numbers and values
- Product descriptions
- Quantities and HSN codes
- Payment information
- Shipping addresses

### Think of it as:
A blueprint or recipe that shows you how the conversion process works.

---

## Script 2: convert_invoice_to_sql.py

### What it does:
This is **your actual working script** that converts YOUR invoice data (invoice_data_with_profit.csv) into a MySQL database file.

### Main features:
- Reads your invoice data from "invoice_data_with_profit.csv"
- Cleans and formats all the data properly
- Handles 22 different columns of information
- Creates a complete SQL file ready to import

### The data it handles:
All the same fields as Script 1, PLUS:
- **Year, Month, Day** - Breakdown of order dates
- **Day of Week** - Which day the order was placed (Monday, Tuesday, etc.)
- **Week of Year** - Which week number (1-52)
- **State** - Which Indian state the order came from
- **Profit** - The profit amount for each order

### Output:
Creates a file called **invoice_data_mysql.sql** containing:
- Instructions to create a database called "food_business"
- Instructions to create an "invoices" table
- 103 INSERT statements (one for each invoice record)

### Think of it as:
A translator that takes your spreadsheet and writes out all the database commands needed to store that information permanently.

---

## How These Scripts Work (Step by Step)

### Step 1: Read the CSV File
```
The script opens your CSV file like opening a spreadsheet
```

### Step 2: Clean the Data
```
- Removes extra commas from numbers (249,000 → 249000)
- Fixes date formats (11/12/2025 → 2025-12-11)
- Handles empty cells properly
- Removes special characters that might cause problems
```

### Step 3: Create Database Structure
```
Writes SQL commands to:
- Create a database named "food_business"
- Create a table named "invoices" with 22 columns
- Define what type of data each column can hold (text, numbers, dates)
```

### Step 4: Generate Insert Commands
```
For each row in your spreadsheet:
- Creates an INSERT statement
- Properly formats all the values
- Escapes special characters (like apostrophes in names)
- Handles NULL values for empty cells
```

### Step 5: Save Everything
```
Writes all the SQL commands to a file that you can:
- Import directly into MySQL
- Share with your database administrator
- Use to recreate the database anywhere
```

---

## What's in the Generated SQL File?

The **invoice_data_mysql.sql** file contains:

### 1. Database Creation
```sql
CREATE DATABASE IF NOT EXISTS food_business;
USE food_business;
```
*Creates a database called "food_business" to store all your invoice data*

### 2. Table Structure
```sql
CREATE TABLE `invoices` (
    pdf_filename VARCHAR(50),
    order_number VARCHAR(50),
    order_date DATE,
    ...22 columns total...
);
```
*Defines what the table looks like and what kind of data each column holds*

### 3. Data Insertion (103 records)
```sql
INSERT INTO `invoices` VALUES (...);
INSERT INTO `invoices` VALUES (...);
...103 times...
```
*Adds all 103 invoice records into the table*

---

## Key Differences Between the Two Scripts

| Feature | csv_to_mysql_sql.py | convert_invoice_to_sql.py |
|---------|---------------------|---------------------------|
| Purpose | Sample/Template | Your actual converter |
| Input File | all_invoices.csv | invoice_data_with_profit.csv |
| Output File | food_business_mysql.sql | invoice_data_mysql.sql |
| Columns | 15 columns | 22 columns (includes profit, state, date breakdowns) |
| Use Case | Learning/Reference | Production use |

---

## How to Use These Scripts

### Prerequisites:
You need Python installed with the **pandas** library.

### To run the script:

1. Make sure your CSV file is in the same folder
2. Open a terminal/command prompt
3. Run the command:
   ```bash
   python convert_invoice_to_sql.py
   ```
4. The script will create **invoice_data_mysql.sql**
5. Import this SQL file into your MySQL database

### To import into MySQL:
```bash
mysql -u your_username -p < invoice_data_mysql.sql
```
*This command feeds the SQL file into MySQL, creating the database and adding all your data*

---

## What Gets Created in Your Database?

After running the SQL file, you'll have:

- **Database:** food_business
- **Table:** invoices (with 103 rows)
- **Columns:** 22 different fields tracking everything about each invoice

You can then run queries like:
- "Show me all orders from Tamil Nadu"
- "What's my total profit for December 2025?"
- "Which products sell best on weekends?"
- "How many orders did I get each month?"

---

## Common Terms Explained

| Term | What It Means |
|------|---------------|
| **CSV** | Comma-Separated Values - a simple spreadsheet format |
| **SQL** | Structured Query Language - the language databases speak |
| **MySQL** | A popular free database system |
| **INSERT** | A command that adds data to a database |
| **VARCHAR** | A data type for text (like names, addresses) |
| **DECIMAL** | A data type for precise numbers (like money: 249.00) |
| **DATE** | A data type for dates (YYYY-MM-DD format) |
| **DATETIME** | A data type for dates with time (YYYY-MM-DD HH:MM:SS) |
| **NULL** | Represents an empty/missing value |

---

## Benefits of Converting to SQL

### Why not just keep using Excel/CSV?

1. **Speed:** Databases can search millions of records instantly
2. **Security:** Better control over who can see/edit data
3. **Integrity:** Prevents duplicate or invalid data
4. **Relationships:** Can link invoices to customers, products, etc.
5. **Scalability:** Handles growing data much better than spreadsheets
6. **Multi-user:** Many people can access safely at the same time
7. **Backup:** Easier to backup and restore
8. **Analytics:** Much more powerful querying and reporting

---

## Example Use Cases

### Business Intelligence:
- "What's my monthly revenue trend?"
- "Which states generate the most profit?"
- "What are my best-selling products?"

### Operations:
- "Show all unpaid invoices"
- "Find orders from last week"
- "List customers who ordered more than 5 times"

### Analytics:
- "What's the average order value by state?"
- "Which day of the week has most sales?"
- "Calculate profit margins by product"

---

## Troubleshooting

### If the script doesn't run:
1. Check that Python is installed: `python --version`
2. Install pandas if missing: `pip install pandas`
3. Make sure the CSV file path is correct
4. Check for any error messages in the console

### If data looks wrong:
1. Open the generated SQL file in a text editor
2. Check a few INSERT statements
3. Verify dates and numbers are formatted correctly
4. Make sure special characters are properly escaped

---

## Summary

These scripts are your **automated data translators**. They take your invoice spreadsheet and transform it into a format that professional databases can use. This lets you move from simple spreadsheets to powerful database-driven business intelligence!

Think of it as upgrading from a paper filing cabinet to a searchable, organized digital system that can answer complex questions about your business in seconds.

---

## Need Help?

If you need to modify these scripts or have questions:
1. The code is well-commented to explain what each section does
2. The pandas library documentation: https://pandas.pydata.org/
3. MySQL documentation: https://dev.mysql.com/doc/

Happy data organizing! 🚀
