# Generated by Django 4.2.6 on 2023-10-29 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_quantity_alter_order_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_time']},
        ),
        migrations.AlterModelTable(
            name='order',
            table='orders',
        ),
    ]
