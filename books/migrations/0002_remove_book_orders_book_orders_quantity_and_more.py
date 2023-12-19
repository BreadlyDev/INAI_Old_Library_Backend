# Generated by Django 4.2.6 on 2023-12-19 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='orders',
        ),
        migrations.AddField(
            model_name='book',
            name='orders_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='book',
            name='e_book',
            field=models.FileField(null=True, upload_to='e_books_files'),
        ),
        migrations.AlterField(
            model_name='book',
            name='inventory_number',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='reviews_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
