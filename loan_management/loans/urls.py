from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    # Loan CRUD
    path('', views.loan_list, name='loan_list'),
    path('create/<str:member_number>/', views.loan_create, name='loan_create'),
    path('<int:loan_id>/', views.loan_detail, name='loan_detail'),
    path('<int:loan_id>/approve/', views.loan_approval, name='loan_approval'),

    # Loan Schemes
    path('schemes/', views.loan_schemes_list, name='schemes_list'),
    path('schemes/create/', views.scheme_create, name='scheme_create'),
    path('schemes/<int:scheme_id>/edit/', views.scheme_edit, name='scheme_edit'),
    path('schemes/<int:scheme_id>/delete/', views.scheme_delete, name='scheme_delete'),

    # Witness, Guarantor, Manjurinama (to be created)
    # path('witness/<str:member_number>/', views.witness_form, name='witness_form'),
    # path('guarantor/<str:member_number>/', views.guarantor_form, name='guarantor_form'),
    # path('manjurinama/<str:member_number>/', views.manjurinama_form, name='manjurinama_form'),
]
