# Generated by Django 3.2.7 on 2022-07-17 05:39

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0044_auto_20220716_2253'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productrequest',
            options={'ordering': ['-id'], 'verbose_name': 'Ապրանքի հարցում', 'verbose_name_plural': 'Ապրանքների հարցումներ'},
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(blank=True, verbose_name='Հասցե'),
        ),
        migrations.AlterField(
            model_name='order',
            name='all_total',
            field=models.FloatField(blank=True, default=0, verbose_name='Պատվերի ընդհանուր արժեք'),
        ),
        migrations.AlterField(
            model_name='order',
            name='bank_message',
            field=models.CharField(blank=True, max_length=255, verbose_name='Բանկի պատասխանը տեսքստի տեսքով'),
        ),
        migrations.AlterField(
            model_name='order',
            name='bank_order_id',
            field=models.CharField(blank=True, max_length=255, verbose_name='Բանկային id'),
        ),
        migrations.AlterField(
            model_name='order',
            name='bank_order_status',
            field=models.IntegerField(blank=True, null=True, verbose_name='Բանկից ստացված պատասխան'),
        ),
        migrations.AlterField(
            model_name='order',
            name='city_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Քաղաքի/մարզի անուն'),
        ),
        migrations.AlterField(
            model_name='order',
            name='country_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Երկրի անուն'),
        ),
        migrations.AlterField(
            model_name='order',
            name='curr_code',
            field=models.CharField(blank=True, max_length=8, verbose_name='Պատվերի կատարման արտարժույթի կոդ'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_price',
            field=models.FloatField(blank=True, default=0, verbose_name='Առաքման արժեք'),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Էլ. հասցե'),
        ),
        migrations.AlterField(
            model_name='order',
            name='first_name',
            field=models.CharField(blank=True, max_length=80, verbose_name='Անուն և ազգանուն'),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Վճարված է'),
        ),
        migrations.AlterField(
            model_name='order',
            name='language_code',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='Պատվերի կատարման լեզու'),
        ),
        migrations.AlterField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Նշումներ'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.orderstatus', verbose_name='Պատվերի կարգավիճակ'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, max_length=30, verbose_name='Հեռ.'),
        ),
        migrations.AlterField(
            model_name='order',
            name='session_key',
            field=models.CharField(blank=True, editable=False, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.FloatField(blank=True, default=0, verbose_name='Ապրանքերի հանրագումար'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Հարցումն իրականացրած և գրանցված օգտատեր'),
        ),
        migrations.AlterField(
            model_name='order',
            name='zip_code',
            field=models.CharField(blank=True, max_length=50, verbose_name='Փոստային դասիչ'),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='address',
            field=models.TextField(blank=True, verbose_name='Հասցե'),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='all_total',
            field=models.FloatField(blank=True, default=0, verbose_name='Պատվերի վերջնական արժեք'),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='city_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Քաղաքի/մարզի անունը'),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='country_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Երկրի անունը'),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='curr_code',
            field=models.CharField(blank=True, default='AMD', help_text='Հարցումը կատարվել է նշված արտարժույթով', max_length=5, null=True, verbose_name='Արտարժությթի կոդ'),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='delivery',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.delivery'),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='delivery_price',
            field=models.FloatField(blank=True, default=0, verbose_name='Առաքման արժեք'),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Ադմինի կողմից կատարվող նշումներ'),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Էլ. փոստ'),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='first_name',
            field=models.CharField(blank=True, max_length=80, verbose_name='Անուն և ազգանուն'),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='is_exists',
            field=models.BooleanField(default=False, help_text='Ակտիվացնելով այս դաշտը հարցումը հասանելի կլինի վճարման', verbose_name='Թույլատրելի է վճարման'),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='is_expired',
            field=models.BooleanField(default=False, editable=False, verbose_name='Պատվերը ժամկետանց է'),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Նշումներ'),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='payments',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.paymenttypes'),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Հեռ.'),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='session_key',
            field=models.CharField(blank=True, editable=False, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='total_price',
            field=models.FloatField(blank=True, default=0, verbose_name='Ապրանքների արժեքների հանրագումար'),
        ),
        migrations.AlterField(
            model_name='productrequest',
            name='zip_code',
            field=models.CharField(blank=True, max_length=50, verbose_name='Փոստային դասիչ'),
        ),
    ]
