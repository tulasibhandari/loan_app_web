from django import forms
from .models import (
    CollateralBasic, CollateralProperty,
    CollateralFamilyDetail, CollateralIncomeExpense
)

class CollateralBasicForm(forms.ModelForm):
    class Meta:
        model = CollateralBasic
        exclude = ['member']
        widgets ={
            'monthly_saving': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'child_saving': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'total_saving': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'share_amount': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }
