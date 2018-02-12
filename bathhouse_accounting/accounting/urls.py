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
]