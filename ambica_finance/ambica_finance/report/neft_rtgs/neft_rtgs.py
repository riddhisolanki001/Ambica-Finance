# Copyright (c) 2024, riddhi and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = [
        {"label": "Transaction Type", "fieldname": "transaction_type", "fieldtype": "Data"},
        {"label": "Blank", "fieldname": "blank", "fieldtype": "Data"},
        {"label": "Beneficiary Account Number", "fieldname": "beneficiary_account_number", "fieldtype": "Data"},
        {"label": "Instrument Amount", "fieldname": "instrument_amount", "fieldtype": "Dat"},
		{"label": "Beneficiary Name", "fieldname": "beneficiary_name", "fieldtype": "Data"},
		{"label": "Blank", "fieldname": "blank1", "fieldtype": "Data"},
		{"label": "Blank", "fieldname": "blank2", "fieldtype": "Data"},
		{"label": "Beneficiary Address 1", "fieldname": "beneficiary_address_1", "fieldtype": "Data"},
		{"label": "Beneficiary Address 2", "fieldname": "beneficiary_address_2", "fieldtype": "Data"},
		{"label": "Beneficiary Address 3", "fieldname": "beneficiary_address_3", "fieldtype": "Data"},
		{"label": "Beneficiary Address 4", "fieldname": "beneficiary_address_4", "fieldtype": "Data"},
		{"label": "Beneficiary Address 5", "fieldname": "beneficiary_address_5", "fieldtype": "Data"},
		{"label": "Instruction Reference Number", "fieldname": "instruction_reference_number", "fieldtype": "Data"},
		{"label": "Customer Reference Number", "fieldname": "customer_reference_number", "fieldtype": "Data"},
		{"label": "Payment Details 1", "fieldname": "payment_details_1", "fieldtype": "Data"},
		{"label": "Payment Details 2", "fieldname": "payment_details_2", "fieldtype": "Data"},
		{"label": "Payment Details 3", "fieldname": "payment_details_3", "fieldtype": "Data"},
		{"label": "Payment Details 4", "fieldname": "payment_details_4", "fieldtype": "Data"},
		{"label": "Payment Details 5", "fieldname": "payment_details_5", "fieldtype": "Data"},
		{"label": "Payment Details 6", "fieldname": "payment_details_6", "fieldtype": "Data"},
		{"label": "Payment Details 7", "fieldname": "payment_details_7", "fieldtype": "Data"},
		{"label": "Blank", "fieldname": "blank3", "fieldtype": "Data"},
		{"label": "Transaction Date", "fieldname": "transaction_date", "fieldtype": "Date"},
		{"label": "Blank", "fieldname": "blank4", "fieldtype": "Data"},
		{"label": "IFSC Code", "fieldname": "ifsc_code", "fieldtype": "Data"},
		{"label": "Bank Name", "fieldname": "bank_name", "fieldtype": "Data"},
		{"label": "Branch Name", "fieldname": "branch_name", "fieldtype": "Data"},
		{"label": "Email ID", "fieldname": "email_id", "fieldtype": "Data"},
    ]

    # Write your SQL query
    sql_query = """
        SELECT
            'N' AS transaction_type,
            NULL AS blank,
            party_bank_account AS beneficiary_account_number,
			paid_amount AS instrument_amount,
			party_name AS beneficiary_name,
		    NULL AS blank1,			
			NULL AS blank2,	
			NULL AS beneficiary_address_1,	
			NULL AS beneficiary_address_2,	
			NULL AS beneficiary_address_3,	
			NULL AS beneficiary_address_4,	
			NULL AS beneficiary_address_5,	
			NULL AS instruction_reference_number,	
			NULL AS customer_reference_number,	
			NULL AS payment_details_1,	
			NULL AS payment_details_2,	
			NULL AS payment_details_3,	
			NULL AS payment_details_4,	
			NULL AS payment_details_5,	
			NULL AS payment_details_6,	
			NULL AS payment_details_7,	
			NULL AS blank3,				
            posting_date AS transaction_date,
			NULL AS blank4,	
			NULL AS ifsc_code,	
			NULL AS bank_name,	
			NULL AS branch_name,	
			NULL AS email_id	
        FROM `tabPayment Entry`
        WHERE custom_neftrtgs != 'Fund Transfer' AND docstatus != 2 AND docstatus != 0
    """

    # Execute the SQL query
    data = frappe.db.sql(sql_query, as_dict=True)

    return columns, data



				