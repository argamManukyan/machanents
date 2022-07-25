from django.core.validators import FileExtensionValidator
from django.db import models

from core.utils import CustomModel


class ContactUsPage(CustomModel):
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(max_length=300, blank=True, null=True)
    iframe = models.TextField(verbose_name="Քարտեզ (Iframe)", blank=True, null=True)
    # breadcrumb_image = models.FileField(validators=[FileExtensionValidator(
    #     allowed_extensions=['jpg', 'svg', 'png', 'jpeg']
    # )], verbose_name="Breadcrumb -ի Նկար", blank=True, null=True)
    # breadcrumbs_text = models.TextField(verbose_name="Breadcrumb -ի տեքստ", blank=True, null=True)

    # my_order = models.PositiveIntegerField(default=0, verbose_name="Դասավորել")

    class Meta:
        verbose_name = 'Հետադարձ կապի էջ'
        verbose_name_plural = 'Հետադարձ կապի էջ'
        # ordering = ['-my_order']

    def __str__(self):
        return "Հետադարձ կապի էջի"


class ContactUsJoinUsData(CustomModel):
    contact_us = models.ForeignKey(ContactUsPage, on_delete=models.CASCADE)
    text = models.CharField(max_length=400, verbose_name="Տեքստ")
    icon = models.FileField(validators=[FileExtensionValidator(
        allowed_extensions=['jpg', 'svg', 'png', 'jpeg']
    )], verbose_name="Նկար", blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True, verbose_name="Հղում")

    my_order = models.PositiveIntegerField(default=0, verbose_name="Դասավորել")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Կոնտակտային տվյալ"
        verbose_name_plural = "Կոնտակտային տվյալներ"
        ordering = ['-my_order']


class FollowUsContactUs(CustomModel):
    contact_us = models.ForeignKey(ContactUsPage, on_delete=models.CASCADE)
    text = models.CharField(max_length=400, verbose_name="Սոց. ցանցի անուն")
    icon = models.FileField(validators=[FileExtensionValidator(
        allowed_extensions=['jpg', 'svg', 'png', 'jpeg']
    )], verbose_name="Նկար")
    link = models.CharField(max_length=500, blank=True, null=True, verbose_name="Հղում")

    my_order = models.PositiveIntegerField(default=0, verbose_name="Դասավորել")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Հետևեք մեզ - սոց. ցանցեր"
        verbose_name_plural = "Հետևեք մեզ - սոց. ցանցեր"
        ordering = ['-my_order']


class ContactUsRequest(CustomModel):
    first_name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Հետադարձ կապի պատվեր'
        verbose_name_plural = 'Հետադարձ կապի պատվերներ'


class WorkingHours(models.Model):
    name = models.CharField(max_length=120, unique=True,
                            verbose_name="Ժամանակահատված",
                            help_text="Օր.՝ 12:00 - 15:00")
    my_order = models.PositiveIntegerField(default=0, verbose_name='Դասավորել')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Ամրագրման ժամ'
        verbose_name_plural = 'Ամրագրման ժամեր'


class Bookings(models.Model):
    name = models.CharField(max_length=255, verbose_name='Անուն')
    phone = models.CharField(max_length=40, verbose_name='Հեռ.')
    date_of_book = models.DateField(verbose_name="Ամրագրման օրը")
    time_of_pick = models.ForeignKey(WorkingHours, verbose_name="Ամրագրված ժամանակահատված",
                                     on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Ամրագրումներ'
        verbose_name_plural = 'Ամրագրումներ'
