import pytest
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from agro.models import CropType


# Positve cases
@pytest.mark.django_db
def test_croptype_list(client, create_crop_types):
    url = reverse('croptype-list')
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 2

@pytest.mark.django_db
def test_croptype_create(client):
    url = reverse('croptype-list')
    data = {'name': 'Café'}
    response = client.post(url, data, format='json')
    assert response.status_code == HTTP_201_CREATED
    assert CropType.objects.filter(name='Café').exists()

@pytest.mark.django_db
def test_croptype_update(client, create_crop_types):
    croptype = create_crop_types[0]
    url = reverse('croptype-detail', kwargs={'pk': croptype.pk})
    data = {'name': 'Soja convencional'}
    response = client.put(url, data, content_type='application/json')
    assert response.status_code == HTTP_200_OK
    croptype.refresh_from_db()
    assert croptype.name == 'Soja convencional'

@pytest.mark.django_db
def test_croptype_delete(client, create_crop_types):
    croptype = create_crop_types[0]
    url = reverse('croptype-detail', kwargs={'pk': croptype.pk})
    response = client.delete(url)
    assert response.status_code == HTTP_204_NO_CONTENT
    assert CropType.objects.count() == 1

@pytest.mark.django_db
def test_croptype_retrieve(client, create_crop_types):
    croptype = create_crop_types[0]
    url = reverse('croptype-detail', kwargs={'pk': croptype.pk})
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.data['name'] == croptype.name

# Negative cases
@pytest.mark.django_db
def test_croptype_create_without_data(client):
    url = reverse('croptype-list')
    data = {}
    response = client.post(url, data, format='json')
    assert response.status_code == HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_croptype_update_nonexistent(client, fake_id):
    url = reverse('croptype-detail', kwargs={'pk': fake_id})
    data = {'name': 'Soja convencional'}
    response = client.put(url, data, content_type='application/json')
    assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_croptype_delete_nonexistent(client, fake_id):
    url = reverse('croptype-detail', kwargs={'pk': fake_id})
    response = client.delete(url)
    assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_croptype_create_with_duplicate_name(client):
    CropType.objects.create(name='Café')
    url = reverse('croptype-list')
    data = {'name': 'Café'}
    response = client.post(url, data, format='json')
    assert response.status_code == HTTP_400_BAD_REQUEST

# Edge/corner/boundary cases
@pytest.mark.django_db
def test_croptype_create_with_long_name(client):
    url = reverse('croptype-list')
    long_name = 'a' * 256
    data = {'name': long_name}
    response = client.post(url, data, format='json')
    assert response.status_code == HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_croptype_update_with_empty_name(client, create_crop_types):
    croptype = create_crop_types[0]
    url = reverse('croptype-detail', kwargs={'pk': croptype.pk})
    data = {'name': ''}
    response = client.put(url, data, content_type='application/json')
    assert response.status_code == HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_croptype_create_with_whitespace_name(client):
    url = reverse('croptype-list')
    data = {'name': '   '}
    response = client.post(url, data, format='json')
    assert response.status_code == HTTP_400_BAD_REQUEST
