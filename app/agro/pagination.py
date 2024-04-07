from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = settings.REST_FRAMEWORK_PAGINATION["DEFAULT_PAGE_SIZE"]
    page_query_param = settings.REST_FRAMEWORK_PAGINATION["DEFAULT_PAGE_QUERY_PARAM"]
    max_page_size = settings.REST_FRAMEWORK_PAGINATION["MAX_PAGE_SIZE"]
