from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_center, name='report_center'),
    path('generate/', views.generate_report, name='generate_report'),
    path('success/', views.report_success, name='report_success'),
    path('download/<str:filename>/', views.download_report, name='download_report'),
    path('history/', views.report_history, name='report_history'),
]
