// Copyright (c) 2023, riddhi and contributors
// For license information, please see license.txt
var symbol = "0";
var TOTAL = 0
frappe.ui.form.on('Bill Purchase', {
    treasury_bill: function(frm) {
        calculateNetInterest(frm);
    },
    spread: function(frm) {
        calculateNetInterest(frm);
    },
    subsequent: function(frm) {
        calculateNetInterest(frm);
    },
    refresh(frm) {
        // Add a custom button for exporting Sales Invoice List
        frm.add_custom_button(__('Export Invoice'), function() {
            frappe.call({
                method: "ambica_finance.ambica_finance.doctype.bill_purchase.bill_purchase.get_sales_invoice_for_bill_purchase",
                args:{
                    'customer':frm.doc.customer
                },
                callback: function(r) {
                    if (r.message) {
                        let d = new frappe.ui.form.MultiSelectDialog({
                            doctype: "Sales Invoice",
                            target: frm,
                            setters: {
                                status: 'Overdue'
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
                                        row.grand_total = invoice.total;
                                        symbol = invoice.symbol
                                        TOTAL += invoice.grand_total
                                        console.log(symbol)
                                        console.log(TOTAL+ "<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>")
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
        // var totalAmount = frm.doc.table_vnvs.reduce(function(sum, row) {
        //     // console.log(symbol + "__________________________")
        //     // totality =  sum + (row.grand_total);
        //     // console.log(totality)
        //     return sum + (row.grand_total || 0);
        // }, 0);

        // Set the calculated total amount in the 'amount' field
        totalAmount = symbol + " " + TOTAL;
        frm.doc.amount = totalAmount;
        // Refresh the 'amount' field
        frm.refresh_field('amount');
        TOTAL = 0;
    },

    on_submit: function(frm) {
        frappe.call({
            method: 'ambica_finance.ambica_finance.doctype.bill_purchase.bill_purchase.create_Journal_entry',
            args:{
                'date':frm.doc.date,
                'company':frm.doc.company,
                'amount':frm.doc.amount
            },
            callback: function(r){
                frappe.msgprint(r.message)
            }
        });
    }
});


function calculateNetInterest(frm) {
    var treasury_bill = frm.doc.treasury_bill;
    var spread = frm.doc.spread;
    var subsequent = frm.doc.subsequent;


    // Check if start_date and days_to_add have valid values
    if (treasury_bill && spread && subsequent) {

        var NetInterest = treasury_bill + spread - subsequent
        // Set the calculated due_date in the due_date field
        frm.set_value('interest', NetInterest);
    }
}
