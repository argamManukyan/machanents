# Generated by Django 3.2.7 on 2022-07-30 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0052_auto_20220730_2146'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authorcategories',
            options={'ordering': ['my_order'], 'verbose_name': 'Բաժին', 'verbose_name_plural': 'Արտիստների բաժիններ'},
        ),
        migrations.AlterModelOptions(
            name='authors',
            options={'ordering': ['my_order'], 'verbose_name': 'Արտիստ', 'verbose_name_plural': 'Արտիստներ'},
        ),
        migrations.AddField(
            model_name='authorcategories',
            name='my_order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='authors',
            name='my_order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]