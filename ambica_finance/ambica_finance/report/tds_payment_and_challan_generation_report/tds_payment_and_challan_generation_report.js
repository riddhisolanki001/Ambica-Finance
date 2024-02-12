// Copyright (c) 2024, riddhi and contributors
// For license information, please see license.txt

frappe.query_reports["TDS Payment and Challan generation Report"] = {
	"filters": [
		{
            "fieldname": "sheet",
            "fieldtype": "Select",
            "label": "Sheet",
			"options": [
                {"value": "sheet1", "label": "Company Details"},
                {"value": "sheet2", "label": "Challan Details"},
                {"value": "sheet2", "label": "Employee Details"},
                {"value": "sheet2", "label": "Section"},
                {"value": "sheet2", "label": "Remarks"},
                {"value": "sheet2", "label": "Read me"}
            ],
            "default": "sheet1"
        }
	]
};
