# Generated by Django 3.2.7 on 2022-07-10 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0039_productrequestitem_product_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='productrequestitem',
            name='description',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
