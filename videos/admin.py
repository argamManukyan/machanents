from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin


from .models import Video, VideoCategory


@admin.register(Video)
class VideoAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass


@admin.register(VideoCategory)
class VideoAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass

