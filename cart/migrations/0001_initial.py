# Generated by Django 3.2.7 on 2021-10-10 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0006_rename_product_viewedproducts_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('item_price', models.IntegerField(blank=True, default=0, null=True)),
                ('item_total_price', models.IntegerField(blank=True, default=0, null=True)),
                ('features', models.JSONField(blank=True, null=True)),
                ('item_description', models.TextField(blank=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('ip', models.CharField(blank=True, max_length=25)),
                ('cart_total', models.IntegerField(default=0)),
                ('item', models.ManyToManyField(to='cart.CartItem')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
