import frappe

@frappe.whitelist(allow_guest=1)
def update_epc_status(epcNames):
    for epcName in epcNames:
        epc_doc = frappe.get_doc('EPC PCFC Entry', epcName)
        # Update the 'status' field or any other fields as needed
        epc_doc.status = 'Adjusted'
        epc_doc.save()
    
    return "Status updated successfully"