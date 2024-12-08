# Generated by Django 5.1.3 on 2024-12-08 08:41

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('category', models.CharField(choices=[('A', 'Appetizer'), ('E', 'Entree'), ('M', 'Main'), ('S', 'Side'), ('D', 'Dessert'), ('B', 'Beverage'), ('O', 'Other')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'Pending'), ('C', 'Completed'), ('D', 'Delivered'), ('N', 'Not Paid')], max_length=1)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=3, max_digits=7)),
                ('items', models.ManyToManyField(blank=True, default=None, to='main_app.menu')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('categories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('A', 'Appetizer'), ('E', 'Entree'), ('M', 'Main'), ('S', 'Side'), ('D', 'Dessert'), ('B', 'Beverage'), ('O', 'Other')], max_length=1), size=None)),
                ('orders_history', models.ManyToManyField(blank=True, default=None, to='main_app.order')),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.restaurant'),
        ),
    ]