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
		if (data[column.fieldname+"_name"]=="--------"){
			var data_checkin = {
				fieldname: column.fieldname,
				employee: data.employee,
				c_date: data.c_date,
			}
			column.link_onclick =
					"frappe.query_reports['Monthly Checkin Detail Report'].open_checkin(" + JSON.stringify(data_checkin) + ")";
		}	
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
		var me = this;
		me.data = data;
		me.data.log_type = "UNKNOWN"
		me.data.c_time = "07:30:00";

		if(me.data.fieldname == "duty_in"){
			me.data.log_type = "IN"
			me.data.c_time = "07:30:00";
		}else if(me.data.fieldname == "lunch_out"){
			me.data.log_type = "OUT";
			me.data.c_time = "11:45:00";
		}else if(me.data.fieldname == "lunch_in"){
			me.data.log_type = "IN"
			me.data.c_time = "12:30:00";
		}else if(me.data.fieldname == "duty_out"){
			me.data.log_type = "OUT";
			me.data.c_time = "17:00:00";
		}

		if (me.check_in) {
			me.check_in.set_value("c_time", me.data.c_time);
			me.check_in.show();
			return false;
		}				

		var fields = [
			{fieldname:'c_time', fieldtype:'Time', label: __('Time'), "reqd": 1, default: me.data.c_time}
		];

		me.check_in = new frappe.ui.Dialog({
			title: __("Add Checkin"),
			fields: fields
		});

		me.check_in.set_primary_action(__("Add"), function() {
			
			var data_form = me.check_in.get_values();
			if(!data_form) return;

			me.check_in.hide();
			me.data.c_time = data_form.c_time;

			frappe.db.insert({
				doctype: "Employee Checkin", 
				employee: me.data.employee,
				log_type: me.data.log_type,
				time: me.data.c_date + " " + me.data.c_time,
				time_only: me.data.c_time,
			}).then(() => {
				frappe.query_report.refresh();
			})
			
		});
		me.check_in.show();
		return false;
	}
};
