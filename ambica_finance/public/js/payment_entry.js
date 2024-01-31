frappe.ui.form.on('Payment Entry', {
	party_type(frm) {
        if (frm.doc.party_type == "Supplier") {
            frappe.call({
                method: "ambica_finance.public.py.block_supplier.block_supplier",
                args: {
                    all: 'All',
                    other: 'Payments'
                },
                callback: function(responce){
                    var supplier_names = responce.message;
                    frm.set_query("party", function() {
                        return {
                            filters: {
                                'name': ['in', supplier_names]
                            }
                        };
                    });
                }
            });
        }
        else {  
            frm.set_query("party", null);
        }
	}
});