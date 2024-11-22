# Generated by Django 4.2.16 on 2024-11-21 06:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('communities', '0004_alter_community_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='users_manytomany', to=settings.AUTH_USER_MODEL),
        ),
    ]
