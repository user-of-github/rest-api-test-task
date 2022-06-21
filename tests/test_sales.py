import pytest

from .data import DATA_1, DATA_2
from rest_framework.test import APIClient


client: APIClient = APIClient()


@pytest.mark.django_db
def test_valid_imports():
    response = client.post(path='/imports', data=DATA_1, format='json')
    assert response.status_code == 200

    response = client.post(path='/imports', data=DATA_2, format='json')
    assert response.status_code == 200

    response = client.get(path='/sales?')
    assert response.status_code == 400

    response = client.get(path='/sales?date=hetgbtr')
    assert response.status_code == 400
