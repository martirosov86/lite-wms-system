from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Расширенная модель пользователя
    """
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=20, blank=True, null=True)
    position = models.CharField(_('position'), max_length=100, blank=True, null=True)
    
    # Связь с компанией (будет создана позже)
    company = models.ForeignKey(
        'companies.Company', 
        on_delete=models.CASCADE, 
        related_name='employees',
        blank=True, 
        null=True
    )
    
    # Дополнительные поля для двухфакторной аутентификации
    is_two_factor_enabled = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def __str__(self):
        return self.username
