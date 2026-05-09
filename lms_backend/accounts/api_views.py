from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Employee, Department, LeaveBalance
from .serializers import EmployeeSerializer, DepartmentSerializer, LeaveBalanceSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_permissions(self):
        # Allow unauthenticated creation (registration) and login
        if self.action in ['create', 'login']:
            return [permissions.AllowAny()]
        if self.action == 'list':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # create token for the new user
        token, _ = Token.objects.get_or_create(user=user)
        data = serializer.data
        data['token'] = token.key
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            data = EmployeeSerializer(user, context={'request': request}).data
            data['token'] = token.key
            return Response(data)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class LeaveBalanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LeaveBalance.objects.select_related('employee')
    serializer_class = LeaveBalanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users see only their balance unless staff
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(employee=user)
