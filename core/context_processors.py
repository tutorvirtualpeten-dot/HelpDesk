from .models import SystemSettings

def system_settings(request):
    try:
        settings = SystemSettings.objects.first()
    except:
        settings = None
        
    if not settings:
        # Return defaults if no settings in DB yet
        return {
            'SITE_NAME': 'HelpDesk',
            'PRIMARY_COLOR': '#3B82F6',
            'SECONDARY_COLOR': '#10B981',
            'ACCENT_COLOR': '#F59E0B',
            'TICKET_PREFIX': 'TICKET',
            'SYSTEM_SETTINGS': None
        }
        
    return {
        'SITE_NAME': settings.site_name,
        'PRIMARY_COLOR': settings.primary_color,
        'SECONDARY_COLOR': settings.secondary_color,
        'ACCENT_COLOR': settings.accent_color,
        'TICKET_PREFIX': settings.ticket_prefix,
        'SYSTEM_SETTINGS': settings
    }
