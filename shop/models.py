from enum import Enum

from django.db import models
from django.contrib.postgres.fields import ArrayField


class ShopUnitType(Enum):
    OFFER = 'OFFER'
    CATEGORY = 'CATEGORY'

    CHOICES = ((OFFER, OFFER), (CATEGORY, CATEGORY))

    unit_type = models.CharField(max_length=15, choices=CHOICES, default=OFFER, unique=True)

    def __str__(self):
        return self.unit_type

SHOP_UNIT_TYPES: tuple = tuple((i.name, i.value) for i in ShopUnitType)


class ShopUnit(models.Model):
    id = models.CharField(max_length=100, null=False)
    name = models.CharField(max_length=100, null=False)
    date = models.DateTimeField(null=False)
    parentId = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=False, choices=SHOP_UNIT_TYPES)
    price = models.IntegerField(null=True)
    children = models.ForeignKey('self')