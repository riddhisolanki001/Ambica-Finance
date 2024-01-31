frappe.ui.form.on("Purchase Invoice", {
    refresh: function(frm) {
        frm.set_df_property('get_advances','hidden',1);
        frappe.call({
            method: "ambica_finance.public.py.block_supplier.block_supplier",
            args: {
                all: 'All',
                other: 'Invoices'
            },
            callback: function(responce){
                var supplier_names = responce.message;
                frm.set_query("supplier", function() {
                    return {
                        filters: {
                            'name': ['in', supplier_names]
                        }
                    };
                });
            }
        });
    },
    supplier: function(frm) {
        frm.fields_dict['get_advances'].$input.click();
        frm.set_df_property('get_advances','hidden',1);
        payment_from_supplier_bill_date = frappe.db.get_value('Supplier', {'name': frm.doc.supplier}, 'custom_payment_from_supplier_bill_date')
        .then((responce) => {
            payment_from_supplier_bill_date = responce.message['custom_payment_from_supplier_bill_date'];
            if (payment_from_supplier_bill_date) {
                frm.set_df_property('bill_date', 'hidden', 1);
                frm.set_df_property('custom_supplier_invoice_date', 'hidden', 0);
            } else {
                frm.set_df_property('bill_date', 'hidden', 0);
                frm.set_df_property('custom_supplier_invoice_date', 'hidden', 1);
            }
        });
    },
});