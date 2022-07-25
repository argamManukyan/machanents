from modeltranslation.translator import TranslationOptions, register


from .models import VideoCategory


@register(VideoCategory)
class VideoCategoryTrans(TranslationOptions):
    fields = ['meta_title', 'meta_description', 'breadcrumbs_text', 'name']