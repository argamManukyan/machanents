from django.db.models import Q
from django.template import Library

register = Library()


@register.filter
def filter_links(qs, trigger):
    return qs.filter(
        Q(is_auth__isnull=True) | Q(is_auth=trigger)
    )
