from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^administrator/$', views.admin_bill_index, name='admin_index'),
    url(r'^administrator/bill/$', views.admin_bill_index, name='admin_bill_index'),
    url(r'^administrator/bill/today/$', views.admin_bill_today, name='admin_bill_today'),
    url(r'^administrator/payment-method/$', views.admin_payment_method, name='admin_payment_method'),
    url(r'^administrator/member/$', RedirectView.as_view(permanent=True, url='job/'), name='admin_member_index'),
    url(r'^administrator/member/job/$', views.admin_member_job, name='admin_member_job'),
    url(r'^administrator/member/staff/$', views.admin_member_staff, name='admin_member_staff'),
    url(r'^administrator/member/auth/$', views.admin_member_auth, name='admin_member_auth'),
    url(r'^administrator/service/$', views.admin_service, name='admin_service'),
    url(r'^administrator/VIP/$', views.admin_VIP, name='admin_VIP'),
    url(r'^administrator/VIP/methods/$', views.admin_VIP_methods, name='admin_VIP_methods'),
    url(r'^administrator/VIP/update', views.admin_VIP_update, name='admin_VIP_update'),
    url(r'^cashier/$', RedirectView.as_view(permanent=True, url='bill/'), name='cashier_index'),
    url(r'^cashier/bill/$', views.cashier_bill, name='cashier_bill'),
    url(r'^cashier/bill/create/$', views.cashier_bill_create, name='cashier_bill_create'),
    url(r'^cashier/bill/pay', views.cashier_bill_pay, name='cashier_bill_pay'),
    url(r'^cashier/bill/edit', views.cashier_bill_edit, name='cashier_bill_edit'),
    url(r'^cashier/VIP/$', views.cashier_vip, name='cashier_vip'),
]