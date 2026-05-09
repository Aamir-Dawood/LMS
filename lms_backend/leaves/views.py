from django.views.generic import TemplateView
# Removed all other imports and classes as they are no longer needed

# Template-based views moved to API. Use leaves.api_views for DRF viewsets.

# Keep placeholder to avoid import errors from other modules that import these names
class DashboardView(TemplateView):
    template_name = 'leaves/dashboard.html'