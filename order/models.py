import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from shop.models import Product, ProductFeature
from shop.utils import CustomModel

User = get_user_model()


class Zonas(models.Model):
    name = models.CharField(max_length=150)
    round_maark = models.FloatField(blank=True, help_text='Կլորացվող թիվ , օրինակ USA -ի ժամանակ 0.5', null=True)
    every_rounded_price = models.FloatField(blank=True, help_text='Ամեն կլորացվող թվի համար հաշվարկվող գումար',
                                            null=True)
    fixed_price = models.FloatField(blank=True, null=True,
                                    help_text='Այս դաշտում նշում ենք այն արժեքը , որը համապատասխանում է մինիմալ միջակայքին։')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Զոնաներ'
        verbose_name_plural = 'Զոնաներ'


class Countries(models.Model):
    zonas = models.ForeignKey(Zonas, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=150)
    round_maark = models.FloatField(blank=True, help_text='Կլորացվող թիվ , օրինակ USA -ի ժամանակ 0.5', null=True)
    every_rounded_price = models.FloatField(blank=True, help_text='Ամեն կլորացվող թվի համար հաշվարկվող գումար',
                                            null=True)
    fixes_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Երկերներ'
        verbose_name_plural = 'Երկերներ'


class Regions(models.Model):
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    del_up = models.BooleanField(default=False, help_text='20 կգ ից բարձր առաքքումը գործում է։')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Մարզեր'
        verbose_name_plural = 'Մարզեր'


class FixedValues(models.Model):
    countries = models.ForeignKey(Countries, on_delete=models.CASCADE, null=True, blank=True)
    fixed_gramm = models.FloatField(help_text='Ֆիսված կգ ,օր՝ 3,5', verbose_name='Ֆիքսված քաշ')
    fixed_price = models.FloatField(help_text='Ֆիսված արժեք ,օր՝ 11․500 (արժեքը նշել ՀՀ դրամով)',
                                    verbose_name='Ֆիքսված արժեք')

    def __str__(self):
        return self.countries.name


class PaymentTypes(CustomModel):
    title = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.title


class OrderStatus(models.Model):
    title = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.title


class Delivery(models.Model):
    title = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.title


class Order(CustomModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, blank=True,
                             verbose_name="Հարցումն իրականացրած և գրանցված օգտատեր")
    first_name = models.CharField(max_length=80, blank=True, verbose_name="Անուն և ազգանուն")
    session_key = models.CharField(max_length=80, blank=True, null=True, editable=False)
    email = models.EmailField(blank=True, verbose_name='Էլ. հասցե')
    address = models.TextField(blank=True, verbose_name='Հասցե')

    phone = models.CharField(max_length=30, blank=True, verbose_name='Հեռ.')
    zip_code = models.CharField(max_length=50, blank=True, verbose_name='Փոստային դասիչ')
    notes = models.TextField(blank=True, verbose_name='Նշումներ')

    total_price = models.FloatField(default=0, blank=True, verbose_name='Ապրանքերի հանրագումար')
    delivery_price = models.FloatField(default=0, blank=True, verbose_name='Առաքման արժեք')
    all_total = models.FloatField(default=0, blank=True, verbose_name='Պատվերի ընդհանուր արժեք')

    payments = models.ForeignKey(PaymentTypes, on_delete=models.SET_NULL, null=True, blank=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, null=True, blank=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL,
                                     blank=True, null=True, verbose_name='Պատվերի կարգավիճակ')

    bank_order_status = models.IntegerField(null=True, blank=True, verbose_name='Բանկից ստացված պատասխան')
    bank_order_id = models.CharField(max_length=255, blank=True, verbose_name='Բանկային id')
    bank_message = models.CharField(max_length=255, blank=True, verbose_name='Բանկի պատասխանը տեսքստի տեսքով')
    is_paid = models.BooleanField(default=False, verbose_name='Վճարված է')
    hidden = models.BooleanField(default=False, editable=False)
    request_id = models.IntegerField(blank=True, null=True, editable=False)

    country_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Երկրի անուն")
    city_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Քաղաքի/մարզի անուն")
    language_code = models.CharField(max_length=2, blank=True, null=True, verbose_name='Պատվերի կատարման լեզու')
    curr_code = models.CharField(max_length=8, blank=True, verbose_name='Պատվերի կատարման արտարժույթի կոդ')

    def __str__(self):
        return f'{self.first_name} - {self.all_total}'

    class Meta:
        verbose_name = 'Պատվերներ'
        verbose_name_plural = 'Պատվերներ'
        ordering = ['-id']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=250)
    product_image = models.ImageField()
    product_price = models.FloatField(default=0.0)
    qty = models.IntegerField(default=0)
    item_total_price = models.FloatField(default=0)
    description = models.CharField(max_length=300, blank=True, null=True)
    uuid_field = models.CharField(max_length=255, blank=True, null=True, editable=False)
    tracking_number = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.order.first_name

    def save(self, *args, **kwargs):
        if self._state.adding:
            ids = list(self.description) if self.description else []
            item_about = [value.value.title for value in ProductFeature.objects.filter(id__in=ids)] if ids else []
            item_about = ' (' + ',  '.join(item_about) + ')' if item_about else ''

            self.product_name = self.product_name + item_about

        self.item_total_price = self.qty * self.product_price
        super().save(*args, **kwargs)


class ProductRequest(CustomModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=80, blank=True, verbose_name='Անուն և ազգանուն')
    session_key = models.CharField(max_length=80, blank=True, null=True, editable=False)
    email = models.EmailField(blank=True, verbose_name='Էլ. փոստ')

    address = models.TextField(blank=True, verbose_name='Հասցե')
    notes = models.TextField(blank=True, verbose_name='Նշումներ')

    phone = models.CharField(max_length=30, blank=True, null=True, verbose_name='Հեռ.')
    zip_code = models.CharField(max_length=50, blank=True, verbose_name="Փոստային դասիչ")

    total_price = models.FloatField(default=0, blank=True, verbose_name="Ապրանքների արժեքների հանրագումար")
    delivery_price = models.FloatField(default=0, blank=True, verbose_name='Առաքման արժեք')
    all_total = models.FloatField(default=0, blank=True, verbose_name="Պատվերի վերջնական արժեք")

    payments = models.ForeignKey(PaymentTypes, on_delete=models.SET_NULL, null=True, blank=True, editable=False)
    delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    country_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Երկրի անունը")
    city_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Քաղաքի/մարզի անունը")

    is_exists = models.BooleanField(default=False, verbose_name='Թույլատրելի է վճարման',
                                    help_text='Ակտիվացնելով այս դաշտը հարցումը հասանելի կլինի վճարման')
    is_expired = models.BooleanField(default=False, editable=False, verbose_name="Պատվերը ժամկետանց է")
    curr_code = models.CharField(max_length=5, default='AMD',
                                 blank=True, null=True, verbose_name="Արտարժությթի կոդ",
                                 help_text='Հարցումը կատարվել է նշված արտարժույթով')
    description = RichTextUploadingField(blank=True, null=True,
                                         verbose_name="Ադմինի կողմից կատարվող նշումներ")

    @property
    def expired_order(self):
        return self.created_at > timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return f'{self.first_name} - {self.all_total}'

    def save(self, *args, **kwargs):
        generated_total = ProductRequestItem.objects.filter(
            models.Q(available_quantity__isnull=False) |
            models.Q(available_quantity=0), request=self).distinct().aggregate(total=models.Sum('item_total_price'))['total'] or 0

        self.total_price = generated_total
        self.all_total = self.total_price + self.delivery_price

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ապրանքի հարցում'
        verbose_name_plural = 'Ապրանքների հարցումներ'
        ordering = ['-id']


class ProductRequestItem(models.Model):
    request = models.ForeignKey(ProductRequest, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    item_total_price = models.FloatField(default=0, verbose_name='Ընդհանուր արժեք')
    product_price = models.FloatField(default=0, verbose_name='Ապրանքի գին')
    product_image = models.FileField(blank=True, null=True, verbose_name='Ապրանքի նկար')
    qty = models.IntegerField(default=1, verbose_name='Պատվիրված քանակություն')
    available_quantity = models.PositiveIntegerField(blank=True, null=True, verbose_name='Առկա քանակություն')
    tracking_number = models.CharField(max_length=30, blank=True, null=True, verbose_name='Թրեքինգ կոդ')
    product_name = models.CharField(max_length=255, verbose_name='Ապրանքի անուն')
    product_code = models.CharField(max_length=80, blank=True, null=True, verbose_name='Ապրանքի կոդ')
    _product_id = models.CharField(max_length=80, blank=True, null=True, verbose_name='Ապրանքի Id')
    features = models.CharField(max_length=300, blank=True, null=True)
    send_email = models.BooleanField(default=False, verbose_name='Ուղարկել առաքանու կոդը էլ. հասցեին')
    uuid_field = models.CharField(max_length=200, blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):

        if self._state.adding:
            ids = list(self.features)

            item_about = [value.value.title for value in ProductFeature.objects.filter(id__in=ids)] if ids else []
            item_about = ' (' + ',  '.join(item_about) + ')' if item_about else ''
            self.product_name = self.product_name + item_about

        if isinstance(self.available_quantity, (int, float)):
            self.item_total_price = self.available_quantity * self.product_price
            order_id = None
            av_qty = ProductRequestItem.objects.get(id=self.id)
            order_item = OrderItem.objects.filter(uuid_field__iexact=self.uuid_field)
            # modifying order total price=
            if order_item:
                order_item = order_item.first()
                order_id = order_item.order_id
                order_item.tracking_number = self.tracking_number or ''
                order_item.qty = self.available_quantity
                order_item.save()

            if order := Order.objects.filter(id=order_id).first():

                price = OrderItem.objects.filter(
                    order_id=order_id).aggregate(sumprice=models.Sum('item_total_price'))['sumprice']

                order.total_price = price
                order.all_total = price + order.delivery_price
                order.save(update_fields=['all_total', 'total_price'])

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)

    def clean(self):
        super().clean()
        if self.available_quantity and self.available_quantity > self.qty:
            raise ValidationError({'available_quantity': "Առկա քանակությունը պետք է փոքր կամ "
                                                     "հավասար լինի պատվիրված քանակությանը"})


def post_save_requested_items_total_price(sender, instance: ProductRequestItem, created, *args, **kwargs):

    if req_obj := ProductRequest.objects.filter(productrequestitem=instance).first():
        for item in req_obj.productrequestitem_set.filter(available_quantity__isnull=False):
            if order_item := OrderItem.objects.filter(uuid_field__iexact=item.uuid_field):
                order_item = order_item.first()
                order_item.qty = item.available_quantity
                order_item.save()

        req_obj.total_price = req_obj.productrequestitem_set.aggregate(
            total=models.Sum('item_total_price'))['total'] or 0

        req_obj.all_total = req_obj.total_price + req_obj.delivery_price
        req_obj.save()


post_save.connect(post_save_requested_items_total_price, sender=ProductRequestItem)
