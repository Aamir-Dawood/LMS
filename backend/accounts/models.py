# from django.contrib.auth.models import AbstractUser
# from django.db import models

# def generate_employee_id():
#     last_employee = Employee.objects.order_by('id').last()
#     if not last_employee:
#         return "EMP1000"
    
#     # Safely extract numeric part
#     last_id = last_employee.employee_id
#     if last_id.startswith('EMP') and last_id[3:].isdigit():
#         return f"EMP{int(last_id[3:]) + 1}"
#     return "EMP1001"

# class Department(models.Model):
#     name = models.CharField(max_length=100)
#     manager = models.ForeignKey(
#         'Employee',
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='managed_department',
#         blank=True)

# class Employee(AbstractUser):
#     employee_id = models.CharField(max_length=20, unique=True,default=generate_employee_id)
#     department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
#     phone = models.CharField(max_length=15, blank=True)
#     class Meta:
#         verbose_name = 'Employee'  # Singular name
#         verbose_name_plural = 'Employees'  # Plural name

# ----------------------------------SOLUTION FROM CHAT GPT FOR SELF-CUSTOMIZED EMPID-------------------------------------------------------

# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class Department(models.Model):
#     name = models.CharField(max_length=100)
#     manager = models.ForeignKey(
#         'Employee',
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='managed_department',
#         blank=True
#     )

#     def __str__(self):
#         return self.name

# class Employee(AbstractUser):
#     employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
#     department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
#     phone = models.CharField(max_length=15, blank=True)

#     def save(self, *args, **kwargs):
#         if not self.employee_id:
#             # Save to generate a primary key if new
#             super().save(*args, **kwargs)
#             self.employee_id = f"EMP{self.pk + 1000}"
#             Employee.objects.filter(pk=self.pk).update(employee_id=self.employee_id)
#         else:
#             super().save(*args, **kwargs)


#     class Meta:
#         verbose_name = 'Employee'
#         verbose_name_plural = 'Employees'

#     def __str__(self):
#         return f"{self.username} ({self.employee_id})"

# FINAL RESULT FROM DEEPSEEK(IMPROVEMENTS)--------------------------------------------------------------------------------------
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group

class Department(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_departments'
    )

    def __str__(self):
        return self.name

class Employee(AbstractUser):
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        db_index=True
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    phone = models.CharField(max_length=15, blank=True)

    def save(self, *args, **kwargs):
        """Persist employee and ensure business invariants.

        - Auto-generate `employee_id` on first save using format EMP01001
        - Ensure HR_Managers group membership when this user manages their department
        """
        created = self.pk is None
        super().save(*args, **kwargs)

        if created and not self.employee_id:
            # Avoid recursion: update via queryset
            self.employee_id = f"EMP{self.pk + 1000:05d}"
            Employee.objects.filter(pk=self.pk).update(employee_id=self.employee_id)

        # Maintain HR_Managers group membership for department managers
        if hasattr(self, 'department') and self.department and self.department.manager_id == self.id:
            managers_group, _ = Group.objects.get_or_create(name='HR_Managers')
            self.groups.add(managers_group)

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['employee_id']

    def __str__(self):
        return f"{self.username} ({self.employee_id})"
    
class LeaveBalance(models.Model):
    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='leave_balance'
    )
    vacation_days = models.PositiveIntegerField(default=20)
    sick_days = models.PositiveIntegerField(default=10)
    personal_days = models.PositiveIntegerField(default=5)
    
    def deduct_leave(self, leave_type, days):
        field_map = {
            'vacation': 'vacation_days',
            'sick': 'sick_days',
            'personal': 'personal_days'
        }
        field_name = field_map.get(leave_type)
        if not field_name:
            raise ValueError('Unknown leave type')
        if days < 0:
            raise ValueError('Days must be non-negative')

        current = getattr(self, field_name)
        if current < days:
            raise ValueError('Insufficient leave balance')

        setattr(self, field_name, current - days)
        self.save()

