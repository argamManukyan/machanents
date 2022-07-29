from modeltranslation.translator import register, TranslationOptions


from .models import *


@register(CompanyInformation)
class CompanyInformationTrans(TranslationOptions):
    fields = ['text', 'url', 'name']


@register(FooTerCategory)
class FooTerCategoryTrans(TranslationOptions):
    fields = ['name']


@register(FooterItems)
class FooterItemsTrans(TranslationOptions):
    fields = ['name', 'url']


@register(FooterInformationText)
class FooterItemsTrans(TranslationOptions):
    fields = ['text']


@register(FooterPartners)
class FooterPartnersTrans(TranslationOptions):
    fields = ['alt_title']


