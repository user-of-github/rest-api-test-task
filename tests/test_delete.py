import pytest
from rest_framework.test import APIClient

from .data import DATA_1, DATA_2

client: APIClient = APIClient()


@pytest.mark.django_db
def test_deleting_not_existing_item():
    response = client.delete(path='/delete/witgut')
    assert response.status_code == 400

    response = client.delete(path='/delete/d515e43f-f3f6-4471-bb77-6b455017a2d2')
    assert response.status_code == 404


@pytest.mark.django_db
def test_deleting_existing_item():
    response = client.post(path='/imports', data=DATA_1, format='json')
    assert response.status_code == 200

    response = client.delete(path='/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_updating_after_deleting():
    response = client.post(path='/imports', data=DATA_1, format='json')
    assert response.status_code == 200

    response = client.post(path='/imports', data=DATA_2, format='json')
    assert response.status_code == 200

    response = client.delete(path='/delete/b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4')
    assert response.status_code == 200
