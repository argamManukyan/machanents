# Generated by Django 3.2.7 on 2021-11-09 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0020_order_bank_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='bank_message',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
