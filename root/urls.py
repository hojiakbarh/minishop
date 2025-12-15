# root/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.sitemaps import ProductSitemap, CategorySitemap

sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

# Media files (development only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin panel sozlamalar
admin.site.site_header = 'Premium Store Admin'
admin.site.site_title = 'Admin Panel'
admin.site.index_title = 'Boshqaruv Paneli'