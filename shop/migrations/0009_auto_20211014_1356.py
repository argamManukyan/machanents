# Generated by Django 3.2.7 on 2021-10-14 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20211014_1349'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='slider',
            options={'ordering': ['my_order'], 'verbose_name': 'Գլխավոր սլայդեր', 'verbose_name_plural': 'Գլխավոր սլայդեր'},
        ),
        migrations.AddField(
            model_name='slider',
            name='my_order',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
