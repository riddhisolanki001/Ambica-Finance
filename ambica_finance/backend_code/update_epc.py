import frappe

@frappe.whitelist()
def update_epc(epc_name,amount):
    epc_entry = frappe.get_doc('EPC PCFC Entry',epc_name)

    sql = """
            SELECT epc_ref.amount,
                pe.name,
                epc_ref.epc_name
            FROM `tabPayment Entry` as pe INNER JOIN `tabPayment Entry EPC` as epc_ref ON epc_ref.parent = pe.name 
    """

    epc_entry.balance = epc_entry.amount - amount
    epc_entry.save()
    frappe.db.commit()
    return "Balance updated Successfully"
