from django.urls import path, include

app_name = 'leaves'

urlpatterns = [
    path('', include('leaves.api_urls')),
]