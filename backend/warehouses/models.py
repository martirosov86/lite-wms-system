from django.db import models
from django.utils.translation import gettext_lazy as _


class Warehouse(models.Model):
    """
    Модель склада
    """
    WAREHOUSE_TYPES = (
        ('client', _('Client warehouse')),
        ('fulfillment', _('Fulfillment warehouse')),
        ('marketplace', _('Marketplace warehouse')),
    )
    
    name = models.CharField(_('name'), max_length=255)
    type = models.CharField(_('type'), max_length=20, choices=WAREHOUSE_TYPES)
    address = models.TextField(_('address'))
    
    # Связь с компанией
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='warehouses'
    )
    
    # Контактная информация
    contact_person = models.CharField(_('contact person'), max_length=255, blank=True, null=True)
    contact_phone = models.CharField(_('contact phone'), max_length=20, blank=True, null=True)
    contact_email = models.EmailField(_('contact email'), blank=True, null=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('warehouse')
        verbose_name_plural = _('warehouses')
        
    def __str__(self):
        return self.name


class StorageUnit(models.Model):
    """
    Модель единицы хранения (юнита)
    """
    UNIT_TYPES = (
        ('shelf', _('Shelf')),
        ('rack', _('Rack')),
        ('pallet', _('Pallet')),
        ('box', _('Box')),
        ('cell', _('Cell')),
    )
    
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='storage_units'
    )
    
    name = models.CharField(_('name'), max_length=100)
    type = models.CharField(_('type'), max_length=20, choices=UNIT_TYPES)
    code = models.CharField(_('code'), max_length=50, unique=True)
    
    # Размеры в см
    width = models.DecimalField(_('width'), max_digits=10, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(_('height'), max_digits=10, decimal_places=2, blank=True, null=True)
    depth = models.DecimalField(_('depth'), max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Максимальная вместимость
    max_weight = models.DecimalField(_('max weight'), max_digits=10, decimal_places=2, blank=True, null=True)
    max_items = models.IntegerField(_('max items'), blank=True, null=True)
    
    parent_unit = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='child_units',
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('storage unit')
        verbose_name_plural = _('storage units')
        
    def __str__(self):
        return f"{self.code} - {self.name}"
