import frappe
@frappe.whitelist()
def delete_entry(name):
    data= frappe.db.sql("select name from `tabNot Approve GL Entery` where voucher_no=%s",name,as_dict=True)
    
    for i in range(len(data)):
        doc = frappe.get_doc("Not Approve GL Entery", data[i]["name"])
        print("\n\n\n\n" , doc.docstatus,"\n",doc.name,"\n\n\n")
        # Check if the document is in the "Submitted" status
        if doc.docstatus == 1:
            # Set the document status to "Cancelled"
            # frappe.db.set_value("Not Approve GL Entery", data[i]["name"], "is_cancelled", 1,ignore_missing=True)
            # doc.save()
            # print("\n\n\n",doc.is_cancelled,"\n\n\n")
            # frappe.db.commit()
            doc.cancel()
            
           
        
            frappe.delete_doc("Not Approve GL Entery", data[i]["name"], ignore_missing=True)
        
    