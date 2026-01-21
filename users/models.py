from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Administrator')
        AGENT = 'AGENT', _('Agent')
        CUSTOMER = 'CUSTOMER', _('Customer')

    role = models.CharField(_("Role"), max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    department = models.ForeignKey(
        'core.Department', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='agents',
        help_text=_("Department this user belongs to (if Agent)")
    )
    phone_number = models.CharField(_("Phone Number"), max_length=20, blank=True)
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_agent(self):
        return self.role == self.Role.AGENT
    
    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN
