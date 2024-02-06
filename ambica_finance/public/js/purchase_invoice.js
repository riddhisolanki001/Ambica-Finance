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

