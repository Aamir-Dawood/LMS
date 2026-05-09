# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import Employee, Department

# @admin.register(Department)
# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'manager')
#     search_fields = ('name',)
#     # list_select_related = ('manager',)
#     pass

# @admin.register(Employee)
# class EmployeeAdmin(UserAdmin):
#     verbose_name = 'Employee'
#     verbose_name_plural = 'Employees'
#     list_display = ('username', 'email', 'department', 'is_staff')
#     # list_filter = ('is_staff', 'department')
#     fieldsets = UserAdmin.fieldsets + (
#         ('Employee Info', {'fields': ('employee_id', 'department', 'phone')}),
#     )

# admin.site.register(Department, DepartmentAdmin)
# admin.site.register(Employee)  # Explicit registration
# admin.site.register(Department)

# FINALIZED SOLUTION AFTER CREATING EMPID FROM CHATGPT------------------------------------------------------------------
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import Employee, Department

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
    
    def clean_employee_id(self):
        emp_id = self.cleaned_data['employee_id']
        if emp_id and not emp_id.startswith('EMP'):
            raise forms.ValidationError("Employee IDs must start with 'EMP'")
        return emp_id

@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    form = EmployeeForm
    list_display = ('username', 'email', 'employee_id', 'department', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Employee Info', {
            'fields': ('employee_id', 'department', 'phone'),
        }),
    )

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager')
    search_fields = ('name',)