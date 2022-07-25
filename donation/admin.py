from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from adminsortable2.admin import SortableAdminMixin
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin


from .models import DonationCurrencies, DonationRanges, DonationHomepageText, Donations


@admin.register(DonationHomepageText)
class DonationHomepageContextAdmin(SingleModelAdmin, TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(DonationCurrencies)
class DonationCurrenciesAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass


admin.site.register(DonationRanges)
admin.site.register(Donations)
