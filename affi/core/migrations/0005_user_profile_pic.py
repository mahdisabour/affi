# Generated by Django 3.2.7 on 2021-10-02 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_user_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='profile/default_profile_pic.png', upload_to='profile/'),
        ),
    ]
