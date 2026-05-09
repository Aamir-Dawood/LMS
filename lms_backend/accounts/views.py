from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import Employee, Department
from django.contrib import messages
from django.contrib.auth import views as auth_views
import logging

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


logger = logging.getLogger(__name__)

# Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Employee ID is now generated in Employee.save(); do not set here
            # employee = Employee.objects.get(pk=user.pk)
            # employee.employee_id = f"EMP{user.pk + 1000:05d}"
            # employee.save()
            
            login(request, user)
            messages.success(request, "Registration successful! Please complete your profile.")
            return redirect('profile-edit')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Profile Views
@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
        'is_manager': Department.objects.filter(manager=user).exists()
    }
    return render(request, 'accounts/profile.html', context)

class ProfileUpdateView(UpdateView):
    model = Employee
    fields = ['first_name', 'last_name', 'email', 'phone', 'department']
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)

# Enhanced Login View
@sensitive_post_parameters()
@csrf_protect
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('leaves:dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            
            # Safe department manager check
            if hasattr(user, 'department') and user.department and user.department.manager == user:
                return redirect('leaves:manager-dashboard')
            return redirect('leaves:dashboard')
        
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

# Keep the original LoginView as fallback
class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        is_manager = Department.objects.filter(manager=user).exists()
        
        logger.info(f"User {user.username} logged in via LoginView. Manager: {is_manager}")
        messages.success(self.request, f"Welcome, {user.get_full_name() or user.username}!")
        
        if is_manager:
            return redirect('leaves:manager-dashboard')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)
    
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group

def hr_manager_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is in HR_Managers group
            if user.groups.filter(name='HR_Managers').exists():
                login(request, user)
                return redirect('leaves:hr-manager-dashboard')
            else:
                messages.error(request, "This account is not authorized for HR Manager access")
        else:
            messages.error(request, "Invalid credentials")
    
    return render(request, 'accounts/hr_manager_login.html')

# Template views removed in API-only migration. Use API viewsets in accounts.api_views instead.