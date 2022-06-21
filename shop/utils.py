from .custom_types import SHOP_UNIT_TYPES
from .models import ShopUnit


def update_parent_prices_after_creating(item_to_start) -> None:
    #print('UPDATING')
    price_to_add: int = item_to_start.price

    if item_to_start.parentId is None:
        return

    current = item_to_start
    nexts = ShopUnit.objects.filter(id=item_to_start.parentId)

    while len(nexts) != 0:
        parent = nexts[0]
        print('PARENT: ', parent.name)
        parent.totally_inner_goods_count = parent.totally_inner_goods_count + 1
        parent.total_inner_sum = parent.total_inner_sum + price_to_add
        parent.price = parent.total_inner_sum // parent.totally_inner_goods_count
        parent.save()
        current = parent
        nexts = ShopUnit.objects.filter(id=current.parentId)


def update_parent_prices_after_deleting(nexts_initial, price_to_subtract: int, goods_count_to_subtract: int) -> None:
    nexts = nexts_initial

    while len(nexts) != 0:
        parent = nexts[0]

        parent.totally_inner_goods_count -= goods_count_to_subtract
        parent.total_inner_sum -= price_to_subtract
        if parent.totally_inner_goods_count != 0:
            parent.price = parent.total_inner_sum // parent.totally_inner_goods_count
        else:
            parent.price = None

        parent.save()

        nexts = ShopUnit.objects.filter(id=parent.parentId)


def update_parent_prices_after_item_updating(nexts_initial, price: int, count: int) -> None:
    nexts = nexts_initial

    while len(nexts) != 0:
        parent = nexts[0]

        parent.totally_inner_goods_count += count
        parent.total_inner_sum += price
        if parent.totally_inner_goods_count != 0:
            parent.price = parent.total_inner_sum // parent.totally_inner_goods_count
        else:
            parent.price = None

        parent.save()

        nexts = ShopUnit.objects.filter(id=parent.parentId)


def update_parents_date_after_item_updating(nexts_initial, date: str) -> None:
    print('UPDATING PARENTS DATE')
    nexts = nexts_initial

    while len(nexts) != 0:
        parent = nexts[0]
        print('parent ', parent.name)
        parent.date = date
        parent.save()
        nexts = ShopUnit.objects.filter(id=parent.parentId)


def create_new_item(item: dict, date: str) -> None:
    if item['type'] == SHOP_UNIT_TYPES[0][0]: # category
        created_object = ShopUnit.objects.create(
            id=item['id'],
            name=item['name'],
            parentId=item['parentId'],
            type=item['type'],
            price=None,
            date=date,
            totally_inner_goods_count=0,
            total_inner_sum=0
        )
    else:
        created_object = ShopUnit.objects.create(
            id=item['id'],
            name=item['name'],
            parentId=item['parentId'],
            type=item['type'],
            price=item['price'],
            date=date,
            totally_inner_goods_count=1,
            total_inner_sum=item['price']
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

    if created_object.type != SHOP_UNIT_TYPES[0][0]:
        update_parent_prices_after_creating(created_object)


def update_existing_item(item: dict, date: str) -> None:
    existing_item = ShopUnit.objects.get(id=item['id'])

    # firstly remove price and counts from statistics (maybe we move whole category, for example)
    if existing_item.parentId is not None:
        update_parent_prices_after_deleting(
            ShopUnit.objects.filter(id=existing_item.parentId),
            existing_item.total_inner_sum,
            existing_item.totally_inner_goods_count
        )

    existing_item.name = item['name']
    existing_item.date = date

    if item['type'] != SHOP_UNIT_TYPES[0][0]:
        existing_item.price = item['price']
        existing_item.total_inner_sum = item['price']

    # logics of moving
    if existing_item.parentId is not None and existing_item.parentId != item['parentId']:
        previous_parent = ShopUnit.objects.get(id=existing_item.parentId)
        previous_parent.children.remove(existing_item)
        previous_parent.save()

        existing_item.parentId = item['parentId']

        if existing_item.parentId is not None:
            new_parent = ShopUnit.objects.filter(id=existing_item.parentId)[0]
            new_parent.children.add(existing_item)
            new_parent.save()

    update_parent_prices_after_item_updating(ShopUnit.objects.filter(id=existing_item.parentId), existing_item.total_inner_sum, existing_item.totally_inner_goods_count)
    update_parents_date_after_item_updating(ShopUnit.objects.filter(id=existing_item.parentId), date)

    existing_item.save()


def remove_item(element) -> None:
    if element.type != SHOP_UNIT_TYPES[0][0]:
        element.delete()
    else:
        all_children = element.children.all()

        for child in all_children:
            remove_item(child)

        element.delete()
