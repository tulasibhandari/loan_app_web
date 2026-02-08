from django.urls import path
from . import views

app_name = 'collateral'

urlpatterns = [
    path('<str:member_number>/basic/', views.basic_form, name='basic_form'),
    # Need to add others collateral forms as needed
]
