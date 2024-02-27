// Copyright (c) 2024, riddhi and contributors
// For license information, please see license.txt

// Create a script element
const script = document.createElement('script');
// Set the source attribute to the CDN URL of the xlsx library
script.src = 'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.17.3/xlsx.full.min.js';
// Append the script element to the document's head
document.head.appendChild(script);


frappe.ui.form.on("Auto Outstandings", {
    refresh:function(frm) {
        set_css(frm)
        
        frm.add_custom_button('Export Unadjusted', () => {
            frappe.call({ 
                method: "ambica_finance.ambica_finance.report.auto_payment_not_paid_remarks.auto_payment_not_paid_remarks.auto_payment_not_paid_remarks",
                callback: function(r) {
                    var data = r.message;
                    console.log(data)
                    let downloadCounter = localStorage.getItem('downloadCounter') || 1;
        
                    if (data.length > 1) {
                        // Combine report columns and data into one object
                        const jsonData = data;
                        const workbook = XLSX.utils.book_new();
                        const worksheet = XLSX.utils.json_to_sheet(jsonData, { skipHeader: true }); // Skip the first row
                        XLSX.utils.book_append_sheet(workbook, worksheet, "Sheet1");
                        // Convert workbook to binary Excel format
                        const excelData = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
                        // Convert binary Excel data to Blob
                        const blob = new Blob([excelData], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                        // Create download link
                        const a = document.createElement('a');
                        a.style.display = 'none';
                        document.body.appendChild(a);
                        if (downloadCounter > 1) {
                            a.download = `auto_payment_not_paid_remarks_${downloadCounter}.xlsx`;
                        } else {
                            a.download = 'auto_payment_not_paid_remarks.xlsx';
                        }
                        // Set href attribute of download link
                        a.href = window.URL.createObjectURL(blob);
                        a.click();
                        document.body.removeChild(a);
                        downloadCounter++;
                        localStorage.setItem('downloadCounter', downloadCounter);
                    } else {
                        frappe.msgprint(__('No data found in the report.'));
                    }
                }                
            });
        });
        // frm.fields_dict['bank_name'].get_query = function(doc, cdt, cdn) {
        //     console.log("bank accounts")
        //     return {
        //         filters: {
        //             account_type: 'Bank'
        //         }
        //     };
        // };    
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
    },

    // after_save: function (frm) {
    //     frappe.msgprint("You de button")
    //     frm.add_custom_button('Click Me', () => {
    //         frappe.msgprint("You clicked button")
    //     })
    // },

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
                    
                            // Loop through selected rows and set "Payment Entry" checkbox to true
                            $.each(selected_rows, function(index, row) {
                                // Assuming the checkbox fieldname is "payment_entry"
                                frappe.model.set_value(row.doctype, row.name, 'payment_entry', 1);
                            });
                    
                            // Refresh the form to reflect the changes
                            frm.refresh();
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
