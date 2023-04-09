from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import F

from products.models import (
    Products, DeviceType, Location,
    Designation, Department
)
from accounts.decorators import (
    login_required, check_user_permissions
)


# Products Views
@login_required
@check_user_permissions(permission_code="VIPR")
def home(request):
    if request.method == 'GET':
        products_objs = Products.objects.values(
            'id', 'model_no',
            'service_tag', 'brand', 'ram', 'memory', 'assigned',
            'additional_comments',
            loc=F('location__name'),
            loc_id=F('location__id'),
            dev_type=F('device_type__name'),
            dev_type_id=F('device_type__id'),
        )
        device_type_objs = DeviceType.objects.values()
        location_objs = Location.objects.values()
        context = {
            "data": products_objs,
            "device_type_objs": device_type_objs,
            "location_objs": location_objs,
        }
        return render(request, 'main/home.html', context)


@login_required
def get_product_detail(request, id):
    product_obj = list(Products.objects.filter(
        id=id
    ).values(
        'id', 'model_no',
        'service_tag', 'brand', 'ram', 'memory', 'assigned',
        'additional_comments',
        loc=F('location__name'),
        loc_id=F('location__id'),
        dev_type=F('device_type__name'),
        dev_type_id=F('device_type__id'),
    ))
    return JsonResponse(product_obj, safe=False)


@login_required
@check_user_permissions(permission_code="ADPR")
def add_product_data(request):
    Products.objects.create(
        device_type=DeviceType.objects.filter(
            id=request.POST['add_device_type'][0]).first(),
        location=Location.objects.filter(
            id=request.POST['add_location'][0]).first(),
        model_no=request.POST['add_model_no'],
        service_tag=request.POST['add_service_tag'],
        brand=request.POST['add_brand'],
        ram=request.POST['add_ram'],
        memory=request.POST['add_memory'],
        assigned=request.POST['add_assigned'],
        additional_comments=request.POST['add_additional_comments'],
        created_by=request.user
    )
    messages.success(request, "Product has been added.")
    return redirect(home)


@login_required
@check_user_permissions(permission_code="EDPR")
def edit_product_data(request):
    product_obj = Products.objects.filter(id=request.POST['edit_id']).first()

    product_obj.device_type = DeviceType.objects.filter(
        id=request.POST['edit_device_type'][0]).first()
    product_obj.location = Location.objects.filter(
        id=request.POST['edit_location'][0]).first()
    product_obj.model_no = request.POST['edit_model_no']
    product_obj.service_tag = request.POST['edit_service_tag']
    product_obj.brand = request.POST['edit_brand']
    product_obj.ram = request.POST['edit_ram']
    product_obj.memory = request.POST['edit_memory']
    product_obj.assigned = request.POST['edit_assigned']
    product_obj.additional_comments = request.POST['edit_additional_comments']
    product_obj.updated_by = request.user
    product_obj.save()

    messages.success(request, "Product has been updated.")

    return redirect(home)


@login_required
@check_user_permissions(permission_code="DEPR")
def delete_product(request):
    product_obj = Products.objects.filter(id=request.POST['delete_id']).first()
    product_obj.delete()

    messages.success(request, "Product has been deleted.")

    return redirect(home)


# Device Views
@login_required
@check_user_permissions(permission_code="VIDETY")
def device_type(request):
    if request.method == 'GET':
        device_type_objs = DeviceType.objects.values()
        context = {
            "data": device_type_objs,
        }
        return render(request, 'main/device_type.html', context)


@login_required
def get_device_type_detail(request, id):
    device_type_obj = list(DeviceType.objects.filter(
        id=id
    ).values(
        'id', 'name', 'code'
    ))
    return JsonResponse(device_type_obj, safe=False)


@login_required
@check_user_permissions(permission_code="ADDETY")
def add_device_type_data(request):
    DeviceType.objects.create(
        name=request.POST['add_name'],
        code=request.POST['add_code'],
        created_by=request.user
    )
    messages.success(request, "Device Type has been added.")
    return redirect(device_type)


@login_required
@check_user_permissions(permission_code="EDDETY")
def edit_device_type_data(request):
    # print("===> request.POST: ", request.POST)
    device_type_obj = DeviceType.objects.filter(
        id=request.POST['edit_id']).first()

    device_type_obj.name = request.POST['edit_name']
    device_type_obj.code = request.POST['edit_code']
    device_type_obj.updated_by = request.user
    device_type_obj.save()

    messages.success(request, "Device type has been updated.")

    return redirect(device_type)


@login_required
@check_user_permissions(permission_code="DEDETY")
def delete_device_type(request):
    device_type_obj = DeviceType.objects.filter(
        id=request.POST['delete_id']).first()
    device_type_obj.delete()

    messages.success(request, "Product has been deleted.")

    return redirect(device_type)


# ---------- LOCATION VIEWS ----------
@login_required
@check_user_permissions(permission_code="VILO")
def location(request):
    if request.method == 'GET':
        location_objs = Location.objects.values()
        context = {
            "data": location_objs,
        }
        return render(request, 'main/location.html', context)


@login_required
def get_location_detail(request, id):
    location_obj = list(Location.objects.filter(
        id=id
    ).values(
        'id', 'name'
    ))
    return JsonResponse(location_obj, safe=False)


@login_required
@check_user_permissions(permission_code="ADLO")
def add_location_data(request):
    Location.objects.create(
        name=request.POST['add_name'],
        created_by=request.user
    )
    messages.success(request, "Location has been added.")

    return redirect(location)


@login_required
@check_user_permissions(permission_code="EDLO")
def edit_location_data(request):
    # print("===> request.POST: ", request.POST)
    location_obj = Location.objects.filter(
        id=request.POST['edit_id']).first()

    location_obj.name = request.POST['edit_name']
    location_obj.updated_by = request.user
    location_obj.save()

    messages.success(request, "Location has been updated.")

    return redirect(location)


@login_required
@check_user_permissions(permission_code="DELO")
def delete_location(request):
    location_obj = Location.objects.filter(
        id=request.POST['delete_id']).first()
    location_obj.delete()

    messages.success(request, "Location has been deleted.")

    return redirect(location)


# ---------- DESIGNATION VIEWS ----------
@login_required
@check_user_permissions(permission_code="VILO")
def designation(request):
    if request.method == 'GET':
        designation_objs = Designation.objects.values()
        context = {
            "data": designation_objs,
        }
        return render(request, 'main/designation.html', context)


@login_required
def get_designation_detail(request, id):
    designation_obj = list(Designation.objects.filter(
        id=id
    ).values(
        'id', 'name'
    ))
    return JsonResponse(designation_obj, safe=False)


@login_required
@check_user_permissions(permission_code="ADLO")
def add_designation_data(request):
    Designation.objects.create(
        name=request.POST['add_name'],
        created_by=request.user
    )
    messages.success(request, "Designation has been added.")

    return redirect(designation)


@login_required
@check_user_permissions(permission_code="EDLO")
def edit_designation_data(request):
    # print("===> request.POST: ", request.POST)
    designation_obj = Designation.objects.filter(
        id=request.POST['edit_id']).first()

    designation_obj.name = request.POST['edit_name']
    designation_obj.updated_by = request.user
    designation_obj.save()

    messages.success(request, "Designation has been updated.")

    return redirect(designation)


@login_required
@check_user_permissions(permission_code="DELO")
def delete_designation(request):
    designation_obj = Designation.objects.filter(
        id=request.POST['delete_id']).first()
    designation_obj.delete()

    messages.success(request, "Designation has been deleted.")

    return redirect(designation)


# ---------- DEPARTMENT VIEWS ----------
@login_required
@check_user_permissions(permission_code="VILO")
def department(request):
    if request.method == 'GET':
        department_objs = Department.objects.values()
        context = {
            "data": department_objs,
        }
        return render(request, 'main/department.html', context)


@login_required
def get_department_detail(request, id):
    department_obj = list(Department.objects.filter(
        id=id
    ).values(
        'id', 'name'
    ))
    return JsonResponse(department_obj, safe=False)


@login_required
@check_user_permissions(permission_code="ADLO")
def add_department_data(request):
    Department.objects.create(
        name=request.POST['add_name'],
        created_by=request.user
    )
    messages.success(request, "Department has been added.")

    return redirect(department)


@login_required
@check_user_permissions(permission_code="EDLO")
def edit_department_data(request):
    # print("===> request.POST: ", request.POST)
    department_obj = Department.objects.filter(
        id=request.POST['edit_id']).first()

    department_obj.name = request.POST['edit_name']
    department_obj.updated_by = request.user
    department_obj.save()

    messages.success(request, "Department has been updated.")

    return redirect(department)


@login_required
@check_user_permissions(permission_code="DELO")
def delete_department(request):
    department_obj = Department.objects.filter(
        id=request.POST['delete_id']).first()
    department_obj.delete()

    messages.success(request, "Department has been deleted.")

    return redirect(department)
