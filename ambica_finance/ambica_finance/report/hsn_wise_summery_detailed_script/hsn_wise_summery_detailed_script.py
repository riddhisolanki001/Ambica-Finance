# Copyright (c) 2024, riddhi and contributors
# For license information, please see license.txt

# import frappe

import frappe

def execute(filters=None):
    # Define the columns for your report
    columns = [
        {"label": "Name", "fieldname": "name", "fieldtype": "Link", "options": "Sales Invoice"},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date"},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer"},
        {"label": "Total", "fieldname": "total", "fieldtype": "Currency"},
        # Add more columns as needed
    ]

    # Fetch all sales invoice data without specific filters
    data = frappe.get_all("Sales Invoice",
                          filters=filters,
                          fields=["name", "posting_date", "customer", "total"])

    return columns, data

