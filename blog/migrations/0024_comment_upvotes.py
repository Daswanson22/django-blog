# Generated by Django 5.1.7 on 2025-04-23 21:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_team_stadium_alt'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='upvotes',
            field=models.ManyToManyField(blank=True, related_name='comment_upvotes', to=settings.AUTH_USER_MODEL),
        ),
    ]
