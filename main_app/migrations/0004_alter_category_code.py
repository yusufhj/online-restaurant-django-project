# Generated by Django 5.1.3 on 2024-12-09 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_category_name_alter_category_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='code',
            field=models.CharField(max_length=2, unique=True),
        ),
    ]
