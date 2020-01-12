# -*- coding: utf-8 -*-
# Copyright (c) 2020, vinhnguyen.t090@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

class CheckinShiftType(Document):
	def validate(self): 
		if self.lunch_out_from <= self.morning_duty_in_to: 
			frappe.throw(_(""" Difference between "Get Time from" of "LUNCH CHECK OUT" and "Get Time to" "MORNING DUTY IN" should not be greater than "0:01" """)) 
		
		if self.lunch_in_from <= self.lunch_out_to: 
			frappe.throw(_(""" Difference between "Get Time from" of "LUNCH CHECK IN" and "Get Time to" "LUNCH CHECK OUT" should not be greater than "0:01" """)) 
		
		if self.evening_duty_out_from <= self.lunch_in_to: 
			frappe.throw(_(""" Difference between "Get Time from" of "EVENING DUTY CHECK OUT" and "Get Time to" "LUNCH CHECK IN" should not be greater than "0:01" """)) 
