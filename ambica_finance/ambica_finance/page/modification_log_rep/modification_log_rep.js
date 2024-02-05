frappe.pages['modification-log-rep'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Modification Log Report',
		single_column: true
	});

    let fields = [
        {
            label: 'From Date',
            fieldtype: 'Date',
            fieldname: 'from'
        },
        {
            label: 'To Date',
            fieldtype: 'Date',
            fieldname: 'to'
        }
    ];
    
    function convert_date_format(date){
        var inputDate = new Date(date);
        // Format the date using toLocaleDateString with the appropriate options
        var formattedDate = inputDate.toLocaleDateString('en-GB'); // 'en-GB' for dd/mm/yyyy format
        return formattedDate;
    }

	// Apply filters from localStorage after reloading
	function applyFiltersFromLocalStorage() {
		fromDate = localStorage.getItem('fromDate');
		toDate = localStorage.getItem('toDate');
        // Set values in date fields if they exist
        if (page.fields_dict['from']) {
            page.fields_dict['from'].set_input(fromDate);
        }
        if (page.fields_dict['to']) {
            page.fields_dict['to'].set_input(toDate);
        }
	}
	
	fields.forEach(field => {
		let filterField = page.add_field(field);
		// Add an event listener for the "blur" event instead of "change"
		filterField.$input.on('blur', function() {
			var changing_value = filterField.get_value();
			// The code inside this block will be executed when the date is selected
			if (field.fieldname === 'from' && fromDate != changing_value && changing_value) {
				localStorage.setItem('fromDate', changing_value);
				if (toDate) {
					location.reload(true);
					// body.empty()
				}
			}
			if (field.fieldname === 'to' && toDate != changing_value && changing_value ) {
				localStorage.setItem('toDate', changing_value);
				if (fromDate) {
					location.reload(true);
					// body.empty()
				}
            }
		});
		applyFiltersFromLocalStorage();
	});

    dateFrom = convert_date_format(fromDate)
    dateTo = convert_date_format(toDate)

	frappe.call({
		method:
		"ambica_finance.ambica_finance.page.modification_log_rep.modification_log_rep.frm_call",
		args: {
			fromDate: fromDate,
			toDate: toDate
		},
		callback: function (response) {
			let records = response.message;
			for (let record of records){
				record.data = JSON.parse(record.data);
				console.log(record.data)
				
			}
			company = frappe.defaults.get_user_default("Company")
			$(frappe.render_template("modification_log_rep", { company, records})).appendTo(page.body);
		}
	});
}