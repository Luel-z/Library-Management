# Copyright (c) 2025, Luel Fekadu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class Loan(Document):
	def before_submit(self):
		if self.type == "Issue":
			self.validate_issue()
			self.validate_maximum_limit()
			# set the book status to be Issued
			book_title = frappe.get_doc("Book", self.book_title)
			book_title.status = "Issued"
			book_title.save()
		elif self.type == "Return":
			self.validate_return()
			# set the book status to be Available
			book_title = frappe.get_doc("Book", self.book_title)
			book_title.status = "Available"
			book_title.save()

	def validate_issue(self):
		self.validate_membership()
		book_title = frappe.get_doc("Book", self.book_title)
		# book cannot be issued if it is already issued
		if book_title.status == "Issued":
			frappe.throw("Book is already issued by another member")

	def validate_return(self):
		book_title = frappe.get_doc("Book", self.book_title)
		# book cannot be returned if it is not issued first
		if book_title.status == "Available":
			frappe.throw("Book cannot be returned without being issued first")

	def validate_maximum_limit(self):
		max_book = frappe.db.get_single_value("Library Settings", "max_book")
		count = frappe.db.count(
			"Loan",
			{"member": self.member,"type": "Issue", "docstatus": DocStatus.submitted()},
		)
		if count >= max_book:
			frappe.throw("Maximum limit reached for issuing articles")

	def validate_membership(self):
		# check if a valid membership exist for this library member
		valid_membership = frappe.db.exists(
			"Membership",
			{
				"member": self.member,
				"docstatus": DocStatus.submitted(),
				"from_date": ("<", self.loan_date),
				"to_date": (">", self.loan_date),
			},
		)
		if not valid_membership:
			frappe.throw("The member does not have a valid membership")
