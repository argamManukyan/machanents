# Generated by Django 3.2.7 on 2022-07-17 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0045_auto_20220717_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='tracking_number',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='productrequestitem',
            name='send_email',
            field=models.BooleanField(default=False, verbose_name='Ուղարկել առաքանու կոդը էլ. հասցեին'),
        ),
    ]
