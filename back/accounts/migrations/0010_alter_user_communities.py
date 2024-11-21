# Generated by Django 4.2.16 on 2024-11-21 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0009_alter_community_user'),
        ('accounts', '0009_user_communities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='communities',
            field=models.ManyToManyField(blank=True, related_name='members', to='communities.community'),
        ),
    ]