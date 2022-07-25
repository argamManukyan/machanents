from django.urls import path

from .views import AboutUsView, BLogListView, BlogDetailView, GalleryListView, \
    GalleryCategoryDetailView, ServiceDetailView, ServiceListView, \
    FAQView, AboutUsCategoryView, BlogCategoryDetailView

urlpatterns = [
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('about-us/<slug>/', AboutUsCategoryView.as_view(), name='about_us_category'),
    path('gallery/', GalleryListView.as_view(), name='gallery_list'),
    path('gallery/<str:slug>/', GalleryCategoryDetailView.as_view(), name='gallery_details'),
    path('blog/', BLogListView.as_view(), name='blog_list'),
    path('blog-category/<slug>/', BlogCategoryDetailView.as_view(), name='blog_category_details'),
    path('blog/<slug>/', BlogDetailView.as_view(), name='blog_details'),
    path('service/', ServiceListView.as_view(), name='service_list'),
    path('service/<slug>/', ServiceDetailView.as_view(), name='service_details'),
    path('faq/', FAQView.as_view(), name='faq')

]
