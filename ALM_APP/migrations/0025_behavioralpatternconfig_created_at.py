# Generated by Django 4.1 on 2024-10-04 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ALM_APP', '0024_alter_behavioralpatternentry_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='behavioralpatternconfig',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]