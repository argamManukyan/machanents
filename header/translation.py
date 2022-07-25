from modeltranslation.translator import register, TranslationOptions
from .models import Header, Slider


@register(Header)
class HeaderTranslation(TranslationOptions):
    fields = ['name', 'url']


@register(Slider)
class SliderTrans(TranslationOptions):
    fields = ['text', 'url']