# Generated by Django 3.2.7 on 2022-07-02 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactus', '0007_alter_workinghours_options_workinghours_my_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactusjoinusdata',
            options={'ordering': ['-my_order'], 'verbose_name': 'Կոնտակտային տվյալ', 'verbose_name_plural': 'Կոնտակտային տվյալներ'},
        ),
        migrations.AlterModelOptions(
            name='followuscontactus',
            options={'ordering': ['-my_order'], 'verbose_name': 'Հետևեք մեզ - սոց. ցանցեր', 'verbose_name_plural': 'Հետևեք մեզ - սոց. ցանցեր'},
        ),
        migrations.AddField(
            model_name='contactusjoinusdata',
            name='my_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Դասավորել'),
        ),
        migrations.AddField(
            model_name='followuscontactus',
            name='my_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Դասավորել'),
        ),
    ]
