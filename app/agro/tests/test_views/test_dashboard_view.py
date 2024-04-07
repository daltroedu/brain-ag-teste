import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from agro.models import Crop, Farm


# Positive cases
@pytest.mark.django_db
def test_dashboard_api_view(client, create_farms, create_crop_types):
    farm1, farm2 = create_farms
    crop_type1, crop_type2 = create_crop_types
    Crop.objects.create(farm=farm1, crop_type=crop_type1)
    Crop.objects.create(farm=farm2, crop_type=crop_type2)
    url = reverse("dashboard")
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.data["farm_count"] == 2
    assert (
        response.data["total_area_hectares"]
        == farm1.total_area_hectares + farm2.total_area_hectares
    )
    assert any(
        item["state"] == farm1.state and item["total"] == 1
        for item in response.data["count_by_state"]
    )
    assert any(
        item["state"] == farm2.state and item["total"] == 1
        for item in response.data["count_by_state"]
    )
    assert any(
        item["crop_type_name"] == crop_type1.name and item["total"] == 1
        for item in response.data["farm_count_by_crop"]
    )
    assert any(
        item["crop_type_name"] == crop_type2.name and item["total"] == 1
        for item in response.data["farm_count_by_crop"]
    )
    assert (
        response.data["soil_usage"]["total_arable_area_hectares"]
        == farm1.arable_area_hectares + farm2.arable_area_hectares
    )
    assert (
        response.data["soil_usage"]["total_vegetation_area_hectares"]
        == farm1.vegetation_area_hectares + farm2.vegetation_area_hectares
    )


# Negative cases
@pytest.mark.django_db
def test_dashboard_api_view_no_data(client):
    url = reverse("dashboard")
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.data["farm_count"] == 0
    assert response.data["total_area_hectares"] == 0
    assert len(response.data["count_by_state"]) == 0
    assert len(response.data["farm_count_by_crop"]) == 0
    assert response.data["soil_usage"]["total_arable_area_hectares"] == 0
    assert response.data["soil_usage"]["total_vegetation_area_hectares"] == 0


# Edge/corner/boundary cases
@pytest.mark.django_db
def test_dashboard_api_view_extreme_data(client, create_farmers, create_crop_types):
    farmer = create_farmers[0]
    crop_type = create_crop_types[0]
    for i in range(1000):
        Farm.objects.create(
            name=f"Fazenda {i}",
            farmer=farmer,
            city="Juazeiro",
            state="BA",
            total_area_hectares=10000 * i,
            arable_area_hectares=5000 * i,
            vegetation_area_hectares=5000 * i,
        )
    for i in range(100):
        Crop.objects.create(
            farm=Farm.objects.all()[i],
            crop_type=crop_type,
        )
    url = reverse("dashboard")
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.data["farm_count"] == 1000
    assert response.data["total_area_hectares"] == sum([10000 * i for i in range(1000)])
    assert response.data["soil_usage"]["total_arable_area_hectares"] == sum(
        [5000 * i for i in range(1000)]
    )
    assert response.data["soil_usage"]["total_vegetation_area_hectares"] == sum(
        [5000 * i for i in range(1000)]
    )
    assert len(response.data["farm_count_by_crop"]) == 1
