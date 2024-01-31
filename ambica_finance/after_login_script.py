# custom_app/after_login_script.py
import frappe
from frappe import _

def execute():
    # Your script logic here
    party_type = frappe.get_doc({"doctype":"Party Type", "party_type": "Customer-Supplier", "account_type": "Payable/Receivable"})
    party_type.insert(
        ignore_permissions=True, # ignore write permissions during insert
        ignore_links=True, # ignore Link validation in the document
        ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
        ignore_mandatory=True # insert even if mandatory fields are not set
    )
    # doc = frappe.get_doc('Party Type', 'Customer')
    # doc.account_type = 'Payable/Receivable'
    # doc.save()