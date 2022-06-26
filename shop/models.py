from django.db import models
from .constants import SHOP_UNIT_TYPES


class ShopUnit(models.Model):
    id = models.CharField(max_length=100, null=False, primary_key=True)
    name = models.CharField(max_length=100, null=False)
    date = models.CharField(max_length=40, null=False)
    parentId = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=False, choices=SHOP_UNIT_TYPES)
    price = models.IntegerField(null=True, default=0)
    children = models.ManyToManyField('ShopUnit', null=True, default=[])
    totally_inner_goods_count = models.IntegerField(null=False, default=0)
    total_inner_sum = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f'{self.type} | {self.name}'


class ShopUnitHistory(models.Model):
    unit_reference = models.CharField(max_length=100, null=False)
    name = models.CharField(max_length=100, null=False)
    date = models.CharField(max_length=40, null=False)
    parentId = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=False, choices=SHOP_UNIT_TYPES)
    price = models.IntegerField(null=True, default=0)

    def __str__(self):
        return f'State in history: {self.name} ({self.unit_reference})'


class HistoryTable(models.Model):
    id = models.CharField(max_length=100, null=False, primary_key=True)
    history_objects = models.ManyToManyField(ShopUnitHistory)

    def __str__(self):
        return f'History for: {self.id}'
