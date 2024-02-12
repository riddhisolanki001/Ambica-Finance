frappe.ui.form.on("Purchase Order", {
    refresh: function(frm) {
        frappe.call({
            method: "ambica_finance.backend_code.block_supplier.block_supplier",
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
    },
    before_save: function(frm) {
        if  (! frm.is_new() && !localStorage.getItem('values') && frm.is_dirty()) {
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
            method: "ambica_finance.backend_code.version.version_remark",
            args: {"remark":  localStorage.getItem('values')},
            callback: function() {
                localStorage.removeItem('values');
            }
        });
    },
});