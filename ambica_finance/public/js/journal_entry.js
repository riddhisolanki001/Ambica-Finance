frappe.ui.form.on('Journal Entry', {
	refresh:function(frm){
		cur_frm.add_custom_button(__('Delete'), function () {
            let title = cur_frm.doc.name;
            let doctype = cur_frm.doctype;
			var dr_acocunt_name= ""
            var cr_acocunt_name = ""
            frm.doc.accounts.forEach(function(child2) {
                if (child2.debit_in_account_currency) {
                    dr_acocunt_name = child2.debit_in_account_currency;
                }
                if (child2.credit_in_account_currency) {
                    cr_acocunt_name = child2.credit_in_account_currency
                }
            });
            if (cur_frm.doc.docstatus == 1) {
                frappe.throw(doctype + " " + cur_frm.doc.name + ": Submitted Record cannot be deleted. You must Cancel it first.");
            } else {
                frappe.prompt([
                    {
                        label: 'Remark',
                        fieldname: 'remark',
                        fieldtype: 'Small Text',
                        reqd: 1
                    }
                ], function (values) {
                    frappe.confirm(__("Permanently delete {0}?", [title.bold()]), function () {
                        frappe.call({
                            method: "ambica_finance.delete_doc.delete_doc",
                            args: {
                                doctype: doctype,
                                name: cur_frm.doc.name,
                                remark: values.remark
                            },
                            callback: function (r, rt) {

                                frappe.call({
                                    method: "ambica_finance.delete_doc.add_to_deleted_document",
                                    args: {
                                        doctype: doctype,
                                        name: title,
                                        remark: values.remark,
                                        custom_owner: cur_frm.doc.owner,
                                        dr_acocunt_name:dr_acocunt_name,
                                        cr_acocunt_name:cr_acocunt_name,
                                        creation:cur_frm.doc.creation,
                                        voucher_date:cur_frm.doc.posting_date,
                                        dr_amount:cur_frm.doc.total_debit,
                                        cr_amount:cur_frm.doc.total_credit
                                    },
                                    callback: function (r) {
                                        frappe.set_route("List", doctype);
                                    }
                                })

                            },
                        });
                    });
                }, __("Enter Reason"));
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
    on_submit:function(frm){
        alert("cfdnjgfn")
        frappe.call({
            method: "ambica_finance.backend_code.delete_not_approve_gl_entery.delete_entry",
            args: {"name": cur_frm.doc.name},
            callback: function() {
                localStorage.removeItem('values');
            }
        });
    },
})