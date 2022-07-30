from django.contrib import admin
from django.utils.html import format_html
from flatpages.forms import GalleryUploadForm
from .models import FAQ, AboutUs, Blog, Gallery, GalleryCategory, Service, BlogCategory, AboutUsSocialIcons
from singlemodeladmin import SingleModelAdmin
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin


@admin.register(AboutUs)
class AboutUsAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(AboutUsSocialIcons)
class AboutUsSocialIconsAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass


# admin.site.register(Blog, TabbedDjangoJqueryTranslationAdmin)
admin.site.register(FAQ, TabbedDjangoJqueryTranslationAdmin)
admin.site.register(Service, TabbedDjangoJqueryTranslationAdmin)


class GalleryImageTabularInline(admin.TabularInline):
    model = Gallery
    extra = 4


class GalleryImagesAdmin(admin.ModelAdmin):
    form = GalleryUploadForm

    def save_model(self, request, obj, form, change):
        obj.save()
        img_list = request.FILES.getlist('image')[:-1]
        for i in img_list:
            Gallery.objects.create(category_id=obj.category.id, image=i)

    def image_tag(self, obj):
        return format_html(f'<img src="{obj.image.url}" style="width:150px;height:150px;margin-right:10px" /> ')

    image_tag.short_description = 'Image'

    list_display = ['image_tag', 'category']


admin.site.register(Gallery, GalleryImagesAdmin)


class CategoryGalleryImagesAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass


admin.site.register(GalleryCategory, CategoryGalleryImagesAdmin)

@admin.register(BlogCategory, Blog)
class SortableElementAdmin(SortableInlineAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass
