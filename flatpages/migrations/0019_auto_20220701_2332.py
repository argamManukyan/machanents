# Generated by Django 3.2.7 on 2022-07-01 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0018_auto_20220701_2313'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aboutussocialicons',
            options={'ordering': ['my_order'], 'verbose_name': '«Մեր մասին» էջի սոց. ցանցի լոգո', 'verbose_name_plural': '«Մեր մասին» էջի սոց. ցանցերի լոգոներ'},
        ),
        migrations.AddField(
            model_name='aboutussocialicons',
            name='my_order',
            field=models.PositiveIntegerField(default=1, verbose_name='Դասավորել'),
            preserve_default=False,
        ),
    ]
