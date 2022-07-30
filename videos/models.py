from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from core.utils import CustomLogoField, slug_generator, CustomMetaModel


class VideoCategory(CustomMetaModel):

    name = models.CharField(max_length=255, verbose_name='Անուն')
    slug = models.SlugField(blank=True, null=True, verbose_name='Հղում')
    breadcrumbs_text = models.TextField(blank=True, null=True, verbose_name='Breadcrumb -ի տեքստ')
    breadcrumbs_image = CustomLogoField(blank=True, null=True, verbose_name='Breadcrumb -ի Նկար')
    my_order = models.PositiveIntegerField(default=0, verbose_name='Դասավորել')

    def get_absolute_url(self):
        return reverse('video_category', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slug_generator(self.name, VideoCategory)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Տեսահոլովակի բաժին'
        verbose_name_plural = 'Տեսահոլովակի բաժիններ'
        ordering = ['my_order']

    def __str__(self):
        return self.name


class Video(models.Model):

    category = models.ForeignKey(VideoCategory, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Բաժին')
    video_iframe = models.TextField(verbose_name='Տեսահոլովակի Iframe', blank=True)
    video_file = models.FileField(verbose_name='Տեսահոլովակ (ֆայլ)', blank=True)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')
    show_on_homepage = models.BooleanField(default=False, verbose_name='Ցուցադրել գլխավոր էջում՝ «Machanents TV» սլայդերում')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Տեսահոլովակ'
        verbose_name_plural = 'Machanents TV'
        ordering = ['my_order']

    def clean(self):
        if all([not self.video_file, not self.video_iframe]):
            raise ValidationError({'video_iframe': "Պարտադիր է լրացնել «Տեսահոլովակի Iframe»/«Տեսահոլովակ (ֆայլ)»"
                                              " դաշտերից որևէ մեկը"})