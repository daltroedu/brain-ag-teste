import logging
from django.conf import settings
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Farmer, Farm, CropType, Crop
from .serializers import FarmerSerializer, FarmSerializer, CropTypeSerializer, CropSerializer
from .business.dashboard import get_dashboard_data

logger = logging.getLogger(__name__)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = settings.REST_FRAMEWORK_PAGINATION['DEFAULT_PAGE_SIZE']
    page_query_param = settings.REST_FRAMEWORK_PAGINATION['DEFAULT_PAGE_QUERY_PARAM']
    max_page_size = settings.REST_FRAMEWORK_PAGINATION['MAX_PAGE_SIZE']


class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    pagination_class = StandardResultsSetPagination


class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.select_related('farmer').all()
    serializer_class = FarmSerializer
    pagination_class = StandardResultsSetPagination


class CropTypeViewSet(viewsets.ModelViewSet):
    queryset = CropType.objects.all()
    serializer_class = CropTypeSerializer


class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.select_related('crop_type').prefetch_related('farm').all()
    serializer_class = CropSerializer
    pagination_class = StandardResultsSetPagination


class DashboardAPIView(APIView):
    def get(self, request):
        try:
            dashboard_data = get_dashboard_data()
            return Response(dashboard_data)
        except Exception as e:
            logger.error(f"Erro ao recuperar dados do dashboard: {e}", exc_info=True)
            return Response({'error': 'Ocorreu um erro ao processar sua solicitação.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
