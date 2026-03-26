from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def approved_user_required(view_func):
    """Decorator that requires user to be authenticated.
    
    Note: User approval has been removed, so this just checks authentication.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper
