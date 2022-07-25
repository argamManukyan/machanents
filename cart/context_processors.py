from django.conf import settings

from order.models import Order, OrderStatus
from .models import Cart


def get_cart(request):
    try:
        cart_id = request.session.get('cart_id')
        cart = Cart.objects.get(id=cart_id)
        request.session['cart_total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
        request.session['cart_total'] = cart.item.count()

    if not request.session.has_key('currency'):
        request.session['currency'] = settings.CURRENCY

    if request.session.has_key('pay_order'):
        order = Order.objects.get(id=request.session['pay_order'])

        if order.bank_order_status != 2:
            order.order_status = OrderStatus.objects.get(id=3) if OrderStatus.objects.filter(id=3).exists() else None
            order.save()

        del request.session['pay_order']

    if request.session.get('cart_two_id'):
        if request.get_full_path().split('/')[-2] != 'checkout':
            del request.session['cart_two_id']

    return {'cart': cart, 'cart_items': cart.item}
