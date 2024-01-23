# Copyright (c) 2023, riddhi and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):

    columns = [
        {
            "fieldname": "party_name",
            "fieldtype": "Data",
            "label": "Party Name",
        },
        {
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Payment Entry",
            "label": "Reference Number",
        },
        {
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "label": "Reference Date",
        },
        {
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "label": "Payment Date",
        },
        {
            "fieldname": "paid_amount",
            "fieldtype": "Currency",
            "label": "Amount Paid",
        },
        {
            "fieldname": "tentative_date",
            "fieldtype": "Date",
            "label": "Tentative Date",
        },
        {
            "fieldname": "remarks",
            "fieldtype": "Small Text",
            "label": "Remarks",
        },
    ]

    sql = """
        SELECT 
            pe.party_name,
            pe.name,
            pe.posting_date,
            pe.paid_amount,
            CASE
                WHEN per.reference_doctype = 'Purchase Invoice' THEN
                    (SELECT pi.due_date FROM `tabPurchase Invoice` pi WHERE pi.name = per.reference_name)
                WHEN per.reference_doctype = 'Purchase Order' THEN
                    (SELECT so.schedule_date FROM `tabPurchase Order` so WHERE so.name = per.reference_name)
                ELSE
                    pe.reference_date
            END as tentative_date,
            pe.remarks
        FROM 
            `tabPayment Entry` as pe
        LEFT JOIN
            `tabPayment Entry Reference` as per ON per.parent = pe.name
        LEFT JOIN 
            `tabDocType` as dt ON dt.name = per.reference_doctype
        WHERE
            pe.payment_type = "Pay" and pe.party_type = "Supplier"
    """

    conditions = []

    if filters:
        from_date = filters.get("from_date")
        to_date = filters.get("to_date")

        if from_date and to_date:
            conditions.append(f"pe.posting_date BETWEEN '{from_date}' AND '{to_date}'")
        
        if conditions:
            sql += " AND " + " AND ".join(conditions)

    data = frappe.db.sql(sql, as_dict=True)
    return columns, data