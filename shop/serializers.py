from rest_framework import serializers
from .models import ShopUnit
from .custom_types import SHOP_UNIT_TYPES


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        if self.parent.parent.__class__(value)['type'].value != SHOP_UNIT_TYPES[0][0]:
            return None

        return serializer.data


class ShopUnitSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = ShopUnit
        fields = ('id', 'name', 'type', 'parentId', 'date', 'price', 'children')


def data_to_dict(data) -> dict:
    response: dict = dict()

    response['id'] = data.id
    response['name'] = data.name
    response['type'] = data.type
    response['parentId'] = data.parentId
    response['date'] = data.date
    response['price'] = data.price

    if data.type == SHOP_UNIT_TYPES[0][0]:
        response['children'] = list()

        for child in data.children.all():
            response['children'].append(data_to_dict(child))
    else:
        response['children'] = None

    return response
