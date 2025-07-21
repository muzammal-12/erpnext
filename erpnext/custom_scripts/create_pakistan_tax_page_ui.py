# This script creates the Pakistan Tax Setup UI page manually
import frappe

def create_pakistan_tax_page():
    # 1. Create Page record (do not recreate if exists)
    if not frappe.db.exists("Page", "pakistan-tax-setup"):
        frappe.get_doc({
            "doctype": "Page",
            "name": "pakistan-tax-setup",
            "page_name": "pakistan-tax-setup",
            "module": "Accounts",
            "title": "Pakistan Tax Setup",
            "standard": "No",
            "content": "<div id=\"pakistan-tax-setup\"></div>",
            "script": "/assets/js/pakistan_tax_setup_ui.js",
            "style": ""
        }).insert()
        frappe.db.commit()
        print("✅ Created Page: pakistan-tax-setup")
    else:
        print("✅ Page already exists: pakistan-tax-setup")

    # 2. Inject into Accounting workspace sidebar
    ws = frappe.get_doc("Workspace", "Accounting")
    if not any(link.link_to == "pakistan-tax-setup" for link in ws.links):
        ws.append("links", {
            "type": "Page",
            "link_to": "pakistan-tax-setup",
            "label": "Pakistan Tax Setup",
            "icon": "fa fa-flag"
        })
        ws.save()
        frappe.db.commit()
        print("✅ Added Pakistan Tax Setup to Accounting workspace")
    else:
        print("✅ Sidebar link already exists")

    # 3. Create public JS file
    js_path = frappe.get_site_path("public", "js", "pakistan_tax_setup_ui.js")
    frappe.create_folder(js_path.rsplit("/", 1)[0], with_init=True)
    with open(js_path, "w") as f:
        f.write("""
frappe.pages['pakistan-tax-setup'].on_page_load = function(wrapper) {
    let page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Pakistan Tax Setup',
        single_column: true
    });

    $(wrapper).html(`
        <div class='p-4'>
            <p>This is the Pakistan Tax Setup UI page.</p>
            <button class='btn btn-primary' onclick='create_customer_with_tax()'>Create Demo Customer with Tax Info</button>
        </div>
    `);
}

function create_customer_with_tax() {
    frappe.call({
        method: "frappe.client.insert",
        args: {
            doc: {
                doctype: "Customer",
                customer_name: "Demo Tax Customer",
                nic: "35201-1234567-8",
                ntn: "1234567-8",
                strn: "PK-112233"
            }
        },
        callback: function(r) {
            if (!r.exc) {
                frappe.msgprint("✅ Created demo tax customer: " + r.message.name);
            }
        }
    });
}
        """)
    print("✅ Created public JS: pakistan_tax_setup_ui.js")


# Run it in bench console:
# from path.to.this_script import create_pakistan_tax_page
# create_pakistan_tax_page()

