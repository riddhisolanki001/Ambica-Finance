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
	},
    before_save: function(frm) {
        if  (! frm.is_new() && !localStorage.getItem('values')) {
            frappe.prompt([
                {
                    fieldtype: 'Data',
                    label: __('Audit Log Remark'),
                    fieldname: 'user_input',
                    reqd: true
                }
            ], function(values){
                localStorage.setItem('values', values.user_input);
                frm.save();
            }, __('What is the reason for this modification?'), __('Submit'));
            if  (!localStorage.getItem('values')) {
                frappe.validated = false;
            }
        }
    },
    after_save: function(frm) {
        frappe.call ({
            method: "ambica_finance.public.py.version.version_remark",
            args: {"remark":  localStorage.getItem('values')},
            callback: function() {
                localStorage.removeItem('values');
            }
        });
    },
});