# Generated by Django 5.0.2 on 2024-03-13 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_cloth_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloth',
            name='image',
            field=models.ImageField(upload_to='uploads/product/'),
        ),
    ]