from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

from role_permission.models import (
    Permissions, Roles
)

# Permissions Views
def permission(request):
    if request.method == 'GET':
        permission_objs = Permissions.objects.values()
        context = {
            "data": permission_objs,
        }
        return render(request, 'role_permission/permission.html', context)


def get_permission_detail(request, id):
    permission_obj = list(Permissions.objects.filter(
        id=id
    ).values(
        'id', 'name', 'code', 'table_name'
    ))
    return JsonResponse(permission_obj, safe=False)


def add_permission_data(request):
    Permissions.objects.create(
        name=request.POST['add_name'],
        code=request.POST['add_code'],
        table_name=request.POST['add_table_name'],
    )
    messages.success(request, "Permission has been added.")
    return redirect(permission)


def edit_permission_data(request):
    permission_obj = Permissions.objects.filter(
        id=request.POST['edit_id']).first()

    permission_obj.name = request.POST['edit_name']
    permission_obj.code = request.POST['edit_code']
    permission_obj.table_name = request.POST['edit_table_name']
    permission_obj.save()

    messages.success(request, "Permission has been updated.")

    return redirect(permission)


def delete_permission(request):
    permission_obj = Permissions.objects.filter(
        id=request.POST['delete_id']).first()
    permission_obj.is_active = False
    permission_obj.is_delete = True
    permission_obj.save()

    messages.success(request, "Permission has been deleted.")

    return redirect(permission)


def role(request):
    if request.method == 'GET':
        role_objs = Roles.objects.values()
        context = {
            "data": role_objs,
        }
        return render(request, 'role_permission/role.html', context)


def add_role(request):
    if request.method == 'GET':
        role_objs = Roles.objects.values()
        permission_objs = Permissions.objects.values()
        context = {
            "data": role_objs,
            "permissions_list": permission_objs,
        }
        return render(request, 'role_permission/add_role.html', context)


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

        messages.success(request, "Role has been created with given permissions.")

        return redirect(role)
