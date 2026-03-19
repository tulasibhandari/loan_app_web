from django.urls import path
from . import views

app_name = 'collateral'

urlpatterns = [
    path('<str:member_number>/basic/', views.basic_form, name='basic_form'),
    path('<str:member_number>/property/', views.property_form, name='property_form'),
    path('<str:member_number>/family/', views.family_form, name='family_form'),
    path('<str:member_number>/income-expense/', views.income_expense_form, name='income_expense_form'),
    path('<str:member_number>/affiliation/', views.affiliation_form, name='affiliation_form'),
    path('<str:member_number>/overview/', views.collateral_overview, name='overview'),
]