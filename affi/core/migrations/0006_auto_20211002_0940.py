# Generated by Django 3.2.7 on 2021-10-02 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_user_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profile_pic',
        ),
    ]
