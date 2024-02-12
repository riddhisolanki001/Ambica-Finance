import frappe

@frappe.whitelist()
def version_remark(remark):
    doc = frappe.get_last_doc('Version')
    doc.custom_audit_log_remark = remark
    doc.save()