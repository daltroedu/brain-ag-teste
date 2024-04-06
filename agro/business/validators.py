def validate_total_area(data):
    return data['arable_area_hectares'] + data['vegetation_area_hectares'] <= data['total_area_hectares']
