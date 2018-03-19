from __future__ import unicode_literals

from functools import wraps
from django.db.models.query import QuerySet
    
def action(label, short_description=None):
    """Decorateur qui facilite la definition d action """
    
    def decorator(func):
        
        def takes_instance_or_queryset(func):
            """Decorator that makes standard Django admin actions compatible."""
            @wraps(func)
            def decorated_function(self, request, queryset):
                if not isinstance(queryset, QuerySet):
                    queryset = self.get_queryset(request).filter(pk=queryset.pk)
                return func(self, request, queryset)
            return decorated_function
        
        
        
        func.label = label
        if short_description is not None:
            func.short_description = short_description
        return takes_instance_or_queryset(func)

    return decorator


def field(short_description, admin_order_field=None, allow_tags=None):
    """Decorateur qui facilite la definition d action """
    
    def decorator(func):
        func.short_description = short_description
        if admin_order_field is not None:
            func.admin_order_field = admin_order_field
        if allow_tags is not None:
            func.allow_tags = allow_tags
        return func

    return decorator
