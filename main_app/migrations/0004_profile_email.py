# Generated by Django 5.1.3 on 2024-12-08 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_remove_profile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default=1, max_length=320),
            preserve_default=False,
        ),
    ]
