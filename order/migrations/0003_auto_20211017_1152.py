# Generated by Django 3.2.7 on 2021-10-17 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20211017_1149'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Delivery',
        ),
        migrations.DeleteModel(
            name='Payments',
        ),
        migrations.DeleteModel(
            name='PaymentStatus',
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]
