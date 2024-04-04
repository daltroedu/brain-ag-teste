import pytest
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from .conftest import create_farms, fake_id
from agro.models import Farm


# Positve cases
@pytest.mark.django_db
def test_farm_list(client, create_farms):
    url = reverse('farm-list')
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert len(response.data['results']) == 2

@pytest.mark.django_db
def test_farm_create(client, create_farmers, create_farms):
    farmer = create_farmers[0]
    url = reverse('farm-list')
    data = {
        'name': 'Fazenda Ceará',
        'farmer_id': farmer.id,
        'city': 'Sobral',
        'state': 'CE',
        'total_area_hectares': 300,
        'arable_area_hectares': 200,
        'vegetation_area_hectares': 100,
    }
    response = client.post(url, data, format='json')
    assert response.status_code == HTTP_201_CREATED
    assert Farm.objects.count() == 3

@pytest.mark.django_db
def test_farm_update(client, create_farms):
    farm = create_farms[0]
    url = reverse('farm-detail', kwargs={'pk': farm.pk})
    data = {
        'name': 'Fazenda Barreiras',
        'farmer_id': farm.farmer.id,
        'city': 'Barreiras',
        'state': 'BA',
        'total_area_hectares': 150,
        'arable_area_hectares': 75,
        'vegetation_area_hectares': 75,
    }
    response = client.put(url, data, content_type='application/json')
    assert response.status_code == HTTP_200_OK
    farm.refresh_from_db()
    assert farm.name == 'Fazenda Barreiras'
    assert farm.city == 'Barreiras'
    assert farm.state == 'BA'
    assert farm.total_area_hectares == 150
    assert farm.arable_area_hectares == 75
    assert farm.vegetation_area_hectares == 75

@pytest.mark.django_db
def test_farm_delete(client, create_farms):
    farm = create_farms[0]
    url = reverse('farm-detail', kwargs={'pk': farm.pk})
    response = client.delete(url)
    assert response.status_code == HTTP_204_NO_CONTENT
    assert Farm.objects.count() == 1

@pytest.mark.django_db
def test_farm_retrieve(client, create_farms):
    farm = create_farms[0]
    url = reverse('farm-detail', kwargs={'pk': farm.pk})
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.data['name'] == farm.name
    assert response.data['city'] == farm.city

# Negative cases
@pytest.mark.django_db
def test_farm_create_with_invalid_data(client, create_farmers):
    """
    Cases:
        - XX is a invalid state in STATE_CHOICES/Brazil
        - arable_area_hectares + vegetation_area_hectares > total_area_hectares
    """
    farmer = create_farmers[0]
    url = reverse('farm-list')
    data = {
        'name': 'Fazenda XYZ',
        'farmer_id': farmer.id,
        'city': 'Cidade XYZ',
        'state': 'XX',
        'total_area_hectares': 50,
        'arable_area_hectares': 30,
        'vegetation_area_hectares': 30,
    }
    response = client.post(url, data, format='json')
    assert response.status_code == HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_retrieve_nonexistent_farm(client):
    url = reverse('farm-detail', kwargs={'pk': fake_id})
    response = client.get(url)
    assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_delete_nonexistent_farm(client):
    url = reverse('farm-detail', kwargs={'pk': fake_id})
    response = client.delete(url)
    assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_update_nonexistent_farm(client, create_farmers):
    farmer = create_farmers[0]
    url = reverse('farm-detail', kwargs={'pk': fake_id})
    data = {
        'name': 'Fazenda Igarassu',
        'farmer_id': farmer.id,
        'city': 'Igarassu',
        'state': 'PE',
        'total_area_hectares': 150,
        'arable_area_hectares': 100,
        'vegetation_area_hectares': 50,
    }
    response = client.put(url, data, content_type='application/json')
    assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_farm_create_without_name(client, create_farmers):
    farmer = create_farmers[0]
    url = reverse('farm-list')
    data = {
        'farmer_id': farmer.id,
        'city': 'Igarassu',
        'state': 'PE',
        'total_area_hectares': 100,
        'arable_area_hectares': 50,
        'vegetation_area_hectares': 50,
    }
    response = client.post(url, data, format='json')
    assert response.status_code == HTTP_400_BAD_REQUEST

# Edge/corner/boundary cases
@pytest.mark.django_db
def test_farm_create_with_zero_total_area(client, create_farmers):
    """
    Case: total_area_hectares = 0
    """
    farmer = create_farmers[0]
    url = reverse('farm-list')
    data = {
        'name': 'Fazenda BA',
        'farmer_id': farmer.id,
        'city': 'Vitória da Conquista',
        'state': 'BA',
        'total_area_hectares': 0,
        'arable_area_hectares': 0,
        'vegetation_area_hectares': 0,
    }
    response = client.post(url, data, format='json')
    assert response.status_code == HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_farm_create_with_negative_area_values(client, create_farmers):
    """
    Case: negative values
    """
    farmer = create_farmers[0]
    url = reverse('farm-list')
    data = {
        'name': 'Fazenda BA',
        'farmer_id': farmer.id,
        'city': 'Vitória da Conquista',
        'state': 'BA',
        'total_area_hectares': -100,
        'arable_area_hectares': -50,
        'vegetation_area_hectares': -50,
    }
    response = client.post(url, data, format='json')
    assert response.status_code == HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_farm_update_exceeding_total_area(client, create_farms):
    """
    Case: updating farm so that sum of areas exceeds total area
    """
    farm = create_farms[0]
    url = reverse('farm-detail', kwargs={'pk': farm.pk})
    data = {
        'name': farm.name,
        'city': farm.city,
        'state': farm.state,
        'total_area_hectares': 100,
        'arable_area_hectares': 60,
        'vegetation_area_hectares': 50,
    }
    response = client.put(url, data, content_type='application/json')
    assert response.status_code == HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_farm_update_with_invalid_state(client, create_farms):
    """
    Case: updating farm with an invalid state value in STATE_CHOICES/Brazil
    """
    farm = create_farms[0]
    url = reverse('farm-detail', kwargs={'pk': farm.pk})
    data = {
        'name': farm.name,
        'city': farm.city,
        'state': 'XX',
        'total_area_hectares': farm.total_area_hectares,
        'arable_area_hectares': farm.arable_area_hectares,
        'vegetation_area_hectares': farm.vegetation_area_hectares,
    }
    response = client.put(url, data, content_type='application/json')
    assert response.status_code == HTTP_400_BAD_REQUEST
