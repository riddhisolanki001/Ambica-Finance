// Copyright (c) 2024, riddhi and contributors
// For license information, please see license.txt

frappe.query_reports["e-TDS-26Q4-2223"] = {
	"filters": [
		{
			"label": __("Select"),
			"fieldname": "select",
			"fieldtype": "Select",
			"options": ["Company Details","Challan Details", "Deductee Details", "Section", "Deductee Code","Remarks"],
            "default": "Company Details"			
		}
	],
};
