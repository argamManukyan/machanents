from shop.models import Category
from .models import Header
from django.urls import resolve

from core.utils import generic_context_processor


def header_links(request):

    # trigger for check or uncheck activity for collections in header
    url_name = request.resolver_match.url_name
    check_collection = False
    if url_name in ['category_details', 'brand_details', 'brand_list']:
        check_collection = True

    return {
        "header_links": Header.objects.all(),
        'header_categories': Category.objects.filter(parent=None),
        'check_collection': check_collection
    }
