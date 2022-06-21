from .custom_types import SHOP_UNIT_TYPES


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
