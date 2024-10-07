from collections import defaultdict
import os
import pandas as pd
from decimal import Decimal
import csv
import traceback
from django.contrib import messages  # Import messages framework
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from .forms import *
from datetime import datetime
from django.http import HttpResponse
from .Functions.Aggregated_Prod_Cashflow_Base import *
from .Functions.populate_liquidity_gap_results_base import *
from .Functions.aggregate_cashflows import *
from .Functions.Aggregated_Acc_level_cashflows import *
from .Functions.behavioral_pattern_utils import define_behavioral_pattern_from_form_data, delete_behavioral_pattern_by_id, update_behavioral_pattern_from_form_data
from .Functions.time_bucket_utils import define_time_bucket_from_form_data, update_time_bucket_from_form_data, delete_time_bucket_by_id
from .forms import TimeBucketsForm
from .models import TimeBuckets
from .models import FSI_Expected_Cashflow

from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .models import TimeBuckets, TimeBucketDefinition,product_level_cashflows






def create_behavioral_pattern(request):
    if request.method == 'POST':
        # Call the function to process the form data
        result = define_behavioral_pattern_from_form_data(request)
        
        # Check if there is an error
        if 'error' in result:
            # Use Django messages framework to display the error on the frontend
            messages.error(request, result['error'])

            # Return the form with existing data to repopulate the form fields
            return render(request, 'behavioral/create_behavioral_pattern.html', {
                'v_prod_type': request.POST.get('v_prod_type'),
                'description': request.POST.get('description'),
                'tenors': request.POST.getlist('tenor[]'),
                'multipliers': request.POST.getlist('multiplier[]'),
                'percentages': request.POST.getlist('percentage[]')
            })

        # If no error, assume success and redirect using the PRG pattern
        if 'success' in result:
            messages.success(request, "Behavioral pattern saved successfully!")
            return redirect('behavioral_patterns_list')  # Redirect to a success page or list

    # If it's not a POST request, render the form
    return render(request, 'behavioral/create_behavioral_pattern.html') # Redirect to the behavioral patterns list page

# View for Behavioral Pattern List
def behavioral_patterns_list(request):
    patterns = BehavioralPatternConfig.objects.all().order_by('-created_at')  # Fetching all patterns sorted by newest first
    return render(request, 'behavioral/behavioral_patterns_list.html', {'patterns': patterns})

# View for Editing Behavioral Pattern
# In your views.py

def edit_behavioral_pattern(request, id):
    try:
        # Get the pattern to edit
        pattern = BehavioralPatternConfig.objects.get(id=id)

        if request.method == 'POST':
            # Call the utility function to update the pattern
            result = update_behavioral_pattern_from_form_data(request, pattern)

            if 'error' in result:
                return render(request, 'behavioral/edit_behavioral_pattern.html', {
                    'error': result['error'],
                    'v_prod_type': pattern.v_prod_type,
                    'description': pattern.description,
                    'tenors': [entry.tenor for entry in pattern.entries.all()],
                    'multipliers': [entry.multiplier for entry in pattern.entries.all()],
                    'percentages': [entry.percentage for entry in pattern.entries.all()],
                })

            # If successful, display the success message and redirect
            messages.success(request, "Behavioral pattern updated successfully!")
            return redirect('behavioral_patterns_list')  # Redirect back to the patterns list

        # If GET request, prepopulate the form with the current data
        return render(request, 'behavioral/edit_behavioral_pattern.html', {
            'v_prod_type': pattern.v_prod_type,
            'description': pattern.description,
            'tenors': [entry.tenor for entry in pattern.entries.all()],
            'multipliers': [entry.multiplier for entry in pattern.entries.all()],
            'percentages': [entry.percentage for entry in pattern.entries.all()],
        })

    except BehavioralPatternConfig.DoesNotExist:
        messages.error(request, "Behavioral pattern not found.")
        return redirect('behavioral_patterns_list')
    
    


# View for Deleting Behavioral Pattern
def delete_behavioral_pattern(request, id):
    if request.method == 'POST':
        result = delete_behavioral_pattern_by_id(id)

        if 'error' in result:
            messages.error(request, result['error'])
        else:
            messages.success(request, "Behavioral pattern deleted successfully!")

        return redirect('behavioral_patterns_list')
    

def view_behavioral_pattern(request, id):
    behavioral_pattern = get_object_or_404(BehavioralPatternConfig, id=id)
    pattern_entries = BehavioralPatternEntry.objects.filter(pattern=behavioral_pattern).order_by('order')
    
    return render(request, 'behavioral/view_behavioral_pattern.html', {
        'behavioral_pattern': behavioral_pattern,
        'pattern_entries': pattern_entries
    })







def create_time_bucket(request):
    # Check if a Time Bucket Definition already exists
    if TimeBucketDefinition.objects.exists():
        messages.error(request, "Only one Time Bucket Definition is allowed.")
        return redirect('time_bucket_list')  # Redirect to the list page if one already exists

    if request.method == 'POST':
        # Call the function to process the form data
        result = define_time_bucket_from_form_data(request)
        
        # Check if there is an error
        if 'error' in result:
            # Use Django messages framework to display the error on the frontend
            messages.error(request, result['error'])

            # Return the form with existing data to repopulate the form fields
            return render(request, 'time_buckets/create_time_bucket.html', {
                'name': request.POST.get('name'),
                'frequencies': request.POST.getlist('frequency[]'),
                'multipliers': request.POST.getlist('multiplier[]'),
                'start_dates': request.POST.getlist('start_date[]'),
                'end_dates': request.POST.getlist('end_date[]')
            })

        # If no error, assume success and redirect using the PRG pattern
        if 'success' in result:
            messages.success(request, "Time bucket saved successfully!")
            return redirect('time_bucket_list')  # Redirect to a success page or list

    # If it's not a POST request, render the form
    return render(request, 'time_buckets/create_time_bucket.html')  # Redirect to the time buckets list page


# View for Listing Time Buckets
def time_buckets_list(request):
    time_buckets = TimeBucketDefinition.objects.all().order_by('-created_at')  # Fetching all time buckets sorted by newest first
    return render(request, 'time_buckets/time_bucket_list.html', {'time_buckets': time_buckets})


# View for Editing a Time Bucket
def edit_time_bucket(request, id):
    try:
        # Get the time bucket definition to edit
        time_bucket = TimeBucketDefinition.objects.get(id=id)

        if request.method == 'POST':
            # Call the utility function to update the time bucket
            result = update_time_bucket_from_form_data(request, time_bucket)

            if 'error' in result:
                return render(request, 'time_buckets/edit_time_bucket.html', {
                    'error': result['error'],
                    'name': time_bucket.name,
                    'frequencies': [entry.frequency for entry in time_bucket.buckets.all()],
                    'multipliers': [entry.multiplier for entry in time_bucket.buckets.all()],
                    'start_dates': [entry.start_date for entry in time_bucket.buckets.all()],
                    'end_dates': [entry.end_date for entry in time_bucket.buckets.all()],
                })

            # If successful, display the success message and redirect
            messages.success(request, "Time bucket updated successfully!")
            return redirect('time_bucket_list')  # Redirect back to the time buckets list

        # If GET request, prepopulate the form with the current data
        return render(request, 'time_buckets/edit_time_bucket.html', {
            'name': time_bucket.name,
            'frequencies': [entry.frequency for entry in time_bucket.buckets.all()],
            'multipliers': [entry.multiplier for entry in time_bucket.buckets.all()],
            'start_dates': [entry.start_date for entry in time_bucket.buckets.all()],
            'end_dates': [entry.end_date for entry in time_bucket.buckets.all()],
        })

    except TimeBucketDefinition.DoesNotExist:
        messages.error(request, "Time bucket not found.")
        return redirect('time_bucket_list')


# View for Deleting a Time Bucket
def delete_time_bucket(request, id):
    if request.method == 'POST':
        result = delete_time_bucket_by_id(id)

        if 'error' in result:
            messages.error(request, result['error'])
        else:
            messages.success(request, "Time bucket deleted successfully!")

        return redirect('time_bucket_list')
    

def view_time_bucket(request, id):
    # Retrieve the specific Time Bucket Definition
    time_bucket = get_object_or_404(TimeBucketDefinition, id=id)

    # Pass the time bucket and its entries to the template
    return render(request, 'time_buckets/view_time_bucket.html', {
        'time_bucket': time_bucket,
        'buckets': time_bucket.buckets.all().order_by('serial_number')
    })

    






































    


# View to project cash flows based on the fic_mis_date parameter
def project_cash_flows_view(request):
    process_name='contractual'
    fic_mis_date = '2024-08-31'
    status= aggregate_by_prod_code(fic_mis_date, process_name)
    status=populate_liquidity_gap_results_base(fic_mis_date, process_name)
    #status= calculate_time_buckets_and_spread(process_name, fic_mis_date)
    #status= aggregate_cashflows_to_product_level(fic_mis_date)
    print(status)
    #project_cash_flows(fic_mis_date)       
    return render(request, 'ALM_APP/project_cash_flows.html')






