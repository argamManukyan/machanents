# Generated by Django 3.2.7 on 2022-07-16 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_cartitem_features'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='uuid_field',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
