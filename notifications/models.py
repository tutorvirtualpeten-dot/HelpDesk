from django.db import models
from django.utils.translation import gettext_lazy as _

class SMTPSettings(models.Model):
    host = models.CharField(_("SMTP Host"), max_length=200)
    port = models.PositiveIntegerField(_("SMTP Port"), default=587)
    username = models.CharField(_("SMTP Username"), max_length=200)
    password = models.CharField(_("SMTP Password"), max_length=200) # Encrypt this in real app?
    use_tls = models.BooleanField(_("Use TLS"), default=True)
    use_ssl = models.BooleanField(_("Use SSL"), default=False)
    default_from_email = models.EmailField(_("Default From Email"))

    def __str__(self):
        return f"SMTP Config ({self.host})"
        
    def save(self, *args, **kwargs):
        # Singleton logic similar to SystemSettings
        if not self.pk and SMTPSettings.objects.exists():
            pass # Or clear others
        super().save(*args, **kwargs)

class EmailTemplate(models.Model):
    class Type(models.TextChoices):
        TICKET_CREATED = 'TICKET_CREATED', _('Ticket Created')
        TICKET_ASSIGNED = 'TICKET_ASSIGNED', _('Ticket Assigned')
        TICKET_RESOLVED = 'TICKET_RESOLVED', _('Ticket Resolved')
        TICKET_COMMENT = 'TICKET_COMMENT', _('New Comment')

    name = models.CharField(_("Template Name"), max_length=100)
    template_type = models.CharField(_("Type"), max_length=50, choices=Type.choices, unique=True)
    subject_template = models.CharField(_("Subject Template"), max_length=200, help_text="Available vars: {{ticket_id}}, {{subject}}")
    body_template = models.TextField(_("Body Template (HTML)"), help_text="HTML content. Available vars: {{ticket_id}}, {{subject}}, {{status}}")

    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
