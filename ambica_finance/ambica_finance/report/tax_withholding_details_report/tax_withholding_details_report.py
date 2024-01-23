# Copyright (c) 2024, riddhi and contributors
# For license information, please see license.txt

import frappe
from frappe import _
 

def execute(filters=None):
	columns = [
		{
			"label": _("Section Code"),
			"options": "TDS Master",
			"fieldname": "custom_section",
			"fieldtype": "Link",
			"width": 90,
		},
		{
			"label": _("Tax Withholding Category"),
			"options": "Tax Withholding Category",
			"fieldname": "tax_withholding_category",
			"fieldtype": "Link",
			"width": 90,
		},
		{
			"label": _("TDS Rate %"),
			"fieldname": "tax_withholding_rate",
			"fieldtype": "Percent",
			"width": 60,
		},
		{
			"label": _("Total Amount"),
			"fieldname": "total",
			"fieldtype": "Float",
			"width": 120,
		},
		{
			"label": _("Base Total"),
			"fieldname": "total",
			"fieldtype": "Float",
			"width": 120,
		},
		{
			"label": _("Tax Amount"),
			"fieldname": "tax_amount",
			"fieldtype": "Float",
			"width": 120,
		},
		{
			"label": _("Grand Total"),
			"fieldname": "grand_total",
			"fieldtype": "Float",
			"width": 120,
		},
	]

	sql = """
			SELECT 
            	pi.tax_withholding_category,
				SUM(pi.grand_total) AS grand_total,
				SUM(pi.total) AS total,
				SUM(ptc.tax_amount) AS tax_amount,
				twc.custom_section,
				twr.tax_withholding_rate
			FROM `tabPurchase Invoice` AS pi
			INNER JOIN (
				SELECT *
				FROM `tabPurchase Taxes and Charges`
				WHERE parenttype = "Purchase Invoice" AND account_head LIKE "%TDS%"
			) AS ptc
			ON ptc.parent = pi.name
			INNER JOIN `tabTax Withholding Category` as twc ON twc.name = pi.tax_withholding_category
			LEFT JOIN `tabTax Withholding Rate` as twr ON twr.parent = twc.name
		"""
	
	if filters:
		company = filters.get("company")
		from_date = filters.get("from_date")
		to_date = filters.get("to_date")

		sql += f"""
				WHERE pi.company = '{company}'
				AND pi.posting_date BETWEEN '{from_date}' AND '{to_date}'
			"""
	sql += "GROUP BY twc.custom_section"
	data = frappe.db.sql(sql,as_dict=True)
	return columns, data

