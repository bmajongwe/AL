import os
import pandas as pd
import csv
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import FileUploadForm
from datetime import datetime
from django.http import HttpResponse
from .Functions.cashflow import *
from .Functions.aggregate_cashflows import *
from .Functions.product_level_cashflows import *
from .forms import TimeBucketsForm
from .models import TimeBuckets
from .models import FSI_Expected_Cashflow

from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .models import TimeBuckets, TimeBucketDefinition,product_level_cashflows



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
                return render(request, 'define_time_buckets.html', {'error': f"Error inserting time bucket for serial number {serial_number}: {e}"})

        print("All time buckets successfully created!")
        return redirect('ALM_APP/time_buckets_list')

    # If it's not a POST request, render the form
    return render(request, 'ALM_APP/define_time_buckets.html')








# View to project cash flows based on the fic_mis_date parameter
def project_cash_flows_view(request):
    process_name='contractual'
    fic_mis_date = '2024-08-31'
    status= calculate_time_buckets_and_spread(process_name, fic_mis_date)
    #status= aggregate_cashflows_to_product_level(fic_mis_date)
    print(status)
    #project_cash_flows(fic_mis_date)       
    return render(request, 'ALM_APP/project_cash_flows.html')






