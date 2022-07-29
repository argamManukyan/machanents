from ckeditor_uploader.fields import RichTextUploadingFormField
from django.db import models
from core.utils import CustomLogoField, CustomModel


class CompanyInformation(models.Model):
    # icon = CustomLogoField(blank=True)
    text = models.CharField(max_length=255, verbose_name="Տեքստ")
    name = models.CharField(max_length=255,  verbose_name='Դաշտի անուն')
    url = models.CharField(max_length=1000,  blank=True, null=True, verbose_name="Հղում")
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Կոնտակտային տվյալ'
        verbose_name_plural = 'Կոնտակտային տվյալներ'


class FooTerCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Անուն")
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Footer -ի բաժին'
        verbose_name_plural = 'Footer -ի բաժիններ'


class FooterItems(CustomModel):
    LOGIN_CHOICES = [
        ('logged', 'Օգտատերեր'),
        ('guests', 'Հյուրեր'),
    ]

    category = models.ForeignKey(FooTerCategory,
                                 on_delete=models.RESTRICT,
                                 blank=True,
                                 verbose_name='Բաժին',
                                 null=True)
    name = models.CharField(max_length=255, unique=True, verbose_name="Անուն")
    url = models.URLField(verbose_name="Ամբողջական հղում")
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')
    is_auth = models.CharField(max_length=120,
                               blank=True, null=True,
                               choices=LOGIN_CHOICES,
                               verbose_name='Ցուցադրել միայն մուտք գործած օգտատերերին')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Footer -ի հղումներ'
        verbose_name_plural = 'Footer -ի հղումներ'


class SocialShareButtons(CustomModel):
    icon = CustomLogoField()
    url = models.URLField(verbose_name='Ամբողջական հղում')
    name = models.CharField(max_length=255, unique=True, verbose_name="Անուն (alt)")
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Սոց. ցանցի լոգո'
        verbose_name_plural = 'Սոց. ցանցերի լոգոներ'


class FooterMessengers(CustomModel):
    icon = CustomLogoField(blank=False, null=False)
    url = models.CharField(max_length=255, verbose_name="Հղում")

    class Meta:
        verbose_name = 'Messenger'
        verbose_name_plural = 'Messenger -ներ'

    def __str__(self):
        return f'{self.id}'


class FooterInformationText(CustomModel):
    text = models.TextField(verbose_name='Տեքստ')

    class Meta:
        verbose_name = 'Ինֆորմացիոն տեքստ'
        verbose_name_plural = 'Ինֆորմացիոն տեքստ'

    def __str__(self):
        return 'Ինֆորմացիոն տեքստ'

class FooterPartners(CustomModel):
    icon = CustomLogoField(blank=False, null=False, verbose_name='Լոգո')
    my_order = models.PositiveIntegerField(default=0, verbose_name='Դասավորել')
    alt_title = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Գործընկեր'
        verbose_name_plural = 'Գործընկերներ'


class CardIcons(CustomModel):
    icon = CustomLogoField()
    my_order = models.PositiveIntegerField(default=0, verbose_name='Դասավորել')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Վճարային քարտի լոգո'
        verbose_name_plural = 'Վճարային քարտերի լոգոներ'