import frappe

def get_columns(filters, trans):
    # Define the months for which you want columns
    months = [
        "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"
    ]

    # Generate columns for each month
    month_columns = []
    for month in months:
        month_columns.append({"fieldname": f"{month.lower()}_qty", "label": f"{month}(Qty)", "fieldtype": "Currency", "width": 120})
        month_columns.append({"fieldname": f"{month.lower()}_amount", "label": f"{month}(Amount)", "fieldtype": "Currency", "width": 120})

        # Add extra 2 columns after every 6 columns starting from the 4th column
        if len(month_columns) >= 4 and (len(month_columns) - 4) % 6 == 0:
            month_columns.extend([
                {"fieldname": f"{month.lower()}_qty_diff", "label": "Qty Diff", "fieldtype": "Percent", "width": 120},
                {"fieldname": f"{month.lower()}_amount_diff", "label": "Amount Diff", "fieldtype": "Percent", "width": 120}
            ])

    # Concatenate basic columns and month-wise columns
    columns = month_columns

    # Prepare a dictionary of conditions to be returned
    conditions = {
        "columns": columns,
        "trans": trans,
        "months": months
    }

    return conditions

def calculate_percentage_difference(value1, value2):
    try:
        percentage_diff = (value2/value1)-1 
        Answer = percentage_diff * 100
        return Answer
    except ZeroDivisionError:
        return None

def calculate_and_fill_percentage_difference(row, cur_month_qty_col, prev_month_qty_col, cur_month_amount_col, prev_month_amount_col, month):
    if row[prev_month_qty_col] != 0:
        row[f"{month.lower()}_qty_diff"] = calculate_percentage_difference(row[prev_month_qty_col], row[cur_month_qty_col])
    else:
        row[f"{month.lower()}_qty_diff"] = None

    if row[prev_month_amount_col] != 0:
        row[f"{month.lower()}_amount_diff"] = calculate_percentage_difference(row[prev_month_amount_col], row[cur_month_amount_col])
    else:
        row[f"{month.lower()}_amount_diff"] = None

def execute(filters=None):
    columns = [
        {
            "fieldname": 'customer',
            "label": 'Customer',
            "fieldtype": 'Link',
            "options": 'Customer',
            "width": 180
        },
    ]

    # Call the get_columns method to get the dynamically generated columns
    dynamic_columns = get_columns(filters, None)

    # Extend the columns list with the dynamically generated columns
    columns.extend(dynamic_columns["columns"])

    # Your SQL query to fetch data (you may need to modify it based on your requirements)
    # Generate the part of the query for each month
    months = [
        "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"
    ]
    month_conditions_qty = [
        f"SUM(CASE WHEN MONTH(si.posting_date) = {month_num} THEN sii.qty ELSE 0 END) AS {month.lower()}_qty"
        for month_num, month in enumerate(months, start=4)
    ]
    month_conditions_amount = [
        f"SUM(CASE WHEN MONTH(si.posting_date) = {month_num} THEN sii.amount ELSE 0 END) AS {month.lower()}_amount"
        for month_num, month in enumerate(months, start=4)
    ]

    # Join the conditions using a comma
    month_query_qty = ", ".join(month_conditions_qty)
    month_query_amount = ", ".join(month_conditions_amount)

    # Use the generated query in your main SQL query
    sql = f"""
        SELECT 
            si.customer,
            {month_query_qty},
            {month_query_amount}
        FROM 
            `tabSales Invoice` as si
        LEFT JOIN
            `tabSales Invoice Item` as sii ON sii.parent = si.name
        
            
        GROUP BY si.customer
    """

    data = frappe.db.sql(sql, as_dict=True)

    for row in data:
        for month in dynamic_columns["months"]:
            cur_month_qty_col = f"{month.lower()}_qty"
            cur_month_amount_col = f"{month.lower()}_amount"

            prev_month_index = (dynamic_columns["months"].index(month) - 1) % 12
            prev_month_qty_col = f"{dynamic_columns['months'][prev_month_index].lower()}_qty"
            prev_month_amount_col = f"{dynamic_columns['months'][prev_month_index].lower()}_amount"

            calculate_and_fill_percentage_difference(row, cur_month_qty_col, prev_month_qty_col, cur_month_amount_col, prev_month_amount_col, month)

    return columns, data