# Generated by Django 3.2.7 on 2022-07-30 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0015_auto_20220730_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationhomepagetext',
            name='title',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Վերնագիր'),
        ),
        migrations.AlterField(
            model_name='donationhomepagetext',
            name='title_en',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Վերնագիր'),
        ),
        migrations.AlterField(
            model_name='donationhomepagetext',
            name='title_hy',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Վերնագիր'),
        ),
        migrations.AlterField(
            model_name='donationhomepagetext',
            name='title_ru',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Վերնագիր'),
        ),
    ]
