# forms.py
from django import forms
from .models import TimeBuckets

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
