# Generated by Django 3.2.7 on 2022-06-29 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breadcrumbs', '0008_alter_breadcrumbtexts_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breadcrumbtexts',
            name='location',
            field=models.CharField(choices=[('categories', 'Բաժինների էջ'), ('brands', 'Բրենդների էջ'), ('blog', 'Բլոգ'), ('gallery', 'Տեսադարան'), ('contacts', 'Կապ'), ('abouts', 'Մեր մասին'), ('faq', 'Հաճախակի տրվող հարցեր'), ('machanents_tv', 'Machanents TV')], max_length=150, unique=True, verbose_name='Ընտրեք էջը'),
        ),
    ]
