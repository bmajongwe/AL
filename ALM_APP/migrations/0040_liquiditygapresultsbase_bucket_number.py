# Generated by Django 4.1 on 2024-11-05 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ALM_APP', '0039_rename_product_name_liquiditygapresultsbase_v_prod_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='liquiditygapresultsbase',
            name='bucket_number',
            field=models.IntegerField(default=1188),
            preserve_default=False,
        ),
    ]