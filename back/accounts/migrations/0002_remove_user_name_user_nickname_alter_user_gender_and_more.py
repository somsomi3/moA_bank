# Generated by Django 4.2.6 on 2024-11-20 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='grade',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='job',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='main_bank',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='region',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
