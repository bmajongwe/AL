# Generated by Django 5.1.3 on 2024-11-22 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ALM_APP', '0045_liquiditygapresultscons'),
    ]

    operations = [
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('function_name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'dim_function',
            },
        ),
        migrations.CreateModel(
            name='Process_Rn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_name', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'dim_process',
            },
        ),
        migrations.CreateModel(
            name='RunProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('function', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ALM_APP.function')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='run_processes', to='ALM_APP.process_rn')),
            ],
            options={
                'db_table': 'dim_process_dtl',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='FunctionExecutionStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('execution_start_date', models.DateTimeField(auto_now_add=True)),
                ('execution_end_date', models.DateTimeField(blank=True, null=True)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('execution_order', models.PositiveIntegerField(null=True)),
                ('reporting_date', models.DateField(null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Ongoing', 'Ongoing'), ('Success', 'Success'), ('Failed', 'Failed')], default='Pending', max_length=20)),
                ('process_run_id', models.CharField(max_length=50)),
                ('run_count', models.PositiveIntegerField()),
                ('function', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ALM_APP.function')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ALM_APP.process_rn')),
            ],
            options={
                'db_table': 'dim_function_execution_status',
                'ordering': ['run_count', 'execution_start_date'],
                'constraints': [models.UniqueConstraint(fields=('execution_start_date', 'process_run_id', 'function'), name='unique_execution_process')],
            },
        ),
    ]