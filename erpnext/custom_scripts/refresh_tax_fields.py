import frappe

def refresh_tax_fields():
    customer_fields = [
        {
            "fieldname": "tax_nic",
            "label": "NIC Number",
            "fieldtype": "Data",
            "reqd": 0,
            "insert_after": "customer_type",
            "description": "National Identity Card"
        },
        {
            "fieldname": "tax_ntn",
            "label": "NTN Number",
            "fieldtype": "Data",
            "reqd": 0,
            "insert_after": "tax_nic",
            "description": "National Tax Number"
        },
        {
            "fieldname": "tax_strn",
            "label": "STRN Number",
            "fieldtype": "Data",
            "reqd": 0,
            "insert_after": "tax_ntn",
            "description": "Sales Tax Registration Number"
        },
    ]

    for field in customer_fields:
        df_name = f"Customer-{field['fieldname']}"
        try:
            if frappe.db.exists("Custom Field", df_name):
                frappe.delete_doc("Custom Field", df_name, force=True)
                print(f"🗑️ Removed: {df_name}")
        except Exception as e:
            print(f"⚠️ Error removing {df_name}: {e}")

        try:
            cf = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Customer",
                **field
            })
            cf.insert()
            print(f"✅ Created: {df_name}")
        except Exception as e:
            print(f"❌ Error creating {df_name}: {e}")

    frappe.db.commit()
    print("🎉 Done refreshing NIC, NTN, STRN fields.")
