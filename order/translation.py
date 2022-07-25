from modeltranslation.translator import register, TranslationOptions

from .models import Countries, Regions, Delivery, OrderStatus, PaymentTypes


@register(Countries)
class StateTranslation(TranslationOptions):
    fields = ['name']


@register(Regions)
class CountryTranslation(TranslationOptions):
    fields = ['name']


@register(Delivery)
class DeliveryTranslation(TranslationOptions):
    fields = ['title']


@register(OrderStatus)
class OrderStatusTranslation(TranslationOptions):
    fields = ['title']


@register(PaymentTypes)
class PaymentTypesTranslation(TranslationOptions):
    fields = ['title']
