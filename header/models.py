from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from core.utils import CustomModel, CustomLogoField


class Slider(CustomModel):
    image = CustomLogoField(blank=False,  verbose_name="Մեծ նկար")
    image_small = CustomLogoField(blank=False, verbose_name="Փոքր նկար")
    text = RichTextUploadingField(blank=True, null=True)
    url = models.URLField(blank=True, null=True, verbose_name="Ամբողջական հղում")
    my_order = models.PositiveIntegerField(default=0, verbose_name="Դասավորել")

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Գլխավոր էջի սլայդ'
        verbose_name_plural = 'Գլխավոր էջի սլայդեր'


class Header(CustomModel):
    """ Header table """

    name = models.CharField(max_length=255, verbose_name='Անուն')
    icon = CustomLogoField(verbose_name='Լոգո', blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True, verbose_name="Ամբողջական հղում")
    my_order = models.PositiveIntegerField(default=0, verbose_name="Դասավորել")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.url and not self.url.endswith('/'):
            self.url += '/'
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['my_order']


