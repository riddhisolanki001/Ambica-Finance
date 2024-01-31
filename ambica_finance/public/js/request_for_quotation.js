frappe.ui.form.on('Request for Quotation', {
    refresh: function(frm) {
        frappe.call({
            method: "ambica_finance.public.py.block_supplier.block_supplier",
            args: {
                all: 'All',
                other: 'All'
            },
            callback: function(responce){
                var supplier_names = responce.message;
                frm.fields_dict['suppliers'].grid.get_field('supplier').get_query = function(frm, cdt, cdn) {
                    // var child = locals[cdt][cdn];
                    return {
                        filters: {
                            'name': ['in', supplier_names]
                        }
                    };
                };
            }
        });
    }
});