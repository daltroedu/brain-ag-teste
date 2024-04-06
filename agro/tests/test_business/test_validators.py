import pytest
from agro.business.validators import validate_total_area


@pytest.mark.parametrize("data, expected", [
    ({"arable_area_hectares": 50, "vegetation_area_hectares": 30, "total_area_hectares": 100}, True),
    ({"arable_area_hectares": 70, "vegetation_area_hectares": 30, "total_area_hectares": 100}, True),
])
def test_validate_total_area_positive_cases(data, expected):
    assert validate_total_area(data) == expected

@pytest.mark.parametrize("data, expected", [
    ({"arable_area_hectares": 60, "vegetation_area_hectares": 50, "total_area_hectares": 100}, False),
    ({"arable_area_hectares": 101, "vegetation_area_hectares": 0, "total_area_hectares": 100}, False),
])
def test_validate_total_area_negative_cases(data, expected):
    assert validate_total_area(data) == expected

@pytest.mark.parametrize("data, expected", [
    ({"arable_area_hectares": 0, "vegetation_area_hectares": 0, "total_area_hectares": 0}, True),
    ({"arable_area_hectares": 100, "vegetation_area_hectares": 0, "total_area_hectares": 100}, True),
    ({"arable_area_hectares": 0, "vegetation_area_hectares": 100, "total_area_hectares": 100}, True),
    ({"arable_area_hectares": 50, "vegetation_area_hectares": 50, "total_area_hectares": 100}, True),
])
def test_validate_total_area_edge_cases(data, expected):
    assert validate_total_area(data) == expected
