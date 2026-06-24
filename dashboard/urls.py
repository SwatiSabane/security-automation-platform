from django.urls import path
from .views import dashboard_home,upload_report

urlpatterns = [
    path('', dashboard_home, name='dashboard-home'),
    path('upload/', upload_report, name='upload-report'),
]