# Generated by Django 3.2.7 on 2021-11-18 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0023_order_currency_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='bank_order_status',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
