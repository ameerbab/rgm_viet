// Copyright (c) 2016, vinhnguyen.t090@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly Checkin Detail Report"] = {
	"filters": [
		{
			"fieldname":"month",
			"label": __("Month"),
			"fieldtype": "Select",
			"options": "Jan\nFeb\nMar\nApr\nMay\nJun\nJul\nAug\nSep\nOct\nNov\nDec",
			"default": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
				"Dec"][frappe.datetime.str_to_obj(frappe.datetime.get_today()).getMonth()-1],
		},
		{
			"fieldname": "year",
			"label": __("Year"),
			"fieldtype": "Data",
			"default": new Date().getFullYear()
		},
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			// "default":"HR-EMP-00446"
		},
		{
			"fieldname":"grace_period",
			"label": __("Grace Period"),
			"fieldtype": "Select",
			"options": ["", "Late In", "Early Out", "Late or Early"],
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
		
		if(column.fieldname=="late_in") {
			console.log(data.late_in);
			value = data.late_in;
		}

		value = default_formatter(value, row, column, data);

		if((column.fieldname=="duty_in" && data.late_in=="Late In") || (column.fieldname=="duty_out" && data.early_out=="Early Out")) {
			value = $(`<span>${value}</span>`);
			var $value = $(value).css("color", "red");
			value = $value.wrap("<p></p>").parent().html();
		}

		// if(column.fieldname=="duty_in") {
		// 	column.link_onclick =
		// 			"frappe.query_reports['Monthly Checkin Detail Report'].open_checkin(" + JSON.stringify(data) + ")";
		// }

		return value;
	},
	"open_checkin": function(data) {
		alert(1);
	}
};
