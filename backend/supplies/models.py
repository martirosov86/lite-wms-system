from django.db import models
from django.utils.translation import gettext_lazy as _


class Supply(models.Model):
    """
    Модель поставки
    """
    SUPPLY_STATUSES = (
        ('draft', _('Draft')),
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('in_transit', _('In transit')),
        ('received', _('Received')),
        ('cancelled', _('Cancelled')),
    )
    
    # Связь с компанией
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='supplies'
    )
    
    # Склады
    source_warehouse = models.ForeignKey(
        'warehouses.Warehouse',
        on_delete=models.CASCADE,
        related_name='outgoing_supplies'
    )
    
    destination_warehouse = models.ForeignKey(
        'warehouses.Warehouse',
        on_delete=models.CASCADE,
        related_name='incoming_supplies'
    )
    
    # Основная информация
    status = models.CharField(_('status'), max_length=20, choices=SUPPLY_STATUSES, default='draft')
    supply_date = models.DateField(_('supply date'))
    supply_time_slot = models.CharField(_('supply time slot'), max_length=20)
    
    # Физические характеристики
    pallets_count = models.IntegerField(_('pallets count'), default=0)
    boxes_count = models.IntegerField(_('boxes count'), default=0)
    
    # Дополнительные опции
    pickup_required = models.BooleanField(_('pickup required'), default=False)
    comment = models.TextField(_('comment'), blank=True, null=True)
    
    # Даты
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('supply')
        verbose_name_plural = _('supplies')
        
    def __str__(self):
        return f"Supply #{self.id} ({self.get_status_display()})"


class SupplyItem(models.Model):
    """
    Модель товара в поставке
    """
    supply = models.ForeignKey(
        Supply,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='supply_items'
    )
    
    quantity = models.IntegerField(_('quantity'))
    
    # Статус обработки
    quantity_received = models.IntegerField(_('quantity received'), default=0)
    is_processed = models.BooleanField(_('processed'), default=False)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('supply item')
        verbose_name_plural = _('supply items')
        
    def __str__(self):
        return f"{self.product.name} x{self.quantity} in Supply #{self.supply.id}"


class SupplyDocument(models.Model):
    """
    Модель документа поставки
    """
    supply = models.ForeignKey(
        Supply,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    
    name = models.CharField(_('name'), max_length=255)
    file = models.FileField(_('file'), upload_to='supply_documents/')
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('supply document')
        verbose_name_plural = _('supply documents')
        
    def __str__(self):
        return f"{self.name} for Supply #{self.supply.id}"
