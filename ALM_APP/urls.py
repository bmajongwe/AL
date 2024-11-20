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

        # behavioural patterns URLs
    path('create_behavioral_pattern/', views.create_behavioral_pattern, name='create_behavioral_pattern'),
    path('behavioral_patterns_list/', views.behavioral_patterns_list, name='behavioral_patterns_list'),
    path('edit_behavioral_pattern/<int:id>/', views.edit_behavioral_pattern, name='edit_behavioral_pattern'),
    path('delete_behavioral_pattern/<int:id>/', views.delete_behavioral_pattern, name='delete_behavioral_pattern'),
    path('view_behavioral_patterns/<int:id>/', views.view_behavioral_pattern, name='view_behavioral_pattern'),
   
       # Time buckets URLs
    path('time_bucket_list/', views.time_buckets_list, name='time_bucket_list'),
    path('create_time_bucket/', views.create_time_bucket, name='create_time_bucket'),
    path('edit_time_bucket/<int:id>/', views.edit_time_bucket, name='edit_time_bucket'),
    path('delete_time_buckets/<int:id>/', views.delete_time_bucket, name='delete_time_bucket'),
    path('view_time_bucket/<int:id>/', views.view_time_bucket, name='view_time_bucket'),

    # ProductFilter URLs
    path('filters/', ProductFilterListView.as_view(), name='product_filter_list'),
    path('filters/create/', ProductFilterCreateView.as_view(), name='product_filter_create'),
    path('filters/create/', ProductFilterCreateView.as_view(), name='create_filter'),
    path('filters/<int:pk>/edit/', ProductFilterUpdateView.as_view(), name='product_filter_update'),
    path('filters/<int:pk>/delete/', ProductFilterDeleteView.as_view(), name='product_filter_delete'),
    path('filters/<int:pk>/', views.ProductFilterDetailView.as_view(), name='product_filter_detail'),

    # Process URLs
    path('processes/', ProcessListView.as_view(), name='process_list'),
    path('processes/create/', views.process_create_view, name='process_create'),
    path('processes/execute/', views.execute_process_view, name='execute_process'),
    path('processes/<int:pk>/edit/', ProcessUpdateView.as_view(), name='process_update'),
    path('processes/<int:pk>/delete/', ProcessDeleteView.as_view(), name='process_delete'),

    # Reports URLs
    path('reports/liquidity-gap/', views.liquidity_gap_report, name='liquidity_gap_report'),
    path('export/liquidity-gap/', export_liquidity_gap_to_excel, name='export_liquidity_gap_to_excel'),
    path('export/liquidity-gap-cons/', views.export_liquidity_gap_cons_to_excel, name='export_liquidity_gap_cons_to_excel'),






   
]
