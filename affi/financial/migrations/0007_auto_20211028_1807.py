# Generated by Django 3.2.7 on 2021-10-28 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('affiliation', '0005_alter_order_related_products'),
        ('financial', '0006_auto_20211028_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='related_order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='affiliation.order'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_state',
            field=models.CharField(choices=[('pending', 'pending'), ('success', 'success'), ('failed', 'failed')], default='pending', max_length=50),
        ),
    ]
