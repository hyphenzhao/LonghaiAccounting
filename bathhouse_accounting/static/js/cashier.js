var index = 1;
function search_vip() {
	var vip_no = document.getElementById("vip_no");
	window.location.href = "/accounting/cashier/VIP/view?vip_no=" + vip_no.value;
}
function payment_method_alter() {
	var payment_method = document.getElementById("payment_method");
	var current_method = document.getElementById("current_method");
	if(payment_method.value == current_method.value) {
		var auth_method = document.getElementById("payment_auth_method");
		var card_pay = document.getElementById("payment_auth_card");
		var auth_submit = document.getElementById("payment_auth_method_selection");
		auth_method.removeAttribute("hidden");
		card_pay.removeAttribute("hidden");
		auth_submit.value = "card";
	} else {
		var auth_method = document.getElementById("payment_auth_method");
		var card_pay = document.getElementById("payment_auth_card");
		var phone_pay = document.getElementById("payment_auth_phone");
		var auth_submit = document.getElementById("payment_auth_method_selection");
		auth_method.setAttribute("hidden","");
		card_pay.setAttribute("hidden","");
		phone_pay.setAttribute("hidden","");
		auth_submit.value = "";
	}
}

function auth_method_alter() {
	var auth1 = document.getElementById("payment_auth_1");
	var auth2 = document.getElementById("payment_auth_2");
	var card_pay = document.getElementById("payment_auth_card");
	var phone_pay = document.getElementById("payment_auth_phone");
	var auth_submit = document.getElementById("payment_auth_method_selection");
	card_pay.removeAttribute("hidden");
	phone_pay.removeAttribute("hidden");
	if(auth1.checked) {
		phone_pay.setAttribute("hidden","");
		auth_submit.value = "card";
	}else if(auth2.checked) {
		card_pay.setAttribute("hidden","");
		auth_submit.value = "phone";
	}else{
		auth_submit.value = "";
	}
}

function add_new_service() {
	var ready_add_table = document.getElementById("ready-add-table");
	var new_row = document.createElement("tr");
	var new_row_id = "new_service_" + index;
	new_row.setAttribute("id", new_row_id);
	var new_row_innerHTML = "<td>自动</td>" +
							"<td><select class='custom-select' id=\"service_selection_" + index + "\" name='service_selection_"+index+"' onchange=\"service_onchange(" + index + ")\">"+
								options_innerHTML +
							"</select></td>"+
							"<td><p id=\"price_" + index + "\"></p></td>"+
							"<td>" +
								"<input type=\"number\" class=\"form-control\" maxlength=\"3\" style=\"width: 60px;\" name=\"number_" + index +"\" value=\"1\"/>" +
							"</td>"+
							"<td><select class='custom-select' id=\"staff_selection_" + index + "\" name='staff_selection_"+index+"'>"+
								staff_options_innerHTML +
							"</select></td>" +
							"<td><button class='btn btn-danger' onclick=\"delete_element_by_id(\'new_service" + index + "\')\">删除</button></td>";
	new_row.innerHTML = new_row_innerHTML;
	ready_add_table.appendChild(new_row);
	item = document.getElementById("service_selection_" + index);
	item_id = parseInt(item.options[item.selectedIndex].value);
	item_price = document.getElementById("price_" + index);
	item_price.innerHTML = prices.get(item_id);
	index++;
	document.getElementById("index_number").value = index;
}

function service_onchange(id) {
	item = document.getElementById("service_selection_" + id);
	item_id = parseInt(item.options[item.selectedIndex].value);
	item_price = document.getElementById("price_" + id);
	item_price.innerHTML = prices.get(item_id);
}

function select_staff(id) {
	allButtons = document.getElementsByName("staff_selection_button");
	for(var i = 0; i < allButtons.length; i++) {
		allButtons[i].setAttribute("class", "btn btn-lg btn-outline-primary");
	}
	selectedButton = document.getElementById("staff_selection_button_" + id);
	selectedButton.setAttribute("class","btn btn-lg btn-primary");
	selectedInput = document.getElementById("staff_selection_input");
	selectedInput.value = id;
}

function select_service(id) {
	selectedInput = document.getElementById("service_selection_input");
	selectedInput.value = id;
	form = document.getElementById("add_form");
	form.submit();
}