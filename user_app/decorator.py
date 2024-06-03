from functools import wraps
from django.shortcuts import redirect
from core import settings

def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect to login URL, add 'next' parameter to redirect back after login
            login_url = settings.USER_LOGIN_URL
            return redirect(f'{login_url}?next={request.path}')
        return view_func(request, *args, **kwargs)
    return _wrapped_view