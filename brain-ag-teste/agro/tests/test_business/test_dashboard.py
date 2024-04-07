import pytest
from agro.business.dashboard import get_dashboard_data
from agro.models import Crop, Farm
from agro.constants import STATE_CHOICES


# Positive cases
@pytest.mark.django_db
def test_get_dashboard_data(create_farms, create_crop_types):
    farm1, farm2 = create_farms
    crop_type1, crop_type2 = create_crop_types
    Crop.objects.create(farm=farm1, crop_type=crop_type1)
    Crop.objects.create(farm=farm2, crop_type=crop_type2)
    dashboard_data = get_dashboard_data()
    expected_total_area = farm1.total_area_hectares + farm2.total_area_hectares
    expected_arable_area = farm1.arable_area_hectares + farm2.arable_area_hectares
    expected_vegetation_area = farm1.vegetation_area_hectares + farm2.vegetation_area_hectares
    assert dashboard_data['farm_count'] == 2
    assert dashboard_data['total_area_hectares'] == expected_total_area
    assert len(dashboard_data['count_by_state']) == 2
    assert len(dashboard_data['farm_count_by_crop']) == 2
    assert dashboard_data['soil_usage']['total_arable_area_hectares'] == expected_arable_area
    assert dashboard_data['soil_usage']['total_vegetation_area_hectares'] == expected_vegetation_area

# Negative cases
@pytest.mark.django_db
def test_get_dashboard_data_empty_db():
    dashboard_data = get_dashboard_data()
    assert dashboard_data['farm_count'] == 0
    assert dashboard_data['total_area_hectares'] == 0
    assert list(dashboard_data['count_by_state']) == []
    assert dashboard_data['farm_count_by_crop'] == []
    assert dashboard_data['soil_usage']['total_arable_area_hectares'] == 0
    assert dashboard_data['soil_usage']['total_vegetation_area_hectares'] == 0

# Edge/corner/boundary cases
@pytest.mark.django_db
def test_get_dashboard_data_with_farm_having_no_arable_or_vegetation_area(create_farmers):
    farmer = create_farmers[0]
    Farm.objects.create(
        name='Fazenda Coração',
        farmer=farmer,
        city='Coração de Maria',
        state='BA',
        total_area_hectares=100,
        arable_area_hectares=0,
        vegetation_area_hectares=0,
    )
    dashboard_data = get_dashboard_data()
    assert dashboard_data['total_area_hectares'] == 100
    assert any(farm['state'] == 'BA' for farm in dashboard_data['count_by_state'])

@pytest.mark.django_db
def test_get_dashboard_data_with_farm_where_arable_and_vegetation_equal_total(create_farmers):
    farmer = create_farmers[0]
    Farm.objects.create(
        name='Fazenda Coração',
        farmer=farmer,
        city='Coração de Maria',
        state='BA',
        total_area_hectares=200,
        arable_area_hectares=100,
        vegetation_area_hectares=100,
    )
    dashboard_data = get_dashboard_data()
    assert dashboard_data['total_area_hectares'] == 200
    assert dashboard_data['soil_usage']['total_arable_area_hectares'] == 100
    assert dashboard_data['soil_usage']['total_vegetation_area_hectares'] == 100

@pytest.mark.django_db
def test_get_dashboard_data_with_farms_in_all_states(create_farmers):
    for state in [state[0] for state in STATE_CHOICES]:
        Farm.objects.create(
            name=f'Fazenda {state}',
            farmer=create_farmers[0],
            city=f'Cidade {state}',
            state=state,
            total_area_hectares=50,
            arable_area_hectares=25,
            vegetation_area_hectares=25,
        )
    dashboard_data = get_dashboard_data()
    assert len(dashboard_data['count_by_state']) == len(STATE_CHOICES)
    for state in STATE_CHOICES:
        assert any(farm['state'] == state[0] for farm in dashboard_data['count_by_state'])
