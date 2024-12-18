# Generated by Django 4.2.16 on 2024-11-21 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0006_alter_community_user'),
        ('accounts', '0005_user_communities_alter_user_community'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='community',
        ),
        migrations.AlterField(
            model_name='user',
            name='communities',
            field=models.ManyToManyField(blank=True, related_name='members', to='communities.community'),
        ),
    ]
