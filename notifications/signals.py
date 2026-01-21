from django.db.models.signals import post_save
from django.dispatch import receiver
from tickets.models import Ticket, TicketComment
from .models import EmailTemplate
# from .utils import send_email_notification # We will implement this utility stub

@receiver(post_save, sender=Ticket)
def ticket_lifecycle_notifications(sender, instance, created, **kwargs):
    if created:
        # Trigger Ticket Created Notification
        print(f"Signal: Ticket Created {instance.ticket_id}")
        # Logic: Find 'TICKET_CREATED' template and send email
    else:
        # Check for changes (requires tracking previous state or checking here)
        # Simplified for now: check status
        if instance.status == Ticket.Status.RESOLVED:
            print(f"Signal: Ticket Resolved {instance.ticket_id}")
            # Trigger RESOLVED notification
        
        if instance.assigned_agent:
            # If just assigned... (need to detecting change)
            print(f"Signal: Ticket Assigned to {instance.assigned_agent}")

@receiver(post_save, sender=TicketComment)
def comment_notification(sender, instance, created, **kwargs):
    if created:
        ticket = instance.ticket
        print(f"Signal: New Comment on {ticket.ticket_id}")
        # Trigger COMMENT notification
