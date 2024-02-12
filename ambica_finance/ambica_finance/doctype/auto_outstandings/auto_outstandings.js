// Copyright (c) 2024, riddhi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Auto Outstandings", {
    refresh:function(frm) {
        set_css(frm)	

        frm.fields_dict['bank_name'].get_query = function(doc, cdt, cdn) {
            console.log("bank accounts")
            return {
                filters: {
                    account_type: 'Bank'
                }
            };
        };    
    },

    msme: function (frm) {
        if (!frm.doc.msme) {
            console.log("shouldn't add msme when it's not selected")
        } else {
            frappe.call({
                method: 'ambica_finance.ambica_finance.doctype.auto_outstandings.auto_outstandings.get_msme_invoices',
                args: {
                    bank_name: frm.doc.bank_name,
                    due_date: frm.doc.due_date
                },
                callback: function (response) {
                    console.log(response.message);
                    if (response.message) {
                        response.message.forEach(function (invoice) {
                            // Check if the invoice is not already in the table
                            if (!isInvoiceAlreadyAdded(frm, invoice.name)) {
                                var row = frappe.model.add_child(frm.doc, 'Outstanding Child', 'outstandings');
                                row.invoice_number = invoice.name;
                                row.party_name = invoice.party_name;
                            }
                        });
                        frm.refresh_field('outstandings');
                    }
                }
            });
            function isInvoiceAlreadyAdded(frm, invoiceNumber) {
                return frm.doc.outstandings.some(function (row) {
                    return row.invoice_number === invoiceNumber;
                });
            }
        }
    },

    get_invoices: function(frm) {
        frappe.call({
            method: 'ambica_finance.ambica_finance.doctype.auto_outstandings.auto_outstandings.get_invoices',
            args: {
                bank_name: frm.doc.bank_name,
                due_date: frm.doc.due_date
            },
            callback: function(response) {
                console.log(response.message);
                if (response && response.message) {
                    // Clear existing rows in the child table
                    frm.clear_table('outstandings');

                    // Iterate through the sorted invoices and add rows to the child table
                    response.message.forEach(function(invoice) {
                        var row = frappe.model.add_child(frm.doc, 'Outstanding Child', 'outstandings');
                        row.invoice_number = invoice.name;  // Replace with actual field names
                    });

                    frm.refresh_field('outstandings');
                }
            }
        });
    },

    not_due: function (frm) {
        frappe.call({
            method: "ambica_finance.ambica_finance.doctype.auto_outstandings.auto_outstandings.get_not_due_invoices",
            args: {
                bank_name: frm.doc.bank_name,
                due_date: frm.doc.due_date
            },
            callback: function (r) {
                if (r.message) {
                    // Set the filters for the Purchase Invoice query
                    let d = new frappe.ui.form.MultiSelectDialog({
                        doctype: "Purchase Invoice",
                        target: frm,
                        setters: {
                            status: 'Unpaid'
                        },
                        add_filters_group: 1,
                        date_field: "due_date",
                        get_query() {
                            return {
                                filters: { 
                                    name: ['in', r.message.map(item => item.name)] 
                                }
                            };
                        },
                        action(selections) {
                            // Check if the selected invoices are already in the 'Outstandings' table
                            var existingInvoices = [];
                            
                            selections.forEach(selectedInvoice => {
                                var existingRow = frm.doc.outstandings.find(row => row.invoice_number === selectedInvoice);
                        
                                if (!existingRow) {
                                    var row = frm.add_child('outstandings');
                                    row.invoice_number = selectedInvoice;
                                } else {
                                    existingInvoices.push(selectedInvoice);
                                }
                            });
                        
                            if (existingInvoices.length > 0) {
                                frappe.msgprint(__('Invoices already in the table: ') + existingInvoices.join(', '));
                            }
                        
                            frm.refresh_field('outstandings'); // Refresh the child table
                            console.log("Selected invoices:", selections);
                            d.$wrapper.hide();
                        },
                    });
                }
            }
        });
    }

});

// Helper function to check if an invoice is already added
function isInvoiceAlreadyAdded(frm, invoiceNumber) {
    return frm.doc.outstandings.some(function (row) {
        return row.invoice_number === invoiceNumber;
    });
}

frappe.ui.form.on('Outstanding Child', {
    outstandings_add: function(frm) {
        frm.add_custom_button(__('Payment'), function() {
            var selected_rows = frm.fields_dict['outstandings'].grid.get_selected_children();

            if (selected_rows && selected_rows.length > 0) {
                var bank_name = frm.doc.bank_name;
                var payment_date = frm.doc.payment_date;

                // Call server script to handle payment entry creation
                frappe.call({
                    method: 'ambica_finance.ambica_finance.doctype.auto_outstandings.auto_outstandings.create_payment_entry',
                    args: {
                        selected_rows: selected_rows,
                        bank_name: bank_name,
                        payment_date: payment_date
                    },
                    callback: function(response) {
                        if (!response.exc) {
                            frappe.msgprint('Payment entries created successfully');
                        } else {
                            frappe.msgprint('Error creating payment entries: ' + response.exc);
                        }
                    }
                });
            } else {
                frappe.msgprint('No rows selected.');
            }
        });
    }
});

function set_css(frm){
    console.log("hello");
	document.querySelectorAll("[data-fieldname = 'get_invoices']")[1].style.backgroundColor = 'black';
    document.querySelectorAll("[data-fieldname = 'get_invoices']")[1].style.marginTop = '5px';
	document.querySelectorAll("[data-fieldname = 'get_invoices']")[1].style.color = 'white';
	
	document.querySelectorAll("[data-fieldname = 'not_due']")[1].style.backgroundColor = 'black';
    document.querySelectorAll("[data-fieldname = 'not_due']")[1].style.marginTop = '5px';
	document.querySelectorAll("[data-fieldname = 'not_due']")[1].style.color = 'white';

}
