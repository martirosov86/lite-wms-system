from django.db import models
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    """
    Модель компании
    """
    name = models.CharField(_('name'), max_length=255)
    short_name = models.CharField(_('short name'), max_length=100, blank=True, null=True)
    inn = models.CharField(_('INN'), max_length=12, unique=True)
    kpp = models.CharField(_('KPP'), max_length=9, blank=True, null=True)
    legal_address = models.TextField(_('legal address'))
    actual_address = models.TextField(_('actual address'), blank=True, null=True)
    
    # Банковские реквизиты
    bank_name = models.CharField(_('bank name'), max_length=255, blank=True, null=True)
    bank_bik = models.CharField(_('BIK'), max_length=9, blank=True, null=True)
    bank_account = models.CharField(_('bank account'), max_length=20, blank=True, null=True)
    corr_account = models.CharField(_('correspondent account'), max_length=20, blank=True, null=True)
    
    # Настройки дропшиппинга
    is_dropshipping_enabled = models.BooleanField(_('dropshipping enabled'), default=False)
    
    # Контактная информация
    contact_person = models.CharField(_('contact person'), max_length=255, blank=True, null=True)
    contact_phone = models.CharField(_('contact phone'), max_length=20, blank=True, null=True)
    contact_email = models.EmailField(_('contact email'), blank=True, null=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')
        
    def __str__(self):
        return self.name
