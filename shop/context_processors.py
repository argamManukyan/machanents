from django.contrib.sites.shortcuts import get_current_site

from shop.models import Category


def home_path(request):
    if request.is_secure():
        prefix = 'https://' + get_current_site(request=request).domain
    else:
        prefix = 'http://' + get_current_site(request=request).domain
    header_categories = Category.objects.filter(show_in_header=True)

    return {'prefix': prefix, 'header_categories': header_categories}