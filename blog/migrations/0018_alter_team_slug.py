# Generated by Django 5.1.7 on 2025-04-09 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_rename_sports_sport_rename_teams_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='slug',
            field=models.SlugField(blank=True, default=''),
        ),
    ]
