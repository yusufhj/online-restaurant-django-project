# Generated by Django 5.1.3 on 2024-12-09 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_merge_20241209_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=160),
        ),
    ]
