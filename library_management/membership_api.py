import frappe
from frappe import _
from frappe.utils import getdate

# Function to retrieve all memberships
@frappe.whitelist(allow_guest=True)
def get_memberships():
    if frappe.session.user == "Guest":
        return {"Error": "You must be logged in to access this data."}
    
    memberships = frappe.get_all("Membership", fields=["member", "full_name", "email", "phone", "from_date", "to_date", "paid"])
    return memberships

import frappe
from frappe.utils import getdate

# Function to retrieve a specific membership by member ID
@frappe.whitelist(allow_guest=True)
def get_membership(member_id):
    if frappe.session.user == "Guest":
        return {"error": "You must be logged in to access this data."}
    
    try:
        membership = frappe.get_doc("Membership", {"member": member_id})
        return {
            "member": membership.member,
            "full_name": membership.full_name,
            "email": membership.email,
            "phone": membership.phone,
            "from_date": membership.from_date,
            "to_date": membership.to_date,
            "paid": membership.paid
        }
    except frappe.DoesNotExistError:
        return {"error": f"Membership for member {member_id} does not exist."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

# Function to create a new membership
@frappe.whitelist(allow_guest=True)
def create_membership(member_id, from_date, to_date, paid=False):
    if frappe.session.user == "Guest":
        return {"error": "You must be logged in to access this data."}
    
    try:
        member = frappe.get_doc("Member", member_id)

        membership = frappe.get_doc({
            "doctype": "Membership",
            "member": member_id,
            "full_name": member.full_name,
            "email": member.email_address,
            "phone": member.phone,
            "from_date": getdate(from_date),
            "to_date": getdate(to_date),
            "paid": int(paid) 
        })

        membership.insert()
        membership.submit()
        return {
            "message": "Membership created successfully",
            "membership": {
                "member": membership.member,
                "full_name": membership.full_name,
                "email": membership.email,
                "phone": membership.phone,
                "from_date": membership.from_date,
                "to_date": membership.to_date,
                "paid": membership.paid
            }
        }
    
    except frappe.DoesNotExistError:
        return {"error": f"Member {member_id} does not exist. Please create a member first."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

# Function to update an existing membership
@frappe.whitelist(allow_guest=True)
def update_membership(member_id, from_date=None, to_date=None, paid=None):
    if frappe.session.user == "Guest":
        return {"error": "You must be logged in to access this data."}
    
    return {"method error": "can't edit a submitted or cancelled type: you have to delete and post it again"}

# Function to delete a membership
@frappe.whitelist(allow_guest=True)
def delete_membership(member_id):
    if frappe.session.user == "Guest":
        return {"Error": "You must be logged in to access this data."}

    try:
        membership = frappe.get_doc("Membership", {"member": member_id})

        if membership.docstatus == 2:
            membership.delete()
            return {"message": _("Membership deleted successfully.")}

        if membership.docstatus == 1:
            membership.cancel() 
            membership.delete() 
            return {"message": _("Membership was canceled and deleted successfully.")}

        return {"error": "Membership is in an invalid state for deletion."}

    except frappe.DoesNotExistError:
        return {"error": f"Membership for member {member_id} does not exist."}

