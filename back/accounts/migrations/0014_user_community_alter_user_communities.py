# Generated by Django 4.2.16 on 2024-11-21 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0010_alter_community_user'),
        ('accounts', '0013_alter_user_communities'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='community',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_foreignkey', to='communities.community'),
        ),
        migrations.AlterField(
            model_name='user',
            name='communities',
            field=models.ManyToManyField(blank=True, related_name='members', to='communities.community'),
        ),
    ]
