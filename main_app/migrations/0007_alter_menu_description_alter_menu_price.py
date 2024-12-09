# Generated by Django 5.1.3 on 2024-12-09 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_alter_menu_restaurant_alter_order_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='description',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='menu',
            name='price',
            field=models.DecimalField(decimal_places=3, max_digits=5),
        ),
    ]