// Copyright (c) 2023, riddhi and contributors
// For license information, please see license.txt

frappe.ui.form.on("TDS deduction selection", {
    refresh(frm) {

    },

    category: function (frm) {
        // Check if the 'category' field is not empty
        if (frm.doc.category) {
            frappe.call({
                method: "ambica_finance.ambica_finance.doctype.tds_deduction_selection.tds_deduction_selection.Tdsdeductionselection",
                args: {
                    'category': frm.doc.category,
                    'from_date': frm.doc.from_date,
                    'to_date': frm.doc.to_date
                },
                callback: function (r) {
                    console.log(r.message)
                    frm.clear_table('tds_deduction');

                    // Create second row in the child table using 'twcategory' data
                    let row_twcategory = frappe.model.add_child(frm.doc, 'TDS Deduction', 'tds_deduction');
                    row_twcategory.sub_category = r.message.twcategory[0].name;
                    row_twcategory.base_amount = r.message.purchase_invoices_for_category[0].base_amount;
                    row_twcategory.tds_rate = r.message.twcategory[0].tax_withholding_rate;
                    row_twcategory.tds_amount = r.message.purchase_invoices_for_category[0].tds_amount;
                    // Create first row in the child table using 'twc' data
                    let row_twc = frappe.model.add_child(frm.doc, 'TDS Deduction', 'tds_deduction');
                    row_twc.sub_category = r.message.twc[0].name;
                    row_twc.base_amount = r.message.purchase_invoices_fortwc[0].base_amount;
                    row_twc.tds_rate = r.message.twc[0].tax_withholding_rate;
                    row_twc.tds_amount = r.message.purchase_invoices_fortwc[0].tds_amount;

                    // Refresh the child table
                    frm.refresh_field('tds_deduction');

                    // Calculate the sum of base_amount from both rows
                    let totalBaseAmount = row_twcategory.base_amount + row_twc.base_amount;
                    let totalTDSAmount = row_twcategory.tds_amount + row_twc.tds_amount

                    // Set the calculated sum in the Total base amount field of the form
                    frm.set_value({
                        total_base_amount: totalBaseAmount,
                        total_tds_amount: totalTDSAmount
                    });

                    // Assuming 'category' is a variable in your JavaScript code
                    var category = frm.doc.category;  // Replace with the actual value

                    var categoryParts = category.split(' - ');
                    var category_pattern = categoryParts.slice(0, 3).join(' - ') + '%';

                    // Fetch list of purchase invoices with tax withholding category
                    frappe.call({
                        method: "frappe.client.get_list",
                        args: {
                            doctype: "Purchase Invoice",
                            filters: {
                                'tax_withholding_category': ['like', category_pattern],
                                'posting_date': ['between', [frm.doc.from_date, frm.doc.to_date]]
                            },
                            fields: ['name','credit_to', 'total', 'tax_withholding_category', 'taxes.tax_amount'],
                        },
                        callback: function (invoices) {
                            console.log(invoices.message);   
                            
                            frappe.call({
                                method: "frappe.client.get_list",
                                args: {
                                    doctype: "Tax Withholding Category",
                                    fields: ['name', 'rates.tax_withholding_rate'],
                                    filters:{
                                        'name': ['like',category_pattern]
                                    }
                                },
                                callback: function (twcItem) {
                                    console.log(twcItem.message);
                            
                                    // Declare twcItem using let before the loop
                                    let twcItemMessage = twcItem.message;
                            
                                    // Clear existing entries in the 'tds_reference' child table
                                    frm.clear_table('tds_reference');
                            
                                    // Loop through the fetched invoices and add rows to the 'tds_reference' child table
                                    for (let invoice of invoices.message) {
                                        let row = frappe.model.add_child(frm.doc, 'TDS Reference', 'tds_reference');
                                        row.title = invoice.credit_to;
                                        row.category = invoice.tax_withholding_category;
                                        row.base_amount = invoice.total;
                                        row.tds_amount = invoice.tax_amount;
                            
                                        // Loop through the fetched tax withholding categories
                                        for (let twcItem of twcItemMessage) {
                                            // Check if tax_withholding_category name matches
                                            if (invoice.tax_withholding_category == twcItem.name) {
                                                console.log(twcItem.tax_withholding_rate)
                                                row.rate = twcItem.tax_withholding_rate;
                                                // You can set other fields based on your logic
                                            }
                                        }
                                    }
                            
                                    // Refresh the 'tds_reference' child table
                                    frm.refresh_field('tds_reference');
                                }
                            });                   
                        }
                    });
                }
            });
        } else {
            // If 'category' field is empty, clear values from other fields
            frm.clear_table('tds_deduction');
            frm.refresh_field('tds_deduction');

            frm.set_value({
                total_base_amount: 0,
                total_tds_amount: 0
            });
        }
    }
});


frappe.ui.form.on("TDS Deduction", {
    select: function (frm, cdt, cdn) {
        var deductionRow = locals[cdt][cdn];
        var isAnyRowSelected = false;

        // Check if any row in 'TDS Deduction' has 'select' field selected
        $.each(frm.doc.tds_deduction || [], function (index, tdsDeductionRow) {
            if (tdsDeductionRow.select) {
                isAnyRowSelected = true;
                return false; // Break the loop if any row is selected
            }
        });

        // If any row is selected, update 'pay' field in 'tds_reference' child table
        if (isAnyRowSelected) {
            $.each(frm.doc.tds_reference || [], function (index, tdsReferenceRow) {
                // Check if 'title' matches with 'sub_category'
                if (tdsReferenceRow.category === deductionRow.sub_category) {
                    // Set 'pay' field to true for the matched row
                    frappe.model.set_value(tdsReferenceRow.doctype, tdsReferenceRow.name, 'pay', 1);
                }
            });
            // Refresh the 'tds_reference' child table
            frm.refresh_field('tds_reference');
        } else {
            // If no row is selected, clear 'pay' field in 'tds_reference' child table
            $.each(frm.doc.tds_reference || [], function (index, tdsReferenceRow) {
                frappe.model.set_value(tdsReferenceRow.doctype, tdsReferenceRow.name, 'pay', 0);
            });
            // Refresh the 'tds_reference' child table
            frm.refresh_field('tds_reference');
        }
    }
});

