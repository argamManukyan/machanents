from modeltranslation.translator import register, TranslationOptions
from .models import GalleryCategory, \
    AboutUs, FAQ, Blog, Service, BlogCategory, AboutUsSocialIcons


@register(AboutUs)
class AboutUsTranslationOptions(TranslationOptions):
    fields = (
        'meta_description', 'meta_title', 'title', 'breadcrumbs_text'
    )


@register(AboutUsSocialIcons)
class AboutUsSocialIconsTranslateOptions(TranslationOptions):
    fields = ['text']

@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'short_description',
        'large_description',
        'meta_title',
        'meta_description',
    )

@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'short_description',
        'large_description',
        'meta_title',
        'meta_description',
    )

@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')


@register(GalleryCategory)
class GalleryCategoryTranslationOptions(TranslationOptions):
    fields = ('title','meta_title', 'meta_description','breadcrumb_text')


@register(BlogCategory)
class BlogCategoryTrans(TranslationOptions):
    fields = ('name', 'meta_title', 'meta_description', 'breadcrumb_text')