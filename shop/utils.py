from .custom_types import SHOP_UNIT_TYPES
from .models import ShopUnit, HistoryTable, ShopUnitHistory
from dateutil import parser


def add_item_to_history_table(item) -> None:
    if len(HistoryTable.objects.filter(id=item.id)) == 0:
        new_row = HistoryTable.objects.create(id=item.id)
        new_row.save()

    found_row = HistoryTable.objects.filter(id=item.id)[0]

    new_history_item = ShopUnitHistory.objects.create(
        unit_reference=item.id,
        name=item.name,
        date=item.date,
        type=item.type,
        price=item.price,
        parentId=item.parentId
    )
    new_history_item.save()

    found_row.history_objects.add(new_history_item)
    found_row.save()


def add_parents_changes_to_history(parents_filter) -> None:
    nexts = parents_filter

    while len(nexts) != 0:
        parent = nexts[0]
        add_item_to_history_table(parent)
        nexts = ShopUnit.objects.filter(id=parent.parentId)


def remove_item_from_history(id_to_delete: str) -> None:
    ShopUnitHistory.objects.filter(unit_reference=id_to_delete).delete()
    HistoryTable.objects.filter(id=id_to_delete).delete()


def update_parent_prices_after_creating(item_to_start) -> None:
    price_to_add: int = item_to_start.price

    if item_to_start.parentId is None:
        return

    nexts = ShopUnit.objects.filter(id=item_to_start.parentId)

    while len(nexts) != 0:
        parent = nexts[0]
        parent.totally_inner_goods_count = parent.totally_inner_goods_count + 1
        parent.total_inner_sum = parent.total_inner_sum + price_to_add
        parent.price = parent.total_inner_sum // parent.totally_inner_goods_count
        parent.save()
        nexts = ShopUnit.objects.filter(id=parent.parentId)


def update_parent_date_after_creating(item_to_start, new_date) -> None:
    if item_to_start.parentId is None:
        return

    nexts = ShopUnit.objects.filter(id=item_to_start.parentId)

    while len(nexts) != 0:
        parent = nexts[0]
        parent.date = new_date
        parent.save()
        nexts = ShopUnit.objects.filter(id=parent.parentId)


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
    nexts = nexts_initial

    while len(nexts) != 0:
        parent = nexts[0]
        print(f'UPDATING {parent.name} from {parent.date} to {date}')
        parent.date = date
        parent.save()
        nexts = ShopUnit.objects.filter(id=parent.parentId)


def create_new_item(item: dict, date: str) -> None:
    created_object = ShopUnit.objects.create(
        id=item['id'],
        name=item['name'],
        parentId=item['parentId'],
        type=item['type'],
        price=None if item['type'] == SHOP_UNIT_TYPES[0][0] else item['price'],
        date=date,
        totally_inner_goods_count=0 if item['type'] == SHOP_UNIT_TYPES[0][0] else 1,
        total_inner_sum=0 if item['type'] == SHOP_UNIT_TYPES[0][0] else item['price']
    )

    created_object.save()
    add_item_to_history_table(created_object)

    # link parent with its new child
    if created_object.parentId is not None:
        parent = ShopUnit.objects.filter(id=created_object.parentId)[0]
        parent.children.add(created_object)
        parent.save()

    # if it is an offer => update prices in all parent
    if created_object.type != SHOP_UNIT_TYPES[0][0]:
        update_parent_prices_after_creating(created_object)

    update_parent_date_after_creating(created_object, date)

    add_parents_changes_to_history(ShopUnit.objects.filter(id=created_object.parentId))


def update_existing_item(item: dict, date: str) -> None:
    existing_item = ShopUnit.objects.get(id=item['id'])

    # firstly remove price and counts from statistics (maybe we move whole category, for example)
    if existing_item.parentId is not None:
        update_parent_prices_after_deleting(
            ShopUnit.objects.filter(id=existing_item.parentId),
            existing_item.total_inner_sum,
            existing_item.totally_inner_goods_count
        )

        # if moving to another category => update current parent history, than will update new parent history
        if existing_item.parentId != item['parentId']:
            add_parents_changes_to_history(ShopUnit.objects.filter(id=existing_item.parentId))

    existing_item.name = item['name']
    existing_item.date = date
    existing_item.save()

    if item['type'] != SHOP_UNIT_TYPES[0][0]:
        existing_item.price = item['price']
        existing_item.total_inner_sum = item['price']
        existing_item.save()

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

    existing_item.save()
    add_item_to_history_table(existing_item)

    update_parent_prices_after_item_updating(
        ShopUnit.objects.filter(id=existing_item.parentId),
        existing_item.total_inner_sum, existing_item.totally_inner_goods_count
    )

    update_parents_date_after_item_updating(ShopUnit.objects.filter(id=existing_item.parentId), date)
    add_parents_changes_to_history(ShopUnit.objects.filter(id=existing_item.parentId))


def remove_item(element) -> None:
    if element.type == SHOP_UNIT_TYPES[0][0]:
        all_children = element.children.all()

        for child in all_children:
            remove_item(child)

    remove_item_from_history(element.id)
    element.delete()


def satisfies_date_interval(item_date_source: str, right_date_range_border_source: str) -> bool:
    SECONDS_IN_DAY: int = 3600
    HOURS_IN_DAY: int = 24

    right_border = parser.parse(right_date_range_border_source)
    item_date = parser.parse(item_date_source)

    return (right_border >= item_date) and ((right_border - item_date).total_seconds() / SECONDS_IN_DAY <= HOURS_IN_DAY)


def get_node_statistics_filtered_by_date(row_in_history_table, date_from, date_to):
    all_states = list(row_in_history_table.history_objects.all())

    if date_from is not None:
        filtered_by_left_date = list(filter(lambda item: parser.parse(item.date) >= parser.parse(date_from), all_states))
    else:
        filtered_by_left_date = all_states

    if date_to is not None:
        filtered_by_right_date = list(filter(lambda item: parser.parse(item.date) < parser.parse(date_to), filtered_by_left_date))
    else:
        filtered_by_right_date = filtered_by_left_date

    return filtered_by_right_date
