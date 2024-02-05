// Copyright (c) 2023, riddhi and contributors
// For license information, please see license.txt

frappe.ui.form.on("TDS deduction selection", {
	refresh(frm) {

	},

    category:function(frm){
        frappe.call({
            method: "ambica_finance.ambica_finance.doctype.tds_deduction_selection.tds_deduction_selection.Tdsdeductionselection",
            args:{
                'category':frm.doc.category,
                'from_date':frm.doc.from_date,
                'to_date':frm.doc.to_date
            },
            callback:function(r){
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


            }
        });
    }
});
