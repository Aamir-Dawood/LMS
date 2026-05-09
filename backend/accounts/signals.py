from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import LeaveBalance


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_leave_balance_for_new_employee(sender, instance, created, **kwargs):
    if created:
        LeaveBalance.objects.get_or_create(employee=instance)
