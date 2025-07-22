import frappe

@frappe.whitelist()
def upload_srb_to_iris(from_date, to_date, company):
    try:
        # simulate processing
        return f"SRB Report from {from_date} to {to_date} for {company} uploaded to IRIS (mock)."
    except Exception as e:
        frappe.throw(f"Upload to IRIS failed: {e}")

