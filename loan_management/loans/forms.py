from django import forms
from .models import LoanInfo, ApprovalInfo, WitnessInfo, GuarantorDetails, ManjurinamaDetails

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


def _text(placeholder=''):
    return forms.TextInput(attrs={'class': 'form-control', 'placeholder': placeholder})


class WitnessInfoForm(forms.ModelForm):
    class Meta:
        model = WitnessInfo
        exclude = ['member']
        widgets = {
            'name': _text('साक्षीको नाम'),
            'relation': _text('ऋणीसँगको नाता'),
            'address': _text('साक्षीको ठेगाना'),
            'tole': _text('टोल'),
            'ward': _text('वडा नं'),
            'age': _text('साक्षीको उमेर'),
        }

class GuarantorForm(forms.ModelForm):
    class Meta:
        model = GuarantorDetails
        exclude = ['member']
        widgets = {
            'guarantor_member_number':_text('जमानीको स.नं.'),
            'guarantor_name':_text('जमानीको नाम'),
            'guarantor_address':_text('ठेगाना'),
            'guarantor_ward':_text('वडा नं.'),
            'guarantor_phone':_text('सम्पर्क नं'),
            'guarantor_citizenship':_text('नागरिकता नं'),
            'guarantor_grandfather':_text('हजुरबुवाको नाम'),
            'guarantor_father':_text('बाबुको नाम'),
            'guarantor_citizenship_issue_district':_text('ना.प्र.प जारी जिल्ला'),
            'guarantor_age':_text('उमेर'),
        }

class ManjurinamaForm(forms.ModelForm):
    class Meta:
        model = ManjurinamaDetails
        exclude = ['member']
        widgets = {
            'person_name': _text('मञ्जुरीनामा दिनेको नामथर'), 
            'grandfather_name': _text('हजुरबुवाको नाम'), 
            'father_name': _text('बाबुको नाम'), 
            'age': _text('उमेर'), 
            'district': _text('जिल्ला'), 
            'municipality': _text('नगर/गाउँ पालिका'), 
            'wada_no': _text('वडा नं.'), 
            'tole': _text('टोल'), 
        }