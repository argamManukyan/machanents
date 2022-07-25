from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from cart.views import AddToCartView, setcurrency
from order.views import BuyNowView, send_request
from shop.views import create_rating, get_donation_amounts
from wish.views import add_to_wish
from donation.views import send_donation
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin-test-site/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('add-rating/', create_rating, name='create_rating'),
    path('add_to_wish/', add_to_wish, name='add_to_wish'),
    path('setcurrency/', setcurrency, name='setcurrency'),
    path('add-to-cart/', csrf_exempt(AddToCartView.as_view())),
    path('buy-now/', csrf_exempt(BuyNowView.as_view())),
    path('send-request/', csrf_exempt(send_request)),
    path('get-donation-amounts/<obj_id>/', csrf_exempt(get_donation_amounts)),
    path('rosetta/', include('rosetta.urls')),
    path('send-donation/', csrf_exempt(send_donation), name='send_donation'),
    path('', include('shop.urls')),
    path('', include('cart.urls')),
    path('', include('wish.urls')),
    path('', include('order.urls')),
    path('', include('accounts.urls')),
    path('', include('flatpages.urls')),
    path('', include('videos.urls')),
    path('', include('contactus.urls')),
    path('', include('staticpages.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += i18n_patterns(
#     path('', include('shop.urls')),
#     path('', include('cart.urls')),
#     path('', include('wish.urls')),
#     path('', include('order.urls')),
#     path('', include('accounts.urls')),
#     path('', include('flatpages.urls')),
#     path('', include('videos.urls')),
#     prefix_default_language=False
# )

