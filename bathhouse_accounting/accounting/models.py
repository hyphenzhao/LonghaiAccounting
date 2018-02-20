# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
	name = models.CharField(max_length=60)
	priviledge = models.IntegerField(default=100)
	is_deleted = models.BooleanField(default=False)

class Staff(models.Model):
	name = models.CharField(max_length=60)
	# false = male, true = female
	gender = models.BooleanField(default=False)
	title = models.ForeignKey(
			Job,
			on_delete=models.CASCADE,
		)
	salary = models.IntegerField(default=0)
	is_deleted = models.BooleanField(default=False)

class SystemUser(models.Model):
	user = models.ForeignKey(
			User,
			on_delete=models.CASCADE,
		)
	staff = models.ForeignKey(
			Staff,
			on_delete=models.CASCADE,
		)
	role = models.CharField(max_length=30)
	phone = models.CharField(max_length=30, null=True)
	is_deleted = models.BooleanField(default=False)

class Item(models.Model):
	name = models.CharField(max_length=60)
	price = models.DecimalField(max_digits=25, decimal_places=15)
	cost = models.DecimalField(max_digits=25, decimal_places=15)
	promote_ratio = models.DecimalField(max_digits=25, decimal_places=15, default=0.0)
	is_deleted = models.BooleanField(default=False)

class PaymentMethod(models.Model):
	name = models.CharField(max_length=60)
	real_income = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)

class VIP(models.Model):
	card_no = models.CharField(max_length=60)
	holder = models.CharField(max_length=60, null=True)
	phone = models.CharField(max_length=60, null=True)
	balance = models.DecimalField(max_digits=25, decimal_places=15, default=0)
	email = models.CharField(max_length=60, null=True)
	is_deleted = models.BooleanField(default=False)
	password = models.CharField(max_length=100, null=True)

class VIPPayment(models.Model):
	payment = models.ForeignKey(
			PaymentMethod,
			on_delete=models.CASCADE,
			null=True
		)
class VIPTopupRecord(models.Model):
	vip = models.ForeignKey(
			VIP,
			on_delete=models.CASCADE,
		)
	recorder = models.ForeignKey(
			SystemUser,
			on_delete=models.CASCADE,
		)
	# 1 for create, 2 for edit(topup), 3 for delete
	operation = models.IntegerField()
	note = models.CharField(max_length=60)
	date = models.DateTimeField(auto_now_add=True, blank=True)

class Income(models.Model):
	customer_name = models.CharField(max_length=60, null=True)
	# false = male, true = female
	gender = models.BooleanField(default=False)
	total = models.DecimalField(max_digits=25, decimal_places=15, default=0.0)
	date = models.DateTimeField(auto_now_add=True, blank=True)
	card_no = models.CharField(max_length=60)
	recorder = models.ForeignKey(
			SystemUser,
			on_delete=models.CASCADE,
		)
	payment_method = models.ForeignKey(
			PaymentMethod,
			on_delete=models.CASCADE,
			null=True
		)
	vip = models.ForeignKey(
			VIP,
			on_delete=models.CASCADE,
			null=True
		)
	is_deleted = models.BooleanField(default=False)
	is_paid = models.BooleanField(default=False)

class Service(models.Model):
	income = models.ForeignKey(
			Income,
			on_delete=models.CASCADE,
		)
	item = models.ForeignKey(
			Item,
			on_delete=models.CASCADE,
			null=True
		)
	staff = models.ForeignKey(
			Staff,
			on_delete=models.CASCADE,
			null=True
		)
	recorder = models.ForeignKey(
			SystemUser,
			on_delete=models.CASCADE,
			null=True
		)
	item_no = models.DecimalField(max_digits=25, decimal_places=15, default=1.0)
	is_deleted = models.BooleanField(default=False)

# Create your models here.
