# Generated by Django 3.2.7 on 2022-07-30 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0026_alter_aboutussocialicons_icon'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aboutus',
            options={'ordering': ['my_order'], 'verbose_name': 'Մեր մասին', 'verbose_name_plural': 'Մեր մասին'},
        ),
        migrations.AddField(
            model_name='aboutus',
            name='my_order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
