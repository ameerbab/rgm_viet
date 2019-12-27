from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Attendance"),
			"icon": "fa fa-list",
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Monthly Checkin Detail Report",
					"doctype": "Employee Checkin"
				},
			]
		},
		{
			"label": _("Settings"),
			"icon": "fa fa-cog",
			"items": [
				{
					"type": "doctype",
					"name": "Checkin Settings",
				}
			]
		},
	]
