# Generated by Django 5.1.3 on 2024-12-04 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ALM_APP', '0047_tablemetadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='liquiditygapresultsbase',
            name='v_product_splits',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='liquiditygapresultscons',
            name='v_product_splits',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]