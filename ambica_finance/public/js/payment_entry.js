frappe.ui.form.on('Payment Entry', {
	party_type(frm) {
        if (frm.doc.party_type == "Supplier") {
            frappe.call({
                method: "ambica_finance.backend_code.block_supplier.block_supplier",
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
    // before_save: function(frm) {
    //     if  (! frm.is_new() && !localStorage.getItem('values') && frm.is_dirty()) {
    //         frappe.prompt([
    //             {
    //                 fieldtype: 'Data',
    //                 label: __('Audit Log Remark'),
    //                 fieldname: 'user_input',
    //                 reqd: true
    //             }
    //         ], function(values){
    //             localStorage.setItem('values', values.user_input);
    //             frm.save();
    //         }, __('What is the reason for this modification?'), __('Submit'));
    //         if  (!localStorage.getItem('values')) {
    //             frappe.validated = false;
    //         }
    //     }
    // },

	before_save: function(frm) {
			console.log(frm.doc.references);
			console.log(frm.doc.references.length);
			if (frm.doc.references.length == 0) {
				console.log(frm.doc.remarks,">>>>>>>>>>>>>>>>>>")
				frm.set_value('custom_remarks', 1);
				frm.refresh_field('custom_remarks');
				if(frm.doc.remarks == 'undefined'){
					frappe.validated = false;
				}
				frappe.validated = true;	
			}
			if (frm.doc.references.length != 0) {
				frm.set_value('custom_remarks', 0);
				frm.refresh_field('custom_remarks');
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
    refresh: function (frm) {

		frm.fields_dict['custom_generate_om'].grid.get_field('exchange_rate').df.onchange = function(doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            calculateInrAmount(child);
        };

        frm.fields_dict['custom_generate_om'].grid.get_field('fc_amount').df.onchange = function(doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            calculateInrAmount(child);
        };

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

		frm.add_custom_button(__('Get Items From EPC'), function () {
			let d = new frappe.ui.form.MultiSelectDialog({
				doctype: "EPC PCFC Entry",
				target: frm,
				setters: {
					bank_name: null,
					amount: null,
					date: null,
					due_date: null
				},
				size: 'large',
				add_filters_group: 1,
				date_field: "date",
				get_query() {
					return {
						filters: {
							docstatus: ['=', 1],
						}
					};
				},
				action(selections) {
					// Ensure the child table is empty before adding new rows
					frm.doc.custom_epc_references = [];
		            if (selections.length > 1) {
						frappe.msgprint(__('You can only select one row.'));
						return;
					}
					selections.forEach(epcName => {
						// Find the corresponding EPC object based on epcName
						frappe.call({
							method: 'frappe.client.get',
							args: {
							doctype: 'EPC PCFC Entry',
							name: epcName
							},
							callback: function(response) {
							if (response.message) {
								var epcDetails = response.message;
								console.log(typeof epcDetails);
						
								var name = epcDetails.name;
								var date = epcDetails.date;
								var due_date = epcDetails.due_date;
								var bank_name = epcDetails.bank_name;
								var balance = epcDetails.balance ;
						
								// Assuming frm is your current form object
								var row = frappe.model.add_child(frm.doc, 'custom_epc_references');
								row.epc_name = name;
								row.date = date;
								row.due_date = due_date;
								row.amount = balance;
								row.bank_name = bank_name;
						
								// Refresh the form to show the newly added child row
								frm.refresh_field('custom_epc_references');
							} else {
								// Handle the case when EPC details are not found
								console.error('EPC details not found for ' + epcName);
							}
							}
						});
					});
					d.dialog.hide();
				},
			});
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
	on_submit:function(frm){
        frappe.call({
            method: "ambica_finance.backend_code.delete_not_approve_gl_entery.delete_entry",
            args: {"name": cur_frm.doc.name},
			async:false,
            callback: function() {
                localStorage.removeItem('values');
            }
        });

		// // Iterate through the child table and collect epc_names
		// var epcNames = [];
		// frm.doc.custom_epc_references.forEach(function(row) {
		// epcNames.push(row.epc_name);
		// });

		// // Update the 'status' field in 'EPC PCFC Entry' documents
		// frappe.call({
		// 	method: "ambica_finance.backend_code.payment_entry.update_epc_status",
		// 	args: {
		// 		epcNames: epcNames
		// 	},
		// 	async:false,
		// 	callback: function(response) {
		// 		if (response.message) {
		// 		// Handle the response if needed
		// 		console.log('Status updated successfully');
		// 		}
		// 	}
		// });

    },
	before_submit: function(frm) {
		
		// // Iterate through the child table and collect epc_names
		// var epcData = frm.doc.custom_epc_references.map(function(row) {
		// 	return {
		// 		epc_name: row.epc_name,
		// 		amount: row.amount
		// 	};
		// });

		var customEpcReferencesTable = frm.doc.custom_epc_references || [];

		customEpcReferencesTable.forEach(function(row) {
			// Accessing values for each row
			console.log(row.epc_name + "_____________________________-" + row.amount);
		
			// Update the 'status' field in 'EPC PCFC Entry' documents for each row
			frappe.call({
				method: "ambica_finance.backend_code.update_epc.update_epc",
				args: {
					'epc_name': row.epc_name,
					'amount': row.amount
				},
				callback: function(response) {
					if (response.message) {
						// Handle the response if needed
						console.log('Status updated successfully for row: ' + row.epc_name);
					}
				}
			});
		});
		
	},
    // custom_generate_om_add: function(frm) {
	// 	frm.fields_dict['custom_generate_om'].grid.get_field('exchange_rate').df.onchange = frappe.model.curry(calculateInrAmount);
	// 	frm.fields_dict['custom_generate_om'].grid.get_field('fc_amount').df.onchange = frappe.model.curry(calculateInrAmount);
		
    // }
});
function calculateInrAmount(child) {
    console.log('Calculating InrAmount');
    var exchangeRate = child.exchange_rate;
    var fcAmount = child.fc_amount;

    console.log('Exchange Rate:', exchangeRate);
    console.log('FC Amount:', fcAmount);

    var inrAmount = exchangeRate * fcAmount;
    console.log('Calculated InrAmount:', inrAmount);

    frappe.model.set_value(child.doctype, child.name, 'inr_amount', inrAmount);
}
