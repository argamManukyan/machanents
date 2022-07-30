# Generated by Django 3.2.7 on 2022-07-29 19:39

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('header', '0006_alter_header_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='header',
            name='url',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Ամբողջական հղում'),
        ),
        migrations.AlterField(
            model_name='header',
            name='url_en',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Ամբողջական հղում'),
        ),
        migrations.AlterField(
            model_name='header',
            name='url_hy',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Ամբողջական հղում'),
        ),
        migrations.AlterField(
            model_name='header',
            name='url_ru',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Ամբողջական հղում'),
        ),
        migrations.AlterField(
            model_name='slider',
            name='image',
            field=core.utils.CustomLogoField(upload_to='', verbose_name='Մեծ նկար'),
        ),
    ]