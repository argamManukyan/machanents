# Generated by Django 3.2.7 on 2021-10-23 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_auto_20211022_1736'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deliverytime',
            options={'ordering': ['my_order']},
        ),
        migrations.AddField(
            model_name='deliverytime',
            name='my_order',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
