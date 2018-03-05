# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz
import math
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.utils.timezone import now, timedelta
from datetime import datetime
from .models import *
from decimal import *

utc=pytz.UTC

def logout(request):
	del request.session["user_id"]
	return HttpResponseRedirect('/accounting/')

def index(request):
	request.session.set_expiry(0)
	message = ''
	login_status = 0
	if 'user_id' in request.session:
		user = authenticate(id = request.session['user_id'])
		if user is not None:
			login_status = 1
		else:
			login_status = 2
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if user is not None:
			request.session["user_id"] = user.id
			login_status = 1
		else:
			tmp_users = User.objects.filter(first_name = username)
			if not tmp_users:
				return HttpResponseRedirect('/accounting/')
			tmp_user = tmp_users.order_by('-id')[0]
			username = tmp_user.username
			user = authenticate(username = username, password = password)
			if user is not None:
				request.session["user_id"] = user.id
				login_status = 1
			else:
				login_status = 2
	if login_status == 1:
		system_user = SystemUser.objects.filter(user=user).order_by('-id')[0]
		if system_user.is_deleted:
			message = '用户名密码错误'
			context = {
				"message": message,
			}
			return render(request, "index.html", context)
		if system_user.role == 'admin':
			return HttpResponseRedirect('/accounting/administrator/')
		if system_user.role == 'cashier':
			return HttpResponseRedirect('/accounting/cashier/')
		if system_user.role == 'waiter':
			return HttpResponseRedirect('/accounting/waiter/')
	elif login_status == 2:
		message = '用户名密码错误'
	context = {
		"message": message,
	}
	return render(request, "index.html", context)

def waiter_index(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'waiter' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	workers = Staff.objects.filter(is_deleted=False,title__priviledge=100)
	context = {
		"workers":workers
	}
	return render(request, "waiter_index.html", context)

def waiter_view(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'waiter' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	start = now().date()
	end = start + timedelta(days=1)
	staff = Staff.objects.get(pk=request.session['worker_id'])
	records = Service.objects.filter(is_deleted=False, income__date__range=(start,end),staff=staff)
	total = 0
	for i in records:
		total = total + i.item.price * i.item_no
	context = {
		"records": records,
		"total": total,
	}
	return render(request, "waiter_view.html", context)

def waiter_order(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'waiter' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	if request.method == "POST":
		request.session['worker_id'] = request.POST['worker_id']
	elif 'worker_id' not in request.session:
		return HttpResponseRedirect('/accounting/waiter/')
	incomes = Income.objects.filter(is_deleted=False,is_paid=False)
	context = {
		"incomes":incomes,
	}
	return render(request, "waiter_order.html", context)

def waiter_order_service(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'waiter' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	if request.method == "POST":
		request.session['income_id'] = request.POST['income_id']
	staff_id = request.session['worker_id']
	current_staff = Staff.objects.get(pk=staff_id)
	income_id = request.session['income_id']
	income = Income.objects.get(pk=income_id)
	if income.is_paid or income.is_deleted:
		return HttpResponseRedirect('/accounting/waiter/')
	services = Service.objects.filter(income=income,is_deleted=False).order_by("-id")
	items = Item.objects.filter(is_deleted=False).order_by("priority")
	total = 0
	if services.exists():
		for i in services:
			total = total + i.item.price * i.item_no
	context = {
		"tag": "bill",
		"items": items,
		"services": services,
		"income": income,
		"total": total,
		"current_staff": current_staff,
		"current_user": system_user
	}
	return render(request, "waiter_order_service.html", context)

def waiter_order_service_edit(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'waiter' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	staff_id = request.session['worker_id']
	income_id = request.session['income_id']
	income = Income.objects.get(pk=income_id)
	staff = Staff.objects.get(pk=staff_id)
	services = Service.objects.filter(income=income,is_deleted=False).order_by("-id")
	if request.method == "POST" and "add_element" in request.POST:
		item_id = request.POST['service_selection']
		selected_item = Item.objects.get(pk=item_id)
		exist_service = services.filter(staff=staff,item=selected_item,recorder=system_user)
		if exist_service:
			selected_service = exist_service.order_by('-id')[0]
			selected_service.item_no = selected_service.item_no + 1
			selected_service.save()
		else:
			new_service = Service(
					income=income,
					item=selected_item,
					staff=staff,
					recorder=system_user, 
				)
			new_service.save()
	if request.method == "POST" and "delete_element" in request.POST:
		service_id = request.POST['service_id']
		delete_service = Service.objects.get(pk=service_id)
		if delete_service.item_no > 1:
			delete_service.item_no = delete_service.item_no - 1
		else:
			delete_service.item_no = 0
			delete_service.is_deleted = True
		delete_service.save()
	return HttpResponseRedirect('/accounting/waiter/order/service/')

def cashier_vip(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'cashier' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	record = VIP.objects.filter(is_deleted=False)
	context = {
		"record":record,
		"tag":"vip",
	}
	return render(request, "cashier_vip.html", context)

def cashier_vip_topup(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'cashier' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	vip_id = request.GET['vip_no']
	vip = VIP.objects.get(pk=vip_id)
	methods = PaymentMethod.objects.filter(is_deleted=False).order_by("priority")
	if methods:
		first_method = methods[0]
	vip_method_exist = VIPPayment.objects.all()
	if vip_method_exist:
		vip_method = vip_method_exist.order_by('id')[0].payment
	if request.method == "POST":
		payment_method_id = request.POST['payment_method']
		payment_method = PaymentMethod.objects.get(pk=payment_method_id)
		total = request.POST['topup_balance']
		vip.balance = vip.balance + Decimal(total)
		vip.save()
		new_record = VIPTopupRecord(
			vip=vip,
			recorder=system_user,
			operation=2,
			payment_method=payment_method,
			note="充值" + total + "元，充值方式：" + payment_method.name,
			)
		new_record.save()
		return HttpResponseRedirect('/accounting/cashier/VIP/')
	context = {
		"vip":vip,
		"tag":"vip",
		"methods": methods,
		"vip_method": vip_method,
		"first_method": first_method
	}
	return render(request, "cashier_vip_topup.html", context)

def cashier_vip_view(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'cashier' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	vip_id = request.GET['vip_no']
	vips = VIP.objects.filter(is_deleted=False,card_no=vip_id)
	if vips:
		vip = vips.order_by('-id')[0]
	else:
		return HttpResponseRedirect('/accounting/cashier/VIP/')
	context = {
		"vip":vip,
		"tag":"vip",
	}
	return render(request, "cashier_vip_view.html", context)

def cashier_vip_billview(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'cashier' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	vip_no = request.GET['vip_no']
	vip = VIP.objects.get(pk=vip_no)
	record = Income.objects.filter(is_deleted=False, vip=vip)
	services = {}
	for i in record:
		tmp_services = Service.objects.filter(is_deleted=False, income=i)
		services[i.id] = tmp_services
	pages_number = 0
	start_no = 0
	page_no = 0
	if len(record) > 50:
		pages_number = int(math.ceil(len(record)/50.0))
		if "page" not in request.GET:
			return HttpResponseRedirect("/accounting/administrator/VIP/paymentrecord?page=0")
	if "page" in request.GET:
		page_no = int(request.GET['page'])
		start_no = page_no * 50
		if len(record) - start_no >= 50:
			record = record[start_no:start_no + 50]
		else:
			record = record[start_no:]
	context = {
		"vip":vip,
		"tag":"vip",
		"base_no": start_no,
		"pages_number": range(pages_number),
		"page_no": page_no,
		"records": record,
		"services": services
	}
	return render(request, "cashier_vip_billview.html", context)

def cashier_daily(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'cashier' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	start = now().date()
	end = start + timedelta(days=1)
	records = Income.objects.filter(date__range=(start, end),is_deleted=False,is_paid=True,recorder=system_user)
	total_dict = {}
	payment_methods = PaymentMethod.objects.filter(is_deleted=False).order_by("priority")
	final_total = 0
	for i in payment_methods:
		total = 0
		records_paid = records.filter(payment_method=i)
		for j in records_paid:
			total = total + j.total
		total_dict[i.name] = total
		final_total = final_total + total
	context = {
		"tag":"daily",
		"totals": total_dict,
		"final_total": final_total,
		"time": now().date(),
		"recorder": system_user,
		"number": len(records)
	}
	return render(request, "cashier_daily.html", context)

def cashier_bill(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'cashier' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	if request.method == "POST" and "delete_element" in request.POST:
		income_id = request.POST['income_id']
		income = Income.objects.get(pk=income_id)
		income.is_deleted = True
		income.save()
		related_services = Service.objects.filter(is_deleted=False, income=income)
		for i in related_services:
			i.is_deleted = True
			i.save()
		return HttpResponseRedirect('/accounting/cashier/bill/')
	record = Income.objects.filter(is_deleted=False,is_paid=False)
	female_record = [0 for i in range(64)]
	male_record = [0 for i in range(78)]
	for i in record:
		if i.gender:
			female_record[int(i.card_no)] = i.id
		else:
			male_record[int(i.card_no)] = i.id
	context = {
		"record":record,
		"tag":"bill",
		"female_range":range(63),
		"male_range":range(77),
		"male_record": male_record,
		"female_record": female_record
	}
	return render(request, "cashier_bill.html", context)

def cashier_bill_create(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'cashier' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	if request.method == "POST":
		card_no = request.POST['card_no']
		item_no = request.POST['item_no']
		if item_no == "0":
			gender = False
		else:
			gender = True
		new_income = Income(
			card_no=card_no,
			recorder=system_user,
			gender=gender
			)
		new_income.save()
		return HttpResponseRedirect('/accounting/cashier/bill/')
	items = Item.objects.filter(is_deleted=False).order_by("priority")
	context = {
		"tag":"bill",
		"items":items,
	}
	return render(request, "cashier_bill_create.html", context)

def cashier_bill_edit(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'cashier' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	income_id = request.GET['income_id']
	income = Income.objects.get(pk=income_id)
	if income.is_paid or income.is_deleted:
		return HttpResponseRedirect('/accounting/cashier/bill/')
	services = Service.objects.filter(income=income,is_deleted=False).order_by("-id")
	items = Item.objects.filter(is_deleted=False).order_by("priority")
	staffs = Staff.objects.filter(title__priviledge=100,is_deleted=False)
	payment_methods = PaymentMethod.objects.filter(is_deleted=False).order_by("priority")
	current_method = VIPPayment.objects.all().order_by('-id')[0]
	total = 0
	previous_service = None
	if services.exists():
		for i in services:
			total = total + i.item.price * i.item_no
		previous_service = services[0]
	if request.method == "POST" and "add_element" in request.POST:
		staff_id = request.POST['staff_selection']
		item_id = request.POST['service_selection']
		selected_item = Item.objects.get(pk=item_id)
		if staff_id != "0" and staff_id != "":
			selected_staff = Staff.objects.get(pk=staff_id)
			exist_service = services.filter(staff=selected_staff,item=selected_item,recorder=system_user)
		else:
			exist_service = services.filter(item=selected_item,recorder=system_user)
		if exist_service:
			selected_service = exist_service.order_by('-id')[0]
			selected_service.item_no = selected_service.item_no + 1
			selected_service.save()
		else:
			if staff_id != "0" and staff_id != "":
				selected_staff = Staff.objects.get(pk=staff_id)
				new_service = Service(
					income=income,
					item=selected_item,
					staff=selected_staff,
					recorder=system_user, 
				)
			else:
				new_service = Service(
					income=income,
					item=selected_item,
					recorder=system_user, 
				)
			new_service.save()
		return HttpResponseRedirect('/accounting/cashier/bill/edit?income_id=' + income_id)
	if request.method == "POST" and "delete_element" in request.POST:
		service_id = request.POST['service_id']
		delete_service = Service.objects.get(pk=service_id)
		if delete_service.item_no > 1:
			delete_service.item_no = delete_service.item_no - 1
		else:
			delete_service.item_no = 0
			delete_service.is_deleted = True
		delete_service.save()
		return HttpResponseRedirect('/accounting/cashier/bill/edit?income_id=' + income_id)
	first_method = 0
	if payment_methods:
		first_method = payment_methods[0]
	context = {
		"tag":"bill",
		"items":items,
		"services":services,
		"income": income,
		"total": total,
		"staffs": staffs,
		"current_user": system_user,
		"methods": payment_methods,
		"current_method": current_method,
		"first_method": first_method,
		"previous_service": previous_service
	}
	return render(request, "cashier_bill_edit.html", context)

def cashier_bill_pay(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'cashier' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	income_id = request.GET['income_id']
	income = Income.objects.get(pk=income_id)
	if income.is_paid or income.is_deleted:
		return HttpResponseRedirect('/accounting/cashier/bill/')
	services = Service.objects.filter(income=income,is_deleted=False)
	payment_methods = PaymentMethod.objects.filter(is_deleted=False).order_by("priority")
	current_method = VIPPayment.objects.all().order_by('-id')[0]
	total = 0
	if services.exists():
		for i in services:
			total = total + i.item.price * i.item_no
	if request.method == "POST" and "pay" in request.POST:
		vip_pay = request.POST['payment_auth_method_selection']
		if vip_pay != "":
			auth_check = False
			if vip_pay == "card":
				card_no = request.POST['vip_card_no']
				vip_user = VIP.objects.filter(is_deleted=False, card_no=card_no)
				if vip_user:
					vip = vip_user.order_by('-id')[0]
					auth_check = True
			elif vip_pay == "phone":
				phone = request.POST['phone_no']
				password = request.POST['phone_password']
				vip_user = VIP.objects.filter(is_deleted=False, phone=phone)
				if vip_user and vip_user.order_by('-id')[0].password == password:
					vip = vip_user.order_by('-id')[0]
					auth_check = True
			if auth_check and vip.balance >= total:
				vip.balance = vip.balance - total
				vip.save()
				income.customer_name = vip.holder
				payment_method_id = request.POST['payment_method']
				payment_method = PaymentMethod.objects.get(pk=payment_method_id)
				income.total = total
				income.payment_method = payment_method
				income.is_paid = True
				income.vip = vip
				income.paid_date = now()
				income.save()
				context = {
					"tag":"bill",
					"vip": vip,
					"income_id": income_id,
					"total": income.total,
					"time": income.date
				}
				return render(request, "cashier_vip_pay_success.html", context)
			else:
				vip = None
				if auth_check:
					error_message = "余额不足，请充值后支付"
					vip = vip_user.order_by('-id')[0]
				else:
					error_message = "用户不存在，请返回重新刷卡"
				context = {
					"tag":"vip",
					"error_message": error_message,
					"vip": vip,
					"income_id": income_id
				}
				return render(request, "cashier_vip_pay_failed.html", context)
		else:
			payment_method_id = request.POST['payment_method']
			payment_method = PaymentMethod.objects.get(pk=payment_method_id)
			income.total = total
			income.payment_method = payment_method
			income.is_paid = True
			income.paid_date = now()
			income.save()
			return HttpResponseRedirect('/accounting/cashier/bill/')
	context = {
		"tag":"bill",
		"services":services,
		"income": income,
		"methods": payment_methods,
		"current_method": current_method,
		"total": total,
	}
	return render(request, "cashier_bill_pay.html", context)

def admin_bill_index(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	return HttpResponseRedirect('/accounting/administrator/bill/today/')

def admin_bill_search(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	servants = Staff.objects.filter(is_deleted=False, title__priviledge=100)
	methods = PaymentMethod.objects.filter(is_deleted=False).order_by("priority")
	incomes = Income.objects.all().order_by("date")
	if incomes:
		first_income = incomes[0]
	else:
		context = {
		"tag": "bill",
		"label": "search",
		"servants": servants,
		"methods": methods,
		"today": today,
		"error_message":"无记录！"
		}
		return render(request, "admin_bill_search.html", context)
	today = datetime(now().year, now().month, now().day, 23, 59, 59, tzinfo=utc)
	first_day = first_income.date
	if request.method == "POST":
		start_year = request.POST['start_year']
		start_month = request.POST['start_month']
		start_day = request.POST['start_day']
		end_year = request.POST['end_year']
		end_month = request.POST['end_month']
		end_day = request.POST['end_day']
		staff_id = request.POST['staff_filter']
		payment_id = request.POST['payment_filter']
		start_date = datetime(int(start_year), int(start_month), int(start_day), tzinfo=utc)
		end_date = datetime(int(end_year), int(end_month), int(end_day), 23, 59, 59, tzinfo=utc)
		if start_date <= end_date and start_date <= today and end_date <= today:
			if staff_id != "0" and payment_id != "0":
				staff = Staff.objects.get(pk=staff_id)
				payment = PaymentMethod.objects.get(pk=payment_id)
				services = Service.objects.filter(income__is_deleted=False, is_deleted=False, income__date__range=(start_date, end_date),staff=staff, income__payment_method=payment)
			elif staff_id != "0":
				staff = Staff.objects.get(pk=staff_id)
				services = Service.objects.filter(income__is_deleted=False, is_deleted=False, income__date__range=(start_date, end_date),staff=staff)
			elif payment_id != "0":
				payment = PaymentMethod.objects.get(pk=payment_id)
				services = Service.objects.filter(income__is_deleted=False, is_deleted=False, income__date__range=(start_date, end_date), income__payment_method=payment)
			else:
				services = Service.objects.filter(income__is_deleted=False, is_deleted=False, income__date__range=(start_date, end_date))
			all_total = 0
			labour_cost = 0
			ranged_incomes = Income.objects.filter(is_deleted=False, date__range=(start_date, end_date))
			for i in services:
				all_total = all_total + i.item_no * i.item.price
				labour_cost = labour_cost + i.item.price * i.item_no * i.item.promote_ratio
			context = {
				"tag": "bill",
				"label": "search",
				"servants": servants,
				"methods": methods,
				"today": today,
				"services": services,
				"all_total": all_total,
				"labour_cost": labour_cost,
				"start_date": start_date,
				"end_date": end_date
			}
			return render(request, "admin_bill_search_result.html", context)
		else:
			context = {
				"tag": "bill",
				"label": "search",
				"servants": servants,
				"methods": methods,
				"today": today,
				"error_message":"时间输入错误，无记录！"
			}
			return render(request, "admin_bill_search.html", context)
	context = {
		"tag": "bill",
		"label": "search",
		"servants": servants,
		"methods": methods,
		"today": today
	}
	return render(request, "admin_bill_search.html", context)

def admin_bill_droped(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	record = Income.objects.filter(is_deleted=True).order_by('-date')
	pages_number = 0
	start_no = 0
	page_no = 0
	if len(record) > 50:
		pages_number = int(math.ceil(len(record)/50.0))
		if "page" not in request.GET:
			return HttpResponseRedirect("/accounting/administrator/bill/droped?page=0")
	if "page" in request.GET:
		page_no = int(request.GET['page'])
		start_no = page_no * 50
		if len(record) - start_no >= 50:
			record = record[start_no:start_no + 50]
		else:
			record = record[start_no:]
	context = {
		"record":record,
		"tag":"bill",
		"label": "drop",
		"base_no": start_no,
		"pages_number": range(pages_number),
		"page_no": page_no
	}
	return render(request, "admin_bill_today.html", context)

def admin_bill_deleted(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	records = Service.objects.filter(is_deleted=True).order_by('-id')
	pages_number = 0
	start_no = 0
	page_no = 0
	if len(records) > 50:
		pages_number = int(math.ceil(len(records)/50.0))
		if "page" not in request.GET:
			return HttpResponseRedirect("/accounting/administrator/bill/deleted?page=0")
	if "page" in request.GET:
		page_no = int(request.GET['page'])
		start_no = page_no * 50
		if len(records) - start_no >= 50:
			records = records[start_no:start_no + 50]
		else:
			records = records[start_no:]
	context = {
		"records":records,
		"tag":"bill",
		"label": "delete",
		"page_no": page_no,
		"pages_number": range(pages_number),
		"base_no": start_no,
	}
	return render(request, "admin_bill_deleted.html", context)

def admin_bill_view(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	income_id = request.GET['income_id']
	record = Income.objects.get(pk=income_id)
	vip_pay = VIPPayment.objects.all().order_by('id')[0]
	vip_paid = False
	if record.payment_method == vip_pay.payment:
		vip_paid = True
	services = Service.objects.filter(income=record)
	error_message = None
	if record.is_deleted:
		error_message = "已删除"
	context = {
		"tag":"bill",
		"label": "view_detail",
		"services": services,
		"record": record,
		"vip_paid": vip_paid,
		"error_message": error_message,
	}
	return render(request, "admin_bill_view.html", context)

def admin_bill_today(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	start = now().date()
	end = start + timedelta(days=1)
	record = Income.objects.filter(date__range=(start, end),is_deleted=False,is_paid=True).order_by('-date')
	total = 0
	if record:
		for i in record:
			total = total + i.total
	pages_number = 0
	start_no = 0
	page_no = 0
	if len(record) > 50:
		pages_number = int(math.ceil(len(record)/50.0))
		if "page" not in request.GET:
			return HttpResponseRedirect("/accounting/administrator/bill/today?page=0")
	if "page" in request.GET:
		page_no = int(request.GET['page'])
		start_no = page_no * 50
		if len(record) - start_no >= 50:
			record = record[start_no:start_no + 50]
		else:
			record = record[start_no:]
	context = {
		"record":record,
		"tag":"bill",
		"label": "today",
		"total":total,
		"base_no": start_no,
		"pages_number": range(pages_number),
		"page_no": page_no
	}
	return render(request,"admin_bill_today.html", context)

def admin_bill_yesterday(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	end = now().date()
	start = end + timedelta(days=-1)
	record = Income.objects.filter(date__range=(start, end),is_deleted=False,is_paid=True).order_by('-date')
	total = 0
	if record:
		for i in record:
			total = total + i.total
	pages_number = 0
	start_no = 0
	page_no = 0
	if len(record) > 50:
		pages_number = int(math.ceil(len(record)/50.0))
		if "page" not in request.GET:
			return HttpResponseRedirect("/accounting/administrator/bill/yesterday?page=0")
	if "page" in request.GET:
		page_no = int(request.GET['page'])
		start_no = page_no * 50
		if len(record) - start_no >= 50:
			record = record[start_no:start_no + 50]
		else:
			record = record[start_no:]
	context = {
		"record":record,
		"tag":"bill",
		"label": "yesterday",
		"total":total,
		"base_no": start_no,
		"pages_number": range(pages_number),
		"page_no": page_no
	}
	return render(request,"admin_bill_today.html", context)

def admin_bill_month(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	month = str(now().year)
	if now().month < 10:
		month = month + '-0' + str(now().month)
	else:
		month = month + '-' + str(now().month)
	record = Income.objects.filter(is_deleted=False,is_paid=True,date__startswith=month).order_by('-date')
	total = 0
	if record:
		for i in record:
			total = total + i.total
	pages_number = 0
	start_no = 0
	page_no = 0
	if len(record) > 50:
		pages_number = int(math.ceil(len(record)/50.0))
		if "page" not in request.GET:
			return HttpResponseRedirect("/accounting/administrator/bill/month?page=0")
	if "page" in request.GET:
		page_no = int(request.GET['page'])
		start_no = page_no * 50
		if len(record) - start_no >= 50:
			record = record[start_no:start_no + 50]
		else:
			record = record[start_no:]
	context = {
		"record":record,
		"tag":"bill",
		"label": "month",
		"total":total,
		"pages_number": range(pages_number),
		"base_no": start_no,
		"page_no": page_no
	}
	return render(request,"admin_bill_today.html", context)

def admin_bill_year(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	year = now().year
	record = Income.objects.filter(date__year=year,is_deleted=False,is_paid=True).order_by('-date')
	total = 0
	if record:
		for i in record:
			total = total + i.total
	pages_number = 0
	start_no = 0
	page_no = 0
	if len(record) > 50:
		pages_number = int(math.ceil(len(record)/50.0))
		if "page" not in request.GET:
			return HttpResponseRedirect("/accounting/administrator/bill/year?page=0")
	if "page" in request.GET:
		page_no = int(request.GET['page'])
		start_no = page_no * 50
		if len(record) - start_no >= 50:
			record = record[start_no:start_no + 50]
		else:
			record = record[start_no:]
	context = {
		"record":record,
		"tag":"bill",
		"label": "year",
		"total":total,
		"base_no": start_no,
		"pages_number": range(pages_number),
		"page_no": page_no
	}
	return render(request,"admin_bill_today.html", context)

def admin_member_job(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	if request.method == "POST" and "add_element" in request.POST:
		index_number = request.POST['index_number']
		for i in range(1, int(index_number)):
			new_job_name_name = "new_job_" + str(i)
			if new_job_name_name in request.POST:
				new_job_name_value = request.POST[new_job_name_name]
				privilidge_name = "priviledge_" + str(i)
				privilidge_value = int(request.POST[privilidge_name])
				new_job = Job(
					name=new_job_name_value,
					priviledge=privilidge_value
					)
				new_job.save()
		return HttpResponseRedirect('/accounting/administrator/member/job/')
	if request.method == "POST" and "delete_element" in request.POST:
		job_id = request.POST['job_no']
		job = Job.objects.get(pk=job_id)
		job.is_deleted = True
		job.save()
		return HttpResponseRedirect('/accounting/administrator/member/job/')
	record = Job.objects.filter(is_deleted=False)
	context = {
		"record":record,
		"tag":"staff",
		"label": "job"
	}
	return render(request,"admin_member_job.html", context)

def admin_member_staff(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	if request.method == "POST" and "add_element" in request.POST:
		index_number = request.POST['index_number']
	 	for i in range(1, int(index_number)):
	 		staff_name_name = "staff_name_" + str(i)
	 		if staff_name_name in request.POST:
				staff_gender_name = "staff_gender_" + str(i)
				staff_job_name = "staff_job_" + str(i)
				staff_salary_name = "staff_salary_" + str(i)
				staff_name_value = request.POST[staff_name_name]
				staff_gender_value = request.POST[staff_gender_name]
				staff_job_value = int(request.POST[staff_job_name])
				staff_salary_value = int(request.POST[staff_salary_name])
				staff_job = Job.objects.get(pk=staff_job_value)
				new_staff = Staff(
					name=staff_name_value,
					gender=False if staff_gender_value=="0" else True,
					title=staff_job,
					salary=staff_salary_value
					)
				new_staff.save()
				role = "worker"
				if staff_job.priviledge <= 20:
					if staff_job.priviledge == 5:
						role = "admin"
					elif staff_job.priviledge == 20:
						role = "cashier"
					elif staff_job.priviledge == 15:
						role = "waiter"
					staff_username = request.POST["username_" + str(i)]
					staff_password = request.POST["password_" + str(i)]
					new_user = User.objects.create_user(
							username=staff_username,
							password=staff_password,
							first_name=staff_name_value
						)
					new_user.save()
					new_sys_user = SystemUser(
							user=new_user,
							staff=new_staff,
							role=role,
						)
					new_sys_user.save()
	 	return HttpResponseRedirect('/accounting/administrator/member/staff/')
	if request.method == "POST" and "delete_element" in request.POST:
		staff_id = request.POST['staff_no']
	 	staff = Staff.objects.get(pk=staff_id)
	 	staff.is_deleted = True
	 	staff.save()
	 	staff_sys_user = SystemUser.objects.filter(staff=staff).order_by('-id')[0]
	 	staff_sys_user.is_deleted = True
	 	staff_sys_user.save()
	 	return HttpResponseRedirect('/accounting/administrator/member/staff/')
	jobs = Job.objects.filter(is_deleted=False)
	record = Staff.objects.filter(is_deleted=False)
	context = {
		"jobs":jobs,
		"record":record,
		"tag":"staff",
		"label": "staff"
	}
	return render(request,"admin_member_staff.html", context)

def admin_member_auth(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	if request.method == "POST" and "update_element" in request.POST:
		sys_id = request.POST['sys_no']
		username = request.POST['username_' + str(sys_id)]
		password = request.POST['password_' + str(sys_id)]
		sys_user = SystemUser.objects.get(pk=sys_id)
		if password != "":
			sys_user.user.username = username
			sys_user.user.set_password(password)
			sys_user.user.save()
			sys_user.save()
		else:
			sys_user.user.username = username
			sys_user.user.save()
			sys_user.save()
	record = SystemUser.objects.filter(is_deleted=False)
	context = {
		"record":record,
		"tag":"staff",
		"label": "auth"
	}
	return render(request,"admin_member_auth.html", context)

def admin_payment_method(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	if request.method == "POST" and "add_element" in request.POST:
		index_number = request.POST['index_number']
		for i in range(1, int(index_number)):
			new_payment_name_name = "new_payment_name_" + str(i)
			if new_payment_name_name in request.POST:
				new_payment_name_value = request.POST[new_payment_name_name]
				is_real_name = 'new_payment_real_' + str(i)
				is_real = request.POST[is_real_name]
				is_real_value = True
				if(is_real == "no"):
					is_real_value = False
				new_payment = PaymentMethod(
					name=new_payment_name_value,
					real_income=is_real_value
					)
				new_payment.save()
				new_payment.priority = new_payment.id
				new_payment.save()
		return HttpResponseRedirect('/accounting/administrator/payment-method/')
	if request.method == "POST" and "delete_element" in request.POST:
		payment_id = request.POST['payment_no']
		payment_method = PaymentMethod.objects.get(pk=payment_id)
		payment_method.is_deleted = True
		payment_method.save()
		return HttpResponseRedirect('/accounting/administrator/payment-method/')
	if request.method == "POST" and "up_element" in request.POST:
		item_id = request.POST['item_no']
		items = PaymentMethod.objects.filter(is_deleted=False).order_by("priority")
		current_item = PaymentMethod.objects.get(pk=item_id)
		pre_item = items[0]
		for i in items:
			if i.id == current_item.id:
				pre_item_priority = pre_item.priority
				pre_item.priority = current_item.priority
				current_item.priority = pre_item_priority
				current_item.save()
				pre_item.save()
				return HttpResponseRedirect('/accounting/administrator/payment-method/#form_' + str(current_item.id))
			else:
				pre_item = i
	record = PaymentMethod.objects.filter(is_deleted=False).order_by("priority")
	context = {
		"record":record,
		"tag":"payment",
	}
	return render(request,"admin_payment_method.html", context)

def admin_service(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	if request.method == "POST" and "add_element" in request.POST:
		index_number = request.POST['index_number']
		for i in range(1, int(index_number)):
			new_service_name_name = "new_service_name_" + str(i)
			if new_service_name_name in request.POST:
				new_service_name = request.POST[new_service_name_name]
				new_service_price = request.POST['new_service_price_' + str(i)]
				new_service_cost = request.POST['new_service_cost_' + str(i)]
				new_service_ratio = request.POST['new_service_ratio_' + str(i)]
				new_service = Item(
					name=new_service_name,
					price=new_service_price,
					cost=new_service_cost,
					promote_ratio=new_service_ratio
					)
				new_service.save()
				new_service.priority = new_service.id
				new_service.save()
		return HttpResponseRedirect('/accounting/administrator/service/')
	if request.method == "POST" and "delete_element" in request.POST:
		item_id = request.POST['item_no']
		item = Item.objects.get(pk=item_id)
		item.is_deleted = True
		item.save()
		return HttpResponseRedirect('/accounting/administrator/service/')
	if request.method == "POST" and "up_element" in request.POST:
		item_id = request.POST['item_no']
		items = Item.objects.filter(is_deleted=False).order_by("priority")
		current_item = Item.objects.get(pk=item_id)
		pre_item = items[0]
		for i in items:
			if i.id == current_item.id:
				pre_item_priority = pre_item.priority
				pre_item.priority = current_item.priority
				current_item.priority = pre_item_priority
				current_item.save()
				pre_item.save()
				return HttpResponseRedirect('/accounting/administrator/service/#form_' + str(current_item.id))
			else:
				pre_item = i
	record = Item.objects.filter(is_deleted=False).order_by("priority")
	context = {
		"record":record,
		"tag":"service",
	}
	return render(request,"admin_service.html", context)

def admin_VIP(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	if request.method == "POST" and "add_element" in request.POST:
		index_number = request.POST['index_number']
		for i in range(1, int(index_number)):
			new_vip_exist = "new_vip_card_" + str(i)
			if new_vip_exist in request.POST:
				new_vip_card = request.POST[new_vip_exist]
				new_vip_name = request.POST['new_vip_name_' + str(i)]
				new_vip_phone = request.POST['new_vip_phone_' + str(i)]
				new_vip_balance = request.POST['new_vip_balance_' + str(i)]
				new_vip = VIP(
					card_no=new_vip_card,
					holder=new_vip_name,
					phone=new_vip_phone,
					balance=new_vip_balance
					)
				new_vip.save()
				note = "开卡，充值" + new_vip_balance + "元"
				new_vip_record = VIPTopupRecord(
						vip=new_vip,
						recorder=system_user,
						operation=1,
						note=note
					)
				new_vip_record.save()
		return HttpResponseRedirect('/accounting/administrator/VIP/')
	if request.method == "POST" and "delete_element" in request.POST:
		vip_id = request.POST['vip_no']
		vip = VIP.objects.get(pk=vip_id)
		vip.is_deleted = True
		vip.save()
		note = "销卡"
		new_vip_record = VIPTopupRecord(
			vip=vip,
			recorder=system_user,
			operation=3,
			note=note
		)
		new_vip_record.save()
		return HttpResponseRedirect('/accounting/administrator/VIP/')
	record = VIP.objects.filter(is_deleted=False).order_by('card_no')
	methods = PaymentMethod.objects.filter(is_deleted=False).order_by("priority")
	if VIPPayment.objects.all():
		current_method = VIPPayment.objects.all().order_by('-id')[0]
	else:
		current_method = "none"
	context = {
		"record":record,
		"tag":"vip",
		"methods": methods,
		"current_method": current_method,
		"label": "index",
	}
	return render(request,"admin_vip.html", context)
def admin_VIP_viewbill(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	vip_no = request.GET['no']
	vip = VIP.objects.get(pk=vip_no)
	record = Income.objects.filter(is_deleted=False, vip=vip)
	pages_number = 0
	start_no = 0
	page_no = 0
	if len(record) > 50:
		pages_number = int(math.ceil(len(record)/50.0))
		if "page" not in request.GET:
			return HttpResponseRedirect("/accounting/administrator/VIP/paymentrecord?page=0")
	if "page" in request.GET:
		page_no = int(request.GET['page'])
		start_no = page_no * 50
		if len(record) - start_no >= 50:
			record = record[start_no:start_no + 50]
		else:
			record = record[start_no:]
	context = {
		"records": record,
		"tag": "vip",
		"label": "payment_record",
		"vip":vip,
		"base_no": start_no,
		"pages_number": range(pages_number),
		"page_no": page_no
	}
	return render(request, "admin_vip_viewbill.html", context)
def admin_VIP_topuprecord(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	record = VIPTopupRecord.objects.all().order_by('-id')
	pages_number = 0
	start_no = 0
	page_no = 0
	if len(record) > 50:
		pages_number = int(math.ceil(len(record)/50.0))
		if "page" not in request.GET:
			return HttpResponseRedirect("/accounting/administrator/VIP/topuprecord?page=0")
	if "page" in request.GET:
		page_no = int(request.GET['page'])
		start_no = page_no * 50
		if len(record) - start_no >= 50:
			record = record[start_no:start_no + 50]
		else:
			record = record[start_no:]
	context = {
		"record":record,
		"tag":"vip",
		"label": "topup_record",
		"base_no": start_no,
		"pages_number": range(pages_number),
		"page_no": page_no
	}
	return render(request, "admin_vip_topuprecord.html", context)

def admin_VIP_paymentrecord(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	vip_paymethod = VIPPayment.objects.all().order_by('-id')[0]
	record = Income.objects.filter(is_deleted=False,payment_method__id=vip_paymethod.payment.id,is_paid=True).order_by("-id")
	pages_number = 0
	start_no = 0
	page_no = 0
	if len(record) > 50:
		pages_number = int(math.ceil(len(record)/50.0))
		if "page" not in request.GET:
			return HttpResponseRedirect("/accounting/administrator/VIP/paymentrecord?page=0")
	if "page" in request.GET:
		page_no = int(request.GET['page'])
		start_no = page_no * 50
		if len(record) - start_no >= 50:
			record = record[start_no:start_no + 50]
		else:
			record = record[start_no:]
	context = {
		"record":record,
		"tag":"vip",
		"label": "payment_record",
		"base_no": start_no,
		"pages_number": range(pages_number),
		"page_no": page_no
	}
	return render(request, "admin_vip_paymentrecord.html", context)

def admin_VIP_methods(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	if request.method == "POST":
		payment_method = request.POST['payment_method']
		payment = PaymentMethod.objects.get(pk=payment_method)
		if VIPPayment.objects.all(): 
			VIPPayment.objects.all().delete()
		new_payment = VIPPayment(
			payment=payment
			)
		new_payment.save()
	return HttpResponseRedirect('/accounting/administrator/VIP/')

def admin_VIP_update(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	vip_id = request.GET['no']
	record = VIP.objects.get(pk=vip_id)
	if record.is_deleted==True:
		return HttpResponseRedirect('/accounting/administrator/VIP/')
	if request.method == "POST":
		new_no = request.POST['card_no']
		new_name = request.POST['name']
		new_phone = request.POST['phone']
		new_balance = request.POST['balance']
		diff = Decimal(new_balance) - record.balance
		record.card_no = new_no
		record.holder = new_name
		record.phone = new_phone
		record.balance = new_balance
		record.save()
		note = "信息更新，余额变动：" + format(diff,"0.2f") + "元"
		new_vip_record = VIPTopupRecord(
			vip=record,
			recorder=system_user,
			operation=2,
			note=note
		)
		new_vip_record.save()
		return HttpResponseRedirect('/accounting/administrator/VIP/') 
	context = {
		"record":record,
		"tag":"vip",
	}
	return render(request,"admin_vip_update.html", context)
# Create your views here.
