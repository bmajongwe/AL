# Generated by Django 4.1 on 2024-09-20 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ALM_APP', '0009_timebucketdefinition_alter_timebuckets_start_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timebuckets',
            name='definition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ALM_APP.timebucketdefinition'),
        ),
    ]