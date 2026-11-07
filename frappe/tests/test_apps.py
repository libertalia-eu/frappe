# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import frappe
from frappe.apps import get_apps
from frappe.tests.utils import FrappeTestCase


class TestApps(FrappeTestCase):
	def tearDown(self):
		frappe.set_user("Administrator")
		frappe.db.delete("User", {"email": ("like", "test-apps-%")})

	def _user(self, email: str, roles: list[str]):
		frappe.set_user("Administrator")
		user = frappe.get_doc(doctype="User", email=email, first_name="Apps", send_welcome_email=0).insert()
		user.add_roles(*roles)
		return user

	def test_desk_entry_is_for_a_system_manager_only(self):
		self._user("test-apps-manager@example.com", ["System Manager"])
		self._user("test-apps-user@example.com", ["Blogger"])

		frappe.set_user("test-apps-manager@example.com")
		self.assertIn("Desk", [app["title"] for app in get_apps()])

		frappe.set_user("test-apps-user@example.com")
		self.assertNotIn("Desk", [app["title"] for app in get_apps()])
