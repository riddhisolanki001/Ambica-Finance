import frappe
from frappe import get_doc, ValidationError

@frappe.whitelist()
def update_epc(epc_name, amount):
    try:
        # Get the 'EPC PCFC Entry' document
        epc_entry = get_doc('EPC PCFC Entry', epc_name)

        # Convert amount to float
        amount = float(amount)

        # Update the 'balance' field
        new_balance = epc_entry.balance - amount

        # Check if the new_balance is not negative
        if new_balance < 0:
            raise ValidationError("Insufficient balance")

        # Set the new 'balance' value
        epc_entry.balance = new_balance

        # Check if the new_balance is 0
        if new_balance == 0:
            # Set balance to 0
            epc_entry.balance = 0

            # Change status to "Adjusted"
            epc_entry.status = "Adjusted"

        # Save the document
        epc_entry.save()
        
        return {"message": "Balance updated successfully"}
    except Exception as e:
        return {"exc": str(e)}
