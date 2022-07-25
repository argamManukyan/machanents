from django.urls import path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('', TemplateView.as_view(template_name='shop/empty.html'), name='index'),
    path('index/', HomeView.as_view(), name='home'),
    path('category/<slug>/', CategoryView.as_view(), name='category_details'),
    path('products/<slug>/', csrf_exempt(ProductView.as_view()), name='product_details'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('search/', ajaxSearch, name='search'),
    path('result/', SearchListView.as_view(), name='result'),
    path('offer/', ProductListView.as_view(), name='offers'),
    path('products/', AllProductListView.as_view(), name='products_all'),
    
    path('artists/', authors, name='authors'),
    path('artists/<slug>/', author_categories, name='author_categories'),
    path('artist/<slug>/', author_details, name='author_details'),
    path('reviews/', reviews_list, name='reviews'),
]
