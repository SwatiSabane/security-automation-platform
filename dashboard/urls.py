from django.urls import path
from .views import dashboard_home,upload_report
from .api_views import upload_report_api

urlpatterns = [
    path('', dashboard_home, name='dashboard-home'),
    path('upload/', upload_report, name='upload-report'),
    path(
    'api/upload-report/',
    upload_report_api,
    name='upload-report-api'
),
]