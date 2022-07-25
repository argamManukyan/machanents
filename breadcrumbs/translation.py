from modeltranslation.translator import register, TranslationOptions
from breadcrumbs.models import BreadcrumbTexts


@register(BreadcrumbTexts)
class BreadcrumbTextsTranslation(TranslationOptions):
    fields = ['breadcrumbs_text']