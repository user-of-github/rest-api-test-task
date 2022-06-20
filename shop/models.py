from django.db import models
from django.contrib.postgres.fields import ArrayField
from .custom_types import SHOP_UNIT_TYPES


class ShopUnit(models.Model):
    id = models.CharField(max_length=100, null=False, primary_key=True)
    name = models.CharField(max_length=100, null=False)
    date = models.DateTimeField(null=False)
    parentId = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=False, choices=SHOP_UNIT_TYPES)
    price = models.IntegerField(null=True, default=0)
    children = models.ManyToManyField('ShopUnit', null=True, default=[])
    totally_inner_goods_count = models.IntegerField(null=False, default=0)
    total_inner_sum = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f'{self.type} | {self.name}'
