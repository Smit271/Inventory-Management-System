from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from accounts.models import User
from products.models import (
    DeviceType, Location, Products
)

# @receiver(pre_save, sender=[Products, DeviceType])
# def set_created_by(sender, instance, **kwargs):
#     if not instance.created_by:
#         instance.created_by = instance.updated_by or instance.creator


# @receiver(post_save, sender=DeviceType)
# def set_updated_by(sender, instance, **kwargs):
#     print("===> instance.creator: ", **kwargs)
#     instance.updated_by = instance.creator
#     instance.save()

# @receiver(pre_save, sender=Location)
# def set_created_by_updated_by(sender, instance, **kwargs):
#     if not instance.pk:
#         # This is a new instance, set the "created_by" field
#         for i in kwargs:
#             print("===> i: ", i)
#         instance.created_by = instance.updated_by
#     else:
#         # This is an existing instance, update the "updated_by" field
#         instance.updated_by = instance.updated_by
