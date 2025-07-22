SELECT
    name AS "Invoice ID:Link/Sales Invoice:120",
    customer_name AS "Customer",
    posting_date AS "Posting Date:Date",
    tax_category AS "Tax Category",
    net_total AS "Net Total:Currency",
    total_taxes_and_charges AS "Taxes:Currency",
    grand_total AS "Grand Total:Currency"
FROM
    `tabSales Invoice`
WHERE
    docstatus = 1
    AND posting_date BETWEEN %(from_date)s AND %(to_date)s
    AND company = %(company)s
