from functools import wraps
from django.shortcuts import redirect, render


def restrict_access(user_types=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser or request.user.user_type in user_types:
                return view_func(request, *args, **kwargs)
            else:
                return render(request,'permission/no_perm.html')
        return wrapped_view
    return decorator