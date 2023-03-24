from django.db import models
from .managers import ProductManager


class DeviceType(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, default="NA")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    # Custom object manager
    objects = ProductManager()

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.is_delete:
            return
        self.is_delete = True
        self.is_active = False
        self.save()

    class Meta:
        db_table = 'device_type'


class Location(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    # Custom object manager
    objects = ProductManager()

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.is_delete:
            return
        self.is_delete = True
        self.is_active = False
        self.save()

    class Meta:
        db_table = 'location'


class Products(models.Model):
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    model_no = models.CharField(max_length=255)
    service_tag = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    ram = models.CharField(max_length=255)
    memory = models.CharField(max_length=255)
    assigned = models.CharField(max_length=255)
    additional_comments = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Custom object manager
    objects = ProductManager()

    def __str__(self):
        return self.model_no

    def delete(self, *args, **kwargs):
        if self.is_delete:
            return
        self.is_delete = True
        self.is_active = False
        self.save()

    class Meta:
        db_table = 'products'
