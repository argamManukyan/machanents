# Generated by Django 3.2.7 on 2022-05-20 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0030_category_show_in_header'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='show_in_homepage',
            field=models.BooleanField(default=False),
        ),
    ]
