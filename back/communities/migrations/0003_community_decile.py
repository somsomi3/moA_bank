# Generated by Django 4.2.16 on 2024-11-21 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0002_remove_community_user_community_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='decile',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]