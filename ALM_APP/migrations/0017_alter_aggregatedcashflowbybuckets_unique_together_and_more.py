# Generated by Django 4.1 on 2024-10-03 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ALM_APP', '0016_liquiditygapresultsbase'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='aggregatedcashflowbybuckets',
            unique_together=set(),
        ),
        migrations.AlterModelTable(
            name='aggregatedcashflowbybuckets',
            table='ALM_APP_Aggregated_Cashflow_By_Buckets',
        ),
    ]
