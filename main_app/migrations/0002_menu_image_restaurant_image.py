# Generated by Django 5.1.3 on 2024-12-08 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='image',
            field=models.ImageField(blank=True, default=None, upload_to='menu_images'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(blank=True, default=None, upload_to='restaurant_images'),
        ),
    ]
