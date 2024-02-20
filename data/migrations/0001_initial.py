# Generated by Django 4.1.7 on 2024-02-19 09:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0002_alter_category_id_alter_item_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketPriceData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.item')),
            ],
        ),
    ]