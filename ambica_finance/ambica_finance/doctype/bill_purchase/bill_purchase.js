// Copyright (c) 2023, riddhi and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bill Purchase', {
    refresh(frm) {
        // Add a custom button for exporting Sales Invoice List
        frm.add_custom_button(__('Export Invoice'), function() {
            frappe.call({
                method: "ambica_finance.ambica_finance.doctype.bill_purchase.bill_purchase.get_sales_invoice_for_bill_purchase",
                callback: function(r) {
                    if (r.message) {
                        let d = new frappe.ui.form.MultiSelectDialog({
                            doctype: "Sales Invoice",
                            target: frm,
                            setters: {
                                status: 'Unpaid'
                            },
                            get_query() {
                                return {
                                    filters: { 
                                        name: ['in', r.message.map(item => item.name)] 
                                    }
                                };
                            },
                            action(selections) {
                                // Ensure the child table is empty before adding new rows
                                frm.doc.table_vnvs = [];
                            
                                selections.forEach(selectedInvoice => {
                                    var invoice = r.message.find(item => item.name === selectedInvoice);
                                    if (invoice) {
                                        var row = frappe.model.add_child(frm.doc, 'table_vnvs');
                                        row.invoice_number = selectedInvoice;
                                        row.invoice_date = invoice.posting_date;
                                        row.invoice_due_date = invoice.due_date;
                                        row.exchange_rate = invoice.conversion_rate;
                                        row.grand_total = invoice.grand_total;
                                    }
                                });
                            
                                frm.refresh_field('table_vnvs'); // Refresh the child table
                                console.log("Selected invoices:", selections);
                                d.$wrapper.hide();
                            },
                        });
                    }
                }
            });
        });
    },

    before_save: function(frm) {
        // Calculate sum of grand_total from table_vnvs
        var totalAmount = frm.doc.table_vnvs.reduce(function(sum, row) {
            return sum + (row.grand_total || 0);
        }, 0);

        // Set the calculated total amount in the 'amount' field
        frm.doc.amount = totalAmount;

        // Refresh the 'amount' field
        frm.refresh_field('amount');
    }
});
