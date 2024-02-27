// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on("Supplier", {
	setup: function (frm) {
		frm.set_query('default_price_list', { 'buying': 1 });
		if (frm.doc.__islocal == 1) {
			frm.set_value("represents_company", "");
		}
		frm.set_query('account', 'accounts', function (doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			return {
				filters: {
					"account_type": ["in", ["Payable", "Payable/Receivable"]],
					'company': d.company,
					"is_group": 0
				}
			}
		});
		frm.set_query("default_bank_account", function () {
			return {
				filters: {
					"is_company_account": 1
				}
			}
		});

		frm.set_query("supplier_primary_contact", function (doc) {
			return {
				query: "erpnext.buying.doctype.supplier.supplier.get_supplier_primary_contact",
				filters: {
					"supplier": doc.name
				}
			};
		});

		frm.set_query("supplier_primary_address", function (doc) {
			return {
				filters: {
					"link_doctype": "Supplier",
					"link_name": doc.name
				}
			};
		});
		if (cur_frm.doc.custom_msme == "Yes") {
			frm.set_query("payment_terms", function (doc) {
				return {
					filters: {
						"custom_allow_msme": 1,
					}
				};
			});
		}
		frm.set_query('custom_default_party_bank_account', function(doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {
                filters: {
                    'party': frm.doc.name,
                    // "is_group": "1",


                }
            };
        });
	},
	custom_msme:function(frm){
		if (cur_frm.doc.custom_msme == "Yes") {
			frappe.call({
				method: "frappe.client.get_value",
				args: {
					doctype: "Payment Terms Template",
					fieldname: ["name"],
					filters: {
						"custom_allow_msme": 1
					},
				},
				callback: function(r) {
					// alert(r)
					var custom_allow_msme = r.message.name;
					frm.set_value("payment_terms", custom_allow_msme);

				},
			});
			frm.set_query("payment_terms", function (doc) {
				return {
					filters: {
						"custom_allow_msme": 1,
					}
				};
			});
		}
	},
	refresh: function (frm) {
		
		frappe.dynamic_link = { doc: frm.doc, fieldname: 'name', doctype: 'Supplier' }

		if (frappe.defaults.get_default("supp_master_name") != "Naming Series") {
			frm.toggle_display("naming_series", false);
		} else {
			erpnext.toggle_naming_series();
		}

		if (frm.doc.__islocal) {
			hide_field(['address_html', 'contact_html']);
			frappe.contacts.clear_address_and_contact(frm);
		}
		else {
			unhide_field(['address_html', 'contact_html']);
			frappe.contacts.render_address_and_contact(frm);

			// custom buttons
			frm.add_custom_button(__('Accounting Ledger'), function () {
				frappe.set_route('query-report', 'General Ledger',
					{ party_type: 'Supplier', party: frm.doc.name, party_name: frm.doc.supplier_name });
			}, __("View"));

			frm.add_custom_button(__('Accounts Payable'), function () {
				frappe.set_route('query-report', 'Accounts Payable', { supplier: frm.doc.name });
			}, __("View"));

			frm.add_custom_button(__('Bank Account'), function () {
				erpnext.utils.make_bank_account(frm.doc.doctype, frm.doc.name);
			}, __('Create'));

			frm.add_custom_button(__('Pricing Rule'), function () {
				erpnext.utils.make_pricing_rule(frm.doc.doctype, frm.doc.name);
			}, __('Create'));

			frm.add_custom_button(__('Get Supplier Group Details'), function () {
				frm.trigger("get_supplier_group_details");
			}, __('Actions'));

			if (cint(frappe.defaults.get_default("enable_common_party_accounting"))) {
				frm.add_custom_button(__('Link with Customer'), function () {
					frm.trigger('show_party_link_dialog');
				}, __('Actions'));
			}

			// indicators
			erpnext.utils.set_party_dashboard_indicators(frm);
		}
		if(cur_frm.doc.tax_withholding_category!=undefined){
			find_section(frm)
		}
	},
	get_supplier_group_details: function (frm) {
		frappe.call({
			method: "get_supplier_group_details",
			doc: frm.doc,
			callback: function () {
				frm.refresh();
			}
		});
	},

	supplier_primary_address: function (frm) {

		if (frm.doc.supplier_primary_address) {
			frappe.call({
				method: 'frappe.contacts.doctype.address.address.get_address_display',
				args: {
					"address_dict": frm.doc.supplier_primary_address
				},
				callback: function (r) {
					frm.set_value("primary_address", r.message);
				}
			});
		}
		if (!frm.doc.supplier_primary_address) {
			frm.set_value("primary_address", "");
		}
	},

	supplier_primary_contact: function (frm) {
		if (!frm.doc.supplier_primary_contact) {
			frm.set_value("mobile_no", "");
			frm.set_value("email_id", "");
		}
	},

	is_internal_supplier: function (frm) {
		if (frm.doc.is_internal_supplier == 1) {
			frm.toggle_reqd("represents_company", true);
		}
		else {
			frm.toggle_reqd("represents_company", false);
		}
	},
	show_party_link_dialog: function (frm) {
		const dialog = new frappe.ui.Dialog({
			title: __('Select a Customer'),
			fields: [{
				fieldtype: 'Link', label: __('Customer'),
				options: 'Customer', fieldname: 'customer', reqd: 1
			}],
			primary_action: function ({ customer }) {
				frappe.call({
					method: 'erpnext.accounts.doctype.party_link.party_link.create_party_link',
					args: {
						primary_role: 'Supplier',
						primary_party: frm.doc.name,
						secondary_party: customer
					},
					freeze: true,
					callback: function () {
						dialog.hide();
						frappe.msgprint({
							message: __('Successfully linked to Customer'),
							alert: true
						});
					},
					error: function () {
						dialog.hide();
						frappe.msgprint({
							message: __('Linking to Customer Failed. Please try again.'),
							title: __('Linking Failed'),
							indicator: 'red'
						});
					}
				});
			},
			primary_action_label: __('Create Link')
		});
		dialog.show();
	},
	custom_block_supplier(frm) {
		if (frm.doc.custom_block_supplier) {
			frm.set_value('custom_hold_type', "All");
		}
		else {
			frm.set_value('custom_hold_type', "");
		}
	},
	validate: function (frm) {
		if (cur_frm.doc.custom_import == 0 && cur_frm.doc.pan == undefined) {
			frappe.throw("Please fill in at least one mandatory fields.")
		}
	},
	after_save: function(frm) {
		if (cur_frm.doc.country == "India") {
			if (!cur_frm.doc.custom_default_party_bank_account) {
				var bankAccount = frappe.new_doc('Bank Account',fields={"party_type":"Supplier","party":cur_frm.doc.name});
				frappe.msgprint("Please Add Bank Account Details");
				
			}
		}
	},
	tax_withholding_category:function(frm){
		find_section(frm)
	}
	
	
});
function find_section(frm){
	frappe.call({
		method: "frappe.client.get_value",
		args: {
			doctype: "Tax Withholding Category",
			fieldname: ["custom_section"],
			filters: {
				"name": cur_frm.doc.tax_withholding_category
			},
		},
		callback: function(r) {
			// alert(r)
			var custom_section = r.message.custom_section;
			if (custom_section=="194Q"){
				frm.set_df_property("pan", "reqd", "1");
				// frm.set_value("payment_terms", custom_allow_msme);
			}
		},
	});
	
}