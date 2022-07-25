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
    list_display = ['id', 'text']

    def get_icon(self, obj):
        if obj.icon:
            return mark_safe("<img src='{}' height='30px' width='30px' />".format(obj.icon.url))
        return ''

    get_icon.short_description = "Նկար"
    list_display += ['get_icon']


@admin.register(FooTerCategory)
class FooTerCategoryAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(FooterItems)
class FooterItemsAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    form = footerForm


@admin.register(SocialShareButtons)
class SocialShareButtonsAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass


@admin.register(FooterInformationText)
class FooterInformationText(SingleModelAdmin, TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(FooterPartners)
class FooterPartnersAdmin(SortableAdminMixin, admin.ModelAdmin):

    def get_logo(self, obj: FooterPartners):
        return mark_safe('<img src="%s" height="120px" width="120px" />' % obj.icon.url)

    get_logo.short_description = 'Լոգո'

    list_display = ['get_logo']
    readonly_fields = ['get_logo']


@admin.register(CardIcons)
class CardIconsAdmin(admin.ModelAdmin):

    def get_logo(self, obj: CardIcons):
        return mark_safe('<img src="%s" height="120px" width="120px" />' % obj.icon.url)

    get_logo.short_description = 'Լոգո'

    list_display = ['get_logo']
    readonly_fields = ['get_logo']