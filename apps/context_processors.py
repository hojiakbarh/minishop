# apps/context_processors.py
from apps.models import Category

def categories_processor(request):
    """
    Barcha sahifalarda kategoriyalarni ko'rsatish uchun
    """
    return {
        'all_categories': Category.objects.all()
    }