frappe.ui.form.on('Purchase Invoice', {
	refresh:function(frm){
		cur_frm.add_custom_button(__('Delete'), function () {
            let title = cur_frm.doc.name;
            let doctype = cur_frm.doctype;
			var dr_acocunt_name= cur_frm.doc.paid_to
            var cr_acocunt_name = cur_frm.doc.credit_to
            
            frm.doc.items.forEach(function(child2) {
                if (child2.expense_account) {
                    dr_acocunt_name = child2.expense_account;
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
                                        dr_amount:cur_frm.doc.grand_total,
                                        cr_amount:cur_frm.doc.grand_total
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
	}
})