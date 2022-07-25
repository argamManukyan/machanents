from shop.models import Category

from django.template import Library

register = Library()


@register.simple_tag
def categories():
    return Category.objects.filter(parent__isnull=True)
