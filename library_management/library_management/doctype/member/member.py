# Copyright (c) 2025, Luel Fekadu and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Member(Document):
    def before_save(self):
        if isinstance(self.first_name, tuple):
            self.first_name = self.first_name[0]
        if isinstance(self.last_name, tuple):
            self.last_name = self.last_name[0]

        self.full_name = f'{self.first_name.strip()} {self.last_name.strip() if self.last_name else ""}'.strip()
