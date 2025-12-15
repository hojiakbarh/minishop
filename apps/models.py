from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import Model
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

from django.utils import timezone
# Create your models here.

class CustomerUser(UserManager):
    def _create_user_object(self,email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        return user

    def create_user(self,email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user( email, password, **extra_fields)

    def create_superuser(self,email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        user = self._create_user_object(email, password, **extra_fields)
        user.save(using=self._db)
        return user





class BaseSlugModel(models.Model):
    """Slug avtomatik yaratish uchun bazaviy model"""
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    name = models.CharField(max_length=255, verbose_name='Nomi')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while self.__class__.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(BaseSlugModel):
    """Mahsulot kategoriyalari"""
    icon = models.ImageField(
        upload_to='category_icons/',
        blank=True,
        null=True,
        verbose_name='Rasm'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Tavsif'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'
        ordering = ['name']


class Product(BaseSlugModel):
    """Mahsulotlar"""
    image = models.ImageField(
        upload_to='products/',
        verbose_name='Rasm'
    )
    description = RichTextUploadingField(verbose_name='Tavsif')
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Narx'
    )
    affiliate_link = models.URLField(
        max_length=500,
        verbose_name='Affiliate havola'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Kategoriya'
    )

    # SEO maydonlari
    meta_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='SEO sarlavha'
    )
    meta_description = models.TextField(
        blank=True,
        verbose_name='SEO tavsif'
    )
    keywords = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Kalit so\'zlar'
    )

    # Statistika
    views = models.PositiveIntegerField(default=0, verbose_name='Ko\'rishlar')
    clicks = models.PositiveIntegerField(default=0, verbose_name='Kliklar')

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Avtomatik SEO maydonlar
        if not self.meta_title:
            self.meta_title = f"{self.name} - Arzon narxda xarid qiling"
        if not self.meta_description:
            from django.utils.html import strip_tags
            desc = strip_tags(self.description)[:150]
            self.meta_description = f"{desc}. Narxi: {self.price} so'm."
        super().save(*args, **kwargs)


class ProductClick(models.Model):
    """Affiliate link kliklarini tracking qilish"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='click_records'
    )
    ip_address = models.GenericIPAddressField(verbose_name='IP manzil')
    user_agent = models.TextField(blank=True, verbose_name='Brauzer')
    clicked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Klik'
        verbose_name_plural = 'Kliklar'
        ordering = ['-clicked_at']

    def __str__(self):
        return f"{self.product.name} - {self.clicked_at}"







