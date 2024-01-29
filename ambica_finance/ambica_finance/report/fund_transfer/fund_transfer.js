frappe.query_reports["Fund Transfer"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		}
	],
	// "onload": function (report) {
    //     setTimeout(function () {
    //         report.set_filter_value('from_date', null);
    //         report.set_filter_value('to_date', null);
    //     }, 1000); 
    // }
};