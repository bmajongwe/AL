# ALM_APP/urls.py
from django.urls import path
from . import views 
from .views import *



urlpatterns = [
    # path('success/', views.success, name='success'),
    path('project_cash_flows/', project_cash_flows_view, name='project_cash_flows'),
    #path('project-cash-flows/', project_cash_flows_view, name='project_cash_flows'),
    path('define-time-buckets/', views.define_time_buckets, name='define_time_buckets'),
    #path('time-buckets-list/', views.time_buckets_list, name='time_buckets_list'),
    path('liquidity_gap_results/', liquidity_gap_results_view, name='liquidity_gap_results'),


   
]
