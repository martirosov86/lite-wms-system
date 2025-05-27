from django.db import models
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    """
    Модель заказа FBS
    """
    ORDER_STATUSES = (
        ('new', _('New')),
        ('processing', _('Processing')),
        ('ready_to_ship', _('Ready to ship')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
        ('returned', _('Returned')),
    )
    
    # Связь с маркетплейсом
    marketplace = models.ForeignKey(
        'api.Marketplace',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    
    # Связь с компанией
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    
    # Основная информация
    external_id = models.CharField(_('external ID'), max_length=100)
    status = models.CharField(_('status'), max_length=20, choices=ORDER_STATUSES, default='new')
    
    # Информация о доставке
    shipping_warehouse = models.ForeignKey(
        'warehouses.Warehouse',
        on_delete=models.SET_NULL,
        related_name='outgoing_orders',
        blank=True,
        null=True
    )
    
    shipping_wave = models.CharField(_('shipping wave'), max_length=100, blank=True, null=True)
    shipping_date = models.DateField(_('shipping date'), blank=True, null=True)
    
    # Финансовая информация
    total_price = models.DecimalField(_('total price'), max_digits=10, decimal_places=2)
    fulfillment_cost = models.DecimalField(_('fulfillment cost'), max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Физические характеристики
    weight = models.DecimalField(_('weight (g)'), max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Даты
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        unique_together = ('marketplace', 'external_id')
        
    def __str__(self):
        return f"Order {self.external_id} ({self.get_status_display()})"


class OrderItem(models.Model):
    """
    Модель товара в заказе
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    
    quantity = models.IntegerField(_('quantity'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    
    # Статус обработки
    is_processed = models.BooleanField(_('processed'), default=False)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')
        
    def __str__(self):
        return f"{self.product.name} x{self.quantity} in Order {self.order.external_id}"
