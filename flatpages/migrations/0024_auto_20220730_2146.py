# Generated by Django 3.2.7 on 2022-07-30 17:46

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0023_auto_20220730_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutus',
            name='text_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Տեքստ'),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='text_hy',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Տեքստ'),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='text_ru',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Տեքստ'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='my_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Դասավորել'),
        ),
        migrations.AlterField(
            model_name='blogcategory',
            name='my_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Դասավորել'),
        ),
    ]
