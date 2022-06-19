import dataclasses
from datetime import datetime

from .custom_types import SHOP_UNIT_TYPES
from .models import ShopUnit


def check_items_for_import(items_to_check: list[dict], update_date: str) -> bool:
    existing_units = ShopUnit.objects
    new_units: list = list()
    ids_set: set = set()

    for item_to_check in items_to_check:
        # check that all ids are different
        if item_to_check['id'] in ids_set:
            print('dublicate id')
            return False
        ids_set.add(item_to_check['id'])

        # check parent
        print(item_to_check['parentId'])
        if item_to_check['parentId'] is not None:
            found_parent_in_existing = existing_units.filter(id=item_to_check['parentId'])
            found_parent_in_new: list = list(filter(lambda unit: unit['id'] == item_to_check['parentId'], new_units))

            if len(found_parent_in_existing) == 0 and len(found_parent_in_new) == 0:
                print('no parent')
                return False
            else:
                if len(found_parent_in_new) != 0:
                    print(found_parent_in_new)
                    if found_parent_in_new[0]['type'] != SHOP_UNIT_TYPES[0][0]:
                        return False
                else:
                    if found_parent_in_existing[0].type != SHOP_UNIT_TYPES[0][0]:
                        return False

        # check price
        if item_to_check['type'] != SHOP_UNIT_TYPES[0][0] and item_to_check['price'] < 0:
            print('price')
            return False

        new_units.append(item_to_check)

    # check date
    try:
        datetime.fromisoformat(str(update_date).replace('Z', '+00:00'))
    except:
        return False

    return True
