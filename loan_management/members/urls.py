from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('', views.member_list, name='member_list'),
    path('create/', views.member_create, name='member_create'),
    path('<str:member_number>/', views.member_detail, name='member_detail'),
    path('ajax/search/', views.member_search_ajax, name='member_search_ajax'),
]
