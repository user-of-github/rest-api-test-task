from .constants import SHOP_UNIT_TYPES


def shop_unit_to_dict(data, with_children: bool = True) -> dict:
    response: dict = dict()

    response['id'] = data.id
    response['name'] = data.name
    response['type'] = data.type
    response['parentId'] = data.parentId
    response['date'] = data.date
    response['price'] = data.price

    if not with_children:
        return response

    if data.type == SHOP_UNIT_TYPES[0][0]:
        response['children'] = list()

        for child in data.children.all():
            response['children'].append(shop_unit_to_dict(child, True))
    else:
        response['children'] = None

    return response
