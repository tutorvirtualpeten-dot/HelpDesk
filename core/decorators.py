from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return user_passes_test(lambda u: False)(view_func)(request, *args, **kwargs)
            
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            raise PermissionDenied
        return _wrapped_view
    return decorator

def agent_required(view_func):
    return role_required(['AGENT', 'ADMIN'])(view_func)

def admin_required(view_func):
    return role_required(['ADMIN'])(view_func)
