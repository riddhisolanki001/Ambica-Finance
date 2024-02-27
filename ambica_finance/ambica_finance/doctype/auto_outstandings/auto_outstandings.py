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
            (pi.due_date <= %s AND ba.account = %s AND pi.status = "Overdue" AND (s.custom_msme = "No" OR s.custom_msme = ""))

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

        # Iterate through distinct party names
        for party_name in set(row['party_name'] for row in selected_rows):
            # Create a new Payment Entry for each party
            payment_entry = frappe.new_doc('Payment Entry')
            payment_entry.company = 'Sanskar (Demo)'
            payment_entry.payment_type = 'Pay'
            payment_entry.party_type = 'Supplier'
            payment_entry.party = party_name
            payment_entry.paid_from = bank_name
            payment_entry.reference_no = '894521'
            payment_entry.reference_date = payment_date
            payment_entry.mode_of_payment = 'Wire Transfer'

            # Filter rows for the current party
            party_rows = [row for row in selected_rows if row['party_name'] == party_name]

            # Calculate total paid amount for the current party
            total_paid_amount = sum(row['amount'] for row in party_rows)

            # Set paid and received amounts
            payment_entry.paid_amount = total_paid_amount
            payment_entry.received_amount = total_paid_amount

            # Set custom remarks and create remarks text
            payment_entry.custom_remarks = 1
            remarkstext = f"Being Amount {total_paid_amount} Paid to {party_name} as per voucher attach"
            payment_entry.remarks = remarkstext

            # Prepare a list of dictionaries for Payment Entry Reference
            # references_list = []
            # for row in party_rows:
            #     reference_dict = {
            #         'reference_doctype': 'Purchase Invoice',
            #         'reference_name': row['invoice_number'],
            #         'total_amount': row['amount']
            #     }
            #     references_list.append(reference_dict)

            # # Set the references field with the prepared list
            # payment_entry.references = references_list

            # Save the Payment Entry for the current party
            payment_entry.insert()

            # Log and display messages for debugging
            frappe.msgprint(f"Payment Entry '{payment_entry.name}' created successfully for {party_name}")

        # Commit changes to the database after processing all parties
        frappe.db.commit()

        return "Payment Entries created successfully"
    except Exception as e:
        frappe.log_error(f"Error in create_payment_entry: {e}")
        frappe.db.rollback()
        return frappe.throw("Error occurred while creating Payment Entries")





# @frappe.whitelist()
# def create_payment_entry(selected_rows, bank_name, payment_date):
#     try:
#         # Parse the selected_rows string into a list of dictionaries
#         selected_rows = json.loads(selected_rows)

#         # Iterate through distinct party names
#         for party_name in set(row['party_name'] for row in selected_rows):
#             payment_entry = frappe.new_doc('Payment Entry')
#             payment_entry.company = 'Sanskar (Demo)'
#             payment_entry.payment_type = 'Pay'
#             payment_entry.party_type = 'Supplier'
#             payment_entry.party = party_name
#             payment_entry.paid_from = bank_name
#             payment_entry.reference_no = '894521'
#             payment_entry.reference_date = payment_date
#             payment_entry.mode_of_payment = 'Wire Transfer'

#             # Calculate total paid amount for the current party
#             total_paid_amount = sum(row['amount'] for row in selected_rows if row['party_name'] == party_name)

#             # Set paid and received amounts
#             payment_entry.paid_amount = total_paid_amount
#             payment_entry.received_amount = total_paid_amount

#             # Set custom remarks and create remarks text
#             payment_entry.custom_remarks = 1
#             remarkstext = f"Being Amount {total_paid_amount} Paid to {party_name} as per voucher attach"
#             payment_entry.remarks = remarkstext

#             # Save the Payment Entry
#             payment_entry.insert()
#             name = payment_entry.name  # Get the name of the newly created Payment Entry

#             # Iterate through selected rows and create Payment Entry Reference
#             for invoice_row in selected_rows:
#                 if invoice_row['party_name'] == party_name:
#                     reference_entry = frappe.new_doc('Payment Entry Reference')
#                     reference_entry.parent = name
#                     reference_entry.parentfield = 'references'
#                     reference_entry.parenttype = 'Payment Entry'
#                     reference_entry.reference_doctype = 'Purchase Invoice'
#                     reference_entry.reference_name = invoice_row['invoice_number']
#                     reference_entry.total_amount = invoice_row['amount']
#                     reference_entry.insert()

#             frappe.db.commit()

#         return "Payment Entry created successfully"
#     except Exception as e:
#         frappe.log_error(f"Error in create_payment_entry: {e}")
#         frappe.db.rollback()
#         return frappe.throw("Error occurred while creating Payment Entry")
