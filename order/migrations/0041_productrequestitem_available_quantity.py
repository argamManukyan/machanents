# Generated by Django 3.2.7 on 2022-07-12 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0040_productrequestitem_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='productrequestitem',
            name='available_quantity',
            field=models.IntegerField(default=1),
        ),
    ]
