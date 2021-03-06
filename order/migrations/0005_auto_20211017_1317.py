# Generated by Django 3.2.7 on 2021-10-17 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20211017_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='name_hy',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='name_ru',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='state',
            name='name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='state',
            name='name_hy',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='state',
            name='name_ru',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
