from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout

from .models import User
from role_permission.models import (
    Roles,
)
from products.models import (
    Products
)
from .decorators import login_required, check_user_permissions


def dashboard(request):
    product_count = Products.objects.count()
    users_count = User.objects.count()
    roles_count = Roles.objects.count()

    context = {
        'product_count': product_count,
        'users_count': users_count,
        'roles_count': roles_count,
    }
    return render(request, 'main/dashboard.html', context=context)


def login_view(request):
    if request.method == 'GET':
        logout(request)
        return render(request, 'authentication/login.html')
    else:
        user_obj = User.objects.filter(
            email=request.POST['email']
        ).first()

        if not user_obj:
            messages.warning(request, message="Email is not registered.")
            return render(request, 'authentication/login.html')
        else:
            if user_obj.check_password(request.POST['password']):
                # STORING PERMISSION CODES IN SESSION FOR HTML VALIDATION
                request.session['permission_codes'] = [
                    perms['code'] for perms in user_obj.role.permissions.values('code')
                ]
                # LOGIN
                login(request, user_obj)
                return redirect('dashboard')
            else:
                messages.warning(request, message="Wrong credentials.")
                return render(request, 'authentication/login.html')


@login_required
@check_user_permissions(permission_code="VIUS")
def users(request):
    user_objs = User.objects.filter(
        is_superuser=False
    ).all()
    context = {
        'data': user_objs
    }
    return render(request, 'authentication/users.html', context=context)


@login_required
@check_user_permissions(permission_code="ADUS")
def add_user(request):
    roles_objs = Roles.objects.values()
    context = {
        'roles': roles_objs
    }
    return render(request, 'authentication/add_user.html', context)


@login_required
@check_user_permissions(permission_code="ADUS")
def create_user(request):
    print("===> request.POST: ", request.POST)

    # CHECKING FOR UNIQUE EMAIL & MOBILE NUMBER
    check_mail = User.objects.filter(
        email=request.POST['add_email']
    )
    if check_mail:
        messages.error(request, "Email is already registered!")
        return redirect(users)

    check_mobile = User.objects.filter(
        phone_number=request.POST['add_phone']
    )
    if check_mobile:
        messages.error(request, "Mobile number is already registered!")
        return redirect(users)

    role_obj = Roles.objects.filter(
        id=request.POST['add_role']
    ).first()

    user_obj = User.objects.create_user(
        request.POST['add_email'],
        request.POST['add_pass']
    )
    user_obj.name = request.POST['add_name']
    user_obj.phone_number = request.POST['add_phone']
    user_obj.gender = request.POST['add_gender']
    user_obj.role = role_obj
    user_obj.save()

    messages.success(request, "User is created successfully.")

    return redirect(add_user)
