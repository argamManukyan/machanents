# Generated by Django 3.2.7 on 2021-10-23 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_auto_20211023_1613'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['my_order', '-id'], 'verbose_name': 'Ապրանք', 'verbose_name_plural': 'Ապրանքներ'},
        ),
    ]
