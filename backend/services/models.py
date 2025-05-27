from django.db import models
from django.utils.translation import gettext_lazy as _


class Service(models.Model):
    """
    Модель дополнительной услуги
    """
    SERVICE_TYPES = (
        ('packaging', _('Packaging')),
        ('labeling', _('Labeling')),
        ('photo', _('Photography')),
        ('inspection', _('Inspection')),
        ('repair', _('Repair')),
        ('other', _('Other')),
    )
    
    name = models.CharField(_('name'), max_length=255)
    type = models.CharField(_('type'), max_length=20, choices=SERVICE_TYPES)
    description = models.TextField(_('description'), blank=True, null=True)
    
    # Связь с компанией
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='services'
    )
    
    # Стоимость
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    price_type = models.CharField(
        _('price type'),
        max_length=10,
        choices=(
            ('fixed', _('Fixed')),
            ('per_item', _('Per item')),
            ('per_hour', _('Per hour')),
        ),
        default='fixed'
    )
    
    is_active = models.BooleanField(_('active'), default=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')
        
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class ServiceRequest(models.Model):
    """
    Модель заявки на услугу
    """
    REQUEST_STATUSES = (
        ('new', _('New')),
        ('in_progress', _('In progress')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    )
    
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='requests'
    )
    
    # Связь с компанией
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='service_requests'
    )
    
    # Связь со складом
    warehouse = models.ForeignKey(
        'warehouses.Warehouse',
        on_delete=models.CASCADE,
        related_name='service_requests'
    )
    
    # Основная информация
    status = models.CharField(_('status'), max_length=20, choices=REQUEST_STATUSES, default='new')
    quantity = models.IntegerField(_('quantity'), default=1)
    
    # Планирование
    planned_date = models.DateField(_('planned date'))
    completed_date = models.DateField(_('completed date'), blank=True, null=True)
    
    # Стоимость
    total_cost = models.DecimalField(_('total cost'), max_digits=10, decimal_places=2)
    
    # Дополнительные опции
    comment = models.TextField(_('comment'), blank=True, null=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('service request')
        verbose_name_plural = _('service requests')
        
    def __str__(self):
        return f"{self.service.name} request #{self.id} ({self.get_status_display()})"


class ServiceRequestItem(models.Model):
    """
    Модель товара в заявке на услугу
    """
    service_request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='service_items'
    )
    
    quantity = models.IntegerField(_('quantity'))
    
    # Статус обработки
    quantity_processed = models.IntegerField(_('quantity processed'), default=0)
    is_completed = models.BooleanField(_('completed'), default=False)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('service request item')
        verbose_name_plural = _('service request items')
        
    def __str__(self):
        return f"{self.product.name} x{self.quantity} in Service request #{self.service_request.id}"
