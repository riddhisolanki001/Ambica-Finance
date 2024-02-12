frappe.ui.form.on('Tax Withholding Category', {
    after_save: function (frm) {
        frappe.call({
            method: "ambica_finance.public.py.create_tax_withholding_category.create_tax_withholding_category",
            args: {
                'sub_category': frm.doc.custom_sub_category,
                'custom_type': frm.doc.custom_type,
                'custom_section': frm.doc.custom_section,
                'from_date': frm.doc.rates[0].from_date,
                'to_date': frm.doc.rates[0].to_date,
                'tax_withholding_rate': frm.doc.rates[0].tax_withholding_rate,
                'single_threshold': frm.doc.rates[0].single_threshold,
                'cumulative_threshold': frm.doc.rates[0].cumulative_threshold,
                'company': frm.doc.accounts[0].company,
                'account': frm.doc.accounts[0].account,
                'category_name':frm.doc.category_name
            },
            callback: function (response) {
                if (response.message.created) {
                    var formUrl = '/app/tax-withholding-category/' + response.message.name;
                    frappe.msgprint({
                        title: __('Notification'),
                        indicator: 'green',
                        message: 'New Tax Withholding Category <a href="' + formUrl + '">' + response.message.name + '</a> is created automatically. Click on the link to see it.',
                    });
                } else {
                    frappe.msgprint({
                        title: __('Notification'),
                        indicator: 'orange',
                        message: response.message.message,
                    });
                }
            }
            
        });
    }
});
