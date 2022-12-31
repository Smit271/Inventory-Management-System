from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

from role_permission.models import Permissions

# Permissions Views
def permissions(request):
    if request.method == 'GET':
        permissions_objs = Permissions.objects.values()
        context = {
            "data": permissions_objs,
        }
        return render(request, 'main/permissions.html', context)


def get_permissions_detail(request, id):
    permissions_obj = list(Permissions.objects.filter(
        id=id
    ).values(
        'id', 'name', 'code'
    ))
    return JsonResponse(permissions_obj, safe=False)


def add_permissions_data(request):
    Permissions.objects.create(
        name=request.POST['add_name'],
        code=request.POST['add_code'],
    )
    messages.success(request, "Permission has been added.")
    return redirect(permissions)


def edit_permissions_data(request):
    permissions_obj = Permissions.objects.filter(
        id=request.POST['edit_id']).first()

    permissions_obj.name = request.POST['edit_name']
    permissions_obj.code = request.POST['edit_code']
    permissions_obj.save()

    messages.success(request, "Permission has been updated.")

    return redirect(permissions)


def delete_permissions(request):
    permissions_obj = Permissions.objects.filter(
        id=request.POST['delete_id']).first()
    permissions_obj.delete()

    messages.success(request, "Permission has been deleted.")

    return redirect(permissions)
