// Copyright (c) 2024, riddhi and contributors
// For license information, please see license.txt

frappe.query_reports["Party Wise Sales Comparison"] = {
	"filters": [
		{
			"fieldname":"fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options":'Fiscal Year',
			"default": erpnext.utils.get_fiscal_year(frappe.datetime.get_today()),
		},
	]
};
