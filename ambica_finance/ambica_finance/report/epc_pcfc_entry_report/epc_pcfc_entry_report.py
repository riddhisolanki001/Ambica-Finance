# Copyright (c) 2024, riddhi and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
	columns = [
		{
			"fieldname": "sr_no",
			"fieldtype": "Data",
			"label": "Sr. No.",
		},
		{
			"fieldname": "epc_no",
			"fieldtype": "Data",
			"label": "EPC No",
		},
		{
			"fieldname": "epc_date",
			"fieldtype": "Date",
			"label": "EPC Date",
		},
		{
			"fieldname": "epc_due_date",
			"fieldtype": "Date",
			"label": "EPC Due Date",
		},
		{
			"fieldname": "epc_amt",
			"fieldtype": "Currency",
			"label": "EPC Amt",
		},
		{
			"fieldname": "epc_adj_amt",
			"fieldtype": "Currency",
			"label": "EPC Adj Amt",
		},
		{
			"fieldname": "epc_adj_date",
			"fieldtype": "Date",
			"label": "EPC Adj Date",
		},
		{
			"fieldname": "balance",
			"fieldtype": "Currency",
			"label": "Balance",	
            "width": "110"
		},
		{
			"fieldname": "party_name",
			"fieldtype": "Data",
			"label": "Party Name",
            "width": "220"
		},
	]

	return columns

def get_data(filters):

	sql = """
		SELECT 
            # ROW_NUMBER() OVER (ORDER BY EPC.name) AS "sr_no",
			CASE WHEN @prev_epc_name != EPC.name THEN @sr_no := @sr_no + 1
				ELSE @sr_no END AS "sr_no",
				@prev_epc_name := EPC.name AS "epc_name",
			EPC.name AS epc_no,
			EPC.date AS epc_date,
			EPC.due_date AS epc_due_date,
			EPC.amount AS epc_amt,
			PEE.amount AS epc_adj_amt,
			PE.posting_date AS epc_adj_date,
			EPC.amount-PEE.amount AS balance,
			PE.party AS party_name
		FROM
            (SELECT @prev_epc_name := NULL, @sr_no := 1) vars,
			`tabEPC PCFC Entry` AS EPC
		JOIN
			`tabPayment Entry EPC` AS PEE ON PEE.epc_name = EPC.name
		JOIN
			`tabPayment Entry` AS PE ON PE.name = PEE.parent
		WHERE
			EPC.docstatus = 1
	"""
	data = frappe.db.sql(sql, as_dict=True)
	return data