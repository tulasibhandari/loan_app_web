from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.user_list, name='user_list'),
    path('users/register/', views.register_user, name='register'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
]