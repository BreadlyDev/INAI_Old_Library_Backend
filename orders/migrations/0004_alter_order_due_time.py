# Generated by Django 4.2.7 on 2023-11-14 14:05

from django.db import migrations, models
import orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_options_alter_order_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='due_time',
            field=models.DateTimeField(null=True, validators=[orders.models.validate_due_date]),
        ),
    ]
