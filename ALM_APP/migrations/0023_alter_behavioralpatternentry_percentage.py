# Generated by Django 4.1 on 2024-10-04 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ALM_APP', '0022_alter_behavioralpatternconfig_v_prod_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='behavioralpatternentry',
            name='percentage',
            field=models.DecimalField(decimal_places=3, max_digits=5),
        ),
    ]
