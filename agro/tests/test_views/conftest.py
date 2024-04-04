import pytest
from agro.models import Farmer

@pytest.fixture
def create_farmers(db):
    farmers = [
        Farmer.objects.create(name='João', cpf_cnpj='42442756064'),
        Farmer.objects.create(name='Maria', cpf_cnpj='55678926000122')
    ]
    return farmers
