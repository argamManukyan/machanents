# Generated by Django 3.2.7 on 2022-07-24 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0009_auto_20220717_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('amount', models.FloatField(blank=True, null=True, verbose_name='Գումարի չափ')),
                ('first_name', models.CharField(blank=True, max_length=300, null=True, verbose_name='Անուն և ազգանուն')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Էլ. հասցե')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, verbose_name='Հեռ.')),
                ('currency', models.CharField(blank=True, max_length=10, null=True, verbose_name='Արժույթ')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
