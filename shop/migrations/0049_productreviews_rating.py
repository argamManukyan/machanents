# Generated by Django 3.2.7 on 2022-07-24 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0048_auto_20220725_0042'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreviews',
            name='rating',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Գնահատական'),
            preserve_default=False,
        ),
    ]
