from modeltranslation.translator import register, TranslationOptions
from .models import Category, Color, FilterField, FilterValue, Product, Slider, SpecialOfferBanner, TermsAndConditions, \
    DeliveryAndPayMent, PrivacyPolicy, OurAdvantages, HomepageUnderSliderText, AboutUsHomePageText, Authors, \
    AuthorCategories


@register(SpecialOfferBanner)
class SpecialOfferBannerTranslationOptions(TranslationOptions):
    fields = ('text', 'product_url', 'title')


@register([HomepageUnderSliderText, AboutUsHomePageText])
class SpecialOfferBannerTranslationOptions(TranslationOptions):
    fields = ('text',)


@register(Authors)
class SpecialOfferBannerTranslationOptions(TranslationOptions):
    fields = ('meta_title', 'meta_description', 'text', 'name')


@register(AuthorCategories)
class SpecialOfferBannerTranslationOptions(TranslationOptions):
    fields = ('meta_title', 'meta_description', 'breadcrumbs_text', 'name')


@register(Slider)
class SliderTranslationOptions(TranslationOptions):
    fields = ('text', 'url')


@register(OurAdvantages)
class OurAdvantagesTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(PrivacyPolicy)
class PrivacyPolicyranslationOptions(TranslationOptions):
    fields = ('text',)


@register(TermsAndConditions)
class TermsAndConditionsTranslationOptions(TranslationOptions):
    fields = ('text',)


@register(DeliveryAndPayMent)
class DeliveryAndPayMentTranslationOptions(TranslationOptions):
    fields = ('text',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'meta_title', 'meta_description', 'breadcrumb_text')


@register(FilterField)
class FilterFieldTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(FilterValue)
class FilterValueTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Color)
class ColorTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'short_description',
        'large_description',
        'meta_title',
        'meta_description',
    )
