function delete_element_method(form_id) {
	var msg = "您确定要删除吗？删除以后数据不可恢复。\n\n请确认。";
	if (confirm(msg)==true){
		form = document.getElementById(form_id);
		form.submit();
	}else{
		return ;
	}
}
function update_element_method(form_id) {
	var msg = "您确定要更改吗？更改后用户名和密码都将被覆盖。\n\n请确认。";
	if (confirm(msg)==true){
		form = document.getElementById(form_id);
		form.submit();
	}else{
		return ;
	}
}
function delete_element_by_id(id) {
	var thisNode = document.getElementById(id);
	thisNode.parentNode.removeChild(thisNode);
}
function value_up(id) {
	var element = document.getElementById(id);
	element.value++;
}
function value_down(id) {
	var element = document.getElementById(id);
	element.value--;
}