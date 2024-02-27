frappe.ui.form.on("Customer", {
    refresh:function(frm){
        if(cur_frm.doc.tax_withholding_category!=undefined){
			find_section(frm)
		}
    },
    tax_withholding_category:function(frm){
		find_section(frm)
	}
})
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