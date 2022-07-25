import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from breadcrumbs.models import BreadcrumbTexts
from .models import *


def wishlist(request):
    try:
        wish_id = request.session.get('wish_id')
        wish = Wish.objects.get(id=int(wish_id))
        wish_items = WishItem.objects.filter(wish=wish)

    except:
        wish = Wish()
        wish.save()
        wish_id = wish.id
        request.session['wish_id'] = wish_id
        wish_items = WishItem.objects.filter(wish=wish)

    paginator = Paginator(wish_items, 12)
    page = request.GET.get('page')
    page_product = paginator.get_page(page)
    bread_content = BreadcrumbTexts.objects.filter(location='wishlist').first()

    return render(request, 'wish/wishlist.html', locals())


@csrf_exempt
def add_to_wish(request):
    try:
        wish_id = request.session.get('wish_id')
        wish = Wish.objects.get(id=int(wish_id))
        wish_items = WishItem.objects.filter(wish=wish)

    except:
        wish = Wish()
        wish.save()
        wish_id = wish.id
        request.session['wish_id'] = wish_id
        wish_items = WishItem.objects.filter(wish=wish)

    data = json.loads(request.body)
    product = int(data['product'])

    wish_item, created = WishItem.objects.get_or_create(wish=wish, product_id=product)

    if created:
        wish.items.add(wish_item)
        wish.save()
        return JsonResponse({'items_count': wish.items.count()}, status=201)
    else:
        wish.items.remove(wish_item)
        wish.save()
        wish_item.delete()
        return JsonResponse({'items_count': wish.items.count()}, status=200)
