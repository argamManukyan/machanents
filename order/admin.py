from django.contrib import admin, messages
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin

from .models import Order, Countries, OrderItem, Regions, OrderStatus, PaymentTypes, Delivery, FixedValues, Zonas, \
    ProductRequest, ProductRequestItem

from adminsortable2.admin import SortableAdminMixin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget
from import_export import fields


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    readonly_fields = [
        'get_image',
        'product_name',
        'product_price',
        'qty',
        'item_total_price',
    ]
    exclude = ['description', 'product', 'product_image']
    extra = 0

    def get_image(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" height="100" width="100" />'.format(obj.product_image.url))
        return
    get_image.short_description = 'image'


class ProductRequestItemAdmin(admin.StackedInline):
    model = ProductRequestItem
    readonly_fields = [
        'get_image',
        # 'product_name',
        # 'product_code',
        # 'product_price',
        # 'qty',
        # 'item_total_price',

    ]

    exclude = ['product_image', 'features']
    extra = 0

    def get_image(self, obj):
        if obj.product_image:
            return format_html(f'<img src="{obj.product_image.url}" height="100" width="100" />')
        return
    get_image.short_description = 'image'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # list_display = ['id']
    # TODO: Refind the fileds names which will show
    inlines = [OrderItemAdmin]
    actions = ['refund_payment']
    #
    # @admin.action(description='Վերադարձնել գումարը')
    # def refund_payment(self, request, queryset):
    #     from .service import refund_price
    #
    #     refund_data = refund_price(queryset.first().id)
    #     if refund_data:
    #         queryset.update(order_status_id=6)
    #         messages.success(request, 'Գումարը հաջողությամբ հետ է վերադարձվել')
    #
    #     messages.error(request, 'Պրոցեսը ձախողվել է, փորձեք կրկին')
    #
    #     return queryset


class FixedValuesTabInline(admin.TabularInline):
    model = FixedValues
    extra = 1


class ZonaResource(ModelResource):
    zonas = fields.Field(attribute='zonas', column_name='zonas', widget=ForeignKeyWidget(Zonas, 'name'))

    class Meta:
        model = Countries


class RegionResource(ModelResource):
    country = fields.Field(attribute='country', column_name='country', widget=ForeignKeyWidget(Countries, 'id'))


class ExcellModelImport(TabbedDjangoJqueryTranslationAdmin, ImportExportActionModelAdmin):
    resource_class = ZonaResource
    inlines = [FixedValuesTabInline]
    search_fields = ['name']
    list_display = ['id', 'name']


class RegionsModelImport(TabbedDjangoJqueryTranslationAdmin, ImportExportActionModelAdmin):
    resource_class = RegionResource


admin.site.register(Zonas, ImportExportModelAdmin)
admin.site.register(Countries, ExcellModelImport)


class ProductRequestAdmin(admin.ModelAdmin):
    inlines = [ProductRequestItemAdmin]


admin.site.register(OrderStatus)
admin.site.register(Delivery)
admin.site.register(PaymentTypes)
admin.site.register(ProductRequest, ProductRequestAdmin)
admin.site.register(Regions, ImportExportModelAdmin)
admin.site.register(FixedValues, ImportExportModelAdmin)
