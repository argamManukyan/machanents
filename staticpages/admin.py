from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin

from staticpages.models import StaticPages


@admin.register(StaticPages)
class StaffCategoryAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass
