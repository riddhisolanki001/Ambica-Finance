# Copyright (c) 2023, riddhi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EPCPCFCEntry(Document):
    pass

@frappe.whitelist()
def create_Journal_entry():
    date = frappe.form_dict['date']
    due_date = frappe.form_dict['due_date']
    company = frappe.form_dict['company']
    bank_name = frappe.form_dict['bank_name']
    reference_number = frappe.form_dict['reference_number']
    amount = frappe.form_dict['amount']
    
    sql = "SELECT c.abbr FROM `tabCompany` as c WHERE c.name = %s"
    abbr = frappe.db.sql(sql, company, as_dict=True)
    abbr_value = abbr[0].get('abbr')

    
    journal_entry = frappe.new_doc('Journal Entry')

    # Set the fields
    journal_entry.voucher_type = "Journal Entry"
    journal_entry.posting_date = date
    journal_entry.due_date = due_date
    journal_entry.company = company
    journal_entry.cheque_no = reference_number
    journal_entry.cheque_date = date

    # Add accounts and amounts based on your requirements
    # For example, you might have a debit and credit entry
    journal_entry.append('accounts', {
        'account': bank_name,
        'debit_in_account_currency': amount
    })
    journal_entry.append('accounts', {
        'account': f"Export Packing Credit - {abbr_value}",
        'credit_in_account_currency': amount,
    })
    # Add more accounts as needed

    # Save the Journal Entry
    journal_entry.insert()
    frappe.db.commit()
