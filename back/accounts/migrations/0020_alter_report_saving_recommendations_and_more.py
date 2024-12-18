# Generated by Django 4.2.16 on 2024-11-24 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='saving_recommendations',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='report',
            name='tax_refund_estimation',
            field=models.JSONField(default=1),
            preserve_default=False,
        ),
    ]
