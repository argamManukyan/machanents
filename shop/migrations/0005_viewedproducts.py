# Generated by Django 3.2.7 on 2021-10-10 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20211010_0840'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewedProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('session_key', models.CharField(blank=True, max_length=255, null=True)),
                ('product', models.ManyToManyField(blank=True, to='shop.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
