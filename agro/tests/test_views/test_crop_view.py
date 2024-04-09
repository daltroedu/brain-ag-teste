import pytest
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from agro.models import Crop

from ..conftest import fake_id


# Positve cases
@pytest.mark.django_db
def test_crop_list(client, create_farms, create_crop_types):
    farm = create_farms[0]
    crop_type1 = create_crop_types[0]
    crop_type2 = create_crop_types[1]
    Crop.objects.create(farm=farm, crop_type=crop_type1)
    Crop.objects.create(farm=farm, crop_type=crop_type2)
    url = reverse("crop-list")
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 1
    assert len(response.data[0]["crops"]) == 2


@pytest.mark.django_db
def test_crop_create(client, create_farms, create_crop_types):
    farm = create_farms[0]
    crop_type = create_crop_types[0]
    url = reverse("crop-list")
    data = {"farm_id": farm.id, "crop_type_id": crop_type.id}
    response = client.post(url, data, format="json")
    assert response.status_code == HTTP_201_CREATED
    assert Crop.objects.count() == 1
    assert Crop.objects.filter(farm=farm, crop_type=crop_type).exists()


@pytest.mark.django_db
def test_crop_update(client, create_farms, create_crop_types):
    farm = create_farms[0]
    crop_type = create_crop_types[0]
    crop = Crop.objects.create(farm=farm, crop_type=crop_type)
    new_crop_type = create_crop_types[1]
    url = reverse("crop-detail", kwargs={"pk": crop.pk})
    data = {"farm_id": farm.id, "crop_type_id": new_crop_type.id}
    response = client.put(url, data, content_type="application/json")
    assert response.status_code == HTTP_200_OK
    crop.refresh_from_db()
    assert crop.crop_type == new_crop_type


@pytest.mark.django_db
def test_crop_delete(client, create_farms, create_crop_types):
    farm = create_farms[0]
    crop_type = create_crop_types[0]
    crop = Crop.objects.create(farm=farm, crop_type=crop_type)
    url = reverse("crop-detail", kwargs={"pk": crop.pk})
    response = client.delete(url)
    assert response.status_code == HTTP_204_NO_CONTENT
    assert Crop.objects.count() == 0
    assert not Crop.objects.filter(id=crop.id).exists()


@pytest.mark.django_db
def test_crop_retrieve(client, create_farms, create_crop_types):
    farm = create_farms[0]
    crop_type = create_crop_types[0]
    crop = Crop.objects.create(farm=farm, crop_type=crop_type)
    url = reverse("crop-detail", kwargs={"pk": crop.pk})
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.data["farm"]["id"] == str(farm.id)
    assert "crops" in response.data
    assert isinstance(response.data["crops"], list)
    found = False
    for crop_data in response.data["crops"]:
        if crop_data["id"] == crop_type.id:
            found = True
            assert crop_data["name"] == crop_type.name
            break
    assert found


# Negative cases
@pytest.mark.django_db
def test_crop_create_with_invalid_farm(client, create_crop_types):
    crop_type = create_crop_types[0]
    url = reverse("crop-list")
    data = {
        "crop_type_id": crop_type.id,
        "farm_id": fake_id,
    }
    response = client.post(url, data, format="json")
    assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_crop_create_with_invalid_crop_type(client, create_farms):
    farm = create_farms[0]
    url = reverse("crop-list")
    data = {
        "crop_type_id": fake_id,
        "farm_id": farm.id,
    }
    response = client.post(url, data, format="json")
    assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_crop_update_nonexistent(client):
    url = reverse("crop-detail", kwargs={"pk": fake_id})
    data = {
        "crop_type_id": 1,
        "farm_id": 1,
    }
    response = client.put(url, data, content_type="application/json")
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_crop_delete_nonexistent(client):
    url = reverse("crop-detail", kwargs={"pk": fake_id})
    response = client.delete(url)
    assert response.status_code == HTTP_404_NOT_FOUND


# Edge/corner/boundary cases
@pytest.mark.django_db
def test_crop_create_duplicate(client, create_farms, create_crop_types):
    farm = create_farms[0]
    crop_type = create_crop_types[0]
    Crop.objects.create(farm=farm, crop_type=crop_type)
    url = reverse("crop-list")
    data = {
        "crop_type_id": crop_type.id,
        "farm_id": farm.id,
    }
    response = client.post(url, data, format="json")
    assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_crop_update_to_duplicate(client, create_farms, create_crop_types):
    farm = create_farms[0]
    crop_type1, crop_type2 = create_crop_types
    crop1 = Crop.objects.create(farm=farm, crop_type=crop_type1)
    Crop.objects.create(farm=farm, crop_type=crop_type2)
    url = reverse("crop-detail", kwargs={"pk": crop1.pk})
    data = {
        "crop_type_id": crop_type2.id,
        "farm_id": farm.id,
    }
    response = client.put(url, data, content_type="application/json")
    assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_crop_update_to_different_farm(client, create_farms, create_crop_types):
    farm1, farm2 = create_farms
    crop_type = create_crop_types[0]
    crop = Crop.objects.create(farm=farm1, crop_type=crop_type)
    url = reverse("crop-detail", kwargs={"pk": crop.pk})
    data = {
        "crop_type_id": crop_type.id,
        "farm_id": farm2.id,
    }
    response = client.put(url, data, content_type="application/json")
    assert response.status_code == HTTP_200_OK
