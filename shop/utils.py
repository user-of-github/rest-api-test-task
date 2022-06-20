from datetime import datetime
from uuid import UUID

from dateutil import parser
from .custom_types import SHOP_UNIT_TYPES
from .models import ShopUnit


def check_items_for_import(items_to_check: list[dict], update_date: str) -> bool:
    existing_units = ShopUnit.objects
    new_units: list = list()
    ids_set: set = set()

    for item_to_check in items_to_check:
        # check name
        if item_to_check['name'] is None:
            return False

        # check that all ids are different
        if item_to_check['id'] in ids_set:
            return False
        ids_set.add(item_to_check['id'])

        # check parent
        if item_to_check['parentId'] is not None:
            found_parent_in_existing = existing_units.filter(id=item_to_check['parentId'])
            found_parent_in_new: list = list(filter(lambda unit: unit['id'] == item_to_check['parentId'], new_units))

            if len(found_parent_in_existing) == 0 and len(found_parent_in_new) == 0:
                return False
            else:
                if len(found_parent_in_new) != 0:
                    if found_parent_in_new[0]['type'] != SHOP_UNIT_TYPES[0][0]:
                        return False
                else:
                    if found_parent_in_existing[0].type != SHOP_UNIT_TYPES[0][0]:
                        return False

        # check price
        if item_to_check['type'] != SHOP_UNIT_TYPES[0][0] and item_to_check['price'] < 0:
            return False

        new_units.append(item_to_check)

    # check date
    try:
        datetime.fromisoformat(str(update_date).replace('Z', '+00:00'))
    except:
        return False

    return True


def create_new_item(item: dict, date: str) -> None:
    # print('CREATING NEW: ', item['name'])

    if item['type'] == SHOP_UNIT_TYPES[0][0]:
        created_object = ShopUnit.objects.create(
            id=item['id'],
            name=item['name'],
            parentId=item['parentId'],
            type=item['type'],
            date=parser.parse(date)
        )
    else:
        created_object = ShopUnit.objects.create(
            id=item['id'],
            name=item['name'],
            parentId=item['parentId'],
            type=item['type'],
            price=item['price'],
            date=parser.parse(date)
        )

    created_object.save()
    # print('CREATED')
    # print('Now own children are: ', created_object.children.all())
    # print('ParentId is: ', created_object.parentId)

    if created_object.parentId is not None:
        # print('Looking parent for ', created_object.name)
        parent = ShopUnit.objects.filter(id=created_object.parentId)[0]
        # print('So parent is: ', parent.name)
        parent.children.add(created_object)
        # print('Now parents children are: ', parent.children.all())
        # print('And own children are: ', created_object.children.all())
        parent.save()


def update_existing_item(item: dict, date: str) -> None:
    existing_item = ShopUnit.objects.get(id=item['id'])

    existing_item.name = item['name']
    existing_item.date = parser.parse(date)

    if item['type'] != SHOP_UNIT_TYPES[0][0]:
        existing_item.price = item['price']

    if existing_item.parentId is not None and existing_item.parentId != item['parentId']:
        previous_parent = ShopUnit.objects.get(id=existing_item.parentId)
        previous_parent.children.remove(existing_item)
        previous_parent.save()

        existing_item.parentId = item['parentId']

        if existing_item.parentId is not None:
            new_parent = ShopUnit.objects.filter(id=existing_item.parentId)[0]
            new_parent.children.add(existing_item)
            new_parent.save()

    existing_item.save()


def check_id_for_delete(to_delete: str) -> bool:
    if to_delete is None:
        return False

    try:
        uuid_obj = UUID(to_delete)
    except ValueError:
        return False

    return True


def remove_item(element) -> None:
    if element.type != SHOP_UNIT_TYPES[0][0]:
        element.delete()
    else:
        all_children = element.children.all()

        for child in all_children:
            remove_item(child)

        element.delete()
