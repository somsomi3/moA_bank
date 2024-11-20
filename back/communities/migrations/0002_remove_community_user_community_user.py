# Generated by Django 4.2.16 on 2024-11-20 01:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='community',
            name='user',
        ),
        migrations.AddField(
            model_name='community',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='communities', to=settings.AUTH_USER_MODEL),
        ),
    ]
