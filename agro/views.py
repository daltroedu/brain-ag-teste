import logging

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .business.dashboard import get_dashboard_data
from .models import Crop, CropType, Farm, Farmer
from .pagination import StandardResultsSetPagination
from .serializers import (
    CropSerializer,
    CropTypeSerializer,
    FarmerSerializer,
    FarmSerializer,
)

logger = logging.getLogger(__name__)


class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.order_by("-updated_at").all()
    serializer_class = FarmerSerializer
    pagination_class = StandardResultsSetPagination


class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.select_related("farmer").order_by("-updated_at").all()
    serializer_class = FarmSerializer
    pagination_class = StandardResultsSetPagination


class CropTypeViewSet(viewsets.ModelViewSet):
    queryset = CropType.objects.order_by("id").all()
    serializer_class = CropTypeSerializer


class CropViewSet(viewsets.ModelViewSet):
    queryset = (
        Crop.objects.select_related("crop_type", "farm", "farm__farmer")
        .order_by("-updated_at")
        .all()
    )
    serializer_class = CropSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        farm_data = {}
        for crop in queryset:
            farm_id = crop.farm.id
            if farm_id not in farm_data:
                farm_data[farm_id] = {
                    "tttt_id": crop.id,
                    "farm": FarmSerializer(crop.farm).data,
                    "crops": [],
                }
            farm_data[farm_id]["crops"].append(
                {"id": crop.crop_type.id, "name": crop.crop_type.name}
            )
        response_data = [value for value in farm_data.values()]
        return Response(response_data)


class DashboardAPIView(APIView):
    def get(self, request):
        try:
            dashboard_data = get_dashboard_data()
            return Response(dashboard_data)
        except Exception as e:
            logger.error(f"Erro ao recuperar dados do dashboard: {e}", exc_info=True)
            return Response(
                {"error": "Ocorreu um erro ao processar sua solicitação."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
