# Copyright (c) 2024, riddhi and contributors
# For license information, please see license.txt

import frappe
# from frappe import _

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns,data

def get_columns(filters):
    if filters.get("select") == "Company Details":
        columns = [
            {
                "fieldname": "custom_tan",
                "fieldtype": "Data",
                "label": "COMPANY TAN",
            },
            {
                "fieldname": "pan",
                "fieldtype": "Data",
                "label": "COMPANY PAN",
            },
            {
                "fieldname": "name",
                "fieldtype": "Data",
                "label": "COMPANY NAME",
            },
        ]
    elif filters.get("select") == "Challan Details":
        columns = [
            {
                "fieldname": "serial_no",
                "fieldtype": "int",
                "label": "Running Serial No (651)",
            },
            {
                "fieldname": "tcs",
                "fieldtype": "Currency",
                "label": "TCS (652)",
            },
            {
                "fieldname": "surcharge",
                "fieldtype": "Currency",
                "label": "Surcharge (653)",
            },
            {
                "fieldname": "education_cess",
                "fieldtype": "Currency",
                "label": "Education Cess (654)",
            },
			{
                "fieldname": "interest",
                "fieldtype": "Currency",
                "label": "Interest (655)",
            },
            {
                "fieldname": "fee",
                "fieldtype": "Currency",
                "label": "Fee (656)",
            },
            {
                "fieldname": "other",
                "fieldtype": "Currency",
                "label": "Others (657)",
            },
            {
                "fieldname": "total_tax",
                "fieldtype": "Currency",
                "label": "Total Tax Deposited (658)",
            },
            {
                "fieldname": "bsr_code",
                "fieldtype": "Data",
                "label": "BSR Code / 24G Receipt NO (660)",
            },
            {
                "fieldname": "tax_date",
                "fieldtype": "Date",
                "label": "Date on Tax Deposited (dd/mm/yyyy) (662)",
            },
            {
                "fieldname": "challan_serial_no",
                "fieldtype": "Data",
                "label": "Transfer Voucher/Challan Serial No (661)",
            },
            {
                "fieldname": "tds_deposited_by_book_entry",
                "fieldtype": "Data",
                "label": "Whether TDS Deposited by Book Entry (659)",
            },
            {
                "fieldname": "minor_head",
                "fieldtype": "Data",
                "label": "Minor head (663)",
            },
        ]
    elif filters.get("select") == "Deductee Details":
        columns = [
           {
                "fieldname": "party_serial_no",
                "fieldtype": "Data",
                "label": "Party Serial No (664)",
            },
            {
                "fieldname": "challan_serial_ref",
                "fieldtype": "Data",
                "label": "Challan Serial Reference (651)",
            },
            {
                "fieldname": "party_code",
                "fieldtype": "Data",
                "label": "Party Code (414)",
            },
            {
                "fieldname": "deductee_pan",
                "fieldtype": "Data",
                "label": "PAN of Deductee (667)",
            },
            {
                "fieldname": "party_name",
                "fieldtype": "Data",
                "label": "Name of the Party (668)",
            },
            {
                "fieldname": "section_code",
                "fieldtype": "Data",
                "label": "Section Code (672)",
            },
            {
                "fieldname": "pay_credit_date",
                "fieldtype": "Date",
                "label": "Payment/Debit Date (dd/mm/yyyy) (671)",
            },
            {
                "fieldname": "amount_paid",
                "fieldtype": "Currency",
                "label": "Amount Paid/Debited (670)",
            },
            {
                "fieldname": "tcs",
                "fieldtype": "Currency",
                "label": "TCS (673)",
            },
            {
                "fieldname": "surcharge",
                "fieldtype": "Currency",
                "label": "Surcharge (674)",
            },
            {
                "fieldname": "education_cess",
                "fieldtype": "Currency",
                "label": "Education Cess (675)",
            },
            {
                "fieldname": "total_tax_collected",
                "fieldtype": "Currency",
                "label": "Total Tax Collected (676)",
            },
            {
                "fieldname": "total_tax_deposited",
                "fieldtype": "Currency",
                "label": "Total Tax Deposited (677)",
            },
            {
                "fieldname": "collection_rate",
                "fieldtype": "Float",
                "label": "Rate at which Collected (679)",
            },
            {
                "fieldname": "lower_collection_reason",
                "fieldtype": "Data",
                "label": "Reason for Non-deduction/Lower Collection (680)",
            },
            {
                "fieldname": "certificate_no",
                "fieldtype": "Data",
                "label": "Certificate number for Lower/non deduction (681)",
            },
            {
                "fieldname": "value_of_purchase",
                "fieldtype": "Data",
                "label": "Value of Purchase (669)",
            },
            {
                "fieldname": "non_resident",
                "fieldtype": "Data",
                "label": "Non-Resident (Y/N)",
            },
            {
                "fieldname": "perm_established",
                "fieldtype": "Data",
                "label": "Permanently Established (Y/N)",
            },
            {
                "fieldname": "challan_number",
                "fieldtype": "Data",
                "label": "Challan Number (for reason F & G)",
            },
            {
                "fieldname": "challan_date",
                "fieldtype": "Date",
                "label": "Challan Date (for reason F & G)",
            },
        ]
    elif filters.get("select") == "Collection Code":
        columns = [
            {
                "fieldname": "section",
                "fieldtype": "Data",
                "label": "Section",
            },
            {
                "fieldname": "section_desc",
                "fieldtype": "Data",
                "label": "Section Description",
                "width": 600
            },
        ]
    elif filters.get("select") == "Deductee Code":
        columns=[
               {
                "fieldname": "deductee_code",
                "fieldtype": "Data",
                "label": "Deductee Code",
            },
            {
                "fieldname": "deductee_type",
                "fieldtype": "Data",
                "label": "Deductee Type",
            },
		]
    elif filters.get("select") == "Remarks":
        columns=[
               {
                "fieldname": "reason",
                "fieldtype": "Data",
                "label": "Reason",
            },
            {
                "fieldname": "reason_description",
                "fieldtype": "Data",
                "label": "Reason Description",
                "width":800
            },
		]

    return columns

def get_data(filters):
    company = frappe.defaults.get_user_default("Company")

    if filters.get("select") == "Company Details":
        sql = """
            SELECT c.custom_tan, c.pan, c.name 
            FROM `tabCompany` AS c 
            WHERE c.name = %s;
        """
        data = frappe.db.sql(sql, company, as_dict=True)
        return data
       # Add more conditions if needed for other values of "select"
    elif filters.get("select") == "Challan Details":
        sql = """
			SELECT
                ROW_NUMBER() OVER (ORDER BY TDS.name) AS "serial_no",
                TDS.total_tds_amount AS "tcs",
                TDS.interest AS "interest",
                TDS.others AS "other",
                (TDS.total_tds_amount+TDS.interest+TDS.others) AS "total_tax",
                TDS.bank_code AS "bsr_code",
                TDS.challan_date AS "tax_date",
                TDS.challan_number AS "challan_serial_no"
            FROM
                `tabTDS Deduction Selection` AS TDS 
            WHERE TDS.category LIKE %s
        """
        data = frappe.db.sql(sql,'TCS%',as_dict=True)
        return data
    elif filters.get("select") == "Deductee Details":
        # category_pattern = frappe.get_list()
        sql = """
                SELECT
                    ROW_NUMBER() OVER (ORDER BY TDS.name) AS "party_serial_no",
                    CASE WHEN @prev_tds_name != TDS.name THEN @challan_serial_ref := @challan_serial_ref + 1 ELSE @challan_serial_ref END AS "challan_serial_ref",
                    @prev_tds_name := TDS.name AS "tds_name",
                    C.custom_company_status AS "party_code",
                    C.pan AS "deducte_pan",
                    C.name AS "party_name",
                    TWC.custom_section AS "section_code",
                    TDS.challan_date AS "pay_credit_date",
                    "amount_paid",
                    SIT.tax_amount AS "tcs",
                    "surcharge",
                    "education_cess",
                    (TDS.total_tds_amount+TDS.interest+TDS.others) AS "total_tax_collected",
                    (TDS.total_tds_amount+TDS.interest+TDS.others) AS "total_tax_deposited",
                    SIT.rate AS "collection_rate"
                FROM
                    (SELECT @prev_tds_name := NULL, @challan_serial_ref := 1) vars,
                    `tabTDS Deduction Selection` AS TDS
                INNER JOIN 
                    `tabSales Invoice` AS SI 
                ON ((SI.posting_date BETWEEN TDS.from_date AND TDS.to_date) 
                    AND (SI.custom_tax_withholding_category LIKE CONCAT(SUBSTRING_INDEX(TDS.category, ' - ', 3), '%'))) 
                INNER JOIN
                    `tabSales Taxes and Charges` AS SIT ON SIT.parent = SI.name
                LEFT JOIN 
                    `tabCustomer` AS C 
                    ON C.name = SI.customer 
                LEFT JOIN 
                    `tabTax Withholding Category` AS TWC 
                    ON TWC.name = TDS.category
                LEFT JOIN 
                    `tabTax Withholding Rate` AS TWR 
                    ON TWR.parent = TWC.name
        """
        data = frappe.db.sql(sql,as_dict=True)
        return data
    elif filters.get("select") == "Collection Code":
        sql = """
			SELECT
                TM.section AS "section",
                TM.ctegory as "section_desc"
            FROM
                `tabTDS Master` AS TM where TM.section LIKE '206%';
        """
        data = frappe.db.sql(sql,as_dict=True)
        return data 
    elif filters.get("select") == "Deductee Code":
        data = [
            {
                "deductee_code": "1",
                "deductee_type": "Company"
			},
            {
                "deductee_code": "2",
                "deductee_type": "Non-Company"
			},
		]
        return data 
    elif filters.get("select") == "Remarks":
        data = [
            {
                "reason": "",
                "reason_description": "Normal"
			},
            {
                "reason": "A",
                "reason_description": "Lower collection u/s 206C (9)"
			},
            {
                "reason": "B",
                "reason_description": "Non collection u/s 206C (1A)"
			},
            {
                "reason": "C",
                "reason_description": "Higher Rate (Valid PAN not available)"
			},
            {
                "reason": "D",
                "reason_description": "Remittance is less than Rs. 7 lacs"
			},
            {
                "reason": "E",
                "reason_description": "TCS already collected"
			},
            {
                "reason": "F",
                "reason_description": "TDS by Buyer / Sale to Govt. & others as specified"
			},
            {
                "reason": "G",
                "reason_description": "TDS by Buyer on transaction"
			},
            {
                "reason": "H",
                "reason_description": "Sale to Govt. & others as specified"
			},
            
		]
        return data
	   
    return []


