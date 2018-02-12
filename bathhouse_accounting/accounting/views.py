# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.utils.timezone import now, timedelta
from .models import *

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
	elif login_status == 2:
		message = '用户名密码错误'
	context = {
		"message": message,
	}
	return render(request, "index.html", context)

def admin_bill_index(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	return HttpResponseRedirect('/accounting/administrator/bill/today/')

def admin_bill_today(request):
	if 'user_id' not in request.session:
		return HttpResponseRedirect('/accounting/')
	user_id = request.session['user_id']
	system_user = SystemUser.objects.filter(user_id=user_id).order_by('-id')[0]
	if system_user.role != 'admin' or system_user.is_deleted:
		return HttpResponseRedirect('/accounting/')
	start = now().date()
	end = start + timedelta(days=1)
	record = Income.objects.filter(date__range=(start, end))
	context = {
		"record":record,
		"tag":"bill",
		"label": "today"
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
				if staff_job.priviledge <= 20:
					if staff_job.priviledge <=5:
						role = "admin"
					else:
						role = "staff"
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
		return HttpResponseRedirect('/accounting/administrator/payment-method/')
	if request.method == "POST" and "delete_element" in request.POST:
		payment_id = request.POST['payment_no']
		payment_method = PaymentMethod.objects.get(pk=payment_id)
		payment_method.is_deleted = True
		payment_method.save()
		return HttpResponseRedirect('/accounting/administrator/payment-method/')
	record = PaymentMethod.objects.filter(is_deleted=False)
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
		return HttpResponseRedirect('/accounting/administrator/service/')
	if request.method == "POST" and "delete_element" in request.POST:
		item_id = request.POST['item_no']
		item = Item.objects.get(pk=item_id)
		item.is_deleted = True
		item.save()
		return HttpResponseRedirect('/accounting/administrator/service/')
	record = Item.objects.filter(is_deleted=False)
	context = {
		"record":record,
		"tag":"service",
	}
	return render(request,"admin_service.html", context)
# Create your views here.
