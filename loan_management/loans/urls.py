from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('', views.loan_list, name='loan_list'),
    path('create/<str:member_number>/', views.loan_create, name='loan_create'),
    path('approve/<int:loan_id>/', views.loan_approval, name='loan_approval'),
]
