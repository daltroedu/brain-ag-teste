import pytest
from rest_framework.exceptions import ValidationError
from ..serializers import FarmerSerializer, FarmSerializer, CropTypeSerializer, CropSerializer
from ..models import Farm, Crop


@pytest.mark.django_db
def test_farmer_serializer_serialization(create_farmers):
    farmer = create_farmers[0]
    serializer = FarmerSerializer(farmer)
    assert serializer.data == {
        'id': str(farmer.id),
        'cpf_cnpj': farmer.cpf_cnpj,
        'name': farmer.name,
    }

@pytest.mark.django_db
def test_farmer_serializer_deserialization_and_creation():
    valid_data = {
        'cpf_cnpj': '90196790077',
        'name': 'Maria',
    }
    serializer = FarmerSerializer(data=valid_data)
    assert serializer.is_valid()
    farmer = serializer.save()
    assert farmer.cpf_cnpj == valid_data['cpf_cnpj']
    assert farmer.name == valid_data['name']

@pytest.mark.django_db
def test_farmer_serializer_deserialization_with_invalid_data():
    invalid_data = {
        'cpf_cnpj': '12345',
        'name': '',
    }
    serializer = FarmerSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'cpf_cnpj' in serializer.errors
    assert 'name' in serializer.errors

@pytest.mark.django_db
def test_farm_serializer_serialization(create_farms):
    farm = create_farms[0]
    serializer = FarmSerializer(farm)
    assert 'id' in serializer.data
    assert serializer.data['name'] == farm.name
    assert 'farmer' in serializer.data

@pytest.mark.django_db
def test_farm_serializer_deserialization_and_creation(create_farmers):
    farmer = create_farmers[0]
    valid_data = {
        'farmer_id': farmer.id,
        'name': 'Fazenda BA',
        'city': 'Juazeiro',
        'state': 'BA',
        'total_area_hectares': 100.0,
        'arable_area_hectares': 50.0,
        'vegetation_area_hectares': 30.0,
    }
    serializer = FarmSerializer(data=valid_data)
    assert serializer.is_valid()
    farm = serializer.save()
    assert Farm.objects.filter(id=farm.id).exists()
    assert farm.name == 'Fazenda BA'

@pytest.mark.django_db
def test_farm_serializer_state_validation():
    data = {'state': 'XX'}
    serializer = FarmSerializer(data=data)
    assert not serializer.is_valid()
    assert 'state' in serializer.errors

@pytest.mark.django_db
def test_farm_serializer_negative_values(create_farmers):
    farmer = create_farmers[0]
    invalid_data = {
        'farmer_id': farmer.id,
        'name': 'Fazenda BA',
        'city': 'Juazeiro',
        'state': 'BA',
        'total_area_hectares': -100,
        'arable_area_hectares': -50.0,
        'vegetation_area_hectares': -30.0,
    }
    serializer = FarmSerializer(data=invalid_data)
    assert not serializer.is_valid()

@pytest.mark.django_db
def test_crop_type_serializer_serialization(create_crop_types):
    crop_type = create_crop_types[0]
    serializer = CropTypeSerializer(crop_type)
    assert serializer.data == {"id": crop_type.id, "name": crop_type.name}

@pytest.mark.django_db
def test_crop_type_serializer_deserialization_and_creation(create_crop_types):
    valid_data = {"name": "Café"}
    serializer = CropTypeSerializer(data=valid_data)
    assert serializer.is_valid()
    instance = serializer.save()
    assert instance.name == "Café"

@pytest.mark.django_db
def test_crop_type_serializer_validation(create_crop_types):
    existing_crop_type = create_crop_types[0]
    invalid_data = {"name": existing_crop_type.name}
    serializer = CropTypeSerializer(data=invalid_data)
    assert not serializer.is_valid()


@pytest.mark.django_db
def test_crop_serializer_serialization(create_farms, create_crop_types):
    farm = create_farms[0]
    crop_type = create_crop_types[0]
    crop = Crop.objects.create(farm=farm, crop_type=crop_type)
    serializer = CropSerializer(crop)
    expected_data = {
        "id": str(crop.id),
        "farm": FarmSerializer(farm).data,
        "crop_type": CropTypeSerializer(crop_type).data,
    }
    assert serializer.data == expected_data

@pytest.mark.django_db
def test_crop_serializer_deserialization_and_creation(create_farms, create_crop_types):
    farm = create_farms[0]
    crop_type = create_crop_types[0]
    valid_data = {
        "farm_id": farm.id,
        "crop_type_id": crop_type.id
    }
    serializer = CropSerializer(data=valid_data)
    assert serializer.is_valid()
    instance = serializer.save()
    assert instance.farm == farm
    assert instance.crop_type == crop_type

@pytest.mark.django_db
def test_crop_serializer_create_with_duplicate_data(create_farms, create_crop_types):
    farm = create_farms[0]
    crop_type = create_crop_types[0]
    Crop.objects.create(farm=farm, crop_type=crop_type)
    duplicate_data = {
        "farm_id": farm.id,
        "crop_type_id": crop_type.id
    }
    serializer = CropSerializer(data=duplicate_data)
    with pytest.raises(ValidationError) as exc_info:
        serializer.is_valid(raise_exception=True)
        serializer.save()
    assert exc_info.value.detail[0].code == 'invalid'
    assert str(exc_info.value.detail[0]) == serializer.integrity_error_message

@pytest.mark.django_db
def test_crop_serializer_update_with_duplicate_data(create_farms, create_crop_types):
    farm1, farm2 = create_farms
    crop_type = create_crop_types[0]
    crop1 = Crop.objects.create(farm=farm1, crop_type=crop_type)
    Crop.objects.create(farm=farm2, crop_type=crop_type)
    update_data = {
        "farm_id": farm2.id,
        "crop_type_id": crop_type.id
    }
    serializer = CropSerializer(instance=crop1, data=update_data)
    with pytest.raises(ValidationError) as exc_info:
        serializer.is_valid(raise_exception=True)
        serializer.save()
    assert exc_info.value.detail[0].code == 'invalid'
    assert str(exc_info.value.detail[0]) == serializer.integrity_error_message
