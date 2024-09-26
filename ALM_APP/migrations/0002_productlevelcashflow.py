# Generated by Django 4.1 on 2024-09-19 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ALM_APP', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductLevelCashflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fic_mis_date', models.DateField()),
                ('v_prod_code', models.CharField(max_length=50)),
                ('d_cashflow_date', models.DateField()),
                ('n_total_cash_flow_amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('n_total_principal_payment', models.DecimalField(decimal_places=2, max_digits=20)),
                ('n_total_interest_payment', models.DecimalField(decimal_places=2, max_digits=20)),
                ('n_total_balance', models.DecimalField(decimal_places=2, max_digits=20)),
                ('v_ccy_code', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'product_level_cashflows',
            },
        ),
    ]
