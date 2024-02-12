import frappe

@frappe.whitelist()
def frm_call(fromDate, toDate):
        
    query = f"""
        SELECT
            DATE(V.modified) as voucher_date,
            V.modified,
            V.data,
            V.docname,
            V.name,
            V.modified_by,
            V.ref_doctype,
            V.custom_audit_log_remark,
            D.module,
            PO.creation AS po_c,
            PO.owner AS po_o,
            SO.creation AS so_c,
            SO.owner AS so_o,
            PE.creation AS pe_c,
            PE.owner AS pe_o,
            GE.creation AS ge_c,
            GE.owner AS ge_o,
            PI.creation AS pi_c,
            PI.owner AS pi_o,
            SI.creation AS si_c,
            SI.owner AS si_o
        FROM
            `tabVersion` AS V
            INNER JOIN `tabDocType` D ON D.name = V.ref_doctype
            LEFT JOIN `tabPurchase Order` PO ON PO.name = V.docname 
            LEFT JOIN `tabSales Order` SO ON SO.name = V.docname 
            LEFT JOIN `tabPayment Entry` PE ON PE.name = V.docname 
            LEFT JOIN `tabJournal Entry` GE ON GE.name = V.docname 
            LEFT JOIN `tabPurchase Invoice` PI ON PI.name = V.docname 
            LEFT JOIN `tabSales Invoice` SI ON SI.name = V.docname
        WHERE
            (DATE(V.modified) BETWEEN %s AND %s OR  %s = '' OR %s = '')
            AND V.ref_doctype IN ('Purchase Order', 'Sales Order', 'Payment Entry', 'Journal Entry', 'Purchase Invoice' ,'Sales Invoice')
        ORDER BY
            V.creation DESC;
    """
    filters = (fromDate, toDate, fromDate, toDate)
    versionData = frappe.db.sql(query, filters, as_dict=True)
    return versionData