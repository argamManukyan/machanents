import json
from decimal import Decimal

import requests
import xmltodict
from cart.models import CartItem, Cart

from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import floatformat
from currencies.templatetags.currency import calculate
from currencies.models import Currency

from shop.models import ProductFeature
# from order.models import Order
from .context_processors import get_cart


class CartView(View):

    def get(self, request, **kwargs):
        cart = get_cart(request).get('cart')
        cart_items = cart.item.order_by('-id')
        
        return render(request, 'cart/cart.html', {'cart': cart, 'cart_items': cart_items})


class AddToCartView(View):

    def post(self, request, **kwargs):
        data = json.loads(request.body)
        product_id = data.pop('product_id')
        quantity = data.pop('quantity')
        values = ''.join(list(filter(lambda x: int(x) > 0, data.values())))

        cart: Cart = get_cart(request).get('cart')

        if cart.item.filter(product_id=product_id, features=values).exists():
            item = cart.item.filter(product_id=product_id, features__contains=values).first()
            from shop.models import Product
            if product := Product.objects.filter(id=product_id):
                if item.quantity + int(quantity) > product.first().stored_quantity:
                    return HttpResponse(status=200)
            item.quantity += int(quantity)
            item.save()
        else:
            cart.item.create(product_id=product_id, features=values, quantity=quantity)
        cart_total = sum(i.item_total_price for i in cart.item.all())
        cart.cart_total = cart_total
        cart.save()

        return JsonResponse({'cart_items': cart.item.count()}, status=200)


class RemoveFromBAsketView(View):

    def post(self, request):
        data = json.loads(request.body)

        item_id = data.get('id')
        cart = get_cart(request).get('cart')

        try:
            cart_item = CartItem.objects.get(id=item_id)
        except:
            return HttpResponse(status=400)

        cart_item.delete()

        cart_total = 0
        for i in cart.item.all():
            cart_total += i.item_total_price
        cart.cart_total = cart_total
        cart.save()

        return JsonResponse({'cart_total': floatformat(calculate(cart.cart_total, request.session['currency']), 0), 'items_count': cart.item.count()}, status=200)


class ChangeQuantityBasketView(View):

    def post(self, request):
        data = json.loads(request.body)

        item_id = data.get('id')
        quantity = data.get('quantity')
        cart = get_cart(request).get('cart')

        try:
            cart_item = CartItem.objects.get(id=item_id)
        except:
            return HttpResponse(status=400)

        cart_item.quantity = int(quantity)
        cart_item.save()
        cart_total = 0
        for i in cart.item.all():
            cart_total += i.item_total_price
        cart.cart_total = cart_total
        cart.save()

        return JsonResponse({'cart_total': floatformat(calculate(cart.cart_total, request.session['currency']), 0),
                             'item_total': floatformat(calculate(cart_item.item_total_price, request.session['currency']), 0)}, status=200)

@csrf_exempt
def setcurrency(request):
    """ Change currency view """

    last_link = request.META['HTTP_REFERER']
    url="http://api.cba.am/exchangerates.asmx?op=ExchangeRatesLatest"
    headers = {'Content-Type': 'text/xml; charset=utf-8'}
    body = """<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                    <ExchangeRatesLatest xmlns="http://www.cba.am/" />
                </soap:Body>
                </soap:Envelope>
                """

    response = requests.post(url,data=body,headers=headers)
    dict_data = xmltodict.parse(response.content)
    json_data = json.dumps(dict_data, indent=2)
    data = json.loads(json_data)
    rates = data['soap:Envelope']['soap:Body']['ExchangeRatesLatestResponse']['ExchangeRatesLatestResult']['Rates']['ExchangeRate']
    usd = None
    rub = None
    eur = None
    for i in rates:
        if i['ISO'] == 'USD':
            usd = i['Rate']
        elif i['ISO'] == 'EUR':
            eur = i['Rate']
        elif i['ISO'] == 'RUB':
            rub = i['Rate']

    for c in Currency.objects.all():
        if c.code == 'AMD':
            c.factor = 1
            c.save()
        elif c.code == 'USD':
            c.factor = float(1 / Decimal(usd))
            c.save()
        elif c.code == 'EUR':
            c.factor = float(1 / Decimal(eur))
            c.save()
        elif c.code == 'RUB':
            c.factor = float(1 / Decimal(rub))
            c.save()

    if request.method == 'POST':
        request.session['currency'] = request.POST['currency']
        return HttpResponseRedirect(last_link)
    return HttpResponseRedirect(last_link)
