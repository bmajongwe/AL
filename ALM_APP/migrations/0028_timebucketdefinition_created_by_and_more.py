# Generated by Django 4.1 on 2024-10-07 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ALM_APP', '0027_behavioralpatternconfig_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='timebucketdefinition',
            name='created_by',
            field=models.CharField(default='System', max_length=100),
        ),
        migrations.AddField(
            model_name='timebucketdefinition',
            name='last_changed_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='timebucketdefinition',
            name='last_changed_by',
            field=models.CharField(default='System', max_length=100),
        ),
        migrations.AlterField(
            model_name='timebuckets',
            name='definition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buckets', to='ALM_APP.timebucketdefinition'),
        ),
    ]
