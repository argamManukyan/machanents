# Generated by Django 3.2.7 on 2021-11-09 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_alter_orderitem_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='bank_order_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
