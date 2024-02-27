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
            "fieldname": "doc_no",
            "fieldtype": "Link",
            "label": "Doc No",
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "doc_date",
            "fieldtype": "Date",
            "label": "Doc Date",
        },
        {
            "fieldname": "party_name",
            "fieldtype": "Link",
            "label": "Party Name",
            "options": "Supplier",
            # "width": "200",
            # "align": "left"
        },
        {
            "fieldname": "bill_no",
            "fieldtype": "Data",
            "label": "Bill Number",
        },
        {
            "fieldname": "bill_date",
            "fieldtype": "Date",
            "label": "Bill Date",
            "width": "110",
        },
        {
            "fieldname": "bill_amt",
            "fieldtype": "Currency",
            "label": "Bill Amt",
        },
        {
            "fieldname": "adjusted",
            "fieldtype": "Currency",
            "label": "Adjusted",
            # "width": "120"
        },
        {
            "fieldname": "pending_amt",
            "fieldtype": "Currency",
            "label": "Pending Amt",
            # "width": "120"
        },
        {
            "fieldname": "due_date",
            "fieldtype": "Date",
            "label": "Due Date",
            "width": "110",
        },
        {
            "fieldname": "remarks",
            "fieldtype": "Data",
            "label": "Remarks",
            "align": "left",
        },
    ]
    return columns

def get_data(filters):
    docs = frappe.get_list(
        "Auto Outstandings",
        order_by="creation",
    )
    data = []
    for doc in docs:
        doc = frappe.get_doc("Auto Outstandings", doc)
        for entry in doc.outstandings:
            if not entry.payment_entry:
                row = [entry.invoice_number, entry.invoice_date, entry.party_name, entry.party_bill_number, entry.party_bill_date, entry.amount, entry.adjusted, entry.amount - entry.adjusted, entry.due_date, entry.remarks]
                data.append(row)
    return data


@frappe.whitelist()
def auto_payment_not_paid_remarks():
    data = [[column["label"] for column in get_columns(None)]]
    data += (get_data(None))
    return data