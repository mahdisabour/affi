# Generated by Django 3.2.7 on 2021-10-29 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_product_visibility'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_visibility',
            new_name='visibility',
        ),
    ]
