from django.shortcuts import redirect
from django.contrib import messages


def login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect('login_view')
    return wrapper


def check_user_permissions(permission_code):
    def deco(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                user_perms_list = [
                    perms['code'] for perms in request.user.role.permissions.values('code')
                ]
                if permission_code in user_perms_list or request.user.is_superuser:
                    return func(request, *args, **kwargs)
                else:
                    messages.error(request, "You do not have access to this page please contact ADMIN.")
                    return redirect('dashboard')
                    # return func(request, *args, **kwargs)
            else:
                return redirect('login_view')
        return wrapper
    return deco
