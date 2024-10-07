# ALM_APP/urls.py
from django.urls import path
from . import views 
from .views import *



urlpatterns = [
    # path('success/', views.success, name='success'),
    path('project_cash_flows/', project_cash_flows_view, name='project_cash_flows'),
    #path('project-cash-flows/', project_cash_flows_view, name='project_cash_flows'),
    # path('define-time-buckets/', views.define_time_buckets, name='define_time_buckets'),
    #path('time-buckets-list/', views.time_buckets_list, name='time_buckets_list'),
    # path('liquidity_gap_results/', liquidity_gap_results_view, name='liquidity_gap_results'),
    # path('create_behavioral_pattern/', liquidity_gap_results_view, name='create_behavioral_pattern'),

    
    path('create_behavioral_pattern/', views.create_behavioral_pattern, name='create_behavioral_pattern'),
    path('behavioral_patterns_list/', views.behavioral_patterns_list, name='behavioral_patterns_list'),
    path('edit_behavioral_pattern/<int:id>/', views.edit_behavioral_pattern, name='edit_behavioral_pattern'),
    path('delete_behavioral_pattern/<int:id>/', views.delete_behavioral_pattern, name='delete_behavioral_pattern'),
    path('view_behavioral_patterns/<int:id>/', views.view_behavioral_pattern, name='view_behavioral_pattern'),
   
    path('time_bucket_list/', views.time_buckets_list, name='time_bucket_list'),
    path('create_time_bucket/', views.create_time_bucket, name='create_time_bucket'),
    path('edit_time_bucket/<int:id>/', views.edit_time_bucket, name='edit_time_bucket'),
    path('delete_time_buckets/<int:id>/', views.delete_time_bucket, name='delete_time_bucket'),
    path('view_time_bucket/<int:id>/', views.view_time_bucket, name='view_time_bucket'),




   
]
