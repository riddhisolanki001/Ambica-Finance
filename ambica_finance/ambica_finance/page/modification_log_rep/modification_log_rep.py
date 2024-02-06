import frappe
# from datetime import datetime

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
    # query = f"""
    #     SELECT
    #         DATE(V.modified) as voucher_date,
    #         V.modified,
    #         V.data,
    #         V.docname,
    #         V.name,
    #         V.modified_by,
    #         V.ref_doctype,
    #         D.module
    #     FROM
    #         `tabVersion` AS V
    #         INNER JOIN `tabDocType` D ON D.name = V.ref_doctype
    #     WHERE
    #         (DATE(V.modified) BETWEEN %s AND %s OR  %s = '' OR %s = '')
    #         AND V.ref_doctype IN ('Purchase Order', 'Sales Order', 'Payment Entry', 'GL Entry', 'Purchase Invoice', 'Sales Invoice')
    #     ORDER BY
    #         V.creation DESC;
    # """
    # query = f"""
    #     SELECT
    #         V.*
    #     FROM
    #         `tabSales Invoice` AS V
    #     ORDER BY
    #         V.creation DESC;
    # """
    # filters = ()
    filters = (fromDate, toDate, fromDate, toDate)
    versionData = frappe.db.sql(query, filters, as_dict=True)
    return versionData
    # query = f"""
    #     SELECT
    #         P.name,
    #         P.date,
    #         P.party
    #     FROM
    #         `tabProcurement` AS P
    #     WHERE
    #         P.docstatus = 1 AND
    #         (%s = '' OR P.party = %s) AND
    #         (P.date BETWEEN %s AND %s OR  %s = '' OR %s = '')
    #     ORDER BY
    #         P.date DESC
    # """
    # filters = (supplier, supplier, fromDate, toDate, fromDate, toDate)
    # procurementData = frappe.db.sql(query, filters, as_dict=True)
    
    # grand_data = []
    # for pData in procurementData:
    #     pName = pData.name
    #     pData.date = (pData.date).strftime("%d-%m-%Y")
    #     query = f"""
    #         SELECT
    #             PI.item,
    #             PI.quantity,
    #             PI.uom
    #         FROM
    #             `tabProcurement Item` AS PI
    #         WHERE
    #             (%s = '' OR PI.item = %s) AND
    #             PI.parent = %s
    #         ORDER BY
    #             PI.item ASC
    #     """
    #     filters = (item_name, item_name, pName)
    #     procurementItemData = frappe.db.sql(query, filters, as_dict=True)
    #     for pIData in procurementItemData:
    #         pData["pIData"] = procurementItemData
    #         pItem = pIData.item
    #         query = f"""
    #             SELECT
    #                 PR.posting_date as grn_date,
    #                 PR.name as grn_no,
    #                 PRI.amount,
    #                 PR.custom_total_duty,
    #                 PRI.qty,
    #                 PR.bill_of_entry_number,
    #                 PR.custom_bill_date
    #             FROM
    #                 `tabPurchase Receipt` AS PR
    #             JOIN
    #                 `tabPurchase Receipt Item` AS PRI ON
    #                 PR.name = PRI.parent
    #             WHERE
    #                 PR.custom_procurement_id = %s AND
    #                 PR.docstatus = 1 AND
    #                 (PR.posting_date BETWEEN %s AND %s OR  %s = '' OR %s = '') AND
    #                 PRI.item_code = %s
    #             ORDER BY
    #                 grn_date DESC
    #         """
    #         filters = (pName, fromDate, toDate, fromDate, toDate, pItem)
            
    #         purchaseReceiptData = frappe.db.sql(query, filters, as_dict=True)
    #         for pRData in purchaseReceiptData:
    #             pRData.grn_date = frappe.utils.formatdate(pRData.grn_date, 'dd-mm-yyyy')
    #             pRData.custom_bill_date = (pRData.custom_bill_date).strftime("%d.%m.%Y")
    #             pIData["purchaseReceiptData"] = purchaseReceiptData
    #     grand_data.append(pData)
    # return grand_data