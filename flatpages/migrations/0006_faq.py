# Generated by Django 3.2.7 on 2021-10-20 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0005_contactus'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField()),
            ],
        ),
    ]
