import pytest

from .data import DATA_1, DATA_2, DATA_4, DATA_3, DATA_5
from rest_framework.test import APIClient


client: APIClient = APIClient()


@pytest.mark.django_db
def test_on_valid_imports():
    response = client.post(path='/imports', data=DATA_1, format='json')
    assert response.status_code == 200

    response = client.post(path='/imports', data=DATA_2, format='json')
    assert response.status_code == 200

    response = client.get(path='/sales?')
    assert response.status_code == 400

    response = client.get(path='/sales?date=hetgbtr')
    assert response.status_code == 400


@pytest.mark.django_db
def test_on_valid_imports():
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

    response = client.get(path='/sales?date=2022-04-07T16:00:00.000Z', format='json')
    assert response.status_code == 200
    assert len(response.data) == 1

    response = client.get(path='/sales?date=202204-07T16:00:00.000Z', format='json')
    assert response.status_code == 400
    assert response.data['message'] == 'Validation Failed'
    assert response.data['code'] == 400

    response = client.get(path='/sales?dat', format='json')
    assert response.status_code == 400
    assert response.data['message'] == 'Validation Failed'
    assert response.data['code'] == 400
