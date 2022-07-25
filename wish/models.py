from django.db import models
from shop.models import Product


class WishItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return str(self.product.title)

class Wish(models.Model):

    items = models.ManyToManyField(WishItem)

    def __str__(self):
        return str(self.pk)