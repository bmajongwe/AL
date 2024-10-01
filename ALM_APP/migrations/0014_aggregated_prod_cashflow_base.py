# Generated by Django 4.1 on 2024-09-26 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ALM_APP', '0013_aggregatedcashflowbybuckets'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aggregated_Prod_Cashflow_Base',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fic_mis_date', models.DateField()),
                ('process_name', models.CharField(max_length=100)),
                ('v_prod_code', models.CharField(max_length=50)),
                ('v_ccy_code', models.CharField(max_length=10)),
                ('financial_element', models.CharField(max_length=50)),
                ('bucket_1', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_2', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_3', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_4', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_5', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_6', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_7', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_8', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_9', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_10', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_11', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_12', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_13', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_14', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_15', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_16', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_17', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_18', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_19', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_20', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_21', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_22', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_23', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_24', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_25', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_26', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_27', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_28', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_29', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_30', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_31', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_32', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_33', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_34', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_35', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_36', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_37', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_38', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_39', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_40', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_41', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_42', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_43', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_44', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_45', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_46', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_47', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_48', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_49', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('bucket_50', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
            ],
            options={
                'unique_together': {('fic_mis_date', 'process_name', 'financial_element')},
            },
        ),
    ]
