import pytest
from django.db import IntegrityError
from ..models import Crop


@pytest.mark.django_db
def test_create_farmer(create_farmers):
    for farmer in create_farmers:
        assert farmer.id is not None

@pytest.mark.django_db
def test_farmer_unique_cpf_cnpj(create_farmers):
    farmer = create_farmers[0]
    with pytest.raises(IntegrityError):
        farmer.__class__.objects.create(cpf_cnpj=farmer.cpf_cnpj, name="Maria")

@pytest.mark.django_db
def test_create_farm(create_farms):
    for farm in create_farms:
        assert farm.id is not None

@pytest.mark.django_db
def test_create_crop_type(create_crop_types):
    for crop_type in create_crop_types:
        assert crop_type.id is not None

@pytest.mark.django_db
def test_crop_type_unique_name(create_crop_types):
    crop_type = create_crop_types[0]
    with pytest.raises(IntegrityError):
        crop_type.__class__.objects.create(name=crop_type.name)

@pytest.mark.django_db
def test_create_crop(create_farms, create_crop_types):
    farm = create_farms[0]
    crop_type = create_crop_types[0]
    crop = Crop.objects.create(farm=farm, crop_type=crop_type)
    assert crop.id is not None

@pytest.mark.django_db
def test_crop_unique_together_constraint(create_farms, create_crop_types):
    farm = create_farms[0]
    crop_type = create_crop_types[0]
    Crop.objects.create(farm=farm, crop_type=crop_type)
    with pytest.raises(IntegrityError):
        Crop.objects.create(farm=farm, crop_type=crop_type)
