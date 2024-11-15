from datetime import datetime
from dateutil.relativedelta import relativedelta
from ..models import TimeBucketMaster, Dim_Dates
import calendar

def populate_dim_dates_from_time_buckets(fic_mis_date):
    """
    Populate the Dim_Dates table with bucket number, start date, and end date from TimeBucketMaster table.
    Also calculate the calendar-related fields, and manage f_latest_record_indicator.
    """
    if isinstance(fic_mis_date, str):
        fic_mis_date = datetime.strptime(fic_mis_date, "%Y-%m-%d").date()

    # Determine the previous month's fic_mis_date
    previous_fic_mis_date = (fic_mis_date - relativedelta(months=1))

    # Update f_latest_record_indicator to 'N' for the previous month's records
    Dim_Dates.objects.filter(fic_mis_date=previous_fic_mis_date).update(f_latest_record_indicator='N')

    # Fetch all time buckets ordered by bucket number
    time_buckets = TimeBucketMaster.objects.all().order_by('bucket_number')

    if not time_buckets.exists():
        print("No time buckets found.")
        return

    # Clear existing Dim_Dates records for the current fic_mis_date
    Dim_Dates.objects.filter(fic_mis_date=fic_mis_date).delete()

    for time_bucket in time_buckets:
        # Extract bucket start and end dates directly from TimeBucketMaster
        bucket_start_date = time_bucket.start_date
        bucket_end_date = time_bucket.end_date

        # Set n_date_skey to match fic_mis_date (as an integer YYYYMMDD)
        n_date_skey = int(fic_mis_date.strftime("%Y%m%d"))

        # Add calendar-related fields based on the bucket start date
        d_calendar_date = bucket_start_date
        n_day_of_week = bucket_start_date.weekday() + 1  # Monday is 1, Sunday is 7
        n_day_of_month = bucket_start_date.day
        n_day_of_year = (bucket_start_date - datetime(bucket_start_date.year, 1, 1).date()).days + 1
        v_day_name = calendar.day_name[bucket_start_date.weekday()]
        n_month_calendar = bucket_start_date.month
        n_year_calendar = bucket_start_date.year
        n_half_calendar = 1 if n_month_calendar <= 6 else 2
        n_qtr_calendar = (n_month_calendar - 1) // 3 + 1
        n_week_calendar = (bucket_start_date - datetime(bucket_start_date.year, 1, 1).date()).days // 7 + 1
        v_month_period_name = f"{calendar.month_name[n_month_calendar]} {n_year_calendar}"
        v_qtr_period_name = f"Q{n_qtr_calendar} {n_year_calendar}"
        v_week_period_name = f"Week {n_week_calendar} {n_year_calendar}"
        v_year_period_name = str(n_year_calendar)

        # Insert or update the Dim_Dates record
        Dim_Dates.objects.update_or_create(
            fic_mis_date=fic_mis_date,
            bucket_number=time_bucket.bucket_number,
            defaults={
                'n_date_skey': n_date_skey,
                'd_calendar_date': d_calendar_date,  # Updated to use bucket_start_date
                'bucket_start_date': bucket_start_date,
                'bucket_end_date': bucket_end_date,
                'n_day_of_week': n_day_of_week,
                'n_day_of_month': n_day_of_month,
                'n_day_of_year': n_day_of_year,
                'v_day_name': v_day_name,
                'n_month_calendar': n_month_calendar,
                'n_half_calendar': n_half_calendar,
                'n_qtr_calendar': n_qtr_calendar,
                'n_week_calendar': n_week_calendar,
                'n_year_calendar': n_year_calendar,
                'v_month_period_name': v_month_period_name,
                'v_qtr_period_name': v_qtr_period_name,
                'v_week_period_name': v_week_period_name,
                'v_year_period_name': v_year_period_name,
                'f_latest_record_indicator': 'Y',  # Current run is the latest
            }
        )

    print(f"Successfully populated Dim_Dates for fic_mis_date {fic_mis_date}.")
