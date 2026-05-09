from django.urls import path, include

app_name = 'accounts'

urlpatterns = [
    path('', include('accounts.api_urls')),
]