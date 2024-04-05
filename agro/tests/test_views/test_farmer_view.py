import pytest
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from .conftest import create_farmers, fake_id
from agro.models import Farmer


# Positve cases
@pytest.mark.django_db
def test_farmer_list(client, create_farmers):
    url = reverse('farmer-list')
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert len(response.data['results']) == 2

@pytest.mark.django_db
def test_farmer_create(client):
    url = reverse('farmer-list')
    data = {'name': 'João', 'cpf_cnpj': '53545781089'}
    response = client.post(url, data, format='json')
    assert response.status_code == HTTP_201_CREATED
    assert Farmer.objects.count() == 1

@pytest.mark.django_db
def test_farmer_update(client, create_farmers):
    farmer = create_farmers[0]
    url = reverse('farmer-detail', kwargs={'pk': farmer.pk})
    data = {'name': 'João Silva', 'cpf_cnpj': '53545781089'}
    response = client.put(url, data, content_type='application/json')
    assert response.status_code == HTTP_200_OK
    farmer.refresh_from_db()
    assert farmer.name == 'João Silva'

@pytest.mark.django_db
def test_farmer_delete(client, create_farmers):
    farmer = create_farmers[0]
    url = reverse('farmer-detail', kwargs={'pk': farmer.pk})
    response = client.delete(url)
    assert response.status_code == HTTP_204_NO_CONTENT
    assert Farmer.objects.count() == 1

@pytest.mark.django_db
def test_farmer_retrieve(client, create_farmers):
    farmer = create_farmers[0]
    url = reverse('farmer-detail', kwargs={'pk': farmer.pk})
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.data['name'] == farmer.name
    assert response.data['cpf_cnpj'] == farmer.cpf_cnpj

# Negative cases
@pytest.mark.django_db
def test_retrieve_nonexistent_farmer(client):
    url = reverse('farmer-detail', kwargs={'pk': fake_id})
    response = client.get(url)
    assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_delete_nonexistent_farmer(client):
    url = reverse('farmer-detail', kwargs={'pk': fake_id})
    response = client.delete(url)
    assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_update_nonexistent_farmer(client):
    url = reverse('farmer-detail', kwargs={'pk': fake_id})
    data = {'name': 'Novo Nome', 'cpf_cnpj': '12345678901'}
    response = client.put(url, data, content_type='application/json')
    assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_create_farmer_with_incomplete_data(client):
    url = reverse('farmer-list')
    incomplete_data = {}
    response = client.post(url, incomplete_data, format='json')
    assert response.status_code == HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_update_farmer_with_invalid_data(client, create_farmers):
    farmer = create_farmers[0]
    url = reverse('farmer-detail', kwargs={'pk': farmer.pk})
    invalid_data = {'name': 'João', 'cpf_cnpj': None}
    response = client.put(url, invalid_data, content_type='application/json')
    assert response.status_code == HTTP_400_BAD_REQUEST

# Edge/corner/boundary cases
@pytest.mark.django_db
def test_create_farmer_with_invalid_cpf_cnpj_format(client):
    url = reverse('farmer-list')
    data = {'name': 'João', 'cpf_cnpj': '1234'}
    response = client.post(url, data, format='json')
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert 'cpf_cnpj' in response.data

@pytest.mark.django_db
def test_create_farmer_without_name(client):
    url = reverse('farmer-list')
    data = {'cpf_cnpj': '53545781089'}
    response = client.post(url, data, format='json')
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert 'name' in response.data

@pytest.mark.django_db
def test_create_farmer_without_cpf_cnpj(client):
    url = reverse('farmer-list')
    data = {'name': 'João'}
    response = client.post(url, data, format='json')
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert 'cpf_cnpj' in response.data

@pytest.mark.django_db
def test_update_farmer_to_existing_cpf_cnpj(client, create_farmers):
    farmer_to_update = create_farmers[0]
    existing_farmer_cpf_cnpj = create_farmers[1].cpf_cnpj
    url = reverse('farmer-detail', kwargs={'pk': farmer_to_update.pk})
    data = {'name': farmer_to_update.name, 'cpf_cnpj': existing_farmer_cpf_cnpj}
    response = client.put(url, data, content_type='application/json')
    assert response.status_code == HTTP_400_BAD_REQUEST
