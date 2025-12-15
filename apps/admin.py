# apps/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductClick


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_preview', 'product_count', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('slug', 'created_at', 'icon_preview_large')

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover; border-radius:8px;" />',
                obj.icon.url
            )
        return '-'

    icon_preview.short_description = 'Rasm'

    def icon_preview_large(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" width="200" style="border-radius:8px;" />',
                obj.icon.url
            )
        return '-'

    icon_preview_large.short_description = 'Rasm'

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = 'Mahsulotlar'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'price', 'views', 'clicks',
        'image_preview', 'created_at'
    )
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description', 'keywords')
    readonly_fields = ('slug', 'views', 'clicks', 'created_at', 'updated_at', 'image_preview_large')
    list_per_page = 20

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': (
            'name', 'slug', 'category', 'image', 'image_preview_large', 'description', 'price', 'affiliate_link')
        }),
        ('SEO sozlamalar', {
            'fields': ('meta_title', 'meta_description', 'keywords'),
            'classes': ('collapse',)
        }),
        ('Statistika', {
            'fields': ('views', 'clicks', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover; border-radius:8px;" />',
                obj.image.url
            )
        return '-'

    image_preview.short_description = 'Rasm'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="300" style="border-radius:8px;" />',
                obj.image.url
            )
        return '-'

    image_preview_large.short_description = 'Rasm'


@admin.register(ProductClick)
class ProductClickAdmin(admin.ModelAdmin):
    list_display = ('product', 'ip_address', 'clicked_at')
    list_filter = ('clicked_at',)
    search_fields = ('product__name', 'ip_address')
    readonly_fields = ('product', 'ip_address', 'user_agent', 'clicked_at')

    def has_add_permission(self, request):
        return False