from django.db import models
from django.utils.translation import gettext_lazy as _


class Report(models.Model):
    """
    Модель отчета
    """
    REPORT_TYPES = (
        ('inventory', _('Inventory')),
        ('sales', _('Sales')),
        ('orders', _('Orders')),
        ('supplies', _('Supplies')),
        ('shipments', _('Shipments')),
        ('services', _('Services')),
        ('financial', _('Financial')),
        ('custom', _('Custom')),
    )
    
    REPORT_FORMATS = (
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    )
    
    name = models.CharField(_('name'), max_length=255)
    type = models.CharField(_('type'), max_length=20, choices=REPORT_TYPES)
    format = models.CharField(_('format'), max_length=10, choices=REPORT_FORMATS)
    
    # Связь с компанией
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='reports'
    )
    
    # Параметры отчета
    parameters = models.JSONField(_('parameters'), blank=True, null=True)
    
    # Файл отчета
    file = models.FileField(_('file'), upload_to='reports/', blank=True, null=True)
    
    # Статус генерации
    is_generated = models.BooleanField(_('generated'), default=False)
    generation_date = models.DateTimeField(_('generation date'), blank=True, null=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('report')
        verbose_name_plural = _('reports')
        
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Inventory(models.Model):
    """
    Модель инвентаризации
    """
    INVENTORY_STATUSES = (
        ('draft', _('Draft')),
        ('in_progress', _('In progress')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    )
    
    # Связь с компанией
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='inventories'
    )
    
    # Связь со складом
    warehouse = models.ForeignKey(
        'warehouses.Warehouse',
        on_delete=models.CASCADE,
        related_name='inventories'
    )
    
    # Основная информация
    name = models.CharField(_('name'), max_length=255)
    status = models.CharField(_('status'), max_length=20, choices=INVENTORY_STATUSES, default='draft')
    
    # Планирование
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'), blank=True, null=True)
    
    # Дополнительные опции
    comment = models.TextField(_('comment'), blank=True, null=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('inventory')
        verbose_name_plural = _('inventories')
        
    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"


class InventoryItem(models.Model):
    """
    Модель товара в инвентаризации
    """
    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='inventory_items'
    )
    
    # Количество
    expected_quantity = models.IntegerField(_('expected quantity'))
    actual_quantity = models.IntegerField(_('actual quantity'), blank=True, null=True)
    
    # Статус проверки
    is_checked = models.BooleanField(_('checked'), default=False)
    
    # Расхождение
    has_discrepancy = models.BooleanField(_('has discrepancy'), default=False)
    discrepancy_reason = models.TextField(_('discrepancy reason'), blank=True, null=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('inventory item')
        verbose_name_plural = _('inventory items')
        
    def __str__(self):
        return f"{self.product.name} in Inventory {self.inventory.name}"
