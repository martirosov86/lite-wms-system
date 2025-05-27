from django.db import models
from django.utils.translation import gettext_lazy as _


class Marketplace(models.Model):
    """
    Модель маркетплейса
    """
    MARKETPLACE_TYPES = (
        ('wildberries', 'Wildberries'),
        ('ozon', 'Ozon'),
        ('yandex_market', 'Яндекс.Маркет'),
        ('aliexpress', 'AliExpress'),
        ('sber_mega_market', 'СберМегаМаркет'),
        ('other', 'Другой'),
    )
    
    name = models.CharField(_('name'), max_length=100)
    type = models.CharField(_('type'), max_length=20, choices=MARKETPLACE_TYPES)
    
    # Связь с компанией
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='marketplaces'
    )
    
    # API ключи и настройки
    api_key = models.CharField(_('API key'), max_length=255, blank=True, null=True)
    api_secret = models.CharField(_('API secret'), max_length=255, blank=True, null=True)
    client_id = models.CharField(_('client ID'), max_length=255, blank=True, null=True)
    
    # Настройки FBS
    is_fbs_enabled = models.BooleanField(_('FBS enabled'), default=False)
    
    # Статус подключения
    is_connected = models.BooleanField(_('connected'), default=False)
    last_sync = models.DateTimeField(_('last synchronization'), blank=True, null=True)
    
    # Статистика
    products_count = models.IntegerField(_('products count'), default=0)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('marketplace')
        verbose_name_plural = _('marketplaces')
        
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
