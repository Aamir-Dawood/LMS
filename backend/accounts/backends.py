from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import Employee

class EmployeeBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('username') or kwargs.get('email')
        try:
            user = Employee.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=username)
            ).first()
            if user and user.check_password(password):
                return user
        except Employee.DoesNotExist:
            return None
        return None