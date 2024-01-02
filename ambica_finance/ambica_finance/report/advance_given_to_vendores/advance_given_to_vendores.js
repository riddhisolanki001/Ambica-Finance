// Copyright (c) 2024, riddhi and contributors
// For license information, please see license.txt

frappe.query_reports["Advance Given To vendores"] = {
	"filters": [
		{
            "fieldname": "from_date",
            "fieldtype": "Date",
            "label": "From Date",
        },
		{
            "fieldname": "to_date",
            "fieldtype": "Date",
            "label": "To Date",
        },
	],
	"onload": function (report) {
        setTimeout(function () {
            report.set_filter_value('from_date', null);
            report.set_filter_value('to_date', null);
        }, 1000); // Adjust the delay as needed
    }
};
