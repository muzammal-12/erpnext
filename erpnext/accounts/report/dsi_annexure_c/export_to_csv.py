import frappe
import csv
import os
from frappe.utils import get_site_path

def export_dsi_to_csv(from_date, to_date, company):
    filename = f"DSI_{from_date}_to_{to_date}.csv"
    file_path = os.path.join(get_site_path("private", "files"), filename)

    query = """
        SELECT
            si.name AS "Invoice No",
            si.posting_date AS "Date",
            si.customer_name AS "Customer",
            si.tax_id AS "NTN/STRN",
            si.net_total AS "Net Amount",
            si.total_taxes_and_charges AS "Tax Amount",
            si.rounded_total AS "Total",
            si.company AS "Company"
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 1
          AND si.posting_date BETWEEN %s AND %s
          AND si.company = %s
        ORDER BY si.posting_date ASC
    """
    rows = frappe.db.sql(query, (from_date, to_date, company), as_list=True)

    headers = [
        "Invoice No", "Date", "Customer", "NTN/STRN",
        "Net Amount", "Tax Amount", "Total", "Company"
    ]

    with open(file_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    frappe.msgprint(f"✅ Exported DSI to {file_path}")

@frappe.whitelist(allow_guest=True)
def schedule_dsi_export():
    from datetime import date
    from .export_to_csv import export_dsi_to_csv

    today = date.today()
    first_day = today.replace(day=1)
    last_day = today
    export_dsi_to_csv(str(first_day), str(last_day), "RABC Pvt Ltd")
