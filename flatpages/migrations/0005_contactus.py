# Generated by Django 3.2.7 on 2021-10-20 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0004_auto_20211020_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('message', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
