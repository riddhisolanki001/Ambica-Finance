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
			"label": "EPC Sr",
		},
		{
			"fieldname": "epc_no",
			"fieldtype": "Link",
			"label": "EPC No",
			"options": "EPC PCFC Entry"
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
            "width": "120"
		},
		{
			"fieldname": "pe_no",
			"fieldtype": "Link",
			"label": "Payment Entry No",
			"options": "Payment Entry"
		},
		{
			"fieldname": "epc_adj_amt",
			"fieldtype": "Currency",
			"label": "EPC Adj Amt",
            "width": "120"
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
            "width": "120"
		},
		{
			"fieldname": "party_name",
			"fieldtype": "Link",
			"label": "Party Name",
			"options": "Customer",
            "width": "200",
    		"align": "left"
		},
	]
	return columns

def get_data(filters):
	epc_pcfc_docs = frappe.get_list(
		'EPC PCFC Entry',
		filters={'docstatus': 1},
		order_by='creation'
	)
	payment_entry_docs = frappe.get_list(
		'Payment Entry',
		filters={'docstatus': 1},
		order_by='creation'
	)

	data = []
	sr_no = 0
	for epc_doc in epc_pcfc_docs:
		epc_doc = frappe.get_doc('EPC PCFC Entry', epc_doc)
		sr_no += 1
		inner_data = [sr_no, epc_doc.name, epc_doc.date, epc_doc.due_date, epc_doc.amount, None, None, None, epc_doc.amount, None]
		has_pe, is_first = False, True
		for pe_doc in payment_entry_docs:
			pe_doc = frappe.get_doc('Payment Entry', pe_doc)
			for epc in pe_doc.custom_epc_references:
				if epc.epc_name == epc_doc.name:
					if is_first:
						epc_doc_balance = epc_doc.amount - epc.amount
						inner_data = [sr_no, epc_doc.name, epc_doc.date, epc_doc.due_date, epc_doc.amount, pe_doc.name, epc.amount, pe_doc.posting_date, epc_doc_balance, pe_doc.party]
						is_first = False
					else:
						inner_data = [None, None, None, None, epc_doc_balance, pe_doc.name, epc.amount, pe_doc.posting_date, epc_doc_balance - epc.amount, pe_doc.party]
						epc_doc_balance = epc_doc_balance - epc.amount
					has_pe = True
					data.append(inner_data)
		data.append(inner_data) if not has_pe else None
	return data