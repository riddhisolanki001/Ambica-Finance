# Copyright (c) 2024, riddhi and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = [
		{
			"label": "Invoice No.",
			"options": "Sales Invoice",
			"fieldname": "name",
			"fieldtype": "Link",
			# "width": 150,
		},
		{
			"label": "Invoice Date",
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": "Total",
			"fieldname": "total",
			"fieldtype": "Currency",
			"width": 120,
		},
		{
			"label": "Tax Rate",
			"fieldname": "rate",
			"fieldtype": "Percentage",
			# "width": 120,
		},
		{
			"label": "Tax Amount of CGST",
			"fieldname": "cgst_tax_amount",
			"fieldtype": "Currency",
			# "width": 120,
		},
		{
			"label": "Tax Amount of SGST",
			"fieldname": "sgst_tax_amount",
			"fieldtype": "Currency",
			# "width": 120,
		},
		{
			"label": "Tax Amount of IGST",
			"fieldname": "igst_tax_amount",
			"fieldtype": "Currency",
			# "width": 120,
		},
		{
			"label": "Total Taxes and Charges",
			"fieldname": "total_taxes_and_charges",
			"fieldtype": "Currency",
			"width": 120,
		},
		{
			"label": "Grand Total",
			"fieldname": "grand_total",
			"fieldtype": "Currency",
			"width": 150,
		},
	] 

	sql = """
			SELECT 
				si.name,
				si.posting_date,
				SUM(stc.rate) AS rate,
                SUM(CASE WHEN stc.account_head LIKE '%CGST%' THEN stc.tax_amount ELSE 0 END) AS cgst_tax_amount,
                SUM(CASE WHEN stc.account_head LIKE '%SGST%' THEN stc.tax_amount ELSE 0 END) AS sgst_tax_amount,
                SUM(CASE WHEN stc.account_head LIKE '%IGST%' THEN stc.tax_amount ELSE 0 END) AS igst_tax_amount,
				si.total,
				si.total_taxes_and_charges,
				si.grand_total
			FROM
				`tabSales Invoice` as si
			INNER JOIN `tabSales Taxes and Charges` as stc ON stc.parent=si.name
		"""
	if filters:
		company = filters.get("company")
		from_date = filters.get("from_date")
		to_date = filters.get("to_date")
		sql += f"""
				WHERE si.company = '{company}'
				AND si.posting_date BETWEEN '{from_date}' AND '{to_date}'
			"""
	sql += "GROUP BY si.name"

	data = frappe.db.sql(sql,as_dict=True)
	return columns, data
