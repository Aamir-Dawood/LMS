from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer, LeaveDecisionSerializer
from .permissions import IsOwnerOrManagerOrHR

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all().select_related('employee', 'approved_by')
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrManagerOrHR]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser or user.groups.filter(name='HR_Managers').exists() or user.username == 'hr_manager':
            return super().get_queryset()
        return super().get_queryset().filter(employee=user)

    def perform_create(self, serializer):
        instance = serializer.save(employee=self.request.user)
        # recalc business days and save
        instance.days_requested = instance.calculate_business_days()
        instance.save()

    @action(detail=False, methods=['get'])
    def manager_dashboard(self, request):
        user = request.user
        # Only managers and superusers can access
        if not (hasattr(user, 'department') and user.department and user.department.manager_id == user.id) and not user.is_superuser:
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        qs = LeaveRequest.objects.filter(employee__department=user.department, status='pending').select_related('employee')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def hr_dashboard(self, request):
        user = request.user
        if not (user.groups.filter(name='HR_Managers').exists() or user.is_superuser):
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        qs = LeaveRequest.objects.filter(status='pending').select_related('employee')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def decision(self, request, pk=None):
        leave = self.get_object()
        serializer = LeaveDecisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = serializer.validated_data['action']
        comments = serializer.validated_data.get('comments', '')

        # permission check: manager or hr
        user = request.user
        employee_department = getattr(leave.employee, 'department', None)
        is_manager = employee_department is not None and employee_department.manager_id == user.id
        is_hr = user.groups.filter(name='HR_Managers').exists()
        if not (is_manager or is_hr or user.is_superuser):
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        try:
            if action == 'approve':
                leave.approve(user)
                return Response({'detail': 'approved'})
            else:
                leave.reject(user, comments)
                return Response({'detail': 'rejected'})
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
