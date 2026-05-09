from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db import transaction

class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ('vacation', 'Vacation'),
        ('sick', 'Sick Leave'),
        ('personal', 'Personal Leave')
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    # Core Fields
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    days_requested = models.PositiveIntegerField(default=1)  # Added field
    
    # Approval Fields
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_requests'
    )
    comments = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Leave Request'
        verbose_name_plural = 'Leave Requests'

    def __str__(self):
        return f"{self.employee.username} - {self.get_leave_type_display()} ({self.status})"

    def save(self, *args, **kwargs):
        if not self.pk:  # Only calculate for new instances
            self.days_requested = self.calculate_business_days()
        super().save(*args, **kwargs)

    def calculate_business_days(self):
        """
        Calculate business days (Mon-Fri) between start and end dates
        """
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            business_days = 0
            for day in range(delta.days + 1):
                if (self.start_date + timedelta(days=day)).weekday() < 5:
                    business_days += 1
            return max(1, business_days)  # Ensure at least 1 day
        return 1

    def approve(self, manager):
        """Approve this leave request with balance validation and transactional safety"""
        from accounts.models import LeaveBalance

        with transaction.atomic():
            # Lock or create the leave balance row for this employee
            try:
                employee_balance = LeaveBalance.objects.select_for_update().get(employee=self.employee)
            except LeaveBalance.DoesNotExist:
                employee_balance = LeaveBalance.objects.create(employee=self.employee)

            # Map leave type to field name
            field_map = {
                'vacation': 'vacation_days',
                'sick': 'sick_days',
                'personal': 'personal_days'
            }
            field_name = field_map.get(self.leave_type)
            if not field_name:
                raise ValueError('Unknown leave type')

            current = getattr(employee_balance, field_name)
            if current < self.days_requested:
                raise ValueError('Insufficient leave balance')

            # Deduct and persist
            setattr(employee_balance, field_name, current - self.days_requested)
            employee_balance.save()

            self.status = 'approved'
            self.approved_by = manager
            self.save()

    def reject(self, manager, reason):
        """Reject this leave request with a reason"""
        self.status = 'rejected'
        self.approved_by = manager
        self.comments = reason
        self.save()

    @property
    def is_pending(self):
        return self.status == 'pending'

    @property
    def is_approved(self):
        return self.status == 'approved'

    @property
    def is_rejected(self):
        return self.status == 'rejected'