# Generated by Django 3.2.7 on 2021-10-29 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20211028_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_visibility',
            field=models.BooleanField(default=True),
        ),
    ]
