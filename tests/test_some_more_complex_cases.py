import pytest

from .data import DATA_1, DATA_2, DATA_4, DATA_3, DATA_5, DATA_TO_UPDATE, DATA_TO_MOVE_FROM_CATEGORY
from rest_framework.test import APIClient


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
