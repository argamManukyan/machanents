from modeltranslation.translator import TranslationOptions, register
from . import models


@register(models.ContactUsPage)
class ContactUsPageTranslate(TranslationOptions):
    fields = ['meta_title', 'meta_description']


@register([models.ContactUsJoinUsData, models.FollowUsContactUs])
class ContactUsJoinAndFollowTranslation(TranslationOptions):
    fields = ['text']