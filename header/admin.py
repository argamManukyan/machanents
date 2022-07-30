from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin

from .models import Header, Slider


@admin.register(Header)
class HeaderAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(Slider)
class SliderAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):

    def get_xl_image(self, instance: Slider):
        return mark_safe('<img src="{}" height="120px" width="120px" />'.format(instance.image.url))

    get_xl_image.short_description = 'Նկար'

    def get_text(self, obj):
        if obj.text:
            return mark_safe(obj.text)

    get_text.short_description = 'Տեքստ'
    list_display = ['get_xl_image', 'get_text']