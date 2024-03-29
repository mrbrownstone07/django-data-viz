# Generated by Django 5.0.2 on 2024-02-20 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_alter_productinout_units_alter_stock_units'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinout',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Unit Price'),
        ),
    ]
