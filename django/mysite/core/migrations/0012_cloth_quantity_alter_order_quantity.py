# Generated by Django 5.0.2 on 2024-03-18 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_order_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cloth',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]