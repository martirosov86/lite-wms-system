from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """
    Модель товара
    """
    name = models.CharField(_('name'), max_length=255)
    article = models.CharField(_('article'), max_length=100)
    barcode = models.CharField(_('barcode'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    
    # Связь с компанией
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='products'
    )
    
    # Категория и бренд
    brand = models.CharField(_('brand'), max_length=100, blank=True, null=True)
    category = models.CharField(_('category'), max_length=100, blank=True, null=True)
    
    # Физические характеристики
    weight = models.DecimalField(_('weight (g)'), max_digits=10, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(_('width (cm)'), max_digits=10, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(_('height (cm)'), max_digits=10, decimal_places=2, blank=True, null=True)
    depth = models.DecimalField(_('depth (cm)'), max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Цены
    purchase_price = models.DecimalField(_('purchase price'), max_digits=10, decimal_places=2, blank=True, null=True)
    recommended_price = models.DecimalField(_('recommended price'), max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Статусы
    is_active = models.BooleanField(_('active'), default=True)
    is_deleted = models.BooleanField(_('deleted'), default=False)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        
    def __str__(self):
        return f"{self.name} ({self.article})"


class ProductImage(models.Model):
    """
    Модель изображения товара
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    
    image = models.ImageField(_('image'), upload_to='products/')
    is_main = models.BooleanField(_('main image'), default=False)
    order = models.IntegerField(_('order'), default=0)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')
        ordering = ['order']
        
    def __str__(self):
        return f"Image for {self.product.name}"


class ProductMarketplace(models.Model):
    """
    Связь товара с маркетплейсом
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='marketplace_links'
    )
    
    marketplace = models.ForeignKey(
        'api.Marketplace',
        on_delete=models.CASCADE,
        related_name='product_links'
    )
    
    external_id = models.CharField(_('external ID'), max_length=100)
    external_barcode = models.CharField(_('external barcode'), max_length=100, blank=True, null=True)
    external_article = models.CharField(_('external article'), max_length=100, blank=True, null=True)
    
    # Статус на маркетплейсе
    is_active = models.BooleanField(_('active'), default=True)
    last_sync = models.DateTimeField(_('last synchronization'), blank=True, null=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('product marketplace')
        verbose_name_plural = _('product marketplaces')
        unique_together = ('product', 'marketplace')
        
    def __str__(self):
        return f"{self.product.name} on {self.marketplace.name}"
