# Generated by Django 4.1 on 2024-09-19 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ALM_APP', '0006_alter_product_level_cashflows_v_account_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeBuckets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.IntegerField()),
                ('frequency', models.IntegerField()),
                ('multiplier', models.CharField(choices=[('Days', 'Days'), ('Months', 'Months'), ('Years', 'Years')], max_length=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'db_table': 'time_buckets',
            },
        ),
    ]