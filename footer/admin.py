from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin, TranslationTabularInline
from easy_select2 import select2_modelform
from singlemodeladmin import SingleModelAdmin

from .models import *

footerForm = select2_modelform(FooterItems)


@admin.register(CompanyInformation)
class CompanyInformationAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    list_display = ['name', 'text']


@admin.register(FooTerCategory)
class FooTerCategoryAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(FooterItems)
class FooterItemsAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    form = footerForm


@admin.register(SocialShareButtons)
class SocialShareButtonsAdmin(SortableAdminMixin, admin.ModelAdmin):

    def get_logo(self, obj):
        return mark_safe(f'<img src="{obj.icon.url}" height="60px" width="60px" />')

    get_logo.short_description = 'Լոգո'

    list_display = ['name', 'get_logo']


@admin.register(FooterInformationText)
class FooterInformationText(SingleModelAdmin, TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(FooterPartners)
class FooterPartnersAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):

    def get_logo(self, obj: FooterPartners):
        return mark_safe('<img src="%s" height="120px" width="120px" />' % obj.icon.url)

    get_logo.short_description = 'Լոգո'

    list_display = ['get_logo']


@admin.register(CardIcons)
class CardIconsAdmin(SortableAdminMixin, admin.ModelAdmin):

    def get_logo(self, obj: CardIcons):
        return mark_safe('<img src="%s" height="120px" width="120px" />' % obj.icon.url)

    get_logo.short_description = 'Լոգո'

    list_display = ['get_logo']
    readonly_fields = ['get_logo']


@admin.register(FooterMessengers)
class FooterMessengersAdmin(admin.ModelAdmin):

    def get_logo(self, obj):
        return mark_safe(f'<img src="{obj.icon.url}" height="60px" width="60px" />')

    get_logo.short_description = 'Լոգո'

    list_display = ['get_logo']