from datetime import datetime

from django.db.models import Q

from .models import FooTerCategory, CompanyInformation, SocialShareButtons, FooterMessengers, CardIcons, \
    FooterInformationText, FooterPartners


def footer_categories(request):
    """ Return all footer categories for iterate and show items of categories,
        and return the current year and site domain
    """

    year = datetime.now().year

    trigger = 'logged' if request.user.is_authenticated else 'guests'

    return {
        "footer_categories": FooTerCategory.objects.all(),
        "year": year,
        "trigger": trigger,
        "card_icons": CardIcons.objects.all(),
        "info_text": FooterInformationText.objects.first(),
        "footer_partners": FooterPartners.objects.all(),
        # "domain": request.get_host(),
        "site": f"{request.scheme}://{request.get_host()}",
        # "captcha_public": CAPTCHA_PUBLIC_KEY
    }


def company_information(request):
    """ Return company information """

    return {"company_information": CompanyInformation.objects.all()}


def footer_follow_icons(request):
    """ Return all following icons for the website """

    return {'footer_follow_icons': SocialShareButtons.objects.all()}


def footer_messengers(request):

    return {'footer_messengers': FooterMessengers.objects.all()}