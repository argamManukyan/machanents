# Generated by Django 3.2.7 on 2022-07-24 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0012_alter_donations_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donations',
            name='first_name',
            field=models.CharField(blank=True, default='Անհայտ', max_length=300, null=True, verbose_name='Անուն և ազգանուն'),
        ),
    ]
