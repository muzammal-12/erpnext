import frappe
from frappe.utils import formatdate

def execute(filters=None):
    columns = [
        {"label": "Invoice #", "fieldname": "name", "fieldtype": "Link", "options": "Sales Invoice", "width": 120},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {"label": "Customer", "fieldname": "customer_name", "fieldtype": "Data", "width": 150},
        {"label": "NIC", "fieldname": "tax_nic", "fieldtype": "Data", "width": 130},
        {"label": "NTN", "fieldname": "tax_ntn", "fieldtype": "Data", "width": 130},
        {"label": "STRN", "fieldname": "tax_strn", "fieldtype": "Data", "width": 130},
        {"label": "Net Total", "fieldname": "net_total", "fieldtype": "Currency", "width": 120},
        {"label": "Sales Tax", "fieldname": "total_taxes_and_charges", "fieldtype": "Currency", "width": 120},
    ]

    data = frappe.db.sql("""
        SELECT
            si.name, si.posting_date, si.customer_name,
            si.tax_nic, si.tax_ntn, si.tax_strn,
            si.net_total, si.total_taxes_and_charges
        FROM
            `tabSales Invoice` si
        WHERE
            si.docstatus = 1
            AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
    """, filters, as_dict=True)

    return columns, data
