import frappe
from frappe import _

# Function to handle GET request for retrieving all members
@frappe.whitelist(allow_guest=True)
def get_members():
    if frappe.session.user == "Guest":
        return {"Error": "You must be logged in to access this data."}
    try:
        members = frappe.get_all("Member", fields=["first_name", "last_name", "email_address", "phone", "full_name"])
        return members
    except Exception as e:
        return {"Error": f"An unexpected error occurred: {str(e)}"}

# Function to handle GET request for retrieving a single member
@frappe.whitelist(allow_guest=True)
def get_member(member_id):
    if frappe.session.user == "Guest":
        return {"Error": "You must be logged in to access this data."}
    try:
        Member = frappe.get_doc("Member", member_id)
        return {
            "first_name": Member.first_name,
            "last_name": Member.last_name,
            "email_address": Member.email_address,
            "phone": Member.phone,
            "full_name": Member.full_name
        }
    except frappe.DoesNotExistError:
        return {"Error": "Member not found."}
    except Exception as e:
        return {"Error": f"An unexpected error occurred: {str(e)}"}

# Function to handle POST request for creating a new Member
@frappe.whitelist(allow_guest=True)
def create_member(first_name, last_name, email_address, phone):
    if frappe.session.user == "Guest":
        return {"Error": "You must be logged in to access this data."}
    try:
        Member = frappe.get_doc({
            "doctype": "Member",
            "first_name": first_name,
            "last_name": last_name,
            "email_address": email_address,
            "phone": phone,
        })
        Member.insert()
        return {
            "first_name": Member.first_name,
            "last_name": Member.last_name,
            "email_address": Member.email_address,
            "phone": Member.phone,
            "full_name": Member.first_name + Member.last_name
        }
    except Exception as e:
        return {"Error": f"An unexpected error occurred: {str(e)}"}

# Function to handle PUT request for updating a Member
@frappe.whitelist(allow_guest=True)
def update_member(member_id ,first_name, last_name, email_address, phone):
    if frappe.session.user == "Guest":
        return {"Error": "You must be logged in to access this data."}
    try:
        Member = frappe.get_doc("Member", member_id)

        Member.first_name = first_name
        Member.last_name = last_name
        Member.email_address = email_address
        Member.phone = phone
        
        Member.save()

        return {
            "first_name": Member.first_name,
            "last_name": Member.last_name,
            "email_address": Member.email_address,
            "phone": Member.phone,
            "full_name": Member.full_name
        }
    except frappe.DoesNotExistError:
        return {"Error": "Member not found."}
    except Exception as e:
        return {"Error": f"An unexpected error occurred: {str(e)}"}

# Function to handle DELETE request for deleting a Member
@frappe.whitelist(allow_guest=True)
def delete_member(member_id):
    if frappe.session.user == "Guest":
        return {"Error": "You must be logged in to access this data."}
    try:
        Member = frappe.get_doc("Member", member_id)
        Member.delete()  
        return {"message": _("Member deleted successfully")}
    except frappe.DoesNotExistError:
        return {"Error": "Member not found."}
    except Exception as e:
        return {"Error": f"An unexpected error occurred: {str(e)}"}
