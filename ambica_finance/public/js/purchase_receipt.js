frappe.ui.form.on("Purchase Receipt", {
    refresh: function(frm) {
        frappe.call({
            method: "ambica_finance.public.py.block_supplier.block_supplier",
            args: {
                all: 'All',
                other: 'All'
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