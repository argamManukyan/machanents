# Generated by Django 3.2.7 on 2022-07-02 12:25

import core.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0037_auto_20220702_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_description', models.TextField(blank=True, max_length=300, null=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('breadcrumbs_text', models.TextField(blank=True, null=True)),
                ('breadcrumbs_image', core.utils.CustomLogoField(blank=True, null=True, upload_to='')),
            ],
            options={
                'verbose_name': 'Բաժին',
                'verbose_name_plural': 'Հեղինակների բաժիններ',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_products', to='shop.authors'),
        ),
        migrations.AddField(
            model_name='authors',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='authors', to='shop.AuthorCategories'),
        ),
    ]
