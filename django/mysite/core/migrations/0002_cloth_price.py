# Generated by Django 5.0.2 on 2024-03-05 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cloth',
            name='price',
            field=models.FloatField(default=20),
            preserve_default=False,
        ),
    ]