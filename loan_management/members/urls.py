from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    # Member CRUD
    path('', views.member_list, name='member_list'),
    path('create/', views.member_create, name='member_create'),
    path('<str:member_number>/', views.member_detail, name='member_detail'),
    path('<str:member_number>/edit/', views.member_edit, name='member_edit'),
    path('<str:member_number>/delete/', views.member_delete, name='member_delete'),
    
    #AJAX
    path('ajax/search/', views.member_search_ajax, name='member_search_ajax'),

    # Excel operations
    path('excel/template/', views.download_template, name='download_template'),
    path('excel/import/', views.download_template, name='import_page'),

]
