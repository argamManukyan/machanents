from django.urls import path
from .views import video_list, video_category

urlpatterns = [
    path('machanentsTV/', video_list, name='peri_tv'),
    path('machanentsTV/<slug>/', video_category, name='video_category')
]