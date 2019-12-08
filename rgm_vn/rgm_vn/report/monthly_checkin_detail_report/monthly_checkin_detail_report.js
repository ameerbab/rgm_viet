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
		// if (data[column.fieldname+"_name"]=="--------"){
		// 	var data_checkin = {
		// 		employee: data.employee,
		// 		// time: data.c_date,
		// 		// time_only: "08:00:30",
		// 	}
		// 	column.link_onclick =
		// 			"frappe.query_reports['Monthly Checkin Detail Report'].open_checkin(" + JSON.stringify(data_checkin) + ")";
		// }	
		value = default_formatter(value, row, column, data);

		if(column.fieldname == "duty_in" || column.fieldname == "lunch_out" || column.fieldname == "lunch_in" || column.fieldname == "duty_out"){
			if (data[column.fieldname+"_name"]!="--------"){
				value = $(`<span>${value}</span>`);
				var link = "#"
				if(data[column.fieldname+"_name"] != ""){
					link = "#Form/Employee Checkin/" + data[column.fieldname+"_name"];
				}
				var $value = $(value).find("a").attr("href", link);

				if((column.fieldname=="duty_in" && data.late_in=="Late In") || (column.fieldname=="duty_out" && data.early_out=="Early Out")) {
					$value.css("color", "red");
				}
				value = $value.wrap("<p></p>").parent().html();
			}	
		}
		return value;
	},
	"open_checkin": function(data) {
		frappe.new_doc('Employee Checkin', {
			employee: data.employee,
			// time: data.time,
			// time_only: data.time_only,
		});
	}
};
