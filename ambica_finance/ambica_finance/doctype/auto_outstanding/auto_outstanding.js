frappe.ui.form.on("Auto Outstanding", {
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

        // if (frm.fields_dict['outstandings'] && frm.fields_dict['outstandings'].grid) {
        //     // Iterate through the child table and set the color dynamically
        //     frm.fields_dict['outstandings'].grid.get_field('invoice_number').get_query = function(doc, cdt, cdn) {
        //         var child = locals[cdt][cdn];
        //         var condition = frm.doc.due_date && child.due_date && frm.doc.due_date < child.due_date;
        
        //         if (condition) {
        //             // Set the color field based on the condition
        //             frappe.model.set_value(cdt, cdn, 'invoice_number', '#b7e1cd'); // Light green
        //         } else {
        //             frappe.model.set_value(cdt, cdn, 'invoice_number', '#f3c0c0'); // Light red
        //         }
        //     };
        // }
        
    },

    msme: function (frm) {
        if (!frm.doc.msme) {
            console.log("shouldn't add msme when it's not selected")
            // If msme is unchecked, remove related invoices
            // removeMsmeInvoices(frm);
        } else {
            // If msme is checked, you can keep your existing logic here
            frappe.call({
                method: 'ambica_finance.ambica_finance.doctype.auto_outstanding.auto_outstanding.get_msme_invoices',
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
                                row.msme_added = 1; // Add a flag to mark it as added during msme_checked
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
            method: 'ambica_finance.ambica_finance.doctype.auto_outstanding.auto_outstanding.get_invoices',
            args: {
                bank_name: frm.doc.bank_name,
                due_date: frm.doc.due_date
            },
            callback: function(response) {
                console.log(response.message);
                if (response && response.message) {
                    // Clear existing rows in the child table
                    frm.clear_table('outstandings');

                    // Sort the invoices by 'party_name' in ascending order
                    // var sortedInvoices = response.message.sort((a, b) => (a.party_name > b.party_name) ? 1 : -1);

                    // Iterate through the sorted invoices and add rows to the child table
                    response.message.forEach(function(invoice) {
                        var row = frappe.model.add_child(frm.doc, 'Outstanding Child', 'outstandings');
                        row.invoice_number = invoice.name;  // Replace with actual field names
                        // Add other fields as needed
                    });

                    // Refresh the child table
                    frm.refresh_field('outstandings');
                }
            }
        });
    },

    // not_due: function (frm) {
    //     frappe.call({
    //         method: 'ambica_finance.ambica_finance.doctype.auto_outstanding.auto_outstanding.get_not_due_invoices',
    //         args: {
    //             bank_name: frm.doc.bank_name,
    //             due_date: frm.doc.due_date
    //         },
    //         callback: function (response) {
    //             console.log(response.message);
    //             if (response && response.message) {
    //                 // Sort the new invoices by 'party_name' in ascending order
    //                 // var sortedInvoices = response.message.sort((a, b) => (a.party_name > b.party_name) ? 1 : -1);

    //                 // Iterate through the sorted invoices and add rows to the child table
    //                 response.message.forEach(function (invoice) {
    //                     // Check if the invoice is not already in the table
    //                     if (!isInvoiceAlreadyAdded(frm, invoice.name)) {
    //                         // Find the index where the row should be inserted to maintain sorting order
    //                         // var index = findInsertIndex(frm, invoice.party_name);

    //                         var row = frappe.model.add_child(frm.doc, 'Outstanding Child', 'outstandings');
    //                         row.invoice_number = invoice.name;
    //                         row.party_name = invoice.party_name; 
    //                     }
    //                 });
    //                 frm.refresh_field('outstandings');
    //             }
    //         }
    //     });
    //     function isInvoiceAlreadyAdded(frm, invoiceNumber) {
    //         return frm.doc.outstandings.some(function (row) {
    //             return row.invoice_number === invoiceNumber;
    //         });
    //     }
    //     // Function to find the index where the row should be inserted to maintain sorting order
    //     // function findInsertIndex(frm, partyName) {
    //     //     var index = 0;
    //     //     for (var i = 0; i < frm.doc.outstandings.length; i++) {
    //     //         if (frm.doc.outstandings[i].party_name < partyName) {
    //     //             index = i + 1;
    //     //         } else {
    //     //             break;
    //     //         }
    //     //     }
    //     //     return index;
    //     // }
    // },

    not_due: function (frm) {
        // Call the Python method to get not-due invoices
        frappe.call({
            method: "ambica_finance.ambica_finance.doctype.auto_outstanding.auto_outstanding.get_not_due_invoices",
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
                            // d.hide();
                            var existingInvoices = [];
                            
                            selections.forEach(selectedInvoice => {
                                // Check if the invoice is already in the 'Outstandings' table
                                var existingRow = frm.doc.outstandings.find(row => row.invoice_number === selectedInvoice);
                        
                                if (!existingRow) {
                                    // If not present, add it to the 'Outstandings' table
                                    var row = frm.add_child('outstandings');
                                    row.invoice_number = selectedInvoice;
                                    // Set other relevant fields like amount, etc.
                                } else {
                                    // If already present, add it to the list of existing invoices
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

// function removeMsmeInvoices(frm) {
//     // Iterate through the outstandings and remove the ones added during msme_checked
//     frm.doc.outstandings.forEach(function (row, index) {
//         if (row.msme_added) {
//             console.log("tryna remove them")
//             frappe.model.clear_doc(frm.doc, 'Outstanding Child', row.name);
//         }
//     });

//     frm.refresh_field('outstandings');
// }


frappe.ui.form.on('Outstanding Child', {
    outstandings_add: function(frm) {
        frm.add_custom_button(__('Payment'), function() {
            var selected_rows = frm.fields_dict['outstandings'].grid.get_selected_children();

            if (selected_rows && selected_rows.length > 0) {
                var bank_name = frm.doc.bank_name;
                var payment_date = frm.doc.payment_date;

                // Call server script to handle payment entry creation
                frappe.call({
                    method: 'ambica_finance.ambica_finance.doctype.auto_outstanding.auto_outstanding.create_payment_entry',
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