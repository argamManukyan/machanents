from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin
from easy_select2 import select2_modelform
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin
from shop.models import Category, Color, FilterField, FilterValue, Product, ProductFeature, ProductImage, Rating, \
    RatingProduct, Slider, ProductReviews, \
    HomepageUnderSliderText, AboutUsHomePageText, Authors, AuthorCategories
from singlemodeladmin import SingleModelAdmin

ProductAutocompleteForm = select2_modelform(Product, attrs={'fields': ['id', 'title']})
FilterFieldAutocompleteForm = select2_modelform(FilterField, attrs={'fields': ['id', 'title']})
ProductFeatureForm = select2_modelform(ProductFeature, attrs={'fields': ['id', 'field__title', 'value__title']})


class ProductImageTabularInline(SortableInlineAdminMixin,admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductFeatureTabularInline(SortableInlineAdminMixin,admin.TabularInline,):
    model = ProductFeature
    extra = 0
    form = ProductFeatureForm


class ProductModelAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    inlines = [ProductImageTabularInline, ProductFeatureTabularInline]
    form = ProductAutocompleteForm
    list_display = ['product_image', 'title', 'price', 'sale', 'product_id']
    search_fields = ['title', 'product_code']
    list_filter = ['category']

    def product_image(self, obj):
        return mark_safe('<img src="{}" height="80px" width="90px" />'.format(obj.main_photo.url))
    product_image.short_description = 'Նկար'


admin.site.register(Product, ProductModelAdmin)


class CategoryModelAdmin(DraggableMPTTAdmin, TabbedDjangoJqueryTranslationAdmin):
    pass


admin.site.register(Category, CategoryModelAdmin)

# admin.site.register(Slider, TabbedDjangoJqueryTranslationAdmin)


@admin.register(FilterField)
class FilterFieldAutocompleteFormAdmin(TabbedDjangoJqueryTranslationAdmin):
    form = FilterFieldAutocompleteForm


admin.site.register(FilterValue, TabbedDjangoJqueryTranslationAdmin)
admin.site.register(Color, TabbedDjangoJqueryTranslationAdmin)
# admin.site.register(OurAdvantages, TabbedDjangoJqueryTranslationAdmin)
admin.site.register(RatingProduct)
admin.site.register(Rating)


class SingleModelAdminMixin(SingleModelAdmin, TabbedDjangoJqueryTranslationAdmin):
    pass

admin.site.register(HomepageUnderSliderText, SingleModelAdminMixin)
admin.site.register(AboutUsHomePageText, SingleModelAdminMixin)


class ProductReviewsAdmin(admin.ModelAdmin):
    list_display = ['sender', 'product', 'location']
    list_editable = ['hide']
    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" height="100px" width="100px" />')
        return ''

    def get_review(self, obj):
        if obj.review:
            return obj.review
        return ''

    get_image.short_description = 'Նկար'
    get_review.short_description = 'Կարծիք'
    list_display.extend(['get_image', 'get_review', 'hide'])


admin.site.register(ProductReviews, ProductReviewsAdmin)


class SortableMixin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass

admin.site.register(Authors, SortableMixin)
admin.site.register(AuthorCategories, SortableMixin)
# admin.site.register(PrivacyPolicy, SingleModelAdminMixin)
# admin.site.register(DeliveryAndPayMent, SingleModelAdminMixin)
# admin.site.register(SpecialOfferBanner, TabbedDjangoJqueryTranslationAdmin)