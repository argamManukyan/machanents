from modeltranslation.translator import TranslationOptions, register


from .models import DonationHomepageText, DonationCurrencies


@register(DonationHomepageText)
class DonationHomepageTextTranslate(TranslationOptions):
    fields = ['text', 'title']

#
# @register(DonationCurrencies)
# class DonationCurrenciesTranslate(TranslationOptions):
#     fields = ['name']

