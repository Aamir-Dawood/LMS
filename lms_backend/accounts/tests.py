from django.test import TestCase
from .models import Employee, Department
from django.contrib.auth.models import Group

class EmployeeModelTests(TestCase):
    def test_employee_id_generated_on_create(self):
        user = Employee.objects.create_user(username='alice', password='password')
        # Refresh from DB to ensure updates applied
        user.refresh_from_db()
        self.assertIsNotNone(user.employee_id)
        self.assertTrue(user.employee_id.startswith('EMP'))

    def test_department_manager_gets_hr_group(self):
        manager = Employee.objects.create_user(username='manager', password='pass')
        dept = Department.objects.create(name='Engineering')
        # Assign manager to department and also set employee.department to link both sides
        dept.manager = manager
        dept.save()

        # Now set the manager's department and save to trigger group addition
        manager.department = dept
        manager.save()

        managers_group = Group.objects.filter(name='HR_Managers').first()
        self.assertIsNotNone(managers_group)
        self.assertIn(managers_group, manager.groups.all())
