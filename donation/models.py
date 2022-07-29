from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from core.utils import CustomModel


class DonationCurrencies(CustomModel):
    name = models.CharField(max_length=120,
                            unique=True,
                            db_index=True,
                            verbose_name='Արժույթի անուն')
    icon = models.CharField(max_length=2, unique=True, verbose_name='Լոգո')
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')

    class Meta:
        verbose_name = 'Արժութ'
        verbose_name_plural = 'Արժութներ'
        ordering = ['my_order']

    def __str__(self):
        return self.name

#
class DonationRanges(CustomModel):
    currency_name = models.ForeignKey(DonationCurrencies, verbose_name='Արժույթ',
                                      on_delete=models.CASCADE, default=None)
    amount = models.PositiveIntegerField(verbose_name='Գումարի չափ')

    class Meta:
        verbose_name = 'Գումար'
        verbose_name_plural = 'Գումար'

    def __str__(self):
        return f'{self.currency_name.name} - {self.amount}'


class DonationHomepageText(CustomModel):
    text = RichTextUploadingField(verbose_name='Տեքստ', blank=True)
    background_image = models.FileField(verbose_name='Ֆոնային նկար', blank=True, null=True)
    title = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        verbose_name = 'Նվիրատվության տեքստ և նկար'
        verbose_name_plural = 'Նվիրատվության տեքստ և նկար'

    def __str__(self):
        return 'Նվիրատվության տեքստ և նկար'


class Donations(CustomModel):
    """ Donations model """

    amount = models.FloatField(blank=True, null=True, verbose_name='Գումարի չափ')
    first_name = models.CharField(max_length=300,
                                  blank=True,
                                  null=True,
                                  default='Անհայտ',
                                  verbose_name='Անուն և ազգանուն')
    email = models.EmailField(blank=True, null=True, verbose_name='Էլ. հասցե')
    phone = models.CharField(max_length=40, blank=True, null=True, verbose_name='Հեռ.')
    currency = models.CharField(max_length=10, blank=True, null=True, verbose_name='Արժույթ')
    done = models.BooleanField(default=False, verbose_name='Կատարված')

    def __str__(self):
        return f'{self.first_name} - {self.amount}'

    class Meta:
        verbose_name = 'Նվիրատվություն'
        verbose_name_plural = 'Նվիրատվություններ'
        ordering = ['-id']