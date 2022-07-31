from django.db import models
from shop.utils import CustomModel
from shop.models import Product, ProductFeature
from django.db.models import Sum


class CartItem(CustomModel):
    
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.IntegerField(default=0,blank=True,null=True)
    item_price = models.IntegerField(default=0,blank=True,null=True)
    item_total_price = models.IntegerField(default=0,blank=True,null=True)
    features = models.CharField(max_length=300, blank=True, null=True)
    uuid_field = models.CharField(max_length=200, blank=True, null=True)

    def save(self,*args,**kwargs):
        price_item = self.product.get_price
        self.item_price = price_item

        if values := [str(i) for i in self.features]:
            total_price = ProductFeature.objects.filter(
                id__in=values).values('id').aggregate(total=Sum('price'))['total'] if values else 0
            self.item_price += total_price
            self.features = ''.join(values)
        else:
            self.features = ''
        self.item_total_price = int(self.item_price) * int(self.quantity)

        # self.item_price = total_price + self.product.get_price
        # self.item_total_price = int(self.quantity) * int(self.item_price)
        # if len(ids) > 0:
        #     selected_products = ProductFeature.objects.filter(id__in=ids).values('field__title','value__title','price','id')
        #
        #     item_description = f'<span>Цена продукта: <i>{self.product.get_price} руб.</i></span><br />'
        #     for i in selected_products:
        #         if i['price'] > 0:
        #             item_description+= f'<span>{i["field__title"]}: <i>{i["value__title"]}- {i["price"]} руб.</i>  </span><br />'
        #         else:
        #             item_description+= f'<span>{i["field__title"]}: <i>{i["value__title"]}</i></span><br />'
        #     self.item_description = item_description
        return super().save(*args,**kwargs)

    def __str__(self):
        return str(self.pk)


class Cart(CustomModel):
    ip = models.CharField(max_length=25, blank=True)
    item = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pk)