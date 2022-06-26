import pytest
from rest_framework.test import APIClient

from .data import DATA_1, DATA_2, DATA_3, DATA_4, DATA_5, DATA_TO_UPDATE

client: APIClient = APIClient()


@pytest.mark.django_db
def test_statistics_story_after_double_updating():
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

    response = client.get(path='/node/74b81fda-9cdc-4b63-8927-c978afed5cf4/statistic', format='json')
    assert len(response.data) == 3

    response = client.get(path='/node/1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2/statistic', format='json')
    assert len(response.data) == 6


@pytest.mark.django_db
def test_invalid_requests():
    response = client.get(path='/node/74b81fda/statistic')
    assert response.status_code == 400
    assert response.data['code'] == 400
    assert response.data['message'] == 'Validation Failed'

    response = client.get(path='/node/74b81fda-9cdc-4b63-8927-c978afed5cf4/statistic?dateStart=qi4yg35yu')
    assert response.status_code == 400
    assert response.data['code'] == 400
    assert response.data['message'] == 'Validation Failed'

    response = client.get(path='/node/74b81fda-9cdc-4b63-8927-c978afed5cf4/statistic?dateEnd=qi4yg35yu')
    assert response.status_code == 400
    assert response.data['code'] == 400
    assert response.data['message'] == 'Validation Failed'

    response = client.get(path='/node/74b81fda-9cdc-4b63-8927-c978afed5cf4/statistic?')
    assert response.status_code == 404
    assert response.data['code'] == 404
    assert response.data['message'] == 'Item not found'
