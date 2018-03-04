from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/$',views.logout, name='logout'),
    url(r'^administrator/$', views.admin_bill_index, name='admin_index'),
    url(r'^administrator/bill/$', views.admin_bill_index, name='admin_bill_index'),
    url(r'^administrator/bill/search/$', views.admin_bill_search, name='admin_bill_search'),
    url(r'^administrator/bill/droped', views.admin_bill_droped, name='admin_bill_droped'),
    url(r'^administrator/bill/deleted', views.admin_bill_deleted, name='admin_bill_deleted'),
    url(r'^administrator/bill/view', views.admin_bill_view, name='admin_bill_view'),
    url(r'^administrator/bill/today', views.admin_bill_today, name='admin_bill_today'),
    url(r'^administrator/bill/yesterday', views.admin_bill_yesterday, name='admin_bill_yesterday'),
    url(r'^administrator/bill/month', views.admin_bill_month, name='admin_bill_month'),
    url(r'^administrator/bill/year', views.admin_bill_year, name='admin_bill_year'),
    url(r'^administrator/payment-method/$', views.admin_payment_method, name='admin_payment_method'),
    url(r'^administrator/member/$', RedirectView.as_view(permanent=True, url='job/'), name='admin_member_index'),
    url(r'^administrator/member/job/$', views.admin_member_job, name='admin_member_job'),
    url(r'^administrator/member/staff/$', views.admin_member_staff, name='admin_member_staff'),
    url(r'^administrator/member/auth/$', views.admin_member_auth, name='admin_member_auth'),
    url(r'^administrator/service/$', views.admin_service, name='admin_service'),
    url(r'^administrator/VIP/$', views.admin_VIP, name='admin_VIP'),
    url(r'^administrator/VIP/viewbill', views.admin_VIP_viewbill, name='admin_VIP_viewbill'),
    url(r'^administrator/VIP/topuprecord', views.admin_VIP_topuprecord, name='admin_VIP_topuprecord'),
    url(r'^administrator/VIP/paymentrecord', views.admin_VIP_paymentrecord, name='admin_VIP_paymentrecord'),
    url(r'^administrator/VIP/methods/$', views.admin_VIP_methods, name='admin_VIP_methods'),
    url(r'^administrator/VIP/update', views.admin_VIP_update, name='admin_VIP_update'),
    url(r'^cashier/$', RedirectView.as_view(permanent=True, url='bill/'), name='cashier_index'),
    url(r'^cashier/daily/$', views.cashier_daily, name='cashier_daily'),
    url(r'^cashier/bill/$', views.cashier_bill, name='cashier_bill'),
    url(r'^cashier/bill/create/$', views.cashier_bill_create, name='cashier_bill_create'),
    url(r'^cashier/bill/pay', views.cashier_bill_pay, name='cashier_bill_pay'),
    url(r'^cashier/bill/edit', views.cashier_bill_edit, name='cashier_bill_edit'),
    url(r'^cashier/VIP/$', views.cashier_vip, name='cashier_vip'),
    url(r'^cashier/VIP/view', views.cashier_vip_view, name='cashier_vip_view'),
    url(r'^cashier/VIP/billview', views.cashier_vip_billview, name='cashier_vip_billview'),
    url(r'^cashier/VIP/topup', views.cashier_vip_topup, name='cashier_vip_topup'),
    url(r'^waiter/$', views.waiter_index, name='waiter_index'),
    url(r'^waiter/view/$', views.waiter_view, name='waiter_view'),
    url(r'^waiter/order/$', views.waiter_order, name='waiter_order'),
    url(r'^waiter/order/service/$', views.waiter_order_service, name='waiter_order_service'),
    url(r'^waiter/order/service/edit/$', views.waiter_order_service_edit, name='waiter_order_service_edit'),
]