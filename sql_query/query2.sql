SELECT * 
FROM invoices;

SELECT qty, invoice_value, profit
FROM invoices
WHERE qty > 1;

SELECT DISTINCT state
FROM invoices;

SELECT *
FROM invoices
WHERE order_date > '2025-12-31';

SELECT *
FROM invoices
WHERE state LIKE "TAMI__";




