# Copyright (c) 2023, riddhi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TDSDeductionSelection(Document):
	pass


@frappe.whitelist()
def Tdsdeductionselection(category, from_date, to_date):
    sql = """
        SELECT twc.name, twr.tax_withholding_rate
        FROM `tabTax Withholding Category` AS twc 
        INNER JOIN `tabTax Withholding Rate` AS twr ON twr.parent = twc.name
        WHERE twc.name LIKE %s
    """

    # Extracting the first three elements and creating the pattern
    category_pattern = f"{' - '.join(category.split(' - ')[:3])}%"
    category_Type= category.split(' - ')[0]

    twcategory = frappe.db.sql(sql, category, as_dict=True)
    twc = frappe.db.sql(sql, (f'{category_pattern} - Other'), as_dict=True)
    twc_name = twc[0].get('name')

    # from_date = twcategory[0].get('from_date')
    # to_date = twcategory[0].get('to_date')
    
    # from_date_twc = twc[0].get('from_date')
    # to_date_twc = twc[0].get('to_date')

    sql_purchase_invoices_for_category = """
        SELECT SUM(pi.total) as base_amount, SUM(ptc.tax_amount) as tds_amount 
        FROM `tabPurchase Invoice` AS pi 
        INNER JOIN `tabPurchase Taxes and Charges` AS ptc ON ptc.parent = pi.name 
        WHERE pi.tax_withholding_category = %s AND pi.posting_date BETWEEN %s AND %s
    """

    sql_sales_invoices_for_category = """
        SELECT SUM(si.total) as base_amount, SUM(stc.tax_amount) as tds_amount 
        FROM `tabSales Invoice` AS si 
        INNER JOIN `tabSales Taxes and Charges` AS stc ON stc.parent = si.name 
        LEFT JOIN `tabCustomer` as c ON si.Customer = c.name
        WHERE c.tax_withholding_category = %s AND si.posting_date BETWEEN %s AND %s
    """

    purchase_invoices_for_category = frappe.db.sql(sql_purchase_invoices_for_category, (category, from_date, to_date), as_dict=True)

    sales_invoices_for_category = frappe.db.sql(sql_sales_invoices_for_category, (category, from_date, to_date), as_dict=True)

    purchase_invoices_fortwc = frappe.db.sql(sql_purchase_invoices_for_category, (twc_name, from_date, to_date), as_dict=True)
    
    sales_invoices_fortwc = frappe.db.sql(sql_sales_invoices_for_category, (twc_name, from_date, to_date), as_dict=True)

    if category_Type == "TDS":
        return {
            'twcategory': twcategory,
            'twc': twc,
            'invoices_for_category': purchase_invoices_for_category,
            'invoices_fortwc': purchase_invoices_fortwc,
        }
    else:
         return{
            'twcategory': twcategory,
            'twc': twc,
            'invoices_for_category' : sales_invoices_for_category,
            'invoices_fortwc' : sales_invoices_fortwc
         }
    # return []