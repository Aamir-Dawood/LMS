from django.contrib import admin
from .models import LeaveRequest

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'status', 'start_date')
    list_filter = ('status', 'leave_type')