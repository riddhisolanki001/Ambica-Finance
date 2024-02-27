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
                "label": "Running Serial No (401)",
            },
            {
                "fieldname": "tds",
                "fieldtype": "Currency",
                "label": "TDS (402)",
            },
            {
                "fieldname": "surcharge",
                "fieldtype": "Currency",
                "label": "Surcharge",
            },
            {
                "fieldname": "education_cess",
                "fieldtype": "Currency",
                "label": "Education Cess",
            },
			{
                "fieldname": "interest",
                "fieldtype": "Currency",
                "label": "Interest (403)",
            },
            {
                "fieldname": "fee",
                "fieldtype": "Currency",
                "label": "Fee (404)",
            },
            {
                "fieldname": "other",
                "fieldtype": "Currency",
                "label": "Others (405)",
            },
            {
                "fieldname": "total_tax",
                "fieldtype": "Currency",
                "label": "Total Tax Deposited (406)",
            },
            {
                "fieldname": "bsr_code",
                "fieldtype": "Data",
                "label": "BSR Code / 24G Receipt NO (408)",
            },
            {
                "fieldname": "tax_date",
                "fieldtype": "Date",
                "label": "Date on Tax Deposited (dd/mm/yyyy) (410)",
            },
            {
                "fieldname": "challan_serial_no",
                "fieldtype": "Data",
                "label": "Transfer Voucher/Challan Serial No (409)",
            },
            {
                "fieldname": "tds_deposited_by_book_entry",
                "fieldtype": "Data",
                "label": "Whether TDS Deposited by Book Entry (407)",
            },
            {
                "fieldname": "minor_head",
                "fieldtype": "Data",
                "label": "Minor head (411)",
            },
        ]
    elif filters.get("select") == "Deductee Details":
        columns = [
           {
                "fieldname": "deductee_serial_no",
                "fieldtype": "Data",
                "label": "Deductee Serial No (414)",
            },
            {
                "fieldname": "challan_serial_ref",
                "fieldtype": "Data",
                "label": "Challan Serial Reference (401)",
            },
            {
                "fieldname": "deductee_code",
                "fieldtype": "Data",
                "label": "Deductee Code (414)",
            },
            {
                "fieldname": "deducte_pan",
                "fieldtype": "Data",
                "label": "PAN of Deductee (415)",
            },
            {
                "fieldname": "deductee_name",
                "fieldtype": "Data",
                "label": "Name of the Deductee (416)",
            },
            {
                "fieldname": "section_code",
                "fieldtype": "Data",
                "label": "Section Code (417)",
            },
            {
                "fieldname": "pay_credit_date",
                "fieldtype": "Date",
                "label": "Payment/Credit Date (dd/mm/yyyy) (418)",
            },
            {
                "fieldname": "amount_paid",
                "fieldtype": "Currency",
                "label": "Amount Paid/Credited (419)",
            },
            {
                "fieldname": "tds",
                "fieldtype": "Currency",
                "label": "TDS",
            },
            {
                "fieldname": "surcharge",
                "fieldtype": "Currency",
                "label": "Surcharge",
            },
            {
                "fieldname": "education_cess",
                "fieldtype": "Currency",
                "label": "Education Cess",
            },
            {
                "fieldname": "total_tax_deducted",
                "fieldtype": "Currency",
                "label": "Total Tax Deducted (420)",
            },
            {
                "fieldname": "total_tax_deposited",
                "fieldtype": "Currency",
                "label": "Total Tax Deposited (421)",
            },
            {
                "fieldname": "deduction_rate",
                "fieldtype": "Float",
                "label": "Rate at which deducted (423)",
            },
            {
                "fieldname": "lower_deduction_reason",
                "fieldtype": "Data",
                "label": "Reason for Non-deduction/Lower Deduction (424)",
            },
            {
                "fieldname": "certificate_no",
                "fieldtype": "Data",
                "label": "Certificate number for Lower/non deduction (425)",
            },
            {
                "fieldname": "amount_excess_1cr_Sec194n",
                "fieldtype": "Data",
                "label": "Amount Excess 1Cr-Sec194N",
            },
            {
                "fieldname": "section_194nf",
                "fieldtype": "Data",
                "label": "Section 194NF; ITR not Filed (1: 20L-1Cr,2:excess of 1Cr)",
            },
        ]
    elif filters.get("select") == "Section":
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
                "width":800

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
        
    elif filters.get("select") == "Challan Details":
        sql = """
			SELECT
                ROW_NUMBER() OVER (ORDER BY TDS.name) AS "serial_no",
                TDS.total_tds_amount AS "tds",
                 "surcharge",
                 "education_cess",
                TDS.interest AS "interest",
                 "fee",
                TDS.others AS "other",
                (TDS.total_tds_amount+TDS.interest+TDS.others) AS "total_tax",
                TDS.bank_code AS "bsr_code",
                TDS.challan_date AS "tax_date",
                TDS.challan_number AS "challan_serial_no",
                 "tds_deposited_by_book_entry",
                TDS.name AS "minor_head"
            FROM
                `tabTDS Deduction Selection` AS TDS
            WHERE TDS.category LIKE %s
        """
        data = frappe.db.sql(sql,'TDS%',as_dict=True)
        return data
    elif filters.get("select") == "Deductee Details":
        sql = """
			SELECT
                ROW_NUMBER() OVER (ORDER BY TDS.name) AS "deductee_serial_no",
                CASE WHEN @prev_tds_name != TDS.name THEN @challan_serial_ref := @challan_serial_ref + 1 ELSE @challan_serial_ref END AS "challan_serial_ref",
                @prev_tds_name := TDS.name AS "tds_name",
                S.custom_company_status AS "deductee_code",
                S.pan AS "deducte_pan",
                S.name AS "deductee_name",
                TWC.custom_section AS "section_code",
                TDS.challan_date AS "pay_credit_date",
                "amount_paid",
                PIT.tax_amount AS "tds",
                "surcharge",
                "education_cess",
                PIT.tax_amount AS "total_tax_deducted",
                PIT.tax_amount AS "total_tax_deposited",
                # CASE 
                #     WHEN LDC.rate IS NOT NULL THEN LDC.rate 
                #     ELSE TWR.tax_withholding_rate
                # END AS "deduction_rate",
                PIT.tax_amount*100/PI.total AS "deduction_rate",
                LDC.custom_reason AS "lower_deduction_reason",
                LDC.name AS "certificate_no",
                TDS.name AS "amount_excess_1cr_Sec194n",
                TDS.name AS "section_194nf"
            FROM
                (SELECT @prev_tds_name := NULL, @challan_serial_ref := 1) vars,
                `tabTDS Deduction Selection` AS TDS
            INNER JOIN 
                `tabPurchase Invoice` AS PI 
                ON ((PI.posting_date BETWEEN TDS.from_date AND TDS.to_date) 
                    AND (PI.tax_withholding_category LIKE CONCAT (SUBSTRING_INDEX(TDS.category, ' - ',3), '%'))
                    AND PI.docstatus = 1) 
            JOIN
                `tabPurchase Taxes and Charges` AS PIT
                ON PIT.parent = PI.name
            LEFT JOIN 
                `tabSupplier` AS S 
                ON S.name = PI.supplier 
            LEFT JOIN 
                `tabTax Withholding Category` AS TWC 
                ON TWC.name = TDS.category
            LEFT JOIN 
                `tabTax Withholding Rate` AS TWR 
                ON TWR.parent = TWC.name
            LEFT JOIN 
                `tabLower Deduction Certificate` AS LDC 
                ON (LDC.tax_withholding_category = TDS.category
                    AND LDC.supplier = PI.supplier) 
        """
        data = frappe.db.sql(sql,as_dict=True)
        return data
    elif filters.get("select") == "Section":
        sql = """
			SELECT
                ROW_NUMBER() OVER (ORDER BY creation) AS "serial_no",
                TM.section AS "section",
                TM.ctegory as "section_desc"
                
            FROM
                `tabTDS Master` AS TM where TM.section LIKE '19%';
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
                "reason_description": "Lower Deduction/ No deduction u/s 197"
			},
            {
                "reason": "B",
                "reason_description": "No deduction u/s 197A (15G/15H)"
			},
            {
                "reason": "C",
                "reason_description": "Higher Rate (Valid PAN not available)"
			},
            {
                "reason": "D",
                "reason_description": "No/Lower deduction on payment made on account of notification issued u/sub-sec(5) - sec194A"
			},
            {
                "reason": "E",
                "reason_description": "No deduction on payment being made to a person"
			},
            {
                "reason": "M",
                "reason_description": "No deduction/lower deduction on account of notification issued under second provison to section 194N"
			},
            {
                "reason": "N",
                "reason_description": "No deduction-clause(iii, iv or v)-Section 194N"
			},
            {
                "reason": "O",
                "reason_description": "No deduction as per provisions of sub-section(2A) - section 194LBA"
			},
            {
                "reason": "R",
                "reason_description": "Deduction on Interest Income-Senior Citizens"
			},
            {
                "reason": "S",
                "reason_description": "Software Providers"
			},
            {
                "reason": "T",
                "reason_description": "Transporter"
			},
            {
                "reason": "Y",
                "reason_description": "Threshold Limit"
			},
            {
                "reason": "Z",
                "reason_description": "No deduction u/s 197A (1F)"
			},
		]
        return data
	   
    return []


