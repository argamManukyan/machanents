# Generated by Django 3.2.7 on 2021-10-02 07:33

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('meta_title', models.CharField(blank=True, max_length=200)),
                ('meta_description', models.TextField(blank=True, max_length=300)),
                ('breadcrumb_image', models.ImageField(upload_to='category/')),
                ('breadcrumb_text', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='shop.category')),
            ],
            options={
                'verbose_name': 'Բաժին',
                'verbose_name_plural': 'Բաժիններ',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('color_code', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FilterField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('show_in_filters', models.BooleanField(default=False)),
                ('ia_main', models.DateTimeField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FilterValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('image_xl', models.FileField(upload_to='')),
                ('image_ml', models.FileField(upload_to='')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField()),
            ],
            options={
                'verbose_name': 'Գլխավոր սլայդեր',
                'verbose_name_plural': 'Գլխավոր սլայդեր',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('product_code', models.CharField(blank=True, max_length=20)),
                ('short_description', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('large_description', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('meta_title', models.CharField(blank=True, max_length=200)),
                ('meta_description', models.TextField(blank=True, max_length=300)),
                ('old_price', models.IntegerField(default=0)),
                ('new_price', models.IntegerField(default=0)),
                ('main_photo', models.ImageField(upload_to='product/')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.category')),
                ('color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.color')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
