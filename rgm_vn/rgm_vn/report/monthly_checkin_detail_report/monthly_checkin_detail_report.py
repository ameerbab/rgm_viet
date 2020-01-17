# Copyright (c) 2013, vinhnguyen.t090@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import msgprint, _
from frappe.utils import get_first_day, get_last_day, add_to_date, nowdate, getdate, add_days, add_months, formatdate, to_timedelta, cstr, time_diff, time_diff_in_hours
import math

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

	company = filters.get("company")

	checkin_settings = frappe.get_doc("Checkin Settings", company)

	settings_weekday = frappe.get_doc("Checkin Shift Type", checkin_settings.weekday)
	settings_weekend = frappe.get_doc("Checkin Shift Type", checkin_settings.weekend)

	settings = frappe._dict()

	for shift in ["weekday", "weekend"]:
		settings[shift] = frappe._dict()

		if shift == "weekday":
			settings_shift = settings_weekday
		else:
			settings_shift = settings_weekend

		settings[shift]["morning_duty_in"] = to_timedelta(settings_shift.morning_duty_in)

		settings[shift]["morning_duty_in_from"] = to_timedelta(settings_shift.morning_duty_in_from)
		settings[shift]["morning_duty_in_to"] = to_timedelta(settings_shift.morning_duty_in_to)

		settings[shift]["morning_duty_in_round_from"] = to_timedelta(settings_shift.morning_duty_in_round_from)
		settings[shift]["morning_duty_in_round_to"] = to_timedelta(settings_shift.morning_duty_in_round_to)

		settings[shift]["morning_duty_in_display"] = to_timedelta(settings_shift.morning_duty_in_display)
		settings[shift]["morning_duty_in_display_from"] = to_timedelta(settings_shift.morning_duty_in_display_from)
		settings[shift]["morning_duty_in_display_to"] = to_timedelta(settings_shift.morning_duty_in_display_to)


		
		settings[shift]["lunch_out"] = to_timedelta(settings_shift.lunch_out)
		settings[shift]["lunch_out_from"] = to_timedelta(settings_shift.lunch_out_from)
		settings[shift]["lunch_out_to"] = to_timedelta(settings_shift.lunch_out_to)
		settings[shift]["lunch_out_round_from"] = to_timedelta(settings_shift.lunch_out_round_from)
		settings[shift]["lunch_out_round_to"] = to_timedelta(settings_shift.lunch_out_round_to)

		settings[shift]["lunch_out_display"] = to_timedelta(settings_shift.lunch_out_display)
		settings[shift]["lunch_out_display_from"] = to_timedelta(settings_shift.lunch_out_display_from)
		settings[shift]["lunch_out_display_to"] = to_timedelta(settings_shift.lunch_out_display_to)

		settings[shift]["lunch_in"] = to_timedelta(settings_shift.lunch_in)
		settings[shift]["lunch_in_from"] = to_timedelta(settings_shift.lunch_in_from)
		settings[shift]["lunch_in_to"] = to_timedelta(settings_shift.lunch_in_to)
		settings[shift]["lunch_in_round_from"] = to_timedelta(settings_shift.lunch_in_round_from)
		settings[shift]["lunch_in_round_to"] = to_timedelta(settings_shift.lunch_in_round_to)

		settings[shift]["lunch_in_display"] = to_timedelta(settings_shift.lunch_in_display)
		settings[shift]["lunch_in_display_from"] = to_timedelta(settings_shift.lunch_in_display_from)
		settings[shift]["lunch_in_display_to"] = to_timedelta(settings_shift.morning_duty_in_display_to)

		settings[shift]["evening_duty_out"] = to_timedelta(settings_shift.evening_duty_out)
		settings[shift]["evening_duty_out_from"] = to_timedelta(settings_shift.evening_duty_out_from)
		settings[shift]["evening_duty_out_to"] = to_timedelta(settings_shift.evening_duty_out_to)
		settings[shift]["evening_duty_out_round_from"] = to_timedelta(settings_shift.evening_duty_out_round_from)
		settings[shift]["evening_duty_out_round_to"] = to_timedelta(settings_shift.evening_duty_out_round_to)

		settings[shift]["evening_duty_out_display"] = to_timedelta(settings_shift.evening_duty_out_display)
		settings[shift]["evening_duty_out_display_from"] = to_timedelta(settings_shift.evening_duty_out_display_from)
		settings[shift]["evening_duty_out_display_to"] = to_timedelta(settings_shift.evening_duty_out_display_to)

		settings[shift]["max_morning_float"] = time_diff(settings[shift]["lunch_out"], settings[shift]["morning_duty_in"]).seconds/(60*60)
		settings[shift]["max_evening_float"] = time_diff(settings[shift]["evening_duty_out"], settings[shift]["lunch_in"]).seconds/(60*60)
		settings[shift]["max_day_float"] = settings[shift]["max_morning_float"] + settings[shift]["max_evening_float"]

		settings[shift]["morning_duty_in_late"] = settings[shift]["morning_duty_in"]
		settings[shift]["lunch_in_late"] = settings[shift]["lunch_in"] + to_timedelta("00:00:30")
		settings[shift]["lunch_out_early"] = settings[shift]["lunch_out"]
		settings[shift]["evening_duty_out_early"] = settings[shift]["evening_duty_out"]



	for d in data:
		key = (d.employee, d.c_date)

		if d.employee not in employees:
			employees.append(d.employee)
		
		if d.c_date not in dates:
			dates.append(d.c_date)
		
		c_day =  d.c_date.strftime("%a")

		if c_day == "Sat" or c_day == "Sun":
			shift = "weekend"
		else:
			shift = "weekday"

		morning_duty_in = settings[shift]["morning_duty_in"]
		morning_duty_in_from = settings[shift]["morning_duty_in_from"]
		morning_duty_in_to = settings[shift]["morning_duty_in_to"]
		morning_duty_in_round_from = settings[shift]["morning_duty_in_round_from"]
		morning_duty_in_round_to = settings[shift]["morning_duty_in_round_to"]

		morning_duty_in_display = settings[shift]["morning_duty_in_display"]
		morning_duty_in_display_from = settings[shift]["morning_duty_in_display_from"]
		morning_duty_in_display_to = settings[shift]["morning_duty_in_display_to"]
		
		lunch_out = settings[shift]["lunch_out"]
		lunch_out_from = settings[shift]["lunch_out_from"]
		lunch_out_to = settings[shift]["lunch_out_to"]
		lunch_out_round_from = settings[shift]["lunch_out_round_from"]
		lunch_out_round_to = settings[shift]["lunch_out_round_to"]

		lunch_out_display = settings[shift]["lunch_out_display"]
		lunch_out_display_from = settings[shift]["lunch_out_display_from"]
		lunch_out_display_to = settings[shift]["lunch_out_display_to"]

		lunch_in = settings[shift]["lunch_in"]
		lunch_in_from = settings[shift]["lunch_in_from"]
		lunch_in_to = settings[shift]["lunch_in_to"]
		lunch_in_round_from = settings[shift]["lunch_in_round_from"]
		lunch_in_round_to = settings[shift]["lunch_in_round_to"]

		lunch_in_display = settings[shift]["lunch_in_display"]
		lunch_in_display_from = settings[shift]["lunch_in_display_from"]
		lunch_in_display_to = settings[shift]["lunch_in_display_to"]

		evening_duty_out = settings[shift]["evening_duty_out"]
		evening_duty_out_from = settings[shift]["evening_duty_out_from"]
		evening_duty_out_to = settings[shift]["evening_duty_out_to"]
		evening_duty_out_round_from = settings[shift]["evening_duty_out_round_from"]
		evening_duty_out_round_to = settings[shift]["evening_duty_out_round_to"]

		evening_duty_out_display = settings[shift]["evening_duty_out_display"]
		evening_duty_out_display_from = settings[shift]["evening_duty_out_display_from"]
		evening_duty_out_display_to = settings[shift]["evening_duty_out_display_to"]

		max_morning_float = settings[shift]["max_morning_float"]
		max_evening_float = settings[shift]["max_evening_float"]
		max_day_float = settings[shift]["max_day_float"]
		

		morning_duty_in_late = settings[shift]["morning_duty_in_late"]
		lunch_in_late = settings[shift]["lunch_in_late"]
		lunch_out_early = settings[shift]["lunch_out_early"]
		evening_duty_out_early = settings[shift]["evening_duty_out_early"]
		

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
			key_data[key]["break_out_1_name"] = "--------"
			key_data[key]["break_in_1_name"] = "--------"
			key_data[key]["break_out_2_name"] = "--------"
			key_data[key]["break_in_2_name"] = "--------"
		
		c_time = to_timedelta(d.c_time)

		if not key_data[key].get("all_checkin"):
			key_data[key]["all_checkin"] = []

		key_data[key]["all_checkin"].append(cstr(d.c_time))
		
		if d.checkin_type == "Duty In" or (c_time >= morning_duty_in_from and c_time <= morning_duty_in_to and not key_data[key].get("duty_in") and (d.checkin_type == None or d.checkin_type == "")):
			key_data[key]["duty_in_name"] = d.c_name
			key_data[key]["duty_in"] = d.c_time
		
		if d.checkin_type == "Lunch Out" or (c_time >= lunch_out_from and c_time <= lunch_out_to and not key_data[key].get("lunch_out") and (d.checkin_type == None or d.checkin_type == "")):
			key_data[key]["lunch_out_name"] = d.c_name
			key_data[key]["lunch_out"] = d.c_time
		
		if d.checkin_type == "Lunch In" or (c_time >= lunch_in_from and c_time <= lunch_in_to and not key_data[key].get("lunch_in") and (d.checkin_type == None or d.checkin_type == "")):
			key_data[key]["lunch_in_name"] = d.c_name
			key_data[key]["lunch_in"] = d.c_time
		
		if  d.checkin_type == "Duty Out" or (c_time >= evening_duty_out_from and c_time <= evening_duty_out_to and not key_data[key].get("duty_out") and (d.checkin_type == None or d.checkin_type == "")):
			key_data[key]["duty_out_name"] = d.c_name
			key_data[key]["duty_out"] = d.c_time
		
		if d.checkin_type == "Break Out 1":
			key_data[key]["break_out_1_name"] = d.c_name
			key_data[key]["break_out_1"] = d.c_time
		
		if d.checkin_type == "Break In 1":
			key_data[key]["break_in_1_name"] = d.c_name
			key_data[key]["break_in_1"] = d.c_time
		
		if d.checkin_type == "Break Out 2":
			key_data[key]["break_out_2_name"] = d.c_name
			key_data[key]["break_out_2"] = d.c_time
		
		if d.checkin_type == "Break In 2":
			key_data[key]["break_in_2_name"] = d.c_name
			key_data[key]["break_in_2"] = d.c_time

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

				key_data[key]["c_day"] =  c_date.strftime("%a")

				if key_data[key]["c_day"] == "Sat" or key_data[key]["c_day"] == "Sun":
					shift = "weekend"
				else:
					shift = "weekday"

				morning_duty_in = settings[shift]["morning_duty_in"]
				morning_duty_in_from = settings[shift]["morning_duty_in_from"]
				morning_duty_in_to = settings[shift]["morning_duty_in_to"]
				morning_duty_in_round_from = settings[shift]["morning_duty_in_round_from"]
				morning_duty_in_round_to = settings[shift]["morning_duty_in_round_to"]

				morning_duty_in_display = settings[shift]["morning_duty_in_display"]
				morning_duty_in_display_from = settings[shift]["morning_duty_in_display_from"]
				morning_duty_in_display_to = settings[shift]["morning_duty_in_display_to"]
				
				lunch_out = settings[shift]["lunch_out"]
				lunch_out_from = settings[shift]["lunch_out_from"]
				lunch_out_to = settings[shift]["lunch_out_to"]
				lunch_out_round_from = settings[shift]["lunch_out_round_from"]
				lunch_out_round_to = settings[shift]["lunch_out_round_to"]

				lunch_out_display = settings[shift]["lunch_out_display"]
				lunch_out_display_from = settings[shift]["lunch_out_display_from"]
				lunch_out_display_to = settings[shift]["lunch_out_display_to"]

				lunch_in = settings[shift]["lunch_in"]
				lunch_in_from = settings[shift]["lunch_in_from"]
				lunch_in_to = settings[shift]["lunch_in_to"]
				lunch_in_round_from = settings[shift]["lunch_in_round_from"]
				lunch_in_round_to = settings[shift]["lunch_in_round_to"]

				lunch_in_display = settings[shift]["lunch_in_display"]
				lunch_in_display_from = settings[shift]["lunch_in_display_from"]
				lunch_in_display_to = settings[shift]["lunch_in_display_to"]

				evening_duty_out = settings[shift]["evening_duty_out"]
				evening_duty_out_from = settings[shift]["evening_duty_out_from"]
				evening_duty_out_to = settings[shift]["evening_duty_out_to"]
				evening_duty_out_round_from = settings[shift]["evening_duty_out_round_from"]
				evening_duty_out_round_to = settings[shift]["evening_duty_out_round_to"]

				evening_duty_out = settings[shift]["evening_duty_out"]
				evening_duty_out_from = settings[shift]["evening_duty_out_from"]
				evening_duty_out_to = settings[shift]["evening_duty_out_to"]

				max_morning_float = settings[shift]["max_morning_float"]
				max_evening_float = settings[shift]["max_evening_float"]
				max_day_float = settings[shift]["max_day_float"]
				

				morning_duty_in_late = settings[shift]["morning_duty_in_late"]
				lunch_in_late = settings[shift]["lunch_in_late"]
				lunch_out_early = settings[shift]["lunch_out_early"]
				evening_duty_out_early = settings[shift]["evening_duty_out_early"]

				
				key_data[key]["morning"] = 0
				key_data[key]["lunch"] = 0
				key_data[key]["break_1"] = 0
				key_data[key]["break_2"] = 0
				key_data[key]["evening"] = 0
				key_data[key]["full_duty"] = 0
				key_data[key]["ot_hours"] = 0

				key_data[key]["late_in"] = ""
				key_data[key]["early_out"] = ""

				if key_data[key].get("duty_in"):
					if key_data[key].get("duty_in") > morning_duty_in_late:
						key_data[key]["late_in"] = "Late In"
				
				if key_data[key].get("lunch_in"):
					if key_data[key].get("lunch_in") > lunch_in_late:
						key_data[key]["late_in"] = "Late In"
				
				if key_data[key].get("duty_out"):
					if key_data[key].get("duty_out") < evening_duty_out_early:
						key_data[key]["early_out"] = "Early Out"
				
				if key_data[key].get("lunch_out"):
					if key_data[key].get("lunch_out") < lunch_out_early:
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

					if key_data[key].get("duty_in"):
						if key_data[key]["duty_in"] >= morning_duty_in_round_from and key_data[key]["duty_in"] <= morning_duty_in_round_to:
							key_data[key]["duty_in"] = morning_duty_in
					
					if key_data[key].get("lunch_out"):
						if key_data[key]["lunch_out"] >= lunch_out_round_from and key_data[key]["lunch_out"] <= lunch_out_round_to:
							key_data[key]["lunch_out"] = lunch_out

					if key_data[key].get("lunch_in"):
						if key_data[key]["lunch_in"] <= lunch_in_round_from:
							key_data[key]["lunch_in"] = lunch_in_round_from
						elif key_data[key]["lunch_in"] <= lunch_in_round_to:
							key_data[key]["lunch_in"] = lunch_in

					if key_data[key].get("duty_out"):
						if key_data[key]["duty_out"] >= evening_duty_out_round_from and key_data[key]["duty_out"] <= evening_duty_out_round_to:
							key_data[key]["duty_out"] = evening_duty_out

					if key_data[key].get("lunch_out") and key_data[key].get("duty_in"):
						key_data[key]["morning"] = time_diff(key_data[key].get("lunch_out"), key_data[key].get("duty_in"))

					if key_data[key].get("lunch_in") and key_data[key].get("lunch_out"):
						key_data[key]["lunch"] = time_diff(key_data[key].get("lunch_in"), key_data[key].get("lunch_out"))
					
					if key_data[key].get("break_out_1") and key_data[key].get("break_in_1"):
						key_data[key]["break_1"] = time_diff(key_data[key].get("break_in_1"), key_data[key].get("break_out_1"))
					
					if key_data[key].get("break_out_2") and key_data[key].get("break_in_2"):
						key_data[key]["break_2"] = time_diff(key_data[key].get("break_in_2"), key_data[key].get("break_out_2"))

					if key_data[key].get("duty_out") and key_data[key].get("lunch_in"):	
						key_data[key]["evening"] = time_diff(key_data[key].get("duty_out"), key_data[key].get("lunch_in"))

					if key_data[key].get("duty_in") and not key_data[key].get("lunch_out"):
						key_data[key]["error"] = "@"
					elif key_data[key].get("lunch_out") and not key_data[key].get("duty_in"):
						key_data[key]["error"] = "@"
					elif key_data[key].get("lunch_in") and not key_data[key].get("duty_out"):
						key_data[key]["error"] = "@"
					elif key_data[key].get("duty_out") and not key_data[key].get("lunch_in"):
						key_data[key]["error"] = "@"
					elif key_data[key].get("break_out_1") and not key_data[key].get("break_in_1"):
						key_data[key]["error"] = "@"
					elif key_data[key].get("break_in_1") and not key_data[key].get("break_out_1"):
						key_data[key]["error"] = "@"
					elif key_data[key].get("break_out_2") and not key_data[key].get("break_in_2"):
						key_data[key]["error"] = "@"
					elif key_data[key].get("break_in_2") and not key_data[key].get("break_out_2"):
						key_data[key]["error"] = "@"
					
					if shift == "weekday" and not (key_data[key]["morning"] and key_data[key]["evening"]):
						key_data[key]["error"] = "Missing Punches"

					if key_data[key].get("morning") and key_data[key].get("evening"):
						key_data[key]["full_duty"] = 1
					elif key_data[key].get("morning") or key_data[key].get("evening"):
						key_data[key]["full_duty"] = 0.5
										
					key_data[key]["total_hours_float"] = 0
					key_data[key]["morning_float"] = 0
					key_data[key]["lunch_float"] = 0
					key_data[key]["break_1_float"] = 0
					key_data[key]["break_2_float"] = 0
					key_data[key]["breaks_float"] = 0					
					key_data[key]["evening_float"] = 0
					key_data[key]["ot_hours_float"] = 0
					key_data[key]["ot_morning_float"] = 0
					key_data[key]["ot_evening_float"] = 0
					key_data[key]["normal_hours_float"] = 0

					if key_data[key].get("break_1") != 0:
						key_data[key]["break_1_float"] = key_data[key].get("break_1").seconds/(60*60)
					
					if key_data[key].get("break_2") != 0:
						key_data[key]["break_2_float"] = key_data[key].get("break_2").seconds/(60*60)
					
					key_data[key]["breaks_float"] = key_data[key]["break_1_float"] + key_data[key]["break_2_float"]

					if key_data[key].get("morning") != 0:
						key_data[key]["morning_float"] = key_data[key].get("morning").seconds/(60*60) - key_data[key]["break_1_float"]

						if key_data[key]["morning_float"] > max_morning_float:
							key_data[key]["ot_morning_float"] = key_data[key]["morning_float"] - max_morning_float
							key_data[key]["morning_float"] = max_morning_float
					
					if key_data[key].get("lunch") != 0:
						key_data[key]["lunch_float"] = key_data[key].get("lunch").seconds/(60*60)					
					
					if key_data[key].get("evening") != 0:
						key_data[key]["evening_float"] = key_data[key].get("evening").seconds/(60*60) - key_data[key]["break_2_float"]

						if key_data[key]["evening_float"] > max_evening_float:
							key_data[key]["ot_evening_float"] = key_data[key]["evening_float"] - max_evening_float
							key_data[key]["evening_float"] = max_evening_float
					
					key_data[key]["ot_hours_float"] = key_data[key]["ot_morning_float"] + key_data[key]["ot_evening_float"]
					key_data[key]["normal_hours_float"] = key_data[key]["morning_float"] + key_data[key]["evening_float"]
					
					key_data[key]["total_hours_float"] = key_data[key]["normal_hours_float"] + key_data[key]["ot_hours_float"]

					
					key_data[key]["all_checkin"] = " || ".join(key_data[key]["all_checkin"])
					key_data[key]["morning"] = key_data[key].get("morning") or ""
					key_data[key]["lunch"] = key_data[key].get("lunch") or ""
					key_data[key]["evening"] = key_data[key].get("evening") or ""

					key_data[key]["total_hours_float"] = key_data[key].get("total_hours_float") if (key_data[key].get("total_hours_float") > 0) else ""
					key_data[key]["full_duty"] = key_data[key].get("full_duty") or ""
					key_data[key]["ot_hours"] = key_data[key].get("ot_hours") or ""


					if key_data[key].get("duty_in"):
						if key_data[key]["duty_in"] >= morning_duty_in_display_from and key_data[key]["duty_in"] <= morning_duty_in_display_to:
							key_data[key]["duty_in"] = morning_duty_in_display
					
					if key_data[key].get("lunch_out"):
						if key_data[key]["lunch_out"] >= lunch_out_display_from and key_data[key]["lunch_out"] <= lunch_out_display_to:
							key_data[key]["lunch_out"] = lunch_out_display

					if key_data[key].get("lunch_in"):
						if key_data[key]["lunch_in"] >= lunch_in_display_from and key_data[key]["lunch_in"] <= lunch_in_display_to:
							key_data[key]["lunch_in"] = lunch_in_display

					
					if key_data[key].get("duty_out"):
						if key_data[key]["duty_out"] >= evening_duty_out_display_from and key_data[key]["duty_out"] <= evening_duty_out_display_to:
							key_data[key]["duty_out"] = evening_duty_out_display

					key_data[key]["duty_in"] = key_data[key].get("duty_in") or "--------"
					key_data[key]["lunch_out"] = key_data[key].get("lunch_out") or "--------"
					key_data[key]["lunch_in"] = key_data[key].get("lunch_in") or "--------"
					key_data[key]["duty_out"] = key_data[key].get("duty_out") or "--------"
					key_data[key]["break_out_1"] = key_data[key].get("break_out_1") or "--------"
					key_data[key]["break_in_1"] = key_data[key].get("break_in_1") or "--------"
					key_data[key]["break_out_2"] = key_data[key].get("break_out_2") or "--------"
					key_data[key]["break_in_2"] = key_data[key].get("break_in_2") or "--------"

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
			"width": 150
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
			"fieldname": "employee_number",
			"label": _("Emp No"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "c_day",
			"label": _("Day"),
			"fieldtype": "Data",
			"width": 40
		},
		{
			"fieldname": "c_date",
			"label": _("Date"),
			"fieldtype": "Date",
			"width": 80
		},	
		{
			"fieldname": "all_checkin",
			"label": _("All Checkin"),
			"fieldtype": "Data",
			"width": 230
		},	
		{
			"fieldname": "duty_in",
			"label": _("Duty In"),
			"fieldtype": "Link",
			"options": "Employee Checkin",
			"width": 80
		},
		{
			"fieldname": "break_out_1",
			"label": _("Break Out 1"),
			"fieldtype": "Link",
			"options": "Employee Checkin",
			"width": 80
		},
		{
			"fieldname": "break_in_1",
			"label": _("Break In 1"),
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
			"fieldname": "break_out_2",
			"label": _("Break Out 2"),
			"fieldtype": "Link",
			"options": "Employee Checkin",
			"width": 80
		},
		{
			"fieldname": "break_in_2",
			"label": _("Break In 2"),
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
			"fieldname": "morning_float",
			"label": _("Morning"),
			"fieldtype": "Float",
			"precision": 2,
			"width": 80
		},
		{
			"fieldname": "lunch_float",
			"label": _("Lunch"),
			"fieldtype": "Float",
			"precision": 2,
			"width": 80
		},
		{
			"fieldname": "breaks_float",
			"label": _("Breaks"),
			"fieldtype": "Float",
			"precision": 2,
			"width": 80
		},
		{
			"fieldname": "evening_float",
			"label": _("Evening"),
			"fieldtype": "Float",
			"precision": 2,
			"width": 80
		},
		{
			"fieldname": "total_hours_float",
			"label": _("Total Hours"),
			"precision": 2,
			"fieldtype": "Float",
			"width": 80
		},
		{
			"fieldname": "full_duty",
			"label": _("Full Duty"),
			"precision": 1,
			"fieldtype": "Float",
			"width": 80
		},
		{
			"fieldname": "normal_hours_float",
			"label": _("Normal Hours"),
			"fieldtype": "Float",
			"precision": 2,
			"width": 80
		},
		{
			"fieldname": "ot_hours_float",
			"label": _("OT Hours"),
			"fieldtype": "Float",
			"precision": 2,
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
			"fieldname": "error",
			"label": _("Error"),
			"fieldtype": "Data",
			"width": 80
		}
	]

def get_checkins(conditions, filters):

	query = """Select c.name as c_name, c.employee as employee, e.employee_name, e.employee_number, e.department,
	c.log_type,	date(c.time) as c_date, time(c.time) as c_time, c.checkin_type
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

def round_time_up(hour):
	remain = hour - math.floor(hour)
	if remain <= 0.25:
		return math.floor(hour)
	elif remain <= 0.75:
		return math.floor(hour) + 0.5
	elif remain <= 1:
		return math.floor(hour) + 1