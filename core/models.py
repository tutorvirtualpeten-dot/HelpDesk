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

class SystemSettings(models.Model):
    # Singleton logic: we will just assume ID=1 is the valid config.
    site_name = models.CharField(_("Site Name"), max_length=100, default="HelpDesk")
    logo = models.ImageField(_("Logo"), upload_to='branding/', blank=True, null=True)
    favicon = models.ImageField(_("Favicon"), upload_to='branding/', blank=True, null=True)
    
    # Theme Colors
    primary_color = models.CharField(_("Primary Color"), max_length=7, default="#3B82F6", help_text="Hex code")
    secondary_color = models.CharField(_("Secondary Color"), max_length=7, default="#10B981", help_text="Hex code")
    accent_color = models.CharField(_("Accent Color"), max_length=7, default="#F59E0B", help_text="Hex code")
    
    # Localization
    default_timezone = models.CharField(_("Timezone"), max_length=50, default="UTC")
    
    # Tickets
    ticket_prefix = models.CharField(_("Ticket Prefix"), max_length=10, default="TICKET")

    def save(self, *args, **kwargs):
        if not self.pk and SystemSettings.objects.exists():
             # Logic to prevent multiple instances could go here, 
             # but strictly speaking we just need to ensure the admin only edits the first one.
             pass
        return super().save(*args, **kwargs)

    def __str__(self):
        return "System Configuration"
    
    class Meta:
        verbose_name = _("System Configuration")
        verbose_name_plural = _("System Configuration")
