from django.urls import path

from .views import CheckoutView, OrderMoreView, BuyNowView, product_request


urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('order-more/', OrderMoreView.as_view(), name="order_more"),
    path('product-request/<session_key>/', product_request, name='product_request')
]
