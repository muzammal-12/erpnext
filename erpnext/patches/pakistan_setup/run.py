import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def execute():
    def add_custom_fields():
        print("Creating custom fields for NIC, NTN, STRN...")

        common_fields = [
            dict(fieldname='tax_nic', label='NIC Number', fieldtype='Data', insert_after='tax_id', reqd=0),
            dict(fieldname='tax_ntn', label='NTN Number', fieldtype='Data', insert_after='tax_nic', reqd=0),
            dict(fieldname='tax_strn', label='STRN Number', fieldtype='Data', insert_after='tax_ntn', reqd=0),
        ]

        for doctype in ['Customer', 'Supplier', 'Employee']:
            for field in common_fields:
                create_custom_field(doctype, field, ignore_validate=True)

        print("Adding NIC Issue/Expiry Dates to Employee...")
        extra_fields = [
            dict(fieldname='nic_issue_date', label='NIC Issue Date', fieldtype='Date', insert_after='tax_strn'),
            dict(fieldname='nic_expiry_date', label='NIC Expiry Date', fieldtype='Date', insert_after='nic_issue_date'),
        ]
        for field in extra_fields:
            create_custom_field('Employee', field, ignore_validate=True)

    def create_tax_accounts(company_name):
        print(f"Creating tax accounts for company: {company_name}")
        parent_account = frappe.db.get_value("Account", {
            "company": company_name,
            "account_name": "Duties and Taxes"
        }, "name")

        if not parent_account:
            print("❌ Could not find 'Duties and Taxes' parent account. Please check your Chart of Accounts.")
            return

        tax_accounts = [
            ("Sales Tax on Goods", "Sales tax applicable on goods"),
            ("Sales Tax on Services", "Sales tax applicable on services"),
            ("Further Tax", "Additional FBR tax on unregistered buyers"),
            ("Extra Tax", "Extra tax for specific conditions")
        ]

        for acc_name, desc in tax_accounts:
            if not frappe.db.exists("Account", {"company": company_name, "account_name": acc_name}):
                account = frappe.get_doc({
                    "doctype": "Account",
                    "account_name": acc_name,
                    "parent_account": parent_account,
                    "company": company_name,
                    "is_group": 0,
                    "account_type": "Tax",
                    "root_type": "Liability",
                    "report_type": "Balance Sheet",
                    "account_currency": frappe.get_value("Company", company_name, "default_currency"),
                    "description": desc
                })
                account.insert()
                print(f"✔ Created account: {acc_name}")
            else:
                print(f"✔ Account already exists: {acc_name}")

    def create_sales_tax_templates(company_name):
        print("Creating Sales Taxes and Charges Templates...")

        def create_template(title, rate, account_head):
            if not frappe.db.exists("Sales Taxes and Charges Template", {
                "title": title, "company": company_name
            }):
                template = frappe.get_doc({
                    "doctype": "Sales Taxes and Charges Template",
                    "title": title,
                    "company": company_name,
                    "is_default": 0,
                    "taxes": [{
                        "charge_type": "On Net Total",
                        "account_head": account_head,
                        "rate": rate,
                        "description": f"{title} @ {rate}%"
                    }]
                })
                template.insert()
                print(f"✔ Created tax template: {title}")
            else:
                print(f"✔ Tax template already exists: {title}")

        accs = {
            "Sales Tax on Goods": 17.0,
            "Sales Tax on Services": 13.0,
            "Further Tax": 3.0,
            "Extra Tax": 5.0
        }

        for acc_name, rate in accs.items():
            full_account_name = frappe.db.get_value("Account", {
                "company": company_name,
                "account_name": acc_name
            }, "name")
            if full_account_name:
                create_template(acc_name, rate, full_account_name)
            else:
                print(f"⚠ Could not find account for {acc_name}, skipping template.")

    company = frappe.db.get_single_value("Global Defaults", "default_company")
    if not company:
        print("❌ No default company set. Please set it first.")
        return

    add_custom_fields()
    create_tax_accounts(company)
    create_sales_tax_templates(company)

    frappe.db.commit()
    print("🎉 Pakistan Workspace Setup Completed.")
