# Generated by Django 3.2.7 on 2022-07-10 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0034_productrequestitem_qty'),
    ]

    operations = [
        migrations.AddField(
            model_name='productrequestitem',
            name='product_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
