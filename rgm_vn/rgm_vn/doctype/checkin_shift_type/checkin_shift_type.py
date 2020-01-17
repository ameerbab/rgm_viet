# -*- coding: utf-8 -*-
# Copyright (c) 2020, vinhnguyen.t090@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

class CheckinShiftType(Document):
	def validate(self):
		if self.morning_duty_in_enable:
			if not self.morning_duty_in:
				frappe.throw(_("Morning Duty Check In is required")) 
			if not self.morning_duty_in_from:
				frappe.throw(_("Morning Duty Check In From is required"))
			if not self.morning_duty_in_to:
				frappe.throw(_("Morning Duty Check In To is required"))
			if not self.morning_duty_in_round_from:
				frappe.throw(_("Morning Duty Check In - Grace Period Start Time is required"))
			if not self.morning_duty_in_round_to:
				frappe.throw(_("Morning Duty Check In - Grace Period End Time is required"))
			if not self.morning_duty_in_display_from:
				frappe.throw(_("Morning Duty Check In - Display Period Start is required"))
			if not self.morning_duty_in_display_to:
				frappe.throw(_("Morning Duty Check In - Display Period End is required"))
			if not self.morning_duty_in_display:
				frappe.throw(_("Morning Duty Check In - Display Time is required"))
		
		if self.lunch_out_enable:
			if not self.lunch_out:
				frappe.throw(_("Lunch Check Out is required")) 
			if not self.lunch_out_from:
				frappe.throw(_("Lunch Check Out From is required"))
			if not self.lunch_out_to:
				frappe.throw(_("Lunch Check Out To is required"))
			if not self.lunch_out_round_from:
				frappe.throw(_("Lunch Check Out - Grace Period Start Time is required"))
			if not self.lunch_out_round_to:
				frappe.throw(_("Lunch Check Out - Grace Period End Time is required"))
			if not self.lunch_out_display_from:
				frappe.throw(_("Lunch Check Out - Display Period Start is required"))
			if not self.lunch_out_display_to:
				frappe.throw(_("Lunch Check Out - Display Period End is required"))
			if not self.lunch_out_display:
				frappe.throw(_("Lunch Check Out - Display Time is required"))
		
		if self.lunch_in_enable:
			if not self.lunch_in:
				frappe.throw(_("Lunch Check In is required")) 
			if not self.lunch_in_from:
				frappe.throw(_("Lunch Check In From is required"))
			if not self.lunch_in_to:
				frappe.throw(_("Lunch Check In To is required"))
			if not self.lunch_in_round_from:
				frappe.throw(_("Lunch Check In - Grace Period Start Time is required"))
			if not self.lunch_in_round_to:
				frappe.throw(_("Lunch Check In - Grace Period End Time is required"))
			if not self.lunch_in_display_from:
				frappe.throw(_("Lunch Check In - Display Period Start is required"))
			if not self.lunch_in_display_to:
				frappe.throw(_("Lunch Check In - Display Period End is required"))
			if not self.lunch_in_display:
				frappe.throw(_("Lunch Check In - Display Time is required"))
		
		if self.evening_duty_out_enable:
			if not self.evening_duty_out:
				frappe.throw(_("Evening Duty Check Out is required")) 
			if not self.evening_duty_out_from:
				frappe.throw(_("Evening Duty Check Out From is required"))
			if not self.evening_duty_out_to:
				frappe.throw(_("Evening Duty Check Out To is required"))
			if not self.evening_duty_out_round_from:
				frappe.throw(_("Evening Duty Check Out - Grace Period Start Time is required"))
			if not self.evening_duty_out_round_to:
				frappe.throw(_("Evening Duty Check Out - Grace Period End Time is required"))
			if not self.evening_duty_out_display_from:
				frappe.throw(_("Evening Duty Check Out - Display Period Start is required"))
			if not self.evening_duty_out_display_to:
				frappe.throw(_("Evening Duty Check Out - Display Period End is required"))
			if not self.evening_duty_out_display:
				frappe.throw(_("Evening Duty Check Out - Display Time is required"))
		

		if self.lunch_out_enable and self.lunch_out_from <= self.morning_duty_in_to: 
			frappe.throw(_(""" Difference between "Get Time from" of "LUNCH CHECK OUT" and "Get Time to" "MORNING DUTY IN" should not be greater than "0:01" """)) 
		
		if self.lunch_in_enable and self.lunch_in_from <= self.lunch_out_to: 
			frappe.throw(_(""" Difference between "Get Time from" of "LUNCH CHECK IN" and "Get Time to" "LUNCH CHECK OUT" should not be greater than "0:01" """)) 
		
		if self.evening_duty_out_enable and self.evening_duty_out_from <= self.lunch_in_to: 
			frappe.throw(_(""" Difference between "Get Time from" of "EVENING DUTY CHECK OUT" and "Get Time to" "LUNCH CHECK IN" should not be greater than "0:01" """)) 
