# Generated by Django 4.1 on 2024-11-07 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ALM_APP', '0040_liquiditygapresultsbase_bucket_number'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='aggregated_prod_cashflow_base',
            unique_together=set(),
        ),
    ]