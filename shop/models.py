import uuid

from django.db import models
from django.urls import reverse
from datetime import timedelta

from django.utils import timezone
from unidecode import unidecode
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from core.utils import CustomLogoField, CustomMetaModel
from .utils import CustomModel


User = get_user_model()

def generate_slug(name, id):
    return slugify(f'{unidecode(name)}-{str(id)}')


class Slider(CustomModel):
    """ Table of main slider """
    image_xl = models.FileField()
    image_ml = models.FileField()
    text = RichTextUploadingField()
    url = models.URLField(blank=True, null=True)
    my_order = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = _('Գլխավոր սլայդեր')
        ordering = ['my_order']
        verbose_name_plural = verbose_name


class Category(MPTTModel):
    """ Category table """

    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True, max_length=300)
    title = models.CharField(max_length=255, verbose_name='Բաժնի անուն')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Հղում')
    breadcrumb_image = models.ImageField(upload_to='category/', blank=True,
                                         null=True)
    breadcrumb_text = RichTextUploadingField(blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,verbose_name='Հայրական բաժին',
                            null=True, blank=True, related_name='children')
    show_in_homepage = models.BooleanField(default=False, verbose_name='Ցուցադրել գլխավոր էջում')
    image = models.FileField(upload_to='category_image/', verbose_name='Նկար',
                             blank=True, default='category_image/default.jpg')
    show_in_header = models.BooleanField(default=False, verbose_name='Ցուցադրել header -ում')

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_details', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = _('Բաժին')
        verbose_name_plural = _('Բաժիններ')

    def save(self, *args, **kwargs):

        if not self.slug:
            slug_id = Category.objects.last().id if Category.objects.count() else 1
            self.slug = generate_slug(self.title, slug_id)

        return super().save(*args, **kwargs)

    def __str__(self):

        k = self.parent
        current_category = [self.title]

        while k is not None:
            current_category.append(k.title)
            k = k.parent
        return '-->'.join(current_category[::-1]) or ''


class FilterField(CustomModel):
    """ Filter field table """
    category = models.ManyToManyField(Category, verbose_name='Բաժին/Բաժիններ')
    filter_key = models.CharField(max_length=150,
                                  unique=True, blank=True, editable=False)
    title = models.CharField(max_length=255, unique=True, verbose_name='Դաշտի անուն')
    two_inputs = models.BooleanField(default=False, verbose_name='2 մուտքային դաշտ',
                                     help_text='Այս պարամետրը նախատեսված է չափման միավորների համար')
    show_in_filters = models.BooleanField(default=False, verbose_name='Ցուցադրել ֆիլտրերում')
    is_main = models.BooleanField(default=False, verbose_name='Հիմնական դաշտ',
                                  help_text='Այս դաշտից կախված փոփոխվում է ապրանքի տիպի արժեքը')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.filter_key:
            self.filter_key = unidecode(self.title.replace(' ', '_'))

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Ֆիլտրացման դաշտ')
        verbose_name_plural = _('Ֆիլըտրացման դաշտեր')


class FilterValue(CustomModel):
    """ Filter value table """

    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Ֆիլտրվող արժեքներ')
        verbose_name_plural = _('Ֆիլտրվեղ արժեքներ')


class Color(CustomModel):
    """ Color table """
    title = models.CharField(max_length=255)
    color_code = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Գույն')
        verbose_name_plural = _('Գույներ')


class AuthorCategories(CustomMetaModel):
    name = models.CharField(max_length=255, unique=True, verbose_name='Անուն')
    slug = models.SlugField(blank=True, null=True, verbose_name='Հղում')
    breadcrumbs_text = models.TextField(blank=True, null=True, verbose_name='breadcrumb -ի տեքստ')
    breadcrumbs_image = CustomLogoField(blank=True, null=True, verbose_name='breadcrumb -ի նկար')
    my_order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_id = self.__class__.objects.last().id + 1 if self.__class__.objects.count() else 1
            self.slug = generate_slug(self.name, slug_id)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Բաժին'
        verbose_name_plural = 'Արտիստների բաժիններ'
        ordering = ['my_order']

    def get_absolute_url(self):
        return reverse('author_categories', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Authors(CustomMetaModel):
    category = models.ManyToManyField(AuthorCategories, blank=True, related_name='authors')
    name = models.CharField(verbose_name='Անուն ազգանուն', max_length=255)
    slug = models.SlugField(blank=True, null=True, verbose_name='Հղում')
    image = CustomLogoField(blank=True, null=True)
    text = RichTextUploadingField(verbose_name='Հեղինակի մասին', blank=True, null=True)
    my_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _('Արտիստ')
        verbose_name_plural = _('Արտիստներ')
        ordering = ['my_order']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_id = self.__class__.objects.last().id + 1 if self.__class__.objects.count() else 1
            self.slug = generate_slug(self.name, slug_id)

        super().save(*args, **kwargs)


class Product(CustomModel):
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True, max_length=300)

    category = models.ManyToManyField(Category, verbose_name='Բաժին/բաժիններ')
    author = models.ForeignKey(Authors, on_delete=models.CASCADE,
                               verbose_name='Հեղինակ',
                               null=True, blank=True, related_name='author_products')
    title = models.CharField(max_length=255, verbose_name='Անուն')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Հղում')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='Գույն')
    product_code = models.CharField(max_length=20, blank=True, verbose_name='Ապրանքի կոդ', unique=True)
    product_id = models.CharField(blank=True, null=True, max_length=12, unique=True)
    short_description = RichTextUploadingField(blank=True, verbose_name='Հակիրճ նկարագիր')
    large_description = RichTextUploadingField(blank=True, verbose_name='Ամբողջական նկարագիր')

    price = models.PositiveIntegerField(default=0, verbose_name='Գին')
    sale = models.PositiveIntegerField(default=0, verbose_name='Զեղչված գին')
    main_photo = models.FileField(upload_to='product/', verbose_name='Հիմնական նկար')
    my_order = models.PositiveIntegerField(default=0)
    finally_price = models.PositiveIntegerField(default=0, editable=False)
    best_seller = models.BooleanField(default=False, verbose_name='Բեսթ սելլեր')
    show_in_homepage = models.BooleanField(default=False, verbose_name='Ցուցադրել գլխավոր էջում')
    weight = models.FloatField(verbose_name='Ապրանքի քաշ', default=1,
                               help_text='Քաշը նշել կգ -ով, որպեսզի հստակ հաշվարկ կատարվի')

    stored_quantity = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    allowed_buying = models.BooleanField(default=True, verbose_name='Թույլատրելի է ուղիղ վաճառքի')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if not self.slug:
            slug_id = Product.objects.last().id + 1 if Product.objects.count() else 1
            self.slug = generate_slug(self.title, slug_id)

        # Finally price generation
        self.finally_price = self.sale if self.sale > 1 else self.price
        if self.stored_quantity == 0:
            self.allowed_buying = False

        self.product_id = uuid.uuid4().hex[:8]

        return super().save(*args, **kwargs)

    @property
    def is_new(self):
        """ Check is it product added not more than 15 days """
        return self.created_at > timezone.now() - timedelta(days=15)

    def get_absolute_url(self):
        return reverse('product_details', kwargs={'slug': self.slug})

    @property
    def get_sale_percent(self):
        """ Calculating sale percent """
        if self.sale < 1:
            return 0
        else:
            return float('{:.1f}'.format((self.price - self.sale) / (self.price / 100)))

    @property
    def get_price(self):
        return self.sale if self.sale > 0 else self.price

    class Meta:
        verbose_name = _('Ապրանք')
        verbose_name_plural = _('Ապրանքներ')
        ordering = ['my_order']


class ProductReviews(CustomModel):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL,
                               null=True, blank=True, verbose_name='ՈՒղարկող')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                null=True, blank=True, verbose_name='Ապրանք')
    text = models.TextField(verbose_name='Տեքստ')
    location = models.CharField(max_length=200,
                                blank=True,
                                null=True, verbose_name='Ուղարկողի Հասցե')
    hide = models.BooleanField(default=True, verbose_name='Չցուցադրել')
    image = models.FileField(blank=True, null=True, verbose_name='Նկար')
    rating = models.PositiveSmallIntegerField(verbose_name='Գնահատական')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Կարծիք ապրանքի վերաբերյալ'
        verbose_name_plural = 'Կարծիքներ ապրանքնրի վերաբերյալ'


class ProductImage(CustomModel):
    """ Product images table """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.FileField(upload_to='product/')
    my_order = models.PositiveIntegerField(default=0, )
    
    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = _('Ապրանքի նկար')
        verbose_name_plural = _('Ապրանքի նկարներ')
        ordering = ['my_order']


class ProductFeature(CustomModel):
    """ Product feature table """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    field = models.ForeignKey(FilterField, on_delete=models.SET_NULL, null=True)
    value = models.ForeignKey(FilterValue, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(default=0)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f'{self.product.title} - {self.value}'

    class Meta:
        verbose_name = _('Ապրանքի չափորոշիչ')
        verbose_name_plural = _('Ապրանքի չափորոշիչներ')
        ordering = ['my_order']


class Rating(CustomModel):
    """ Rating values model """
    value = models.IntegerField(default=1, unique=True)

    def __str__(self):
        return str(self.value)


class RatingProduct(CustomModel):
    """ Rating of products model """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.SET_NULL, null=True, blank=True)
    ip = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.product.title} - {self.rating}'


class ViewedProducts(CustomModel):
    """ Viewed product table """

    session_key = models.CharField(max_length=255, blank=True, null=True)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return str(self.pk)


class OurAdvantages(CustomModel):
    """  Our advantages table, this table haven't an absolute url"""

    icon = models.FileField(upload_to='advantages/')
    title = models.CharField(max_length=155, blank=True)
    my_order = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        ordering = ['my_order']

    def __str__(self):
        return self.title


class SpecialOfferBanner(CustomModel):
    """ Special offers """

    product_url = models.URLField()
    title = models.CharField(max_length=255)
    text = RichTextUploadingField(blank=True)
    image = models.FileField()

    def __str__(self):
        return str(self.pk)


class AboutUsHomePageText(CustomModel):
    text = RichTextUploadingField(blank=True, null=True, verbose_name='Տեքստ')
    image = CustomLogoField(blank=True, null=True)

    def __str__(self):
        return "Մեր մասին - Գլխավոր էջ"

    class Meta:
        verbose_name = 'Մեր մասին - Գլխավոր էջ'
        verbose_name_plural = 'Մեր մասին - Գլխավոր էջ'


class PrivacyPolicy(CustomModel):

    text = RichTextUploadingField()

    def __str__(self):
        return str(self.pk)


class TermsAndConditions(CustomModel):

    text = RichTextUploadingField()

    def __str__(self):
        return str(self.pk)


class DeliveryAndPayMent(CustomModel):

    text = RichTextUploadingField()

    def __str__(self):
        return str(self.pk)


class HomepageUnderSliderText(models.Model):
    text = RichTextUploadingField()

    def __str__(self):
        return 'Գլխավոր էջի տեքստ'

    class Meta:
        verbose_name = 'Գլխավոր էջի տեքստ'
        verbose_name_plural = 'Գլխավոր էջի տեքստ'

