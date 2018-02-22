var index = 1;
function add_new_service_item() {
	var ready_add_table = document.getElementById("ready-add-table");
	var new_row = document.createElement("tr");
	var new_row_id = "new_service_row_" + index;
	new_row.setAttribute("id", new_row_id);
	var new_row_innerHTML = "<td>自动</td>" +
							"<td><input type='input' class='form-control' name='new_service_name_"+ index +"' required  /></td>"+
							"<td><input type='input' class='form-control' name='new_service_price_"+ index +"' required /></td>"+
							"<td><input type='input' class='form-control' name='new_service_cost_"+ index +"' required /></td>"+
							"<td><input type='input' class='form-control' name='new_service_ratio_"+ index +"' required /></td>"+
							"<td><button class='btn btn-danger' onclick=\"delete_element_by_id(\'new_service_row_" + index + "\')\">删除</button></td>";
	new_row.innerHTML = new_row_innerHTML;
	ready_add_table.appendChild(new_row);
	index++;
	document.getElementById("index_number").value = index;
}
function add_new_vip() {
	var ready_add_table = document.getElementById("ready-add-table");
	var new_row = document.createElement("tr");
	var new_row_id = "new_vip_row_" + index;
	new_row.setAttribute("id", new_row_id);
	var new_row_innerHTML = "<td>自动</td>" +
							"<td><input type='input' class='form-control' name='new_vip_card_"+ index +"' required  /></td>"+
							"<td><input type='input' class='form-control' name='new_vip_name_"+ index +"' /></td>"+
							"<td><input type='input' class='form-control' name='new_vip_phone_"+ index +"' /></td>"+
							"<td><input type='input' class='form-control' name='new_vip_balance_"+ index +"' value=\"0\" /></td>"+
							"<td><button class='btn btn-danger' onclick=\"delete_element_by_id(\'new_vip_row_" + index + "\')\">删除</button></td>";
	new_row.innerHTML = new_row_innerHTML;
	ready_add_table.appendChild(new_row);
	index++;
	document.getElementById("index_number").value = index;
}
function add_new_payment_method() {
	var ready_add_table = document.getElementById("ready-add-table");
	var new_row = document.createElement("tr");
	var new_row_id = "new_payment_row_" + index;
	new_row.setAttribute("id", new_row_id);
	var new_row_innerHTML = "<td>自动</td>" +
							"<td><input type='input' class='form-control' name='new_payment_name_"+ index +"' required /></td>"+
							"<td><div class='form-check'><input class='form-check-input' type='radio' name='new_payment_real_"+ index +"' id='exampleRadios"+ index +"_yes' value='yes' checked><label class='form-check-label' for='exampleRadios"+ index +"_yes'>是</label></div><div class='form-check'><input class='form-check-input' type='radio' name='new_payment_real_"+ index +"' id='exampleRadios"+ index +"_no' value='no'><label class='form-check-label' for='exampleRadios"+ index +"_no'>否</label></div></td>"+
							"<td><button class='btn btn-danger' onclick=\"delete_element_by_id(\'new_payment_row_" + index + "\')\">删除</button></td>";
	new_row.innerHTML = new_row_innerHTML;
	ready_add_table.appendChild(new_row);
	index++;
	document.getElementById("index_number").value = index;
}
function add_new_job() {
	var ready_add_table = document.getElementById("ready-add-table");
	var new_row = document.createElement("tr");
	var new_row_id = "new_job_" + index;
	new_row.setAttribute("id", new_row_id);
	var new_row_innerHTML = "<td>自动</td>" +
							"<td><input type='input' class='form-control' name='new_job_"+ index +"' required /></td>"+
							"<td><select class='custom-select' name='priviledge_"+index+"'>"+
									"<option value='100'>无权限</option>"+
									"<option value='15'>点单权限</option>"+
									"<option value='20'>收银权限</option>"+
									"<option value='0'>管理权限</option>"+
								"</select></td>" +
							"<td><button class='btn btn-danger' onclick=\"delete_element_by_id(\'new_job_" + index + "\')\">删除</button></td>";
	new_row.innerHTML = new_row_innerHTML;
	ready_add_table.appendChild(new_row);
	index++;
	document.getElementById("index_number").value = index;
}
function create_authentication(selectObj, x) {
	var pri_value = selectObj.options[selectObj.selectedIndex].getAttribute("priviledge");
	if(pri_value<=20) {
		var check_if_exist = document.getElementById("username_" + x);
		if(check_if_exist != null)
			return;
		var auth_id = "staff_auth_" + x;
		var auth = document.getElementById(auth_id);
		var label_username = document.createElement("label");
		var input_username = document.createElement("input");
		var str = "username_" + x;
		label_username.setAttribute("id", "label_username_" + x);
		label_username.setAttribute("for", str);
		label_username.innerHTML = "用户名：";
		input_username.setAttribute("name", str);
		input_username.setAttribute("id", str);
		input_username.setAttribute("type", "input");
		input_username.setAttribute("class", "form-control");
		auth.appendChild(label_username);
		auth.appendChild(input_username);
		var label_password = document.createElement("label");
		var input_password = document.createElement("input");
		var str = "password_" + x;
		label_password.setAttribute("id", "label_password_" + x);
		label_password.setAttribute("for", str);
		label_password.innerHTML = "密码：";
		input_password.setAttribute("name", str);
		input_password.setAttribute("id", str);
		input_password.setAttribute("type", "password");
		input_password.setAttribute("class", "form-control");
		auth.appendChild(label_password);
		auth.appendChild(input_password);
	} else {
		var element = document.getElementById("username_" + x);
		if(element == null)
			return;
		delete_element_by_id("label_username_" + x);
		delete_element_by_id("label_password_" + x);
		delete_element_by_id("username_" + x);
		delete_element_by_id("password_" + x);
	}

}
function add_new_staff() {
	var ready_add_table = document.getElementById("ready-add-table");
	var new_row = document.createElement("tr");
	var new_row_id = "new_staff_" + index;
	new_row.setAttribute("id", new_row_id);
	var new_row_innerHTML = "<td>自动</td>" +
							"<td id='staff_auth_"+ index +"'><input type='input' class='form-control' name='staff_name_"+ index +"' required /></td>"+
							"<td><select class='custom-select' name='staff_gender_"+index+"'>"+
									"<option value='0'>男</option>"+
									"<option value='1'>女</option>"+
								"</select></td>" +
							"<td><select onChange='create_authentication(this," + index + ")' class='custom-select' name='staff_job_"+index+"'>"+
								options_innerHTML +
							"</select></td>" +
							"<td><input type='input' class='form-control' name='staff_salary_"+ index +"' required /></td>"+
							"<td><button class='btn btn-danger' onclick=\"delete_element_by_id(\'new_staff_" + index + "\')\">删除</button></td>";
	new_row.innerHTML = new_row_innerHTML;
	ready_add_table.appendChild(new_row);
	index++;
	document.getElementById("index_number").value = index;
}