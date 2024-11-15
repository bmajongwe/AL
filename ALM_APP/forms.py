# forms.py
from django import forms
from .models import *

class TimeBucketsForm(forms.ModelForm):
    class Meta:
        model = TimeBuckets
        fields = ['serial_number', 'frequency', 'multiplier']




class FileUploadForm(forms.Form):
    file = forms.FileField(label='Select a file')
    table = forms.ChoiceField(choices=[
        ('Ldn_Product_Master', 'Ldn Product Master'),
        # ('Ldn_Financial_Assets_Instrument', 'Ldn Financial Assets Instrument'),
        ('Ldn_Common_Coa_Master', 'Ldn Common Coa Master'),
        ('NewFinancialTable', 'NewFinancialTable'),  # Add the new table here

    ])





class ProductFilterForm(forms.ModelForm):
    field_name = forms.ChoiceField(choices=[])

    class Meta:
        model = ProductFilter
        fields = ['field_name', 'condition', 'value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get field names dynamically from the Product Master model
        product_master_fields = [(field.name, field.verbose_name) for field in Ldn_Product_Master._meta.fields]
        self.fields['field_name'].choices = product_master_fields

class ProcessForm(forms.ModelForm):
    filters = forms.ModelMultipleChoiceField(
        queryset=ProductFilter.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )



    class Meta:
        model = Process
        fields = ['name', 'filters']



# forms.py
from django import forms
from .models import LiquidityGapResultsBase

class LiquidityGapReportFilterForm(forms.Form):
    process_name = forms.ChoiceField(
        required=False,
        choices=[('', '--- Select Process ---')] + [(p, p) for p in LiquidityGapResultsBase.objects.values_list('process_name', flat=True).distinct()],
        label="Process"
    )
    fic_mis_date = forms.ChoiceField(
        choices=[('', '-- Select Date --')] + [
            (choice, choice) for choice in LiquidityGapResultsBase.objects.values_list('fic_mis_date', flat=True).distinct().order_by('fic_mis_date')
        ],
        required=False,
        label="As of Date"
    )
    v_ccy_code = forms.ChoiceField(
        required=False,
        choices=[('', '--- Select Currency ---')] + [(c, c) for c in LiquidityGapResultsBase.objects.values_list('v_ccy_code', flat=True).distinct()],
        label="Currency"
    )
    account_type = forms.ChoiceField(
        required=False,
        choices=[('', '--- Select Result Type ---'), ('Inflow', 'Inflow'), ('Outflow', 'Outflow')],
        label="Result Type"
    )
    bucket_number = forms.ChoiceField(
        choices=[('', '-- Select Bucket Number --')] + [
            (choice, choice) for choice in LiquidityGapResultsBase.objects.values_list('bucket_number', flat=True).distinct().order_by('bucket_end_date')
        ],
        required=False,
        label="Bucket End Date"
    )
