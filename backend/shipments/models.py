from django.db import models
from django.utils.translation import gettext_lazy as _


class Shipment(models.Model):
    """
    Модель отгрузки
    """
    SHIPMENT_STATUSES = (
        ('draft', _('Draft')),
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    )
    
    # Связь с компанией
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='shipments'
    )
    
    # Склад отгрузки
    warehouse = models.ForeignKey(
        'warehouses.Warehouse',
        on_delete=models.CASCADE,
        related_name='shipments'
    )
    
    # Основная информация
    status = models.CharField(_('status'), max_length=20, choices=SHIPMENT_STATUSES, default='draft')
    shipment_date = models.DateField(_('shipment date'))
    
    # Транспортная компания
    transport_company = models.CharField(_('transport company'), max_length=255, blank=True, null=True)
    tracking_number = models.CharField(_('tracking number'), max_length=100, blank=True, null=True)
    
    # Физические характеристики
    pallets_count = models.IntegerField(_('pallets count'), default=0)
    boxes_count = models.IntegerField(_('boxes count'), default=0)
    total_weight = models.DecimalField(_('total weight (kg)'), max_digits=10, decimal_places=2, default=0)
    
    # Дополнительные опции
    comment = models.TextField(_('comment'), blank=True, null=True)
    
    # Даты
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('shipment')
        verbose_name_plural = _('shipments')
        
    def __str__(self):
        return f"Shipment #{self.id} ({self.get_status_display()})"


class ShipmentOrder(models.Model):
    """
    Связь отгрузки с заказом
    """
    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name='shipment_orders'
    )
    
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='shipment_links'
    )
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('shipment order')
        verbose_name_plural = _('shipment orders')
        unique_together = ('shipment', 'order')
        
    def __str__(self):
        return f"Order {self.order.external_id} in Shipment #{self.shipment.id}"


class ShipmentDocument(models.Model):
    """
    Модель документа отгрузки
    """
    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    
    name = models.CharField(_('name'), max_length=255)
    file = models.FileField(_('file'), upload_to='shipment_documents/')
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('shipment document')
        verbose_name_plural = _('shipment documents')
        
    def __str__(self):
        return f"{self.name} for Shipment #{self.shipment.id}"
