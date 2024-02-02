// Copyright (c) 2023, riddhi and contributors
// For license information, please see license.txt

frappe.ui.form.on('EPC PCFC Entry', {

    date:function(frm){
        calculateDueDate(frm);

    },
    days:function(frm){
        calculateDueDate(frm);

    },

    finance_effect: function(frm) {
        frappe.call({
            method: 'ambica_finance.ambica_finance.doctype.epc_pcfc_entry.epc_pcfc_entry.create_Journal_entry',
            args:{
                'date':frm.doc.date,
                'due_date':frm.doc.due_date,
                'company':frm.doc.custom_company,
                'bank_name':frm.doc.bank_name,
                'reference_number':frm.doc.reference_number,
                'amount':frm.doc.amount
            },
            callback: function(r){
                frappe.msgprint(r.message)
            }
        });
    }
});

function calculateDueDate(frm) {
    var date = frm.doc.date;
    var days = frm.doc.days;

    // Check if start_date and days_to_add have valid values
    if (date && days) {
        // Parse start_date to Date object
        date = frappe.datetime.str_to_obj(date);

        // Calculate due_date by adding days_to_add to start_date
        var due_date = frappe.datetime.add_days(date, days);

        // Set the calculated due_date in the due_date field
        frm.set_value('due_date', frappe.datetime.obj_to_str(due_date));
    }
}
