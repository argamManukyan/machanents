from django.contrib import admin
from .models import BreadcrumbTexts
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin

admin.site.register(BreadcrumbTexts, TabbedDjangoJqueryTranslationAdmin)
