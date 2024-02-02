# Copyright (c) 2023, riddhi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BillPurchase(Document):
    pass


@frappe.whitelist()
def get_sales_invoice_for_bill_purchase(customer):
    sql = """
        SELECT 
            si.name,
            si.posting_date,
            si.due_date,
            si.conversion_rate,
            si.grand_total
        FROM
            `tabSales Invoice` as si
        WHERE 
            si.currency != 'INR' AND si.customer=%s
    """

    invoices = frappe.db.sql(sql, customer, as_dict=True)
    return invoices


@frappe.whitelist()
def create_Journal_entry():
    try:
        date = frappe.form_dict['date']
        company = frappe.form_dict['company']
        amount = frappe.form_dict['amount']

        sql = "SELECT c.abbr FROM `tabCompany` as c WHERE c.name = %s"
        abbr = frappe.db.sql(sql, company, as_dict=True)
        abbr_value = abbr[0].get('abbr')

        journal_entry = frappe.new_doc('Journal Entry')

        # Set the fields
        journal_entry.voucher_type = "Journal Entry"
        journal_entry.posting_date = date
        journal_entry.company = company

        # Add accounts and amounts based on your requirements
        # For example, you might have a debit and credit entry
        journal_entry.append('accounts', {
            'account': f"Bill Purchase - {abbr_value}",
            'credit_in_account_currency': amount
        })
        journal_entry.append('accounts', {
            'account': f"Export Packing Credit - {abbr_value}",
            'debit_in_account_currency': amount,
        })
        # Add more accounts as needed

        # Save the Journal Entry
        journal_entry.insert()
        frappe.db.commit()
        return "Journal Entry created successfully"

    except Exception as e:
        frappe.log_error(f"Error in create_Journal_entry: {e}")
        frappe.db.rollback()
        return frappe.throw("Error occurred while creating journal Entry")
