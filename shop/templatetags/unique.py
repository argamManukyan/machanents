from django.db.models import Q, Min, Max
from django.template import Library

from cart.models import Cart
from order.models import ProductRequest, Order
from shop.models import ProductFeature, FilterValue

register = Library()


@register.filter
def unique(qs):
    qs_array = []
    for i in qs:
        if not i.value in qs_array:
            qs_array.append(i.value)
    return qs_array


@register.filter
def return_values(values):
    values = list(values)
    """ this template filter  for return cart item features, gets values   """
    return ProductFeature.objects.filter(id__in=values)


@register.filter
def features(qs, product_id):
    return qs.filter(product_id=product_id).order_by('price')


@register.filter
def filter_feature(qs):
    return any(val['field__is_main'] for val in qs.values('field__is_main'))


@register.filter(name='range')
def range_numbers(num):
    return list(range(num, 0, -1))

@register.filter
def usdconverter(price):
    from currencies.utils import convert
    from django.template.defaultfilters import floatformat
    return floatformat(convert(price, 'AMD', 'USD'), 0)


@register.filter
def check_request(cart: Cart):
    return cart.item.filter(product__allowed_buying=False).count() > 0


@register.filter
def check_total(total_price, product_request: ProductRequest):
    if product_request.total_price < 1:
        return sum(i['item_total_price'] for i in product_request.productrequestitem_set.values('item_total_price'))
    return total_price


@register.filter
def check_all_total(all_total, product_request: ProductRequest):
    if product_request.total_price < 1:
        return \
            sum(i['item_total_price'] for i in
                product_request.productrequestitem_set.values('item_total_price')) + product_request.delivery_price
    return all_total


@register.filter
def get_min_val(item, category):
    list_ids_cat = [index.id for index in category.get_descendants(include_self=True)]

    f_values = FilterValue.objects.filter(Q(productfeature__product__category__in=list_ids_cat) |
                                          Q(productfeature__field__show_in_filters=True),
                                          Q(productfeature__field__in=[item.id]),
                                          Q(productfeature__field__two_inputs=True),
                                          Q(productfeature__value__isnull=False)).distinct()

    return f_values.aggregate(min_val=Min('productfeature__value__title'))['min_val'] or 0


@register.filter
def get_max_val(item, category):
    list_ids_cat = [index.id for index in category.get_descendants(include_self=True)]

    f_values = FilterValue.objects.filter(Q(productfeature__product__category__in=list_ids_cat) |
                                          Q(productfeature__field__show_in_filters=True),
                                          Q(productfeature__field__in=[item.id]),
                                          Q(productfeature__field__two_inputs=True),
                                          Q(productfeature__value__isnull=False)).distinct()

    return f_values.aggregate(max_val=Max('productfeature__value__title'))['max_val'] or 0


@register.filter
def filter_order(user, product_id):
    return Order.objects.filter(user_id=user.id, orderitem__product__in=[product_id], is_paid=True).exists()