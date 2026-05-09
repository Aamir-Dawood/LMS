from rest_framework.routers import DefaultRouter
from .api_views import LeaveRequestViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'requests', LeaveRequestViewSet, basename='leaverequest')

urlpatterns = [
    path('', include(router.urls)),
]
