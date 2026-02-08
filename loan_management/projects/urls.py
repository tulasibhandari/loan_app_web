from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    # Main project form with formset
    path('<str:member_number>/', views.project_form, name='project_name'),

    # Individual project operations
    path('<str:member_number>/create/', views.project_create, name='project_create'),
    path('edit/<int:project_id>/', views.project_edit, name='project_edit'),
    path('delete/<int:project_id>/', views.project_delete, name='project_delete'),

    # List and Detail views
    path('<str:member_number>/list/', views.project_list, name='project_list'),
    path('detail/<int:project_id>/', views.project_detail, name='project_detail'),
]
