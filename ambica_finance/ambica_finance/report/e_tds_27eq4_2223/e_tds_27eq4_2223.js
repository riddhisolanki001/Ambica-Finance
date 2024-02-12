// Copyright (c) 2024, riddhi and contributors
// For license information, please see license.txt

frappe.query_reports["e-TDS-27EQ4-2223"] = {
	"filters": [
		{
			"label": __("Select"),
			"fieldname": "select",
			"fieldtype": "Select",
			"options": ["Company Details","Challan Details", "Deductee Details", "Collection Code", "Deductee Code", "Remarks"],
            "default": "Company Details"			
		}
	]
};
