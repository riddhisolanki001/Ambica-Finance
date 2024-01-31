import frappe
@frappe.whitelist()

def delete_doc(doctype, name,remark):
	if frappe.is_table(doctype):
		values = frappe.db.get_value(doctype, name, ["parenttype", "parent", "parentfield"])
		if not values:
			raise frappe.DoesNotExistError
		parenttype, parent, parentfield = values
		parent = frappe.get_doc(parenttype, parent)
		for row in parent.get(parentfield):
			if row.name == name:
				parent.remove(row)
				parent.save()
				break
	else:
		frappe.delete_doc(doctype, name, ignore_missing=False)
@frappe.whitelist()		
def add_to_deleted_document(doctype,name,remark,custom_owner,dr_acocunt_name,cr_acocunt_name,creation,voucher_date,dr_amount,cr_amount):
	"""Add this document to Deleted Document table. Called after delete"""
	if doctype != "Deleted Document" and frappe.flags.in_install != "frappe":
		dt = frappe.get_last_doc("Deleted Document", filters={"deleted_doctype": doctype,"deleted_name":name})
		dt.custom_remark=remark
		dt.custom_owner=custom_owner
		dt.save()
		frappe.db.commit()
		delete_log=frappe.new_doc("Deleted Log")
		delete_log.deleted_doctype=doctype
		delete_log.deleted_name=name
		delete_log.created_by=custom_owner
		delete_log.remark=remark
		delete_log.dr_acocunt_name=dr_acocunt_name
		delete_log.cr_acocunt_name=cr_acocunt_name
		delete_log.date_time_stamp_of_entry=creation
		delete_log.voucher_date=voucher_date
		delete_log.dr_amount=dr_amount
		delete_log.cr_amount=cr_amount
		delete_log.save()
		frappe.db.commit()