from django.shortcuts import render, get_object_or_404

from staticpages.models import StaticPages


def staticpages(request, slug):
    page = get_object_or_404(StaticPages, slug=slug)
    return render(request, 'shop/privacy_policy.html', context={"page": page})
