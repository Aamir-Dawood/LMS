from rest_framework.routers import DefaultRouter
from .api_views import EmployeeViewSet, DepartmentViewSet, LeaveBalanceViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'departments', DepartmentViewSet)
router.register(r'balances', LeaveBalanceViewSet, basename='balances')

urlpatterns = [
    path('', include(router.urls)),
]
