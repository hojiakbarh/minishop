# apps/views.py
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, get_object_or_404
from .models import Category, Product, ProductClick


class HomeView(ListView):
    """Bosh sahifa - Hero + Kategoriyalar + Featured mahsulotlar"""
    model = Category
    template_name = 'apps/home.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Featured mahsulotlar (oxirgi 12 ta)
        context['featured_products'] = Product.objects.select_related('category').all()[:12]
        return context


class ProductListView(ListView):
    """Mahsulotlar ro'yxati - Kategoriya bo'yicha filterlash"""
    template_name = 'apps/product-list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.select_related('category').all()
        category_slug = self.request.GET.get('category')

        if category_slug and category_slug != 'all':
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(
            product_count=Count('products')
        )
        context['active_category'] = self.request.GET.get('category', 'all')
        return context


class ProductDetailView(DetailView):
    """Mahsulot batafsil sahifasi"""
    model = Product
    template_name = 'apps/product-detail.html'
    context_object_name = 'product'

    def get_object(self):
        obj = super().get_object()
        # Ko'rishlar sonini oshirish
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # O'xshash mahsulotlar
        context['related_products'] = Product.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id).select_related('category')[:4]
        return context


def track_affiliate_click(request, product_id):
    """
    Affiliate link klikini tracking qilish va yo'naltirish
    Bu funksiya:
    1. Click statistikasini saqlaydi
    2. Admin panelda ko'rish mumkin
    3. Foydalanuvchini affiliate linkka yo'naltiradi
    """
    product = get_object_or_404(Product, id=product_id)

    # Click ma'lumotlarini saqlash
    ProductClick.objects.create(
        product=product,
        ip_address=request.META.get('REMOTE_ADDR', '0.0.0.0'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
    )

    # Mahsulot click statistikasini yangilash
    product.clicks += 1
    product.save(update_fields=['clicks'])

    # MUHIM: Affiliate linkga yo'naltirish
    # Bu yerda user AliExpress/Amazon/boshqa do'konga o'tadi
    return redirect(product.affiliate_link)



class SearchView(ListView):
    """Qidiruv sahifasi"""
    template_name = 'apps/search.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if query:
            return Product.objects.select_related('category').filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(keywords__icontains=query)
            )
        return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        context['query'] = query
        context['total_results'] = self.get_queryset().count()
        return context


def track_affiliate_click(request, product_id):
    """Affiliate link klikini tracking qilish"""
    product = get_object_or_404(Product, id=product_id)

    # Klikni saqlash
    ProductClick.objects.create(
        product=product,
        ip_address=request.META.get('REMOTE_ADDR', '0.0.0.0'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )

    # Mahsulot klik statistikasini yangilash
    product.clicks += 1
    product.save(update_fields=['clicks'])

    # Affiliate linkga yo'naltirish
    return redirect(product.affiliate_link)