frappe.ui.form.on("Purchase Order", {
    refresh: function(frm) {
        frappe.call({
            method: "ambica_finance.public.py.block_supplier.block_supplier",
            args: {
                all: 'All',
                other: 'Purchase Order'
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
    }
});