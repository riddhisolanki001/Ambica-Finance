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
    refresh: function (frm) {
		cur_frm.add_custom_button(__('Delete'), function () {
			let title = cur_frm.doc.name;
			let doctype = cur_frm.doctype;
			var dr_acocunt_name = cur_frm.doc.paid_to
			var cr_acocunt_name = cur_frm.doc.paid_from
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
										dr_acocunt_name: dr_acocunt_name,
										cr_acocunt_name:cr_acocunt_name,
										creation:cur_frm.doc.creation,
										voucher_date:cur_frm.doc.posting_date,
										dr_amount:cur_frm.doc.paid_amount,
                                        cr_amount:cur_frm.doc.received_amount

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
	get_outstanding_invoices_or_orders: function (frm, get_outstanding_invoices, get_orders_to_be_billed) {
		const today = frappe.datetime.get_today();
		const fields = [
			{ fieldtype: "Section Break", label: __("Posting Date") },
			{
				fieldtype: "Date", label: __("From Date"),
				fieldname: "from_posting_date"
			},
			{ fieldtype: "Column Break" },
			{ fieldtype: "Date", label: __("To Date"), fieldname: "to_posting_date" },
			{ fieldtype: "Section Break", label: __("Due Date") },
			{ fieldtype: "Date", label: __("From Date"), fieldname: "from_due_date" },
			{ fieldtype: "Column Break" },
			{ fieldtype: "Date", label: __("To Date"), fieldname: "to_due_date" },
			{ fieldtype: "Section Break", label: __("Outstanding Amount") },
			{
				fieldtype: "Float", label: __("Greater Than Amount"),
				fieldname: "outstanding_amt_greater_than", default: 0
			},
			{ fieldtype: "Column Break" },
			{ fieldtype: "Float", label: __("Less Than Amount"), fieldname: "outstanding_amt_less_than" },
			{ fieldtype: "Section Break" },
			{
				fieldtype: "Link", label: __("Cost Center"), fieldname: "cost_center", options: "Cost Center",
				"get_query": function () {
					return {
						"filters": { "company": frm.doc.company }
					}
				}
			},
			{ fieldtype: "Column Break" },
			{ fieldtype: "Section Break" },
			{ fieldtype: "Check", label: __("Allocate Payment Amount"), fieldname: "allocate_payment_amount", default: 1 },
		];

		let btn_text = "";

		if (get_outstanding_invoices) {
			btn_text = "Get Outstanding Invoices";
		}
		else if (get_orders_to_be_billed) {
			btn_text = "Get Outstanding Orders";
		}

		frappe.prompt(fields, function (filters) {
			frappe.flags.allocate_payment_amount = true;
			frm.events.validate_filters_data(frm, filters);
			frm.doc.cost_center = filters.cost_center;
			frm.events.get_outstanding_documents(frm, filters, get_outstanding_invoices, get_orders_to_be_billed);
		}, __("Filters"), __(btn_text));
	},
});