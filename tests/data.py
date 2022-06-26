VALID: dict = {
    "items": [
        {
            'type': 'CATEGORY',
            'name': 'Все товары',
            'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            'parentId': None
        }
    ],
    'updateDate': '2022-04-01T12:00:00.000Z'
}

INVALID: dict = {
    'items': [
        {
            'type': 'CATEGORY',
            'name': 'Товары',
            'id': '069cb8d7-bbdd--82ef4c269df1',
            'parentId': None
        }
    ],
    'updateDate': '2022-04-02T12:00:00.000Z'
}

DATA_1: dict = {
    'items': [
        {
            'type': 'CATEGORY',
            'name': 'Все товары',
            'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            'parentId': None
        }
    ],
    'updateDate': '2022-04-01T12:00:00.000Z'
}

DATA_2: dict = {
    'items': [
        {
            'type': 'CATEGORY',
            'name': 'Ноутбуки',
            'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
            'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'
        },
        {
            'type': 'OFFER',
            'name': 'Appple Mucbook Pro 14',
            'id': '863e1a7a-1304-42ae-943b-179184c077e3',
            'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
            'price': 10000
        },
        {
            'type': 'OFFER',
            'name': 'Appple Mucbook Air M2',
            'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
            'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
            'price': 5000
        }
    ],
    'updateDate': '2022-04-03T12:00:00.000Z'
}

DATA_3: dict = {
    'items': [
        {
            'type': 'CATEGORY',
            'name': 'Смартфоны',
            'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
            'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'
        },
        {
            'type': 'OFFER',
            'name': 'Hooawei P50 Pro',
            'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
            'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
            'price': 10000
        },
        {
            'type': 'OFFER',
            'name': 'Gugle Pixel 6',
            'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
            'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
            'price': 2000
        }
    ],
    'updateDate': '2022-04-04T12:00:00.000Z'
}

DATA_4: dict = {
    'items': [
        {
            'type': 'OFFER',
            'name': 'Appple Ifone 13 Pro',
            'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
            'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
            'price': 3000
        }
    ],
    'updateDate': '2022-04-05T16:00:00.000Z'
}

DATA_5: dict = {
    'items': [
        {
            'type': 'OFFER',
            'name': 'Gugle Pixel 6',
            'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
            'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
            'price': 2300
        }
    ],
    'updateDate': '2022-04-07T16:00:00.000Z'
}

DATA_TO_UPDATE: dict = {
    'items': [
        {
            'type': 'OFFER',
            'name': 'Gugle Pixel 6',
            'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
            'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
            'price': 2600
        }
    ],
    'updateDate': '2022-06-06T16:00:00.000Z'
}

DATA_TO_MOVE_FROM_CATEGORY: dict = {
    'items': [
        {
            'type': 'OFFER',
            'name': 'Gugle Pixel 6',
            'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
            'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            'price': 5000
        }
    ],
    'updateDate': '2022-06-08T16:00:00.000Z'
}
