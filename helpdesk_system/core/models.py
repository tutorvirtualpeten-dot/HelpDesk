from django.db import models
from django.utils.translation import gettext_lazy as _

class Department(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SLA(models.Model):
    class Priority(models.TextChoices):
        LOW = 'LOW', _('Low')
        MEDIUM = 'MEDIUM', _('Medium')
        HIGH = 'HIGH', _('High')
        CRITICAL = 'CRITICAL', _('Critical')

    name = models.CharField(_("SLA Name"), max_length=100)
    priority = models.CharField(_("Priority"), max_length=20, choices=Priority.choices, unique=True)
    response_time_hours = models.PositiveIntegerField(_("Response Time (Hours)"), help_text="Max time to respond")
    resolution_time_hours = models.PositiveIntegerField(_("Resolution Time (Hours)"), help_text="Max time to resolve")
    
    def __str__(self):
        return f"{self.name} ({self.get_priority_display()})"
