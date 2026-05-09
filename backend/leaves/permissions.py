from rest_framework import permissions

class IsOwnerOrManagerOrHR(permissions.BasePermission):
    """Allow access if user is owner, department manager of the owner, HR_Managers or superuser."""

    def has_object_permission(self, request, view, obj):
        # obj is a LeaveRequest
        user = request.user
        if user.is_superuser:
            return True
        if getattr(obj, 'employee', None) == user:
            return True
        employee_department = getattr(obj.employee, 'department', None)
        is_manager = employee_department is not None and employee_department.manager_id == user.id
        is_hr = user.groups.filter(name='HR_Managers').exists()
        return is_manager or is_hr

    def has_permission(self, request, view):
        # Allow authenticated users to list/create; object-level will enforce later
        return request.user and request.user.is_authenticated
