# Generated by Django 5.0.2 on 2024-04-15 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_order_checkout'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_completed',
            field=models.BooleanField(default=False),
        ),
    ]
