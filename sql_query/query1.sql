SELECT
    description as Product_Name,
    COUNT(*) as Total_Orders,
    SUM(Qty) as Total_Units_Sold,
    SUM(invoice_value) as Total_Revenue
FROM invoices
GROUP BY description
ORDER BY Total_Revenue DESC
LIMIT 10;
