from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import F

from products.models import (
    Products, DeviceType, Location
)
from authentication.decorators import login_required


# Products Views
@login_required
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
    )
    messages.success(request, "Product has been added.")
    return redirect(home)


@login_required
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
    product_obj.save()

    messages.success(request, "Product has been updated.")

    return redirect(home)


@login_required
def delete_product(request):
    product_obj = Products.objects.filter(id=request.POST['delete_id']).first()
    product_obj.delete()

    messages.success(request, "Product has been deleted.")

    return redirect(home)


# Device Views
@login_required
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
def add_device_type_data(request):
    DeviceType.objects.create(
        name=request.POST['add_name'],
        code=request.POST['add_code'],
    )
    messages.success(request, "Device Type has been added.")
    return redirect(device_type)


@login_required
def edit_device_type_data(request):
    print("===> request.POST: ", request.POST)
    device_type_obj = DeviceType.objects.filter(
        id=request.POST['edit_id']).first()

    device_type_obj.name = request.POST['edit_name']
    device_type_obj.code = request.POST['edit_code']
    device_type_obj.save()

    messages.success(request, "Device type has been updated.")

    return redirect(device_type)


@login_required
def delete_device_type(request):
    device_type_obj = DeviceType.objects.filter(
        id=request.POST['delete_id']).first()
    device_type_obj.delete()

    messages.success(request, "Product has been deleted.")

    return redirect(device_type)



# Location Views
@login_required
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
def add_location_data(request):
    Location.objects.create(
        name=request.POST['add_name'],
    )
    messages.success(request, "Location has been added.")

    return redirect(location)


@login_required
def edit_location_data(request):
    print("===> request.POST: ", request.POST)
    location_obj = Location.objects.filter(
        id=request.POST['edit_id']).first()

    location_obj.name = request.POST['edit_name']
    location_obj.save()

    messages.success(request, "Location has been updated.")

    return redirect(location)


@login_required
def delete_location(request):
    location_obj = Location.objects.filter(
        id=request.POST['delete_id']).first()
    location_obj.delete()

    messages.success(request, "Location has been deleted.")

    return redirect(location)
