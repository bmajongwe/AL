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
def edit_behavioral_pattern(request, pattern_id):
    # Fetch the pattern config using the ID
    pattern_config = get_object_or_404(BehavioralPatternConfig, id=pattern_id)
    entries = pattern_config.entries.all()  # Assuming you use 'entries' as related_name in the BehavioralPatternEntry model

    if request.method == 'POST':
        # Update the pattern
        result = define_behavioral_pattern_from_form_data(request, pattern_config=pattern_config)

        if 'error' in result:
            return render(request, 'behavioral/create_behavioral_pattern.html', {
                'error': result['error'],
                'v_prod_type': pattern_config.v_prod_type,
                'description': pattern_config.description,
                'tenors': request.POST.getlist('tenor[]'),
                'multipliers': request.POST.getlist('multiplier[]'),
                'percentages': request.POST.getlist('percentage[]'),
                'is_edit': True,
                'pattern_id': pattern_id
            })

        # Redirect to the list page after successful update
        return redirect('behavioral_patterns_list')

    # Pre-populate the form with existing pattern data for GET requests
    tenors = [entry.tenor for entry in entries]
    multipliers = [entry.multiplier for entry in entries]
    percentages = [entry.percentage for entry in entries]

    return render(request, 'behavioral/create_behavioral_pattern.html', {
        'v_prod_type': pattern_config.v_prod_type,
        'description': pattern_config.description,
        'tenors': tenors,
        'multipliers': multipliers,
        'percentages': percentages,
        'is_edit': True,
        'pattern_id': pattern_id
    })


# View for Deleting Behavioral Pattern
def delete_behavioral_pattern(request, id):
    if request.method == 'POST':
        result = delete_behavioral_pattern_by_id(id)

        if 'error' in result:
            messages.error(request, result['error'])
        else:
            messages.success(request, "Behavioral pattern deleted successfully!")

        return redirect('behavioral_patterns_list')
    

    

def define_time_buckets(request):
    if request.method == 'POST':
        # Retrieve the name for the TimeBucketDefinition
        time_bucket_name = request.POST.get('time_bucket_name')  # Assuming you add this field in the form

        if not time_bucket_name:
            return render(request, 'ALM_APP/define_time_buckets.html', {'error': 'Please provide a name for the time bucket definition.'})

        # Create a new TimeBucketDefinition entry
        time_bucket_definition = TimeBucketDefinition.objects.create(name=time_bucket_name)

        # Retrieve data from the form submission
        serial_numbers = request.POST.getlist('serial_number[]')
        frequencies = request.POST.getlist('frequency[]')
        multipliers = request.POST.getlist('multiplier[]')
        start_date = request.POST.get('start_date')  # Start date entered manually

        # Debug prints
        print("Received data from form:")
        print(f"Serial Numbers: {serial_numbers}")
        print(f"Frequencies: {frequencies}")
        print(f"Multipliers: {multipliers}")
        print(f"Start Date: {start_date}")

        # If no start date is provided, default to the current date
        if not start_date:
            current_start_date = datetime.now().date()  # Use today's date as default start date
            print(f"No start date provided. Using current date as start date: {current_start_date}")
        else:
            try:
                # Convert the start date to a date object
                current_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                print(f"Starting from: {current_start_date}")
            except Exception as e:
                print(f"Error parsing start date: {e}")
                return render(request, 'ALM_APP/define_time_buckets.html', {'error': 'Invalid start date format.'})

        # Iterate over the submitted rows and create time buckets
        for i in range(len(serial_numbers)):
            serial_number = serial_numbers[i]
            frequency = int(frequencies[i])
            multiplier = multipliers[i]

            try:
                # Calculate end date based on the multiplier and frequency
                if multiplier == 'Days':
                    end_date = current_start_date + timedelta(days=frequency)
                elif multiplier == 'Months':
                    end_date = current_start_date + timedelta(days=frequency * 30)  # Approximate month as 30 days
                elif multiplier == 'Years':
                    end_date = current_start_date + timedelta(days=frequency * 365)

                print(f"Creating TimeBucket: Serial Number {serial_number}, Frequency {frequency}, Multiplier {multiplier}, Start Date {current_start_date}, End Date {end_date}")

                # Create and save the new TimeBucket linked to the TimeBucketDefinition
                TimeBuckets.objects.create(
                    serial_number=serial_number,
                    frequency=frequency,
                    multiplier=multiplier,
                    start_date=current_start_date,
                    end_date=end_date,
                    definition=time_bucket_definition  # Link to the TimeBucketDefinition
                )

                print(f"Successfully created TimeBucket {serial_number}")

                # Update the start date for the next bucket
                current_start_date = end_date + timedelta(days=1)  # The next bucket starts the day after the previous end

            except Exception as e:
                # Capture errors during bucket creation
                print(f"Error inserting time bucket for serial number {serial_number}: {e}")
                return render(request, 'ALM_APP/define_time_buckets.html', {'error': f"Error inserting time bucket for serial number {serial_number}: {e}"})

        print("All time buckets successfully created!")
        return redirect('ALM_APP/time_buckets_list')

   



# def liquidity_gap_results_view(request):
#    # Fetch all results from LiquidityGapResultsBase
#     # Fetch all results from LiquidityGapResultsBase
#     results = LiquidityGapResultsBase.objects.all()

#     # Group the results by product name
#     grouped_results = defaultdict(lambda: {'data': {}, 'account_type': None})

#     # Organize the results by product and date range
#     for result in results:
#         # Generate date_key in the view
#         date_key = f"{result.bucket_start_date}_{result.bucket_end_date}"
#         grouped_results[result.product_name]['data'][date_key] = {
#             'inflows': result.inflows if result.account_type == 'Inflow' else Decimal('0.00'),
#             'outflows': result.outflows if result.account_type == 'Outflow' else Decimal('0.00')
#         }
#         grouped_results[result.product_name]['account_type'] = result.account_type

#     # Get unique date ranges for the table headers
#     unique_date_ranges = sorted(set((result.bucket_start_date, result.bucket_end_date) for result in results))

#     # Prepare data for final rendering
#     inflows_total_per_date = [Decimal('0.00')] * len(unique_date_ranges)
#     outflows_total_per_date = [Decimal('0.00')] * len(unique_date_ranges)
#     net_liquidity_gap = []
#     net_gap_percent = []
#     cumulative_gap = []
#     cumulative_total = Decimal('0.00')

#     # Loop through date ranges and calculate totals for inflows, outflows, and gaps
#     for i, (start_date, end_date) in enumerate(unique_date_ranges):
#         inflows_total = Decimal('0.00')
#         outflows_total = Decimal('0.00')

#         date_key = f"{start_date}_{end_date}"

#         for product_name, product_data in grouped_results.items():
#             inflows_total += product_data['data'].get(date_key, {}).get('inflows', Decimal('0.00'))
#             outflows_total += product_data['data'].get(date_key, {}).get('outflows', Decimal('0.00'))

#         inflows_total_per_date[i] = inflows_total
#         outflows_total_per_date[i] = outflows_total

#         # Calculate Net Liquidity Gap
#         gap = inflows_total - outflows_total
#         net_liquidity_gap.append(gap)

#         # Calculate Net Gap as % of Total Outflows (avoid division by zero)
#         if outflows_total != Decimal('0.00'):
#             net_gap_percent.append((gap / outflows_total) * 100)
#         else:
#             net_gap_percent.append(Decimal('0.00'))

#         # Calculate Cumulative Gap
#         cumulative_total += gap
#         cumulative_gap.append(cumulative_total)

#     # Pass pre-processed data to the template
#     context = {
#         'products': grouped_results,
#         'unique_date_ranges': unique_date_ranges,
#         'inflows_total_per_date': inflows_total_per_date,
#         'outflows_total_per_date': outflows_total_per_date,
#         'net_liquidity_gap': net_liquidity_gap,
#         'net_gap_percent': net_gap_percent,
#         'cumulative_gap': cumulative_gap,
#     }

#     return render(request, 'ALM_APP/liquidity_gap_results.html', context)




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






