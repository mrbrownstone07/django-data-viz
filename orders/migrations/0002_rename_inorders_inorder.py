# Generated by Django 5.0.2 on 2024-03-28 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0016_productinout_discount_productinout_total_price"),
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="InOrders",
            new_name="InOrder",
        ),
    ]
