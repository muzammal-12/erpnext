frappe.query_reports["DSI Annexure C"] = {
  filters: [
    {
      fieldname: "from_date",
      label: "From Date",
      fieldtype: "Date",
      reqd: 1,
      default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
    },
    {
      fieldname: "to_date",
      label: "To Date",
      fieldtype: "Date",
      reqd: 1,
      default: frappe.datetime.get_today(),
    },
    {
      fieldname: "company",
      label: "Company",
      fieldtype: "Link",
      options: "Company",
      reqd: 1,
    },
  ],

  onload: function (report) {
    report.page.add_inner_button("Upload to IRIS", function () {
      const filters = report.get_filter_values(true);
      if (!filters) return;

      const url = `/api/method/erpnext.api.tax_report_api.get_dsi_csv?from_date=${filters.from_date}&to_date=${filters.to_date}&company=${filters.company}`;
      window.open(url, "_blank");
    });
  },
};
