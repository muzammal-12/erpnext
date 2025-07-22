import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = [
        {"label": "Invoice No", "fieldname": "name", "fieldtype": "Link", "options": "Sales Invoice", "width": 120},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 180},
        {"label": "STRN", "fieldname": "tax_strn", "fieldtype": "Data", "width": 120},
        {"label": "Taxable Amount", "fieldname": "taxable_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Sales Tax", "fieldname": "sales_tax", "fieldtype": "Currency", "width": 120}
    ]

    data = []
    if not filters:
        return columns, data

    invoices = frappe.get_all(
        "Sales Invoice",
        filters={
            "docstatus": 1,
            "posting_date": ["between", [filters.from_date, filters.to_date]],
            "company": filters.company
        },
        fields=["name", "posting_date", "customer"]
    )

    for inv in invoices:
        invoice = frappe.get_doc("Sales Invoice", inv.name)
        strn = frappe.db.get_value("Customer", invoice.customer, "tax_strn")
        taxable = 0
        tax = 0

        for item in invoice.taxes:
            if "Sales Tax on Services" in item.account_head:
                tax += flt(item.tax_amount)
                taxable += flt(item.taxable_amount)

        if tax > 0:
            data.append({
                "name": invoice.name,
                "posting_date": invoice.posting_date,
                "customer": invoice.customer,
                "tax_strn": strn,
                "taxable_amount": taxable,
                "sales_tax": tax
            })

    return columns, data
