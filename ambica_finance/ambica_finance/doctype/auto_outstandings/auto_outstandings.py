# Copyright (c) 2024, riddhi and contributors
# For license information, please see license.txt

import frappe
import json
import locale
from frappe.model.document import Document


class AutoOutstandings(Document):
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
    try:
        # Parse the selected_rows string into a list of dictionaries
        selected_rows = json.loads(selected_rows)

        distinct_party_names = set(row['party_name'] for row in selected_rows)
        for party_name in distinct_party_names:
            payment_entry = frappe.new_doc('Payment Entry')
            payment_entry.company = 'Sanskar (Demo)'
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
            remarkstext = f"Being Amount {total_paid_amount} Paid to {party_name} as per voucher attach"
            payment_entry.remarks = remarkstext
            for invoice_row in selected_rows:
                if invoice_row['party_name'] == party_name:
                    payment_entry.append('references', {
                        'reference_doctype': "Purchase Invoice",
                        'reference_name': invoice_row['invoice_number']
                    })
                    payment_entry.save()
                    frappe.db.commit()

            # Retrieve the document again
            saved_payment_entry = frappe.get_doc('Payment Entry', payment_entry.name)

            # Now check references
            print(saved_payment_entry.references)


        return "Payment Entry created successfully"
    except Exception as e:
        frappe.log_error(f"Error in create_payment_entry: {e}")
        frappe.db.rollback()
        return frappe.throw("Error occurred while creating Payment Entry")

        # name = payment_entry.name  # Get the name of the newly created Payment Entry

        # parent = frappe.get_doc("Payment Entry", name)

        # # Iterate through references and create entries in the child table
        # for invoice_row in selected_rows:
        #     if invoice_row['party_name'] == party_name:
        #         frappe.msgprint(f"Adding reference for {party_name}, invoice_number: {invoice_row['invoice_number']}")

        #         reference = parent.append("references", {
        #             'reference_doctype': 'Purchase Invoice',
        #             'reference_name': invoice_row['invoice_number'],
        #         })
        #         frappe.msgprint(f"Reference added: {reference.as_dict()}")
                
        #         frappe.db.commit()  # Commit after each iteration

        # parent.save()
        # frappe.db.commit()  # Commit after the loop completes
 
        # for invoice_row in selected_rows:
        #     if invoice_row['party_name'] == party_name:
        #         reference_entry = frappe.new_doc('Payment Entry Reference')
        #         reference_entry.parent = name
        #         reference_entry.parentfield = 'references'
        #         reference_entry.parenttype = 'Payment Entry'
        #         reference_entry.reference_doctype = 'Purchase Invoice'
        #         reference_entry.reference_name = invoice_row['invoice_number']
        #         reference_entry.total_amount = invoice_row['amount']
        #         reference_entry.save()

        #         frappe.db.commit()
        # frappe.db.commit()