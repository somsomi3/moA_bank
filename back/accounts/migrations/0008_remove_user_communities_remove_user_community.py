# Generated by Django 4.2.16 on 2024-11-21 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_user_community'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='communities',
        ),
        migrations.RemoveField(
            model_name='user',
            name='community',
        ),
    ]