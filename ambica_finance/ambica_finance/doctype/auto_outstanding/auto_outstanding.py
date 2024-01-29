# Copyright (c) 2023, Riddhi and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
import locale


class AutoOutstanding(Document):
	pass

@frappe.whitelist()
def get_msme_invoices(bank_name,due_date):
     
	sql = """
		SELECT 
  			pi.name 
		FROM 
  			`tabBank Account` as ba 
  		INNER JOIN 
			`tabSupplier` as s ON s.default_bank_account = ba.name 
  		LEFT JOIN 
			`tabPurchase Invoice` as pi ON pi.supplier = s.name 
		WHERE 
            ba.account = %s AND pi.status = "Unpaid" AND s.custom_msme = "Yes"

		"""
	invoices = frappe.db.sql(sql,bank_name,as_dict=True)
	return invoices

@frappe.whitelist()
def get_invoices(bank_name,due_date):

	sql = """
		SELECT 
  			pi.name 
		FROM 
  			`tabBank Account` as ba 
  		INNER JOIN 
			`tabSupplier` as s ON s.default_bank_account = ba.name 
  		LEFT JOIN 
			`tabPurchase Invoice` as pi ON pi.supplier = s.name 
		WHERE 
            (pi.due_date <= %s AND ba.account = %s AND pi.status = "Unpaid" AND (s.custom_msme = "No" OR s.custom_msme = ""))

		"""
	invoices = frappe.db.sql(sql,(due_date,bank_name),as_dict=True)
	return invoices

@frappe.whitelist()
def get_not_due_invoices(bank_name, due_date):
    sql_not_due = """
        SELECT 
            pi.name 
        FROM 
            `tabBank Account` as ba 
        INNER JOIN 
            `tabSupplier` as s ON s.default_bank_account = ba.name 
        LEFT JOIN 
            `tabPurchase Invoice` as pi ON pi.supplier = s.name 
        WHERE 
            (pi.due_date > %s AND ba.account = %s AND pi.status="Unpaid" AND (s.custom_msme = "No" OR s.custom_msme = ""));
    """

    invoices_not_due = frappe.db.sql(sql_not_due, (due_date, bank_name), as_dict=True)

    return invoices_not_due


@frappe.whitelist()
def create_payment_entry(selected_rows, bank_name, payment_date):
    # Parse the selected_rows string into a list of dictionaries
    selected_rows = json.loads(selected_rows)

    distinct_party_names = set(row['party_name'] for row in selected_rows)
    for party_name in distinct_party_names:
        payment_entry = frappe.new_doc('Payment Entry')
        payment_entry.payment_type = 'Pay'
        payment_entry.party_type = 'Supplier'
        payment_entry.party = party_name
        payment_entry.paid_from = bank_name
        payment_entry.reference_no = '894521'
        payment_entry.reference_date = payment_date
        payment_entry.mode_of_payment = 'Wire Transfer'

        total_paid_amount = sum(row['amount'] for row in selected_rows if row['party_name'] == party_name)
        payment_entry.paid_amount = total_paid_amount
        payment_entry.received_amount = total_paid_amount
        payment_entry.custom_remarks = 1
        remarkstext = 'Being Amount ' + str(total_paid_amount) + ' Paid to ' + str(party_name) + ' as per voucher attach'
        payment_entry.remarks = remarkstext
        payment_entry.flags.ignore_permissions = True         
        payment_entry.save()

        name = payment_entry.name  # Get the name of the newly created Payment Entry

        # Iterate through references and create entries in the child table
        for invoice_row in selected_rows:
            if invoice_row['party_name'] == party_name:
                reference_entry = frappe.new_doc('Payment Entry Reference')
                reference_entry.parent = name
                reference_entry.parentfield = 'references'
                reference_entry.parenttype = 'Payment Entry'
                reference_entry.reference_doctype = 'Purchase Invoice'
                reference_entry.reference_name = invoice_row['invoice_number']
                reference_entry.total_amount = invoice_row['amount']
            
                # Trigger the before_save method of the child table
                reference_entry.run_method('before_save')                
                reference_entry.insert()
                # payment_entry.save()

    frappe.db.commit()
