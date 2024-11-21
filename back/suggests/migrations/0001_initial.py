# Generated by Django 4.2.16 on 2024-11-20 22:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_name', models.CharField(max_length=100)),
                ('merit_summary', models.TextField()),
                ('base_performance', models.FloatField()),
                ('annual_fee', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Decile_consume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker', models.FloatField()),
                ('per_range', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Decile_income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker', models.FloatField()),
                ('per_range', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='DepositProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_nm', models.CharField(max_length=100)),
                ('kor_co_nm', models.CharField(max_length=50)),
                ('intr_rate2', models.FloatField()),
                ('save_trm', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Incomepergenderage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=10)),
                ('agerange', models.CharField(max_length=20)),
                ('avgallincome', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Incomepergrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(max_length=50)),
                ('avgincome', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Incomeperjob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job', models.CharField(max_length=50)),
                ('avgincome', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SavingProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_nm', models.CharField(max_length=100)),
                ('kor_co_nm', models.CharField(max_length=50)),
                ('intr_rate2', models.FloatField()),
                ('save_trm', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='IncomeSpend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income', models.FloatField()),
                ('consume', models.FloatField()),
                ('gender', models.CharField(max_length=10)),
                ('age', models.IntegerField()),
                ('job', models.CharField(max_length=50)),
                ('grade', models.CharField(max_length=50)),
                ('use_bank', models.CharField(max_length=50)),
                ('save_trm', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]