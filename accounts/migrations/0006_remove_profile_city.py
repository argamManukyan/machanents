# Generated by Django 3.2.7 on 2022-07-03 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_profile_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='city',
        ),
    ]
