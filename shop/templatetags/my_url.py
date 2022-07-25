from django.template import Library

register = Library()

@register.simple_tag
def my_url(value, field, urlencode=None):
    url = '?{}={}'.format(field, value)

    if urlencode:
        querystring = urlencode.split('&')
        
        filtered_queryset = filter(lambda p: p.split('=')[0] != field, querystring)
        encode_qs = '&'.join(filtered_queryset)
        if encode_qs:
            url += '&{}'.format(encode_qs)
    return url


