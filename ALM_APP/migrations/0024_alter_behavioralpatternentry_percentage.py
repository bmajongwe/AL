# Generated by Django 4.1 on 2024-10-04 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ALM_APP', '0023_alter_behavioralpatternentry_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='behavioralpatternentry',
            name='percentage',
            field=models.DecimalField(decimal_places=3, max_digits=6),
        ),
    ]
