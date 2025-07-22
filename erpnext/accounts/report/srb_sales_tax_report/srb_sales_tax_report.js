frappe.query_reports["SRB Sales Tax Report"] = {
  filters: [
    {
      fieldname: "from_date",
      label: "From Date",
      fieldtype: "Date",
      default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
      reqd: 1
    },
    {
      fieldname: "to_date",
      label: "To Date",
      fieldtype: "Date",
      default: frappe.datetime.get_today(),
      reqd: 1
    },
    {
      fieldname: "company",
      label: "Company",
      fieldtype: "Link",
      options: "Company",
      default: frappe.defaults.get_user_default("Company"),
      reqd: 1
    }
  ],
  onload: function(report) {
    report.page.add_inner_button("Upload to IRIS", function() {
      const filters = report.get_values();
      frappe.call({
        method: "erpnext.accounts.report.srb_sales_tax_report.export_to_csv.schedule_srb_export",
        args: {
          from_date: filters.from_date,
          to_date: filters.to_date,
          company: filters.company
        },
        callback: function(r) {
          if (r.message && r.message.success) {
            frappe.msgprint("✅ Upload scheduled to IRIS.");
          } else {
            frappe.msgprint("❌ Upload failed.");
          }
        }
      });
    });
  }
};
