# Generated by Django 4.1 on 2024-10-25 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ALM_APP', '0035_product_level_cashflows_v_cash_flow_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='dim_product',
            name='v_account_type',
            field=models.CharField(max_length=20, null=True),
        ),
    ]