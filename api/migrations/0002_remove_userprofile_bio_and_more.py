# Generated by Django 4.2.4 on 2023-08-27 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='bio',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='preferred_language',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='skill_level',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
