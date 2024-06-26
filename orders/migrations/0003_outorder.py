# Generated by Django 5.0.2 on 2024-03-28 22:54

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0016_productinout_discount_productinout_total_price"),
        ("orders", "0002_rename_inorders_inorder"),
    ]

    operations = [
        migrations.CreateModel(
            name="OutOrder",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("order_id", models.IntegerField(db_index=True, unique=True)),
                ("buyer", models.CharField(max_length=255)),
                ("delivery_address", models.TextField()),
                ("location", models.TextField(max_length=255)),
                (
                    "units",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "unit_price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        verbose_name="Unit Price",
                    ),
                ),
                (
                    "total_price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        null=True,
                        verbose_name="total Price",
                    ),
                ),
                (
                    "discount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        null=True,
                        verbose_name="Discount in Taka",
                    ),
                ),
                (
                    "order_initiated_on",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Order Initiated On"
                    ),
                ),
                (
                    "tentative_delivery_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Requested Delivery Date"
                    ),
                ),
                (
                    "payment_status",
                    models.IntegerField(
                        choices=[(1, "Paid"), (2, "Unpaid"), (3, "Partial Payment")],
                        default=2,
                        verbose_name="Payment Status",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.product",
                    ),
                ),
                (
                    "warehouse",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.warehouse",
                    ),
                ),
            ],
        ),
    ]
