# Generated by Django 3.2.7 on 2021-11-17 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0021_order_bank_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='language_code',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
