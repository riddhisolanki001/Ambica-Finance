import frappe
from frappe.utils import getdate, add_days, now
from datetime import timedelta

@frappe.whitelist()
def change_date():
    date=now()
    filters={"custom_to_date": (">=",date)}
    data=frappe.get_all("Currency Exchange",filters=filters ,fields=["name"])
    data_len=len(data)
    for i in range(data_len):
        get_data=frappe.get_doc("Currency Exchange",data[i]["name"])
        get_data.date=now()
        get_data.save()
        frappe.db.commit()
    return data
