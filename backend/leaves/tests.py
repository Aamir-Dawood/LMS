from django.test import TestCase
from accounts.models import Employee, LeaveBalance, Department
from .models import LeaveRequest
from datetime import date

class LeaveRequestTests(TestCase):
    def setUp(self):
        self.emp = Employee.objects.create_user(username='bob', password='pass')
        LeaveBalance.objects.create(employee=self.emp, vacation_days=5, sick_days=2, personal_days=1)

    def test_business_days_calculation(self):
        lr = LeaveRequest(employee=self.emp, leave_type='vacation', start_date=date(2026,5,4), end_date=date(2026,5,8), reason='test')
        self.assertEqual(lr.calculate_business_days(), 5)

    def test_approve_with_insufficient_balance_raises(self):
        lr = LeaveRequest.objects.create(employee=self.emp, leave_type='vacation', start_date=date(2026,5,4), end_date=date(2026,5,15), reason='long')
        with self.assertRaises(ValueError):
            lr.approve(self.emp)

    def test_approve_deducts_balance(self):
        lr = LeaveRequest.objects.create(employee=self.emp, leave_type='vacation', start_date=date(2026,5,4), end_date=date(2026,5,6), reason='short')
        # 3 business days
        lr.approve(self.emp)
        lb = LeaveBalance.objects.get(employee=self.emp)
        self.assertEqual(lb.vacation_days, 2)
