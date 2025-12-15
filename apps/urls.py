# apps/urls.py
from django.urls import path
from .views import (
    HomeView,
    ProductListView,
    ProductDetailView,
    SearchView,
    track_affiliate_click  # Yangi import
)

app_name = 'apps'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('search/', SearchView.as_view(), name='search'),

    # YANGI: Affiliate tracking
    path('go/<int:product_id>/', track_affiliate_click, name='track_click'),
]