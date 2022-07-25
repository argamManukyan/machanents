from django.contrib import admin
from .models import Wish,WishItem

admin.site.register(WishItem)
admin.site.register(Wish)