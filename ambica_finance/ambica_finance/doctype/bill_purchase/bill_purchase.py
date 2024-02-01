# Copyright (c) 2023, riddhi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BillPurchase(Document):
	pass


@frappe.whitelist()
def get_sales_invoice_for_bill_purchase():
	sql="""
		SELECT 
			si.name,
			si.posting_date,
			si.due_date,
			si.conversion_rate,
			si.grand_total
		FROM
			`tabSales Invoice` as si
		WHERE 
			si.currency != 'INR'
	"""

	invoices = frappe.db.sql(sql,as_dict=True)
	return invoices