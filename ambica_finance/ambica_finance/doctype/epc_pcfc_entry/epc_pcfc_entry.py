# Copyright (c) 2023, riddhi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EPCPCFCEntry(Document):
    pass

@frappe.whitelist()
def create_Journal_entry():
    try:
        date = frappe.form_dict['date']
        due_date = frappe.form_dict['due_date']
        company = frappe.form_dict['company']
        bank_name = frappe.form_dict['bank_name']
        reference_number = frappe.form_dict['reference_number']
        amount = frappe.form_dict['amount']
        epc_name = frappe.form_dict['epc_name']
        
        sql = "SELECT c.abbr FROM `tabCompany` as c WHERE c.name = %s"
        abbr = frappe.db.sql(sql, company, as_dict=True)
        abbr_value = abbr[0].get('abbr')

        existing_entry = frappe.db.exists('Journal Entry',{'bill_no':epc_name})

        if existing_entry:
            # Update existing Journal Entry
            # journal_entry = frappe.get_doc('Journal Entry', existing_entry)
            # journal_entry.posting_date = date
            # journal_entry.due_date = due_date
            # journal_entry.company = company
            # journal_entry.cheque_no = reference_number
            # journal_entry.cheque_date = date
            # journal_entry.bill_no = epc_name

            # journal_entry.accounts = []

            # journal_entry.append('accounts', {
            #     'account': bank_name,
            #     'debit_in_account_currency': amount
            # })
            # journal_entry.append('accounts', {
            #     'account': f"Export Packing Credit - {abbr_value}",
            #     'credit_in_account_currency': amount,
            # })
        
            # journal_entry.save()
            # frappe.db.commit()
            # journal_entry.reload()

            entry_link = frappe.utils.get_url_to_form('Journal Entry', existing_entry)
            return f"Journal Entry <a href='{entry_link}'>{existing_entry}</a> exists already for this EPC PCFC Entry."           
        else:

            journal_entry = frappe.new_doc('Journal Entry')
            # Set the fields
            journal_entry.voucher_type = "Journal Entry"
            journal_entry.posting_date = date
            journal_entry.due_date = due_date
            journal_entry.company = company
            journal_entry.cheque_no = reference_number
            journal_entry.cheque_date = date
            journal_entry.bill_no = epc_name
            journal_entry.bill_date = date


            # Add new accounts based on your requirements
            journal_entry.append('accounts', {
                'account': bank_name,
                'debit_in_account_currency': amount
            })
            journal_entry.append('accounts', {
                'account': f"Export Packing Credit - {abbr_value}",
                'credit_in_account_currency': amount,
            })

            journal_entry.insert()
            frappe.db.commit()

            entry_link = frappe.utils.get_url_to_form('Journal Entry', journal_entry.name)
            return f"Journal Entry <a href='{entry_link}'>{journal_entry.name}</a> created successfully."

    except Exception as e:
        frappe.log_error(f"Error in create_Journal_entry: {e}")
        frappe.db.rollback()
        return frappe.throw("Error occurred while creating journal Entry")