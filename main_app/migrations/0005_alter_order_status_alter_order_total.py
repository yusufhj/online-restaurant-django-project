# Generated by Django 5.1.3 on 2024-12-09 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_category_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('C', 'Completed'), ('D', 'Delivered'), ('N', 'Not Paid')], default='P', max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
    ]