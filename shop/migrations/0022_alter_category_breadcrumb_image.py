# Generated by Django 3.2.7 on 2021-10-23 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_auto_20211023_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='breadcrumb_image',
            field=models.ImageField(blank=True, null=True, upload_to='category/'),
        ),
    ]
