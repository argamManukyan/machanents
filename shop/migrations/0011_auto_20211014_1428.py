# Generated by Django 3.2.7 on 2021-10-14 14:28

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_ouradvantages'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialOfferBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('product_url', models.URLField()),
                ('product_url_hy', models.URLField(null=True)),
                ('product_url_ru', models.URLField(null=True)),
                ('product_url_en', models.URLField(null=True)),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('text_hy', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('text_ru', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('text_en', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('image', models.FileField(upload_to='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='best_seller',
            field=models.BooleanField(default=False),
        ),
    ]
