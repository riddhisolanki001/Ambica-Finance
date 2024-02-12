import frappe

@frappe.whitelist()
def create_tax_withholding_category(category_name,sub_category, custom_type, custom_section, from_date, single_threshold,cumulative_threshold, to_date, tax_withholding_rate, company, account):
    try:
        # Define the two options for subcategory
        subcategory_options = ["Other", "Propritorship"]
    
        # Find the option other than the one in the current form
        new_sub_category = next(option for option in subcategory_options if option != sub_category)

        # Check if Tax Withholding Category already exists with the same parameters
        existing_category = frappe.get_all('Tax Withholding Category', filters={
            'custom_sub_category': new_sub_category,
            'custom_type': custom_type,
            'custom_section': custom_section,
            'category_name': category_name
        }) 
        if not existing_category:
            twc = frappe.new_doc('Tax Withholding Category')
            # Set the fields
            twc.custom_sub_category = new_sub_category
            twc.custom_type = custom_type
            twc.custom_section = custom_section

            twc.append('rates', {
                'from_date':from_date,
                'to_date':to_date,
                'tax_withholding_rate':tax_withholding_rate,
                'single_threshold':single_threshold,
                'cumulative_threshold':cumulative_threshold
            })
            twc.append('accounts', {
                'company': company,
                'account': account,
            })
            # Add more accounts as needed

            # Save the Journal Entry
            twc.insert()
            frappe.db.commit()
            return {'created': True, 'name': twc.name}
        else:
            return {'created': False, 'message': "Other Category for this Section Already Exists"}

    except Exception as e:
        frappe.log_error(f"Error in create_tax_withholding_category: {e}")
        frappe.db.rollback()
        return frappe.throw("Error occurred while creating Tax Withholding Category")
