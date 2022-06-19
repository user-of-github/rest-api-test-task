from rest_framework import serializers
from .models import ShopUnit


class ShopUnitFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUnit
        fields = ['id', 'name', 'date', 'type']


class ShopUnitImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUnit
        fields = ['id', 'name', 'type']