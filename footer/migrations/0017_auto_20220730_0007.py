# Generated by Django 3.2.7 on 2022-07-29 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('footer', '0016_remove_companyinformation_icon'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cardicons',
            options={'ordering': ['my_order'], 'verbose_name': 'Վճարային քարտի լոգո', 'verbose_name_plural': 'Վճարային քարտերի լոգոներ'},
        ),
        migrations.AddField(
            model_name='cardicons',
            name='my_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Դասավորել'),
        ),
    ]
