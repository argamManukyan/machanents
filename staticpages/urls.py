from django.urls import path

from .views import staticpages

urlpatterns = [
    path('<slug>/', staticpages, name='staticpages')
]