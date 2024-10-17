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
