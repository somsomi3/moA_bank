# Generated by Django 4.2.16 on 2024-11-21 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0010_alter_community_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='community',
            name='user',
        ),
    ]
