frappe.ui.form.on("Version", {
    after_save: function(frm) {
        frappe.msgprint("dfghdf")
        x=localStorage.removeItem('values');
        console.log(x)
    },
});