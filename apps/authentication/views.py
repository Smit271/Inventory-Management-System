from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login

from .models import User
from role_permission.models import (
    Roles,
)
from .decorators import login_required


def login_view(request):
    if request.method == 'GET':
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
                login(request, user_obj)
                return redirect('products/home')
            else:
                messages.warning(request, message="Wrong credentials.")
                return render(request, 'authentication/login.html')


@login_required
def add_user(request):
    roles_objs = Roles.objects.values()
    context = {
        'roles': roles_objs
    }
    return render(request, 'authentication/add_user.html', context)


@login_required
def create_user(request):
    print("===> request.POST: ", request.POST)

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

    return redirect(add_user)


@login_required
def users(request):
    user_objs = User.objects.filter(
        is_superuser=False
    ).all()
    context = {
        'data': user_objs
    }
    return render(request, 'authentication/users.html', context=context)
