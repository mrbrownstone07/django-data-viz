# Generated by Django 5.0.2 on 2024-02-19 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_product_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productinout',
            old_name='inout',
            new_name='order_type',
        ),
    ]
