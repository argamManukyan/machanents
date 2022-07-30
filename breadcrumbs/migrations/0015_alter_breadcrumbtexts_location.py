# Generated by Django 3.2.7 on 2022-07-30 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breadcrumbs', '0014_alter_breadcrumbtexts_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breadcrumbtexts',
            name='location',
            field=models.CharField(choices=[('sale', 'Ակցիա'), ('new_products', 'Նորույթ'), ('best_seller', 'Հատուկ առաջարկ'), ('categories', 'Բաժինների էջ'), ('blog', 'Բլոգ'), ('authors', 'Արտիստներ'), ('machanents_tv', 'Machanents TV')], max_length=150, unique=True, verbose_name='Ընտրեք էջը'),
        ),
    ]
