# Generated by Django 5.0.2 on 2024-02-20 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_alter_productinout_order_completed_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinout',
            name='units',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
