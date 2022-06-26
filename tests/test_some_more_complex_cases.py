import pytest

from rest_framework.test import APIClient

from .data import DATA_1, DATA_2, DATA_4, DATA_3, DATA_5, DATA_TO_UPDATE, DATA_TO_MOVE_FROM_CATEGORY
from .data import DATA_EMPTY_CATEGORY, OFFER_FOR_THIS_CATEGORY, UPDATE_OFFER_FOR_THIS_CATEGORY, LETS_MOVE_OFFER
from .data import ANOTHER_EMPTY_SUBCATEGORY, MOVE_THIS_ANOTHER_EMPTY_SUBCATEGORY_TO_ROOT
from .data import LAST_SUBCATEGORY_FOR_SPEAKERS_NON_EMPTY, MOVE_LAST_SUBCATEGORY_FOR_SPEAKERS_NON_EMPTY

client: APIClient = APIClient()


@pytest.mark.django_db
def test_moving_out_from_category():
    response = client.post(path='/imports', data=DATA_1, format='json')
    assert response.status_code == 200

    response = client.post(path='/imports', data=DATA_2, format='json')
    assert response.status_code == 200

    response = client.post(path='/imports', data=DATA_3, format='json')
    assert response.status_code == 200

    response = client.post(path='/imports', data=DATA_4, format='json')
    assert response.status_code == 200

    response = client.post(path='/imports', data=DATA_5, format='json')
    assert response.status_code == 200

    response = client.post(path='/imports', data=DATA_TO_UPDATE, format='json')
    assert response.status_code == 200

    response = client.get(path='/nodes/1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2')
    assert response.status_code == 200
    assert response.data['price'] == 5200

    response = client.get(path='/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')
    assert len(response.data['children']) == 2
    assert response.status_code == 200

    response = client.post(path='/imports', data=DATA_TO_MOVE_FROM_CATEGORY, format='json')
    assert response.status_code == 200

    response = client.get(path='/nodes/1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2')
    assert response.status_code == 200
    assert response.data['price'] == 6500

    response = client.get(path='/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')
    assert response.status_code == 200
    assert response.data['price'] == (33000 // 5)
    assert len(response.data['children']) == 3


@pytest.mark.django_db
def test_some_nuances():
    response = client.post(path='/imports', data=DATA_1, format='json')
    assert response.status_code == 200

    response = client.post(path='/imports', data=DATA_EMPTY_CATEGORY, format='json')
    assert response.status_code == 200

    response = client.get(path='/nodes/74b81fad-9cdc-4b36-8927-c123afed5cf4', format='json')
    assert response.status_code == 200
    assert response.data['date'] == '2022-06-08T16:00:00.000Z'

    response = client.get(path='/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1', format='json')
    assert response.status_code == 200
    assert response.data['date'] == '2022-04-01T12:00:00.000Z'

    response = client.post(path='/imports', data=OFFER_FOR_THIS_CATEGORY, format='json')
    assert response.status_code == 200

    response = client.get(path='/nodes/74b81fad-9cdc-4b36-8927-c123afed5cf4', format='json')
    assert response.status_code == 200
    assert response.data['date'] == '2022-06-08T17:00:00.000Z'
    assert response.data['price'] == 1000

    response = client.get(path='/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1', format='json')
    assert response.status_code == 200
    assert response.data['date'] == '2022-06-08T17:00:00.000Z'
    assert response.data['price'] == 1000

    response = client.post(path='/imports', data=UPDATE_OFFER_FOR_THIS_CATEGORY, format='json')
    assert response.status_code == 200

    response = client.get(path='/nodes/74b81fad-9cdc-4b36-8927-c123afed5cf4', format='json')
    assert response.status_code == 200
    assert response.data['date'] == '2022-06-08T18:00:00.000Z'
    assert response.data['price'] == 1200

    response = client.get(path='/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1', format='json')
    assert response.status_code == 200
    assert response.data['date'] == '2022-06-08T18:00:00.000Z'
    assert response.data['price'] == 1200

    response = client.post(path='/imports', data=LETS_MOVE_OFFER, format='json')
    assert response.status_code == 200

    response = client.get(path='/nodes/74b81fad-9cdc-4b36-8927-c123afed5cf4', format='json')
    assert response.status_code == 200
    assert response.data['date'] == '2022-06-10T19:00:00.000Z'
    assert response.data['price'] is None

    response = client.get(path='/nodes/74b81fad-9cdc-4b36-7777-c123afed5cf4', format='json')
    assert response.status_code == 200
    assert response.data['date'] == '2022-06-10T19:00:00.000Z'
    assert response.data['price'] == 1205

    response = client.get(path='/sales?date=2022-06-10T19:00:00.000Z', format='json')
    assert response.status_code == 200
    assert len(response.data) == 1

    response = client.get(path='/sales?date=2022-06-11T18:00:00.000Z', format='json')
    assert response.status_code == 200
    assert len(response.data) == 1

    response = client.get(path='/sales?date=2022-06-10T00:00:00.000Z', format='json')
    assert response.status_code == 200
    assert len(response.data) == 0

    response = client.get(path='/node/74b81fad-9cdc-4b88-8888-c123afed5cf8/statistic', format='json')
    assert response.status_code == 200
    assert len(response.data) == 3

    response = client.get(path='/node/74b81fad-9cdc-4b36-8927-c123afed5cf4/statistic', format='json')
    assert response.status_code == 200
    assert len(response.data) == 4

    response = client.get(path='/node/74b81fad-9cdc-4b36-7777-c123afed5cf4/statistic', format='json')
    assert response.status_code == 200
    assert len(response.data) == 2

    # empty category, then will move it and check dates and prices and story
    response = client.post(path='/imports', data=ANOTHER_EMPTY_SUBCATEGORY, format='json')
    assert response.status_code == 200

    response = client.get(path='/nodes/74b81fad-9cdc-4b36-7777-c123afed5cf4', format='json')
    assert response.status_code == 200
    assert response.data['date'] != '2022-06-10T20:00:00.000Z'

    response = client.get(path='/node/74b81fad-9cdc-4b36-7777-c123afed5cf4/statistic', format='json')
    assert response.status_code == 200
    assert len(response.data) == 2

    response = client.post(path='/imports', data=MOVE_THIS_ANOTHER_EMPTY_SUBCATEGORY_TO_ROOT, format='json')
    assert response.status_code == 200

    response = client.get(path='/nodes/74b81fad-9cdc-4b00-6666-c123afed5cf4', format='json')
    assert response.status_code == 200
    assert response.data['date'] == '2022-06-10T21:00:00.000Z'

    response = client.get(path='/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1', format='json')
    assert response.status_code == 200
    assert response.data['date'] != '2022-06-10T21:00:00.000Z'

    response = client.get(path='/nodes/74b81fad-9cdc-4b36-8927-c123afed5cf4', format='json')
    assert response.status_code == 200
    assert response.data['date'] != '2022-06-10T21:00:00.000Z'

    # non empty category, then will move it and check dates and prices and story
    response = client.post(path='/imports', data=LAST_SUBCATEGORY_FOR_SPEAKERS_NON_EMPTY, format='json')
    assert response.status_code == 200

    response = client.get(path='/nodes/74b81fad-9cdc-4b36-8927-c123afed5cf4', format='json')
    assert response.status_code == 200
    assert response.data['date'] == '2022-06-26T21:00:00.000Z'

    response = client.get(path='/nodes/74b81fad-9cdc-bd00-2222-c123afed5cf8', format='json')
    assert response.status_code == 200
    assert response.data['date'] == '2022-06-26T21:00:00.000Z'

    response = client.get(path='/nodes/74b81fad-9cdc-4b36-1111-c123afed5cf4', format='json')
    assert response.status_code == 200
    assert response.data['date'] == '2022-06-26T21:00:00.000Z'

    response = client.get(path='/node/74b81fad-9cdc-4b36-1111-c123afed5cf4/statistic', format='json')
    assert response.status_code == 200
    assert len(response.data) == 2

    response = client.get(path='/node/74b81fad-9cdc-4b36-8927-c123afed5cf4/statistic', format='json')
    assert response.status_code == 200

    REMEMBER_CURRENT_STORY_LENGTH: int = len(response.data)

    response = client.post(path='/imports', data=MOVE_LAST_SUBCATEGORY_FOR_SPEAKERS_NON_EMPTY, format='json')
    assert response.status_code == 200

    response = client.get(path='/node/74b18fad-0cdc-4b36-5555-c123afed5cf4/statistic', format='json')
    assert response.status_code == 200
    assert len(response.data) == 2

    response = client.get(path='/node/74b81fad-9cdc-4b36-8927-c123afed5cf4/statistic', format='json')
    assert response.status_code == 200
    assert len(response.data) == REMEMBER_CURRENT_STORY_LENGTH + 1
