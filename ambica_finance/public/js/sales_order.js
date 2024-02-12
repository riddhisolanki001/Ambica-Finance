frappe.ui.form.on("Sales Order", {
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