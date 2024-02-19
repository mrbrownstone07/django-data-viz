# Generated by Django 5.0.2 on 2024-02-19 17:19

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
        ('inventory', '0003_warehouse'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Item',
            new_name='Product',
        ),
        migrations.CreateModel(
            name='ProductInOut',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('inout', models.IntegerField(choices=[(1, 'In Order'), (2, 'Out Order')], default=1)),
                ('units', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_initiated_on', models.DateTimeField(auto_now_add=True)),
                ('order_completed_on', models.DateTimeField()),
                ('status', models.BooleanField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.product')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.warehouse')),
            ],
        ),
    ]
