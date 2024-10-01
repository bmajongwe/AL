from django.db.models import Sum
from ..models import Aggregated_Prod_Cashflow_Base, TimeBucketMaster, Dim_Product, LiquidityGapResultsBase

def populate_liquidity_gap_results_base(fic_mis_date, process_name):
    """
    This function fetches the aggregated data from Aggregated_Prod_Cashflow_Base,
    determines inflows and outflows based on n_total_cash_flow_amount,
    and stores the results in the LiquidityGapResultBase table.
    """

    try:
        # Step 1: Delete any existing records in LiquidityGapResultBase for the same fic_mis_date and process_name
        LiquidityGapResultsBase.objects.filter(fic_mis_date=fic_mis_date, process_name=process_name).delete()
        print(f"Deleted existing records for fic_mis_date: {fic_mis_date} and process_name: {process_name}")
    except Exception as e:
        print(f"Error deleting existing records: {e}")

    try:
        # Step 2: Fetch the product account types from Dim_Product
        product_data = Dim_Product.objects.values('v_prod_code', 'v_prod_name', 'n_account_type')
        product_lookup = {prod['v_prod_code']: prod for prod in product_data}  # Create a dictionary for faster lookup
        print(f"Fetched product data from Dim_Product: {len(product_lookup)} products")
    except Exception as e:
        print(f"Error fetching product data from Dim_Product: {e}")
        return

    try:
        # Step 3: Fetch all cash flow data from Aggregated_Prod_Cashflow_Base for the given fic_mis_date and process_name
        cashflows = Aggregated_Prod_Cashflow_Base.objects.filter(fic_mis_date=fic_mis_date, process_name=process_name)
        if not cashflows.exists():
            print(f"No cashflows found for fic_mis_date: {fic_mis_date} and process_name: {process_name}")
            return
        print(f"Fetched cashflow data from Aggregated_Prod_Cashflow_Base for fic_mis_date: {fic_mis_date}")
    except Exception as e:
        print(f"Error fetching cashflow data: {e}")
        return

    try:
        # Step 4: Fetch the bucket date ranges from TimeBucketMaster
        time_buckets = TimeBucketMaster.objects.filter(process_name=process_name).order_by('bucket_number')
        if not time_buckets.exists():
            print(f"No time buckets found for process: {process_name}")
            return
        print(f"Fetched time buckets for process: {process_name}")
    except Exception as e:
        print(f"Error fetching time bucket data: {e}")
        return

    # Step 5: Group the cashflows by product code and sum the n_total_cash_flow_amount values for each product
    grouped_cashflows = cashflows.values('v_prod_code', 'v_ccy_code').annotate(
        bucket_1=Sum('bucket_1'),
        bucket_2=Sum('bucket_2'),
        bucket_3=Sum('bucket_3'),
        bucket_4=Sum('bucket_4'),
        bucket_5=Sum('bucket_5'),
        bucket_6=Sum('bucket_6'),
        bucket_7=Sum('bucket_7'),
        bucket_8=Sum('bucket_8'),
        bucket_9=Sum('bucket_9'),
        bucket_10=Sum('bucket_10'),
        bucket_11=Sum('bucket_11'),
        bucket_12=Sum('bucket_12'),
        bucket_13=Sum('bucket_13'),
        bucket_14=Sum('bucket_14'),
        bucket_15=Sum('bucket_15'),
        bucket_16=Sum('bucket_16'),
        bucket_17=Sum('bucket_17'),
        bucket_18=Sum('bucket_18'),
        bucket_19=Sum('bucket_19'),
        bucket_20=Sum('bucket_20'),
        bucket_21=Sum('bucket_21'),
        bucket_22=Sum('bucket_22'),
        bucket_23=Sum('bucket_23'),
        bucket_24=Sum('bucket_24'),
        bucket_25=Sum('bucket_25'),
        bucket_26=Sum('bucket_26'),
        bucket_27=Sum('bucket_27'),
        bucket_28=Sum('bucket_28'),
        bucket_29=Sum('bucket_29'),
        bucket_30=Sum('bucket_30'),
        bucket_31=Sum('bucket_31'),
        bucket_32=Sum('bucket_32'),
        bucket_33=Sum('bucket_33'),
        bucket_34=Sum('bucket_34'),
        bucket_35=Sum('bucket_35'),
        bucket_36=Sum('bucket_36'),
        bucket_37=Sum('bucket_37'),
        bucket_38=Sum('bucket_38'),
        bucket_39=Sum('bucket_39'),
        bucket_40=Sum('bucket_40'),
        bucket_41=Sum('bucket_41'),
        bucket_42=Sum('bucket_42'),
        bucket_43=Sum('bucket_43'),
        bucket_44=Sum('bucket_44'),
        bucket_45=Sum('bucket_45'),
        bucket_46=Sum('bucket_46'),
        bucket_47=Sum('bucket_47'),
        bucket_48=Sum('bucket_48'),
        bucket_49=Sum('bucket_49'),
        bucket_50=Sum('bucket_50')
    )

    # Step 6: Iterate over each grouped cashflow and insert the result into LiquidityGapResultBase
    for grouped_cashflow in grouped_cashflows:
        try:
            product_code = grouped_cashflow['v_prod_code']
            currency_code = grouped_cashflow['v_ccy_code']

            # Fetch product details from the lookup dictionary
            product_info = product_lookup.get(product_code)
            if not product_info:
                raise ValueError(f"Error: No product info found for product code: {product_code}. Stopping process.")
            
            account_type = product_info['n_account_type']  # Use this to classify inflow/outflow
            product_name = product_info['v_prod_name']

            # Step 7: Iterate over the available time buckets (limited to the number defined in TimeBucketMaster)
            cumulative_gap = 0  # Initialize cumulative gap

            for idx, bucket in enumerate(time_buckets):
                # Use getattr to access bucket fields in the grouped cashflow dictionary
                inflows = grouped_cashflow[f'bucket_{idx+1}'] if account_type == 1 else 0
                outflows = grouped_cashflow[f'bucket_{idx+1}'] if account_type == 2 else 0
                net_liquidity_gap = inflows - outflows
                cumulative_gap += net_liquidity_gap  # Update cumulative gap

                try:
                    # Insert only up to the defined number of time buckets
                    LiquidityGapResultsBase.objects.create(
                        fic_mis_date=fic_mis_date,
                        process_name=process_name,
                        account_type='Inflow' if account_type == 1 else 'Outflow',
                        product_name=product_name,
                        v_prod_code=product_code,
                        v_ccy_code=currency_code,
                        bucket_start_date=bucket.start_date,
                        bucket_end_date=bucket.end_date,
                        inflows=inflows,
                        outflows=outflows,
                        net_liquidity_gap=net_liquidity_gap,
                        cumulative_gap=cumulative_gap
                    )
                    print(f"Inserted result for product {product_code}, bucket {idx+1}")
                except Exception as e:
                    print(f"Error inserting liquidity gap result for product {product_code}, bucket {idx+1}: {e}")

        except ValueError as ve:
            print(ve)
            # Stop the entire function since we encountered a missing product
            return

        except Exception as e:
            print(f"Error processing product {product_code}: {e}")

    print(f"Liquidity Gap Results populated for fic_mis_date {fic_mis_date} and process {process_name}")
