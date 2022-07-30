from django.db import models

from core.utils import CustomLogoField, CustomMetaModel, slug_generator
from shop.utils import CustomModel
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from shop.models import generate_slug


class AboutUs(CustomMetaModel):
    title = models.CharField(max_length=255, unique=True, verbose_name='Վերնագիր')
    slug = models.SlugField(max_length=255, blank=True, null=True, verbose_name='Հղում')
    logo = CustomLogoField(verbose_name='Լոգո', blank=True, null=True)
    text = RichTextUploadingField(verbose_name='Տեքստ', blank=True, null=True)
    breadcrumbs_image = models.FileField(blank=True, verbose_name='breadcrumb -ի նկար')
    breadcrumbs_text = models.TextField(blank=True, verbose_name='breadcrumb -ի տեքստ')
    is_main = models.BooleanField(default=False, verbose_name='Հիմնական նյութ',
                                  help_text='Ակտիվ լինելու դեպքում այս նյութը կցուցադրվի «Մեր մասին» էջում '
                                            'որպես գլխավոր նյութ'
                                  )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_id = AboutUs.objects.last().id + 1 if AboutUs.objects.count() else 1
            self.slug = generate_slug(self.title, slug_id)
        if self.is_main:
            if self.__class__.objects.filter(is_main=True).exclude(id=self.id).exists():
                for i in self.__class__.objects.filter(is_main=True).exclude(id=self.id):
                    i.is_main = False
                    i.save()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('about_us_category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Մեր մասին'
        verbose_name_plural = 'Մեր մասին'


class ContactUs(CustomModel):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name='Հարց')
    answer = models.TextField(verbose_name='Պատասխան')

    def __str__(self):
        return self.question


class GalleryCategory(CustomModel):
    title = models.CharField(max_length=255, verbose_name='Անուն')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Հղում')
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True, max_length=300)
    breadcrumb_image = models.FileField(blank=True, verbose_name='breadcrumb -ի նկար')
    breadcrumb_text = models.TextField(blank=True, verbose_name='breadcrumb -ի տեքստ')
    my_order = models.PositiveIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Տեսադարանի բաժին'
        verbose_name_plural = 'Տեսադարան բաժիններ'

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_id = GalleryCategory.objects.last().id + 1 if GalleryCategory.objects.count() else 1
            self.slug = generate_slug(self.title, slug_id)

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('gallery_details', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Gallery(CustomModel):
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL,
                                 null=True, blank=True, verbose_name='Բաժին')
    image = CustomLogoField(blank=True, null=True)

    def __str__(self):
        return self.category.title

    class Meta:
        verbose_name = 'Տեսադարան'
        verbose_name_plural = 'Տեսադարան'


class BlogCategory(CustomModel):
    meta_title = models.CharField(max_length=300, blank=True, null=True)
    meta_description = models.TextField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=255, unique=True, db_index=True, verbose_name='Բաժնի անուն')
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True,verbose_name='Հղում')
    breadcrumb_text = models.TextField(blank=True, null=True, verbose_name='breadcrumb -ի տեքստ')
    breadcrumb_image = CustomLogoField(blank=True, null=True, verbose_name='breadcrumb -ի նկար')
    my_order = models.PositiveIntegerField(default=0, verbose_name='Դասավորել')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Բլոգի բաժին'
        verbose_name_plural = 'Բլոգի բաժիններ'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_generator(self.name, self.__class__)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_category_details', kwargs={'slug': self.slug})

class Blog(CustomModel):
    category = models.ForeignKey(BlogCategory,
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True, verbose_name='Բաժին')
    title = models.CharField(max_length=255,
                             verbose_name='Նյութի վերնագիր')
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name='Հղում')
    image = CustomLogoField(blank=True, null=True)
    short_description = RichTextUploadingField(verbose_name='Հակիրճ նկարագիր', blank=True, null=True)
    large_description = RichTextUploadingField(verbose_name='Ամբողջական նկարագիր', blank=True, null=True)
    meta_title = models.CharField(max_length=500, blank=True)
    meta_description = models.TextField(blank=True, null=True)
    views_count = models.PositiveIntegerField(default=0, editable=False)
    my_order = models.PositiveIntegerField(default=0, verbose_name='Դասավորել')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_generator(self.title, self.__class__)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Բլոգ'
        verbose_name_plural = 'Բլոգ'


class Service(CustomModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.FileField()
    short_description = RichTextUploadingField()
    large_description = RichTextUploadingField()
    meta_title = models.CharField(max_length=500, blank=True)
    meta_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('service_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_id = Blog.objects.last().id if Blog.objects.count() else 1
            self.slug = generate_slug(self.title, slug_id)

        super().save(*args, **kwargs)


class AboutUsSocialIcons(models.Model):
    about_us = models.ForeignKey(AboutUs, on_delete=models.CASCADE, blank=True, null=True)
    icon = CustomLogoField()
    text = models.CharField(max_length=255, verbose_name='Տեքստ', blank=True, null=True)
    url = models.CharField(verbose_name='Հղում', max_length=400)
    my_order = models.PositiveIntegerField(verbose_name='Դասավորել')

    def __str__(self):
        return self.text if self.text else str(self.pk)

    class Meta:
        verbose_name = '«Մեր մասին» էջի սոց. ցանցի լոգո'
        verbose_name_plural = '«Մեր մասին» էջի սոց. ցանցերի լոգոներ'
        ordering = ['my_order']
