# Generated by Django 3.2.7 on 2022-07-29 19:45

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('footer', '0013_auto_20220626_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='footerpartners',
            name='alt_title',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='footerpartners',
            name='alt_title_en',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='footerpartners',
            name='alt_title_hy',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='footerpartners',
            name='alt_title_ru',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='footerpartners',
            name='icon',
            field=core.utils.CustomLogoField(upload_to='', verbose_name='Լոգո'),
        ),
        migrations.AlterField(
            model_name='footerpartners',
            name='my_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Դասավորել'),
        ),
    ]
