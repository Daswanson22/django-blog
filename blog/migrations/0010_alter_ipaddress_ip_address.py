# Generated by Django 5.1.7 on 2025-04-06 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_ipaddress_remove_post_views_post_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipaddress',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
