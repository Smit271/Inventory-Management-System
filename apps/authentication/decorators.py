from django.shortcuts import redirect


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
                print("===> Permissions: ",  user_perms_list)
                if permission_code in user_perms_list:
                    print("===> YES")
                    return func(request, *args, **kwargs)
                else:
                    print("===> NO")
                    return func(request, *args, **kwargs)
            else:
                return redirect('login_view')
        return wrapper
    return deco
