# Generated by Django 3.2.7 on 2022-06-25 20:02

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('footer', '0009_auto_20220625_1951'),
    ]

    operations = [
        migrations.CreateModel(
            name='FooterMessengers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('icon', core.utils.CustomLogoField(upload_to='')),
                ('url', models.CharField(max_length=255, verbose_name='Հղում')),
            ],
            options={
                'verbose_name': 'Messenger',
                'verbose_name_plural': 'Messenger -ներ',
            },
        ),
        migrations.AlterField(
            model_name='companyinformation',
            name='name',
            field=models.CharField(default=1, max_length=255, verbose_name='Դաշտի անուն'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='companyinformation',
            name='name_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Դաշտի անուն'),
        ),
        migrations.AlterField(
            model_name='companyinformation',
            name='name_hy',
            field=models.CharField(max_length=255, null=True, verbose_name='Դաշտի անուն'),
        ),
        migrations.AlterField(
            model_name='companyinformation',
            name='name_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='Դաշտի անուն'),
        ),
        migrations.AlterField(
            model_name='companyinformation',
            name='text',
            field=models.CharField(default=1, max_length=255, verbose_name='Տեքստ'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='companyinformation',
            name='text_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Տեքստ'),
        ),
        migrations.AlterField(
            model_name='companyinformation',
            name='text_hy',
            field=models.CharField(max_length=255, null=True, verbose_name='Տեքստ'),
        ),
        migrations.AlterField(
            model_name='companyinformation',
            name='text_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='Տեքստ'),
        ),
    ]
