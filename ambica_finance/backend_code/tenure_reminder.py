import frappe
from frappe.utils import getdate, add_days, now
from datetime import timedelta


@frappe.whitelist()
def send_tenure_reminder():
    today_date = getdate(now())
    result_date = add_days(today_date, -10)
    final_date = result_date.strftime("%Y-%m-%d")
    data = frappe.db.sql(
        "select due_date , owner ,name from `tabEPC PCFC Entry` where due_date=%s",
        final_date,
        as_dict=True,
    )
    for i in range(len(data)):
        print("\n\n\n\n\n\n\n" + data[i]["owner"] + "\n\n\n\n\n\n\n\n")
        nm=data[i]['name']
        frappe.sendmail(
            recipients="riddhi@sanskartechnolab.com",
            subject="Tenure Periode Reminder",
            # sender="dhruvi@sanskartechnolab.com",
            message=f"""<html lang="en" style = "background-color: grey">

                <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                
                </head>

                <body style = "background-color: white; padding:10px 20px; margin: 70px">
                <h1>
                    Tenure Periode Reminder
                </h1>
                <p style="color: black;">Dear, Finance User</p>

                <p style="color: black;">Hello, Tenure Period of EPC Number {nm} is near to end please start required process from your side. click on the button below to view the Details
                </p>
                <br>
                <a href="{ frappe.utils.get_url_to_form('EPC PCFC Entry',nm) }" target="_blank" style="padding: 10px; background-color: black; color: white; text-decoration: none; display: inline-block;">View EPC Details</a>
                <br>
                <br>
                <p style="color: black;">Thank you for your immediate attention to this matter. Should you have any questions or require further assistance, feel free to reach out.</p>
                <br>
                <p style="color: black;">Thank You,</p>
                <p style="color: black;">Best Regards</p>

                </body>

                </html>
            """,
        )
        
        send_system_notification(nm)

    return "hello"
def send_system_notification(nm):

    # You can also create a notification in the database if needed
    frappe.get_doc({
        "doctype": "Notification Log",
        "subject": "TCS Configuration of Customer",
        "description": f"This is a system notification message.{ frappe.utils.get_url_to_form('EPC PCFC Entry',nm) }",
        "user": "admin@example.com",
        "doctype_or_module": "Notification",
        "reference_doctype": "EPC PCFC Entry",
        "reference_name": nm,
    }).insert(ignore_permissions=True)