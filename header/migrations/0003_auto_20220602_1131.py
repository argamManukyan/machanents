# Generated by Django 3.1 on 2022-06-02 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('header', '0002_auto_20220602_1105'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='header',
            options={'ordering': ['my_order']},
        ),
        migrations.AlterModelOptions(
            name='slider',
            options={'ordering': ['my_order'], 'verbose_name': 'Գլխավոր էջի սլայդ', 'verbose_name_plural': 'Գլխավոր էջի սլայդեր'},
        ),
        migrations.AddField(
            model_name='header',
            name='my_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Դասավորել'),
        ),
        migrations.AddField(
            model_name='slider',
            name='my_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Դասավորել'),
        ),
    ]
