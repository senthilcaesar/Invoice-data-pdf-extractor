SELECT *
FROM invoices;

SELECT state, MAX(profit), MIN(profit), COUNT(profit)
FROM invoices
GROUP BY state;

-- This query is essentially creating a summary report of how your customers prefer to pay.
-- It looks through all your invoices, groups them by how people paid (like Cash or Card), and counts how many sales each method had. 
-- Finally, it sorts the list so the most frequently used payment method appears at the top.
SELECT mode_of_payment, COUNT(*) as count
FROM invoices
GROUP BY mode_of_payment
ORDER BY count DESC;




-- Limit
SELECT *
FROM invoices
ORDER BY order_date DESC
LIMIT 5;


























