from django import forms
from django.core.exceptions import ValidationError
import datetime
from .models import LeaveRequest

from django import forms
from .models import LeaveRequest
from django.core.exceptions import ValidationError
from datetime import date

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date < date.today():
                raise ValidationError("Start date cannot be in the past")
            if end_date < start_date:
                raise ValidationError("End date must be after start date")
        
        return cleaned_data