import pytest
from rest_framework.test import APIClient

from .data import DATA_1, DATA_2, DATA_4, DATA_3, DATA_5

client: APIClient = APIClient()


@pytest.mark.django_db
def test_nodes():
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

    response = client.get(path='/nodes/d515e43f-f3f6-4471-bb77-6b455017a2d2')
    assert response.status_code == 200
    assert response.data['name'] == 'Смартфоны'

    response = client.get(path='/nodes/d515e43ffbb776b455017a2d2')
    assert response.status_code == 400

    response = client.get(path='/nodes/d515e43f-f3f8-4471-bb77-6b455071a2d3')
    assert response.status_code == 404

