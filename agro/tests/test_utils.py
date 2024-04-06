import pytest
from agro.utils import validate_cpf_cnpj


# Positive cases
@pytest.mark.parametrize("cpf", ["95181040004", "951.810.400-04"])
def test_validate_cpf_cnpj_with_valid_cpfs(cpf):
    assert validate_cpf_cnpj(cpf) == True, "O CPF válido não foi reconhecido corretamente"

@pytest.mark.parametrize("cnpj", ["77759188000180", "77.759.188/0001-80"])
def test_validate_cpf_cnpj_with_valid_cnpjs(cnpj):
    assert validate_cpf_cnpj(cnpj) == True, "O CNPJ válido não foi reconhecido corretamente"

# Negative cases
@pytest.mark.parametrize("invalid_cpf", ["12345678901", "951.810.400-99"])
def test_validate_cpf_cnpj_with_invalid_cpfs(invalid_cpf):
    assert not validate_cpf_cnpj(invalid_cpf), "Um CPF inválido foi incorretamente identificado como válido"

@pytest.mark.parametrize("invalid_cnpj", ["12345678901234", "77.759.188/0001-99"])
def test_validate_cpf_cnpj_with_invalid_cnpjs(invalid_cnpj):
    assert not validate_cpf_cnpj(invalid_cnpj), "Um CNPJ inválido foi incorretamente identificado como válido"

# Edge/corner/boundary cases
@pytest.mark.parametrize("invalid_value", [
    "00000000000"
    "000.000.000-00",
    "1234567890a",
    "00000000000000",
    "00.000.000/0000-00",
    "1234567890123a",
    "abc",
    "abc12345",
    "!@#$%&*",
    "",
    "   ",
    None,
])
def test_validate_cpf_cnpj_with_invalid_values(invalid_value):
    assert not validate_cpf_cnpj(invalid_value)
