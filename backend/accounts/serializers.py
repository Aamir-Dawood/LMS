from rest_framework import serializers
from .models import Employee, Department, LeaveBalance

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'manager']

class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), allow_null=True, required=False)
    groups = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = Employee
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'employee_id', 'department', 'phone', 'is_staff', 'is_superuser', 'groups']
        read_only_fields = ['employee_id']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = Employee(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class LeaveBalanceSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = LeaveBalance
        fields = ['employee', 'vacation_days', 'sick_days', 'personal_days']
