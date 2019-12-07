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
	data = get_result_as_list(data)

	return columns, data

def get_result_as_list(data):

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
		
		c_time = to_timedelta(d.c_time)

		if not key_data[key].get("all_checkin"):
			key_data[key]["all_checkin"] = []

		key_data[key]["all_checkin"].append(cstr(d.c_time))
		
		if c_time > time_duty_in_from and c_time < time_duty_in_to and not key_data[key].get("duty_in"):
			key_data[key]["duty_in"] = d.c_time
		
		if c_time > time_lunch_out_from and c_time < time_lunch_out_to and not key_data[key].get("lunch_out"):
			key_data[key]["lunch_out"] = d.c_time
		
		if c_time > time_lunch_in_from and c_time < time_lunch_in_to and not key_data[key].get("lunch_in"):
			key_data[key]["lunch_in"] = d.c_time
		
		if c_time > time_duty_out_from and c_time < time_duty_out_to and not key_data[key].get("duty_out"):
			key_data[key]["duty_out"] = d.c_time

	for employee in employees:
		for c_date in dates:

			key = (employee, c_date)
			if key_data.get(key):
				
				error = ""

				if c_date.strftime("%a") == "Sat":
					if not (key_data[key].get("duty_in") and key_data[key].get("lunch_out")):
						error = "@"
				else:
					if not (key_data[key].get("duty_in") and key_data[key].get("lunch_out") and key_data[key].get("lunch_in") and key_data[key].get("duty_out")):
						error = "@"
				
				key_data[key]["morning"] = 0
				key_data[key]["lunch"] = 0
				key_data[key]["evening"] = 0
				key_data[key]["total_hours"] = 0
				key_data[key]["full_duty"] = 0
				key_data[key]["ot_hours"] = 0

				if key_data[key].get("lunch_out") and key_data[key].get("duty_in"):
					key_data[key]["morning"] = time_diff(key_data[key].get("lunch_out"), key_data[key].get("duty_in"))

				if key_data[key].get("lunch_in") and key_data[key].get("lunch_out"):
					key_data[key]["lunch"] = time_diff(key_data[key].get("lunch_in"), key_data[key].get("lunch_out"))

				if key_data[key].get("duty_out") and key_data[key].get("lunch_in"):	
					key_data[key]["evening"] = time_diff(key_data[key].get("duty_out"), key_data[key].get("lunch_in"))
				
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

				row = []

				frappe.errprint(key_data[key].get("total_hours"))

				row.append(key_data[key]["employee"])
				row.append(key_data[key]["employee_name"])
				row.append(key_data[key]["department"])
				row.append(key_data[key]["c_date"])
				
				row.append(key_data[key].get("duty_in") or "")
				row.append(key_data[key].get("lunch_out") or "")
				row.append(key_data[key].get("lunch_in") or "")
				row.append(key_data[key].get("duty_out") or "")

				row.append(key_data[key].get("morning") or "")
				row.append(key_data[key].get("lunch") or "")
				row.append(key_data[key].get("evening") or "")

				row.append(key_data[key].get("total_hours_float") or "")
				row.append(key_data[key].get("full_duty") or "")
				row.append(key_data[key].get("ot_hours") or "")

				row.append(" || ".join(key_data[key]["all_checkin"]))
				row.append(error)

				result.append(row)

	return result

def get_columns():
	columns = []
	return [
		"Id:Link/Employee:100", "Name:Data:150", "Department:Data:150", "Date:Date:80",
		"Duty In:Time:70", "Lunch Out:Time:70", "Lunch In:Time:70", "Duty Out:Time:70",
		"Morning:Time:70", "Lunch:Time:70", "Evening:Time:70",
		"Total Hours:Float:70", "Full Duty:Float:70", "OT Hours:Time:70",
		"All Checkin:Data:230", "Error:Data:80",
	]
	return columns

def get_checkins(conditions, filters):

	query = """Select c.employee as employee, e.employee_name, e.department,
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
