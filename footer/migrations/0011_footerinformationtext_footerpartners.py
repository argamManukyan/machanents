# Generated by Django 3.2.7 on 2022-06-25 20:19

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('footer', '0010_auto_20220626_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='FooterInformationText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('text_hy', models.TextField(null=True)),
                ('text_ru', models.TextField(null=True)),
                ('text_en', models.TextField(null=True)),
            ],
            options={
                'verbose_name': 'Ինֆորմացիոն տեքստ',
                'verbose_name_plural': 'Ինֆորմացիոն տեքստ',
            },
        ),
        migrations.CreateModel(
            name='FooterPartners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('icon', core.utils.CustomLogoField(upload_to='')),
            ],
            options={
                'verbose_name': 'Գործընկեր',
                'verbose_name_plural': 'Գործընկերներ',
            },
        ),
    ]
