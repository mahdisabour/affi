# Generated by Django 3.2.7 on 2021-10-10 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0003_auto_20211002_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='amount',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
