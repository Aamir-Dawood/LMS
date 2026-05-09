# from django.contrib import admin
# from django.urls import path, include
# # from django.views.generic.base import RedirectView
# # from django.contrib.auth import views as auth_views
# from django.contrib.auth.views import LoginView, LogoutView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('accounts/', include('accounts.urls')),
#     path('leaves/', include('leaves.urls')),
#     path('accounts/login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
#     # path('', RedirectView.as_view(url='leaves/')),  # Redirect root to leaves app
#     path('accounts/logout/', LogoutView.as_view(next_page='login')), 
# ]

from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import RedirectView
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'accounts': request.build_absolute_uri('/api/accounts/'),
        'leaves': request.build_absolute_uri('/api/leaves/'),
        'token_auth': request.build_absolute_uri('/api/token-auth/'),
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    # API routes (accounts and leaves)
    path('api/accounts/', include('accounts.api_urls')),
    path('api/leaves/', include('leaves.api_urls')),
    # Token auth endpoint
    path('api/token-auth/', obtain_auth_token, name='api-token-auth'),
    # Optional DRF login for browsable API
    path('api-auth/', include('rest_framework.urls')),
    # API root
    path('api/', api_root, name='api-root'),
    # Redirect root to API root
    path('', RedirectView.as_view(url='/api/', permanent=False), name='root-redirect'),

    # Compatibility redirects for legacy UI links (avoid 404s)
    path('accounts/login/', RedirectView.as_view(url='/api/accounts/employees/login/', permanent=False)),
    path('accounts/register/', RedirectView.as_view(url='/api/accounts/employees/', permanent=False)),
    path('accounts/hr-manager/login/', RedirectView.as_view(url='/api/accounts/employees/login/', permanent=False)),
    path('leaves/', RedirectView.as_view(url='/api/leaves/requests/', permanent=False)),
    path('leaves/request/', RedirectView.as_view(url='/api/leaves/requests/', permanent=False)),
    path('leaves/my-leaves/', RedirectView.as_view(url='/api/leaves/requests/', permanent=False)),
    path('leaves/manager/', RedirectView.as_view(url='/api/leaves/requests/manager_dashboard/', permanent=False)),
    path('leaves/hr-manager/', RedirectView.as_view(url='/api/leaves/requests/hr_dashboard/', permanent=False)),
]