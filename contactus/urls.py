from django.urls import path
from .views import contact_us
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('contact-us/', csrf_exempt(contact_us), name='contact_us')
]