frappe.pages['pakistan-tax-setup'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Pakistan Tax Setup',
        single_column: true
    });

    $(page.body).html(`
        <div class="row">
            <div class="col-md-8">
                <div class="card mb-3">
                    <div class="card-body">
                        <h4>Step 1: Create Sales Tax Accounts</h4>
                        <p>This will create required tax accounts under Duties and Taxes.</p>
                        <button class="btn btn-primary btn-sm" onclick="run_pakistan_patch()">Run Setup</button>
                    </div>
                </div>
                <div class="card mb-3">
                    <div class="card-body">
                        <h4>Step 2: Add Tax Fields</h4>
                        <p>NIC, NTN, STRN fields will be added to Customer, Supplier, Employee.</p>
                    </div>
                </div>
                <div class="card mb-3">
                    <div class="card-body">
                        <h4>Step 3: Create First Tax Invoice</h4>
                        <a href="/app/sales-invoice/new" class="btn btn-outline-primary btn-sm">Create Invoice</a>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h4>Step 4: View FBR Sales Report</h4>
                        <a href="/app/report/domestic-sales-invoices" class="btn btn-outline-info btn-sm">Open Report</a>
                    </div>
                </div>
            </div>
        </div>
    `);
};

function run_pakistan_patch() {
    frappe.call({
        method: "erpnext.patches.pakistan_setup.run.execute",
        callback: function(r) {
            frappe.msgprint("✅ Tax setup patch completed.");
        }
    });
}
