from django.conf import settings
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Farmer, Farm, CropType, Crop
from .serializers import FarmerSerializer, FarmSerializer, CropTypeSerializer, CropSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = settings.REST_FRAMEWORK_PAGINATION['DEFAULT_PAGE_SIZE']
    page_query_param = settings.REST_FRAMEWORK_PAGINATION['DEFAULT_PAGE_QUERY_PARAM']
    max_page_size = settings.REST_FRAMEWORK_PAGINATION['MAX_PAGE_SIZE']


class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    pagination_class = StandardResultsSetPagination
