from modeltranslation.translator import register, TranslationOptions

from .models import StaticPages


@register(StaticPages)
class StaticPagesTrans(TranslationOptions):
    fields = ['page_title', 'text']