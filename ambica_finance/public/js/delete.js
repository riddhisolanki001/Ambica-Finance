
// Wait for hashchange or page load events
$(window).on('hashchange', page_changed);
$(window).on('load', page_changed);

// Callback function for hashchange and page load events
function page_changed() {
    // Wait for the page to load completely
    frappe.after_ajax(function () {
        // Get the current route
        var route = frappe.get_route();
        console.log(route);

        // Check if the route corresponds to a Form
        if (route[0] === "Form") {
            console.log("Form Name:", route[1]);
            cur_frm.cscript.onload = function (frm) {
                console.log("Onload event triggered");
                delete_doc(frm)
                // Your custom logic for the refresh event here
            };
            console.log("After frappe.ui.form.on")
        } else {
            console.log("Not a Form page");
        }
    });
}

function delete_doc(frm) {
    if (cur_frm.doctype == "Payment Entry" || cur_frm.doctype == "Purchase Invoice" || cur_frm.doctype == "Journal Entry" || cur_frm.doctype == "Sales Invoice") {
        var dr_acocunt_name=""
        if(cur_frm.doctype=="Payment Entry"){
            dr_acocunt_name= cur_frm.doc.paid_to
        }
        // if(cur_frm.doctype=="Purchase Invoice"){

        //     dr_acocunt_name= cur_frm.doc.paid_to
        // }
        // if(cur_frm.doctype=="Payment Entry"){
        //     dr_acocunt_name= cur_frm.doc.paid_to
        // }
        if(cur_frm.doctype=="Sales Invoice"){
            dr_acocunt_name= cur_frm.doc.debit_to
        }
        cur_frm.add_custom_button(__('Delete'), function () {
            let title = cur_frm.doc.name;
            let doctype = cur_frm.doctype;

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
                                        dr_acocunt_name:dr_acocunt_name
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
}