from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout

from .models import (
    User, Employee
)
from role_permission.models import (
    Roles,
)
from products.models import (
    Products
)
from .decorators import login_required, check_user_permissions


@login_required
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
        return render(request, 'accounts/login.html')
    else:
        user_obj = User.objects.filter(
            email=request.POST['email']
        ).first()

        if not user_obj:
            messages.warning(request, message="Email is not registered.")
            return render(request, 'accounts/login.html')
        else:
            if user_obj.check_password(request.POST['password']):
                # STORING PERMISSION CODES IN SESSION FOR HTML VALIDATION
                if not user_obj.is_superuser:
                    request.session['permission_codes'] = [
                        perms['code'] for perms in user_obj.role.permissions.values('code')
                    ]
                # LOGIN
                login(request, user_obj)
                return redirect('dashboard')
            else:
                messages.warning(request, message="Wrong credentials.")
                return render(request, 'accounts/login.html')


@login_required
@check_user_permissions(permission_code="VIUS")
def users(request):
    user_objs = User.objects.filter(
        is_superuser=False
    ).all()
    context = {
        'data': user_objs
    }
    return render(request, 'accounts/users.html', context=context)


@login_required
@check_user_permissions(permission_code="ADUS")
def add_user(request):
    roles_objs = Roles.objects.values()
    context = {
        'roles': roles_objs
    }
    return render(request, 'accounts/add_user.html', context)


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
        phone=request.POST['add_phone']
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
    user_obj.phone = request.POST['add_phone']
    user_obj.gender = request.POST['add_gender']
    user_obj.role = role_obj
    user_obj.created_by = request.user
    user_obj.save()

    messages.success(request, "User is created successfully.")

    return redirect(users)


@login_required
@check_user_permissions(permission_code="VIEM")
def employees(request):
    employee_objs = Employee.objects.filter(
    ).values(
        'id',
        'user__name',
        'user__email',
        'user__is_active',
        'user__last_login',
        'emp_code'
    )
    context = {
        'data': employee_objs
    }
    return render(request, 'accounts/employees.html', context=context)


@login_required
@check_user_permissions(permission_code="ADEM")
def add_employee(request):
    employee_objs = Employee.objects.all()
    context = {
        'employees': employee_objs
    }
    return render(request, 'accounts/add_employee.html', context=context)


@login_required
@check_user_permissions(permission_code="ADEM")
def create_employee(request):
    print("===> request.POST: ", request.POST)

    # CHECKING FOR UNIQUE EMAIL & MOBILE NUMBER
    check_mail = User.objects.filter(
        email=request.POST['add_email']
    )
    if check_mail:
        messages.error(request, "Email is already registered!")
        return redirect(users)

    check_mobile = User.objects.filter(
        phone=request.POST['add_phone']
    )
    if check_mobile:
        messages.error(request, "Mobile number is already registered!")
        return redirect(users)

    check_emp_code = Employee.objects.filter(
        emp_code=request.POST['add_emp_code']
    )
    if check_emp_code:
        messages.error(request, "Employee code is already taken")
        return redirect(users)
    
    # role_obj = Roles.objects.filter(
    #     id=request.POST['add_role']
    # ).first()

    user_obj = User.objects.create_employee(
        request.POST['add_email'],
        request.POST['add_pass']
    )
    user_obj.name = request.POST['add_name']
    user_obj.phone = request.POST['add_phone']
    user_obj.gender = request.POST['add_gender']
    user_obj.save()

    # CREATING EMPLOYEE
    employee_obj = Employee.objects.create(
        user=user_obj,
        emp_code=request.POST['add_emp_code'],
        reporting_person=request.POST['add_reporting_person'] if 'add_reporting_person'\
                        in request.POST else None,
        created_by=request.user
    )

    messages.success(request, "Employee is created successfully.")

    return redirect(employees)
