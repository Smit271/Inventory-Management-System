from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

from role_permission.models import (
    Permissions, Roles
)
from authentication.models import (
    User
)
from authentication.decorators import (
    login_required, check_user_permissions
)


# Permissions Views
@login_required
@check_user_permissions(permission_code="VIPE")
def permission(request):
    if request.method == 'GET':
        permission_objs = Permissions.objects.values()
        context = {
            "data": permission_objs,
        }
        return render(request, 'role_permission/permission.html', context)


@login_required
def get_permission_detail(request, id):
    permission_obj = list(Permissions.objects.filter(
        id=id
    ).values(
        'id', 'name', 'code', 'table_name'
    ))
    return JsonResponse(permission_obj, safe=False)


@login_required
@check_user_permissions(permission_code="ADPE")
def add_permission_data(request):
    Permissions.objects.create(
        name=request.POST['add_name'],
        code=request.POST['add_code'],
        table_name=request.POST['add_table_name'],
    )
    messages.success(request, "Permission has been added.")
    return redirect(permission)


@login_required
@check_user_permissions(permission_code="EDPE")
def edit_permission_data(request):
    permission_obj = Permissions.objects.filter(
        id=request.POST['edit_id']).first()

    permission_obj.name = request.POST['edit_name']
    permission_obj.code = request.POST['edit_code']
    permission_obj.table_name = request.POST['edit_table_name']
    permission_obj.save()

    messages.success(request, "Permission has been updated.")

    return redirect(permission)


@login_required
@check_user_permissions(permission_code="DEPE")
def delete_permission(request):
    permission_obj = Permissions.objects.filter(
        id=request.POST['delete_id']).first()
    permission_obj.is_active = False
    permission_obj.is_delete = True
    permission_obj.save()

    messages.success(request, "Permission has been deleted.")

    return redirect(permission)


@login_required
@check_user_permissions(permission_code="VIRO")
def role(request):
    if request.method == 'GET':
        role_objs = Roles.objects.values()
        for obj in role_objs:
            assigned_count = User.objects.filter(
                role_id=obj['id']
            ).count()
            obj['assigned_user_count'] = assigned_count
        permissions_list = Permissions.objects.values()
        context = {
            "data": role_objs,
            "permissions_list": permissions_list,
        }
        return render(request, 'role_permission/role.html', context)


@login_required
@check_user_permissions(permission_code="ADRO")
def add_role(request):
    if request.method == 'GET':
        role_objs = Roles.objects.values()
        permission_objs = Permissions.objects.values()
        context = {
            "data": role_objs,
            "permissions_list": permission_objs,
        }
        return render(request, 'role_permission/add_role.html', context)


@login_required
@check_user_permissions(permission_code="ADRO")
def create_role(request):
    if request.method == 'POST':
        print("===> request.POST: ", request.POST)
        permission_ids = dict(request.POST)['permissions']
        role_obj = Roles.objects.create(
            name=request.POST['add_name'],
            created_by=request.user
        )
        for permission in permission_ids:
            role_obj.permissions.add(permission)

        messages.success(
            request, "Role has been created with given permissions.")

        return redirect(role)


@login_required
def get_role_detail(request, id):
    roles_data = Roles.objects.get(
        id=id
    ).get_full_details()

    return JsonResponse(roles_data, safe=False)


@login_required
@check_user_permissions(permission_code="EDRO")
def edit_role_data(request):
    role_obj = Roles.objects.filter(
        id=request.POST['edit_id']).first()

    permission_ids = dict(request.POST)['edit_permissions']
    role_obj.name = request.POST['edit_name']
    role_obj.permissions.set(permission_ids)
    role_obj.save()

    messages.success(request, "Role has been updated.")

    return redirect(role)
