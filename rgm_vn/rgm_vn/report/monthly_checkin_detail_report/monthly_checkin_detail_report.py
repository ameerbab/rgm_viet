# Copyright (c) 2013, vinhnguyen.t090@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import msgprint, _
from frappe.utils import get_first_day, get_last_day, add_to_date, nowdate, getdate, add_days, add_months, formatdate, to_timedelta, cstr, time_diff, time_diff_in_hours
import math
from datetime import timedelta

def execute(filters=None):
	if not filters: filters = {}
	
	conditions, filters = get_conditions(filters)
	columns = get_columns()

	data = get_checkins(conditions, filters)
	data = get_result_as_list(data, filters)

	return columns, data

def get_result_as_list(data, filters):

	result = []

	key_data = frappe._dict()
	key_list = []

	employees = []
	dates = []

	time_duty_in_from = to_timedelta("07:20:00")
	time_duty_in_to = to_timedelta("11:40:00")
	
	time_lunch_out_from = to_timedelta("11:40:01")
	time_lunch_out_to = to_timedelta("12:00:00")

	time_lunch_in_from = to_timedelta("12:00:01")
	time_lunch_in_to = to_timedelta("13:00:00")

	time_duty_out_from = to_timedelta("13:00:01")
	time_duty_out_to = to_timedelta("19:00:00")

	time_one_day = to_timedelta("08:45:00")

	time_late_in = to_timedelta("07:40:00")
	time_early_out = to_timedelta("16:59:59")

	for d in data:
		key = (d.employee, d.c_date)

		if d.employee not in employees:
			employees.append(d.employee)
		
		if d.c_date not in dates:
			dates.append(d.c_date)

		if not key_data.get(key):
			
			key_data[key] = frappe._dict()
			key_data[key]["employee"] = d.employee
			key_data[key]["employee_name"] = d.employee_name
			key_data[key]["department"] = d.department
			key_data[key]["employee_number"] = d.employee_number
			key_data[key]["c_date"] = d.c_date
			key_data[key]["c_time"] = d.c_time
			key_data[key]["duty_in_name"] = "--------"
			key_data[key]["lunch_out_name"] = "--------"
			key_data[key]["lunch_in_name"] = "--------"
			key_data[key]["duty_out_name"] = "--------"
		
		c_time = to_timedelta(d.c_time)

		if not key_data[key].get("all_checkin"):
			key_data[key]["all_checkin"] = []

		key_data[key]["all_checkin"].append(cstr(d.c_time))
		
		if c_time > time_duty_in_from and c_time < time_duty_in_to and not key_data[key].get("duty_in"):
			key_data[key]["duty_in_name"] = d.c_name
			key_data[key]["duty_in"] = d.c_time
		
		if c_time > time_lunch_out_from and c_time < time_lunch_out_to and not key_data[key].get("lunch_out"):
			key_data[key]["lunch_out_name"] = d.c_name
			key_data[key]["lunch_out"] = d.c_time
		
		if c_time > time_lunch_in_from and c_time < time_lunch_in_to and not key_data[key].get("lunch_in"):
			key_data[key]["lunch_in_name"] = d.c_name
			key_data[key]["lunch_in"] = d.c_time
		
		if c_time > time_duty_out_from and c_time < time_duty_out_to and not key_data[key].get("duty_out"):
			key_data[key]["duty_out_name"] = d.c_name
			key_data[key]["duty_out"] = d.c_time

	for employee in employees:
		for c_date in dates:

			key = (employee, c_date)
			if key_data.get(key):
				
				error = ""

				# if c_date.strftime("%a") == "Sat":
				# 	if not (key_data[key].get("duty_in") and key_data[key].get("lunch_out")):
				# 		error = "@"
				# else:
				# 	if not (key_data[key].get("duty_in") and key_data[key].get("lunch_out") and key_data[key].get("lunch_in") and key_data[key].get("duty_out")):
				# 		error = "@"
				
				key_data[key]["morning"] = 0
				key_data[key]["lunch"] = 0
				key_data[key]["evening"] = 0
				key_data[key]["total_hours"] = 0
				key_data[key]["full_duty"] = 0
				key_data[key]["ot_hours"] = 0

				key_data[key]["late_in"] = ""
				key_data[key]["early_out"] = ""

				if key_data[key].get("duty_in") and key_data[key].get("duty_in") > time_late_in:
					key_data[key]["late_in"] = "Late In"
				
				if key_data[key].get("duty_out") and key_data[key].get("duty_out") < time_early_out:
					key_data[key]["early_out"] = "Early Out"

				
				row_show = True;

				if filters.get("grace_period"):
					if filters.get("grace_period") == "Late or Early":
						if key_data[key]["late_in"] or key_data[key]["early_out"]:
							row_show = True;
						else:
							row_show = False;
					elif (filters.get("grace_period") == key_data[key]["late_in"] or filters.get("grace_period") ==  key_data[key]["early_out"]):
						row_show = True;
					else:
						row_show = False;
					
				if row_show == True:
					if key_data[key].get("lunch_out") and key_data[key].get("duty_in"):
						key_data[key]["morning"] = time_diff(key_data[key].get("lunch_out"), key_data[key].get("duty_in"))

					if key_data[key].get("lunch_in") and key_data[key].get("lunch_out"):
						key_data[key]["lunch"] = time_diff(key_data[key].get("lunch_in"), key_data[key].get("lunch_out"))

					if key_data[key].get("duty_out") and key_data[key].get("lunch_in"):	
						key_data[key]["evening"] = time_diff(key_data[key].get("duty_out"), key_data[key].get("lunch_in"))

					if key_data[key].get("duty_in") and not key_data[key].get("lunch_out"):
						key_data[key]["error"] = "@"
					if key_data[key].get("lunch_in") and not key_data[key].get("duty_out"):
						key_data[key]["error"] = "@"
					
					if key_data[key].get("morning") and key_data[key].get("evening"):
						key_data[key]["total_hours"] = key_data[key].get("morning") + key_data[key].get("evening")

					if key_data[key].get("morning") and key_data[key].get("evening"):
						key_data[key]["full_duty"] = 1
					elif key_data[key].get("morning") or key_data[key].get("evening"):
						key_data[key]["full_duty"] = 0.5
					
					if key_data[key].get("morning") and key_data[key].get("evening"):
						if time_diff_in_hours(key_data[key].get("total_hours"), time_one_day) > 0:
							key_data[key]["ot_hours"] = time_diff(key_data[key].get("total_hours"), time_one_day)
					
					key_data[key]["total_hours_float"] = 0

					if key_data[key].get("total_hours") != 0:
						key_data[key]["total_hours_float"] = key_data[key].get("total_hours").seconds/(60*60)

					key_data[key]["all_checkin"] = " || ".join(key_data[key]["all_checkin"])
					key_data[key]["morning"] = key_data[key].get("morning") or ""
					key_data[key]["lunch"] = key_data[key].get("lunch") or ""
					key_data[key]["evening"] = key_data[key].get("evening") or ""

					key_data[key]["total_hours_float"] = key_data[key].get("total_hours_float") if (key_data[key].get("total_hours_float") > 0) else ""
					key_data[key]["full_duty"] = key_data[key].get("full_duty") or ""
					key_data[key]["ot_hours"] = key_data[key].get("ot_hours") or ""

					# key_data[key]["lunch_out"] = key_data[key].get("lunch_out") or "--------"

					row = key_data[key]

					result.append(row)

	return result

def get_columns():
	return [
		{
			"fieldname": "employee",
			"label": _("Id"),
			"fieldtype": "Link",
			"options": "Employee",
			"width": 100
		},
		{
			"fieldname": "employee_name",
			"label": _("Name"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "department",
			"label": _("Department"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "c_date",
			"label": _("Date"),
			"fieldtype": "Date",
			"width": 80
		},
		{
			"fieldname": "duty_in",
			"label": _("Duty In"),
			"fieldtype": "Link",
			"options": "Employee Checkin",
			"width": 80
		},
		{
			"fieldname": "lunch_out",
			"label": _("Lunch Out"),
			"fieldtype": "Link",
			"options": "Employee Checkin",
			"width": 80
		},
		{
			"fieldname": "lunch_in",
			"label": _("Lunch In"),
			"fieldtype": "Link",
			"options": "Employee Checkin",
			"width": 80
		},
		{
			"fieldname": "duty_out",
			"label": _("Duty Out"),
			"fieldtype": "Link",
			"options": "Employee Checkin",
			"width": 80
		},
		{
			"fieldname": "morning",
			"label": _("Morning"),
			"fieldtype": "Time",
			"width": 80
		},
		{
			"fieldname": "lunch",
			"label": _("Lunch"),
			"fieldtype": "Time",
			"width": 80
		},
		{
			"fieldname": "evening",
			"label": _("Evening"),
			"fieldtype": "Time",
			"width": 80
		},
		{
			"fieldname": "total_hours_float",
			"label": _("Total Hours"),
			"fieldtype": "Float",
			"width": 80
		},
		{
			"fieldname": "full_duty",
			"label": _("Full Duty"),
			"fieldtype": "Float",
			"width": 80
		},
		{
			"fieldname": "ot_hours",
			"label": _("OT Hours"),
			"fieldtype": "Time",
			"width": 80
		},
		{
			"fieldname": "late_in",
			"label": _("Late In"),
			"fieldtype": "Data",
			"width": 80
		},
		{
			"fieldname": "early_out",
			"label": _("Early Out"),
			"fieldtype": "Data",
			"width": 80
		},
		{
			"fieldname": "all_checkin",
			"label": _("All Checkin"),
			"fieldtype": "Data",
			"width": 230
		},
		{
			"fieldname": "error",
			"label": _("Error"),
			"fieldtype": "Data",
			"width": 80
		}
	]
	return columns

def get_checkins(conditions, filters):

	query = """Select c.name as c_name, c.employee as employee, e.employee_name, e.department,
	c.log_type,	date(c.time) as c_date, time(c.time) as c_time
	FROM `tabEmployee Checkin` c
	LEFT JOIN `tabEmployee` e ON  e.name = c.employee
	WHERE 1 %s
	ORDER BY c.employee, c.time asc
	""" %(conditions)

	data = frappe.db.sql(query, filters, as_dict=1)

	return data	

def get_conditions(filters):
	conditions = " "

	if not (filters.get("month") and filters.get("year")):
		msgprint(_("Please select month and year"), raise_exception=1)

	filters["month"] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
		"Dec"].index(filters.month) + 1

	conditions = " and month(date(c.time)) = %(month)s and year(date(c.time)) = %(year)s"

	if filters.get("company"): conditions += " and e.company = %(company)s"
	if filters.get("employee"): conditions += " and c.employee = %(employee)s"
	
	return conditions, filters	
