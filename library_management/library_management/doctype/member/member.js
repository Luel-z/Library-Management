// Copyright (c) 2025, Luel Fekadu and contributors
// For license information, please see license.txt

frappe.ui.form.on("Member", {
    refresh: function (frm) {
        frm.add_custom_button("Create Membership", () => {
            frappe.new_doc("Membership", {
                member: frm.doc.name,
            });
        });
        frm.add_custom_button("Create Loan", () => {
            frappe.new_doc("Loan", {
                member: frm.doc.name,
            });
        });
    },
});
