# Generated by Django 3.2.7 on 2021-10-20 16:44

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0002_auto_20211020_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutus',
            name='image2',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='text2',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
    ]
