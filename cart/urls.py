from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('change-qty/', csrf_exempt(ChangeQuantityBasketView.as_view())),
    path('remove-basket/', csrf_exempt(RemoveFromBAsketView.as_view())),
]
