import pytest
from rest_framework.test import APIClient

from .data import INVALID, VALID, DATA_1, DATA_2, DATA_3, DATA_4, DATA_5

client: APIClient = APIClient()


@pytest.mark.django_db
def test_valid_imports():
    response = client.post(path='/imports', data=VALID, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_invalid_imports():
    response = client.post(path='/imports', data=INVALID, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_just_correct_import():
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
