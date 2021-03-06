# Generated by Django 3.2.7 on 2022-07-01 19:13

import ckeditor_uploader.fields
import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0017_auto_20220629_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUsSocialIcons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', core.utils.CustomLogoField(blank=True, null=True, upload_to='')),
                ('text', models.CharField(blank=True, max_length=255, null=True, verbose_name='Տեքստ')),
                ('text_hy', models.CharField(blank=True, max_length=255, null=True, verbose_name='Տեքստ')),
                ('text_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name='Տեքստ')),
                ('text_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Տեքստ')),
                ('url', models.URLField(verbose_name='Հղում')),
            ],
        ),
        migrations.RenameField(
            model_name='aboutus',
            old_name='created_at',
            new_name='created',
        ),
        migrations.RemoveField(
            model_name='aboutus',
            name='text_en',
        ),
        migrations.RemoveField(
            model_name='aboutus',
            name='text_hy',
        ),
        migrations.RemoveField(
            model_name='aboutus',
            name='text_ru',
        ),
        migrations.RemoveField(
            model_name='aboutus',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='aboutus',
            name='breadcrumbs_image',
            field=models.FileField(blank=True, upload_to='', verbose_name='breadcrumb -ի նկար'),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='breadcrumbs_text',
            field=models.TextField(blank=True, verbose_name='breadcrumb -ի տեքստ'),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='breadcrumbs_text_en',
            field=models.TextField(blank=True, null=True, verbose_name='breadcrumb -ի տեքստ'),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='breadcrumbs_text_hy',
            field=models.TextField(blank=True, null=True, verbose_name='breadcrumb -ի տեքստ'),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='breadcrumbs_text_ru',
            field=models.TextField(blank=True, null=True, verbose_name='breadcrumb -ի տեքստ'),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='meta_description',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='meta_description_en',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='meta_description_hy',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='meta_description_ru',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='meta_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='meta_title_en',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='meta_title_hy',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='meta_title_ru',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Տեքստ'),
        ),
        migrations.AlterField(
            model_name='gallerycategory',
            name='breadcrumb_text',
            field=models.TextField(blank=True, verbose_name='breadcrumb -ի տեքստ'),
        ),
        migrations.AlterField(
            model_name='gallerycategory',
            name='breadcrumb_text_en',
            field=models.TextField(blank=True, null=True, verbose_name='breadcrumb -ի տեքստ'),
        ),
        migrations.AlterField(
            model_name='gallerycategory',
            name='breadcrumb_text_hy',
            field=models.TextField(blank=True, null=True, verbose_name='breadcrumb -ի տեքստ'),
        ),
        migrations.AlterField(
            model_name='gallerycategory',
            name='breadcrumb_text_ru',
            field=models.TextField(blank=True, null=True, verbose_name='breadcrumb -ի տեքստ'),
        ),
    ]
