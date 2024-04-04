import pytest
from agro.models import Farmer, Farm, CropType

@pytest.fixture
def create_farmers(db):
    farmers = [
        Farmer.objects.create(name='João', cpf_cnpj='42442756064'),
        Farmer.objects.create(name='Maria', cpf_cnpj='55678926000122')
    ]
    return farmers

@pytest.fixture
def create_farms(db, create_farmers):
    farmer1, farmer2 = create_farmers
    farms = [
        Farm.objects.create(
            name='Fazenda Bahia',
            farmer=farmer1,
            city='Juazeiro',
            state='BA',
            total_area_hectares=100,
            arable_area_hectares=50,
            vegetation_area_hectares=50,
        ),
        Farm.objects.create(
            name='Fazenda Minas',
            farmer=farmer2,
            city='Salinas',
            state='MG',
            total_area_hectares=200,
            arable_area_hectares=150,
            vegetation_area_hectares=50,
        ),
    ]
    return farms

@pytest.fixture
def create_crop_types(db):
    crop_types = [
        CropType.objects.create(name='Soja'),
        CropType.objects.create(name='Milho'),
    ]
    return crop_types

@pytest.fixture
def fake_id():
    return "01234567-8901-2345-6789-012345678901-XYZ"
