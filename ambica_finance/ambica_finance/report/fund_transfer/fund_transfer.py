# Copyright (c) 2024, riddhi and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):

    columns = [
        {
            "fieldname": "static",
            "fieldtype": "Data",
            "label": "Transaction Type",
        },
        {
            "fieldname": "none",
            "fieldtype": "data",
            "label": "Beneficiary Code",
        },
        {
            "fieldname": "bank_account_no",
            "fieldtype": "Data",
            "label": "Beneficiary Account Number",
        },
        {
            "fieldname": "paid_amount",
            "fieldtype": "Currency",
            "label": "Instrument Amount",
        },
        {
            "fieldname": "party_name",
            "fieldtype": "Data",
            "label": "Beneficiary Name",
        },
        {
            "fieldname": "none",
            "fieldtype": "Data",
            "label": "Blank",
        },
        {
            "fieldname": "none",
            "fieldtype": "Data",
            "label": "Blank",
        },
        {
            "fieldname": "address_line1",
            "fieldtype": "data",
            "label": "Beneficiary Address 1",
        },
        {
            "fieldname": "address_line2",
            "fieldtype": "data",
            "label": "Beneficiary Address 2",
        },
        {
            "fieldname": "city",
            "fieldtype": "data",
            "label": "Beneficiary Address 3",
        },
        {
            "fieldname": "remarks",
            "fieldtype": "Small Text",
            "label": "Beneficiary Address 4",
        },
        {
            "fieldname": "remarks",
            "fieldtype": "Small Text",
            "label": "Beneficiary Address 5",
        },
        {
            "fieldname":"reference_no",
            "fieldtype":"data",
            "label":"Instruction Reference Number"
		},
        {
            "fieldname":"party_name",
            "fieldtype":"data",
            "label":"Customer  Reference Number"
		},
        {
            "fieldname":"",
            "fieldtype":"data",
            "label":"Payment Details 1"
		},
        {
            "fieldname":"",
            "fieldtype":"data",
            "label":"Payment Details 2"
		},
        {
            "fieldname":"",
            "fieldtype":"data",
            "label":"Payment Details 3"
		},
        {
            "fieldname":"",
            "fieldtype":"data",
            "label":"Payment Details 4"
		},
        {
            "fieldname":"",
            "fieldtype":"data",
            "label":"Payment Details 5"
		},
        {
            "fieldname":"",
            "fieldtype":"data",
            "label":"Payment Details 6"
		},
        {
            "fieldname":"",
            "fieldtype":"data",
            "label":"Payment Details 7"
		},
        {
            "fieldname": "none",
            "fieldtype": "Data",
            "label": "Blank",
        }, 
        {
            "fieldname": "posting_date",
            "fieldtype":"Date",
            "label":"Transaction Date"
		},
        {
            "fieldname": "none",
            "fieldtype": "Data",
            "label": "Blank",
        }, 
        {
            "fieldname": "none",
            "fieldtype": "Data",
            "label": "Blank",
        }, 
        {
            "fieldname": "none",
            "fieldtype": "Data",
            "label": "Blank",
        }, 
        {
            "fieldname": "none",
            "fieldtype": "Data",
            "label": "Blank",
        },
        {
            "fieldname": "email",
            "fieldtype":"Data",
            "label":"Beneficiary E Mail"
		},           
    ]
    
    sql="""
		SELECT 
        	pe.party_name,
            ba.bank_account_no,
            pe.paid_amount,
            pe.reference_no,
            pe.posting_date
        FROM 
        	`tabPayment Entry` as pe
        INNER JOIN
			`tabSupplier` as s ON s.name = pe.party
        LEFT JOIN
			`tabBank Account` as ba ON ba.name = s.default_bank_account
        WHERE pe.payment_type = "Pay" AND pe.custom_neftrtgs = "Fund Transfer"
	"""
    conditions = []
    if filters:
        from_date = filters.get("from_date")
        to_date = filters.get("to_date")

        if from_date and to_date:
            conditions.append(f"pe.posting_date BETWEEN '{from_date}' AND '{to_date}'")
        
        if conditions:
            sql += " AND " + " AND ".join(conditions)



    data=frappe.db.sql(sql,as_dict=True)
    
    unique_party_names = set(row.get("party_name") for row in data)
    address_data_dict={}

    for party_name in unique_party_names:
        # Fetch the parent names using dynamic_link_data
        parent_names = dynamic_link_data(party_name)

        # Fetch address data for each parent name and store it in the dictionary
        for parent in parent_names:
            address_data_dict[parent] = fetch_address_data(parent)

    for row in data:
        row["static"] = "I"
        party_name = row.get("party_name")
        email_id = frappe.db.get_value('Contact', {'name': f'-{party_name}'}, 'email_id')
        row["email"] = email_id
        # Get the parent names from dynamic_link_data
        parent_names = dynamic_link_data(party_name)

        # Initialize an empty list to store address data
        address_data_result = []

        # Fetch address data for each parent name
        for parent in parent_names:
            address_data_result += address_data_dict.get(parent, [])

        # Set address details into columns
        set_address_data_into_columns(row, address_data_result)

    return columns,data

def set_address_data_into_columns(row, address_data_result):
    # Assuming you want to set address data into the first row of the result
    if address_data_result:
        # Assuming only one address for simplicity
        address_data = address_data_result[0]

        # Directly access the list elements and set them in columns
        row["address_line1"] = address_data.get("address_line1", "")
        row["address_line2"] = address_data.get("address_line2", "")
        row["city"] = address_data.get("city", "")

    return row


def dynamic_link_data(party_name):
    try:
        filters = {
            "parenttype": "Address",
            "link_title": party_name,
            "link_doctype": "Supplier"
        }

        dynamic_link_data = frappe.get_all(
            "Dynamic Link",
            filters=filters,
            fields=['parent']
        )

        print(f"Dynamic Link Data for {party_name}: {dynamic_link_data}")

        # Extract only the parent names from the dynamic link data
        parent_names = [dynamic_link.get("parent") for dynamic_link in dynamic_link_data]

        return parent_names

    except frappe.DoesNotExistError:
        print("Dynamic Link doctype does not exist")

    except Exception as e:
        print(f"Error fetching data from Dynamic Link: {e}")

def fetch_address_data(parent):
    try:
        # address_fields = [address_line1, address_line2, city]
        filter = {
            "name": parent,
            "is_primary_address": 1
        }

        address_data = frappe.get_all(
            "Address",
            filters=filter,
            fields=['address_line1', 'address_line2', 'city']
        )
        print(f"Address Data for {parent}: {address_data}")

        return address_data

    except frappe.DoesNotExistError:
        print("Address doctype does not exist")

    except Exception as e:
        print(f"Error fetching data from Address: {e}")