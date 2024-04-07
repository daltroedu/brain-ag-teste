from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'farmers', views.FarmerViewSet)
router.register(r'farms', views.FarmViewSet)
router.register(r'crops_type', views.CropTypeViewSet)
router.register(r'crops', views.CropViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.DashboardAPIView.as_view(), name='dashboard'),
]
