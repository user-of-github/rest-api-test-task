from django.db import models

from .custom_types import SHOP_UNIT_TYPES


class ShopUnit(models.Model):
    id = models.CharField(max_length=100, null=False, primary_key=True)
    name = models.CharField(max_length=100, null=False)
    date = models.DateTimeField(null=False)
    parentId = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=False, choices=SHOP_UNIT_TYPES)
    price = models.IntegerField(null=True)
    children = models.ManyToManyField('self')
