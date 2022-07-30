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
    list_display = ['product_image', 'title', 'price', 'sale', 'product_code']
    search_fields = ['title', 'product_code']
    list_filter = ['category']
    readonly_fields = ['product_image']

    def product_image(self, obj):
        return mark_safe('<img src="{}" height="80px" width="90px" />'.format(obj.main_photo.url))
    product_image.short_description = 'Image'

admin.site.register(Product, ProductModelAdmin)


class CategoryModelAdmin(DraggableMPTTAdmin, TabbedDjangoJqueryTranslationAdmin):
    pass


admin.site.register(Category, CategoryModelAdmin)

# admin.site.register(Slider, TabbedDjangoJqueryTranslationAdmin)
admin.site.register(FilterField, TabbedDjangoJqueryTranslationAdmin)
admin.site.register(FilterValue, TabbedDjangoJqueryTranslationAdmin)
admin.site.register(Color, TabbedDjangoJqueryTranslationAdmin)
# admin.site.register(OurAdvantages, TabbedDjangoJqueryTranslationAdmin)
admin.site.register(RatingProduct)
admin.site.register(Rating)


class SingleModelAdminMixin(SingleModelAdmin, TabbedDjangoJqueryTranslationAdmin):
    pass

admin.site.register(HomepageUnderSliderText, SingleModelAdminMixin)
admin.site.register(AboutUsHomePageText, SingleModelAdminMixin)

admin.site.register(ProductReviews)


class SortableMixin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass

admin.site.register(Authors, SortableMixin)
admin.site.register(AuthorCategories, SortableMixin)
# admin.site.register(PrivacyPolicy, SingleModelAdminMixin)
# admin.site.register(DeliveryAndPayMent, SingleModelAdminMixin)
# admin.site.register(SpecialOfferBanner, TabbedDjangoJqueryTranslationAdmin)