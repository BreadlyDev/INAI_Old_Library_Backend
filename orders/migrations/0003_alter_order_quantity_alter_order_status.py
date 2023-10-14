# Generated by Django 4.2.6 on 2023-10-14 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Не рассмотрено', 'Не рассмотрено'), ('Подтверждено', 'Подтверждено'), ('Обрабатывается', 'Обрабатывается'), ('Готово', 'Готово'), ('Ошибка', 'Ошибка')], default='Не рассмотрено', max_length=50),
        ),
    ]
