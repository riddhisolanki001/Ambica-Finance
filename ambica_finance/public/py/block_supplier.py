import frappe

@frappe.whitelist()
def block_supplier(all, other):
    query = f"""
        SELECT 
            `tabSupplier`.`name`
        FROM 
            `tabSupplier`
        WHERE 
            coalesce(`tabSupplier`.`custom_hold_type`, '') NOT IN (%s, %s) 
            OR `tabSupplier`.`custom_effective_date` >  CURDATE()
        ORDER BY
            `tabSupplier`.`modified` ASC, 
            `tabSupplier`.`idx` DESC
        LIMIT 20 OFFSET 0;
    """
    params = (all, other)
    data = frappe.db.sql(query, params, as_dict=True)
    # Extract supplier names from the result
    supplier_names = [row.get('name') for row in data]			
    return supplier_names