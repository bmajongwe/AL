from concurrent.futures import ThreadPoolExecutor
from django.db import transaction
from datetime import timedelta, datetime, date
from ..models import *

# Helper function to parse date safely
def safe_parse_date(date_value):
    if isinstance(date_value, str):
        return datetime.strptime(date_value, '%m/%d/%Y').date()
    return date_value

# Function to get the payment interval based on the repayment type and day count convention
def get_payment_interval(repayment_type, day_count_ind):
    """Determine the payment interval in days based on repayment type and day count convention."""
    if day_count_ind == '30/360' or day_count_ind == '30/365':
        intervals = {'D': 1, 'W': 7, 'M': 30, 'Q': 90, 'H': 180, 'Y': 360}
    elif day_count_ind == 'ACT/360' or day_count_ind == 'ACT/365' or day_count_ind == 'ACT/ACT':
        intervals = {'D': 1, 'W': 7, 'M': 30, 'Q': 91, 'H': 182, 'Y': 365}
    else:
        intervals = {'M': 30}  # Default to monthly if unknown

    return timedelta(days=intervals.get(repayment_type, 30))  # Default monthly

# Main cash flow calculation logic
def calculate_cash_flows_for_loan(loan):
    with transaction.atomic():
        balance = float(loan.n_eop_bal) if loan.n_eop_bal else 0.0
        starting_balance = balance
        current_date = loan.d_next_payment_date
        interest_rate = float(loan.n_curr_interest_rate) if loan.n_curr_interest_rate else 0.0
        repayment_type = loan.v_repayment_type
        day_count_ind = loan.v_day_count_ind
        cashflow_bucket = 1

        # Get the interest method, default to Simple
        interest_method = Fsi_Interest_Method.objects.first()
        if not interest_method:
            interest_method = Fsi_Interest_Method.objects.create(v_interest_method='Simple')

        # Calculate payment interval
        payment_interval = get_payment_interval(repayment_type, day_count_ind)

        # Calculate total periods
        periods = ((loan.d_maturity_date - current_date).days // payment_interval.days) + 1
        fixed_principal_payment = balance / periods if periods > 0 else 0

        while current_date <= loan.d_maturity_date:
            # Calculate interest based on current balance and interest rate
            day_count_factor = 365 if day_count_ind == 'ACT/365' else 360
            interest_payment = 0

            if interest_method.v_interest_method == 'Simple':
                interest_payment = balance * interest_rate * (payment_interval.days / day_count_factor)
            elif interest_method.v_interest_method == 'Compound':
                interest_payment = balance * ((1 + interest_rate / (day_count_factor / payment_interval.days)) ** periods - 1)
            elif interest_method.v_interest_method == 'Amortized':
                interest_rate_per_period = interest_rate / (day_count_factor / payment_interval.days)
                total_payment = balance * (interest_rate_per_period / (1 - (1 + interest_rate_per_period) ** -periods))
                interest_payment = balance * interest_rate_per_period
                principal_payment = total_payment - interest_payment
            elif interest_method.v_interest_method == 'Floating':
                variable_rate = loan.n_curr_interest_rate + loan.n_variable_rate_margin
                interest_payment = balance * variable_rate * (payment_interval.days / day_count_factor)

            # Principal payment logic based on repayment type
            if repayment_type == 'amortized':
                principal_payment = fixed_principal_payment
            elif repayment_type == 'bullet':
                principal_payment = 0 if current_date < loan.d_maturity_date else balance
            else:
                principal_payment = 0  # Default behavior for unknown types

            # Total payment (Principal + Interest)
            total_payment = principal_payment + interest_payment

            # Create cashflow record for this period
            FSI_Expected_Cashflow.objects.create(
                fic_mis_date=loan.fic_mis_date,
                v_account_number=loan.v_account_number,
                n_cash_flow_bucket=cashflow_bucket,
                d_cash_flow_date=current_date,
                n_principal_payment=principal_payment,
                n_interest_payment=interest_payment,
                n_cash_flow_amount=total_payment,
                n_balance=balance - principal_payment,
                V_CCY_CODE=loan.v_ccy_code,
            )

            # Update balance and move to the next period
            balance -= principal_payment
            current_date += payment_interval
            cashflow_bucket += 1
            periods -= 1

# Function to project cash flows for a particular fic_mis_date
def project_cash_flows(fic_mis_date):
    # Delete existing cash flows for this date
    FSI_Expected_Cashflow.objects.filter(fic_mis_date=fic_mis_date).delete()

    # Retrieve loans for the given fic_mis_date
    loans = NewFinancialTable.objects.filter(fic_mis_date=fic_mis_date)
    num_threads = min(30, len(loans))  # Adjust the number of threads if necessary

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(calculate_cash_flows_for_loan, loan) for loan in loans]
        for future in futures:
            future.result()  # Ensure all threads complete successfully
