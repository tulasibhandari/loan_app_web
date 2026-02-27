from django import forms
from .models import LoanInfo, ApprovalInfo

class LoanInfoForm(forms.ModelForm):
    class Meta:
        model = LoanInfo
        exclude = ['member', 'status', 'created_at']
        widgets = {
            'loan_type': forms.Select(attrs={'class': 'form-control', 'id':'id_loan_type'}),
            'interest_type': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'loan_duration': forms.Select(attrs={'class': 'form-control'}),
            'repayment_duration': forms.Select(attrs={'class': 'form-control'}),
            'loan_amount': forms.TextInput(attrs={'class': 'form-control', 'id':'id_loan_amount'}),
            'loan_amount_in_words': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
        }

class ApprovalForm(forms.ModelForm):
    class Meta:
        model = ApprovalInfo
        exclude = ['member', 'entered_by', 'entered_post']
        widgets = {
            'approval_date': forms.TextInput(attrs={'class': 'form-control'}),
            'approved_by': forms.Textarea(attrs={'class': 'form-control'}),
            'approver_post': forms.TextInput(attrs={'class': 'form-control'}),
            'approved_loan_amount': forms.TextInput(attrs={'class': 'form-control'}),
            'approved_loan_amount_words': forms.Textarea(attrs={'class': 'form-control', 'rows':2}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows':3})
        }

