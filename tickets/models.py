from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from core.models import Department, SLA

class Ticket(models.Model):
    class Status(models.TextChoices):
        NEW = 'NEW', _('New')
        OPEN = 'OPEN', _('Open')
        PENDING = 'PENDING', _('Pending')
        RESOLVED = 'RESOLVED', _('Resolved')
        CLOSED = 'CLOSED', _('Closed')

    class Priority(models.TextChoices):
        LOW = 'LOW', _('Low')
        MEDIUM = 'MEDIUM', _('Medium')
        HIGH = 'HIGH', _('High')
        CRITICAL = 'CRITICAL', _('Critical')

    ticket_id = models.CharField(_("Ticket ID"), max_length=20, unique=True, editable=False)
    subject = models.CharField(_("Subject"), max_length=200)
    description = models.TextField(_("Description"))
    
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requested_tickets')
    assigned_agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='tickets')
    
    status = models.CharField(_("Status"), max_length=20, choices=Status.choices, default=Status.NEW)
    priority = models.CharField(_("Priority"), max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    sla_due_date = models.DateTimeField(_("SLA Due Date"), null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.ticket_id:
            import uuid
            # Basic fallback if prefix logic fails or for initial creation
            # Ideally we check SystemSettings here but models shouldn't depend on Request.
            # We can use a signal or overrides. 
            # For now simple ID generation.
            self.ticket_id = f"T-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_id} - {self.subject}"

class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='tickets/attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Attachment for {self.ticket.ticket_id}"

class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    is_internal = models.BooleanField(_("Internal Note"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.ticket.ticket_id} by {self.author}"
