from django.db.models import Sum, Count
from agro.models import Farm, Crop


def get_dashboard_data():
    farm_count = Farm.objects.count()
    total_area = Farm.objects.aggregate(total=Sum('total_area_hectares'))['total'] or 0
    count_per_state = Farm.objects.values('state').annotate(total=Count('state')).order_by('state')
    count_per_crop = Crop.objects.values('crop_type__name').annotate(total=Count('farm', distinct=True)).order_by('crop_type__name')
    count_per_crop = [{'crop_type_name': item['crop_type__name'], 'total': item['total']} for item in count_per_crop]
    total_arable = Farm.objects.aggregate(total=Sum('arable_area_hectares'))['total'] or 0
    total_vegetation = Farm.objects.aggregate(total=Sum('vegetation_area_hectares'))['total'] or 0
    dashboard_data = {
        'farm_count': farm_count,
        'total_area_hectares': total_area,
        'soil_usage': {
            'total_arable_area_hectares': total_arable,
            'total_vegetation_area_hectares': total_vegetation
        },
        'farm_count_by_crop': count_per_crop,
        'count_by_state': count_per_state,
    }
    return dashboard_data
