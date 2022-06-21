import pytest
from rest_framework.test import APIClient

from .data import INVALID, VALID

client: APIClient = APIClient()


@pytest.mark.django_db
def test_valid_imports():
    response = client.post(path='/imports', data=VALID, format='json')

    assert response.status_code == 200


@pytest.mark.django_db
def test_invalid_imports():
    response = client.post(path='/imports', data=INVALID, format='json')

    assert response.status_code == 400
