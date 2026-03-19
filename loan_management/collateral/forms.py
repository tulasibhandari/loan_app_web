from django import forms
from .models import (
    CollateralBasic, CollateralProperty,
    CollateralFamilyDetail, CollateralIncomeExpense,
    CollateralAffiliation
)

INPUT_CLASS = 'form-control'
SELECT_CLASS = 'form-select'

def text_input(placeholder=''):
    return forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': placeholder})

def number_input(placeholder=''):
    return forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': placeholder})

class CollateralBasicForm(forms.ModelForm):
    class Meta:
        model = CollateralBasic
        exclude = ['member']
        widgets ={
            'monthly_saving': text_input('मासिक बचत रकम'),
            'child_saving': text_input('बाल बचत रकम'),
            'total_saving': text_input('जम्मा बचत रकम'),
            'share_amount': text_input('शेयर रकम'),
        }

        labels = {
            'monthly_saving': 'मासिक बचत रकम',
            'child_saving': 'बाल बचत रकम',
            'total_saving': 'जम्मा बचत रकम',
            'share_amount': 'शेयर रकम',
        }


class CollateralPropertyForm(forms.ModelForm):
    class Meta:
        model = CollateralProperty
        exclude = ['member']
        widget = {
            'owner_name': text_input('जग्गाधनीको नाम'),
            'father_or_spouse_name': text_input('बाबु / पतिको नाम'),
            'grandfather_or_father_in_law_name': text_input('हजुरवुवा/ससु्राको नाम'),
            'district': text_input('जिल्ला'),
            'municipality_vdc': text_input('नगरपालिका/गाउँपालिका'),
            'sheet_no': text_input('सिट नं.'),
            'ward_no': text_input('वडा नं.'),
            'plot_no': text_input('कित्ता नं.'),
            'area': text_input('क्षेत्रफल'),
            'land_type': text_input('जग्गाको किसिम'),
        }

        labels = {
            'owner_name': 'जग्गाधनीको नाम',
            'father_or_spouse_name': 'बाबु / पतिको नाम',
            'grandfather_or_father_in_law_name': 'हजुरवुवा/ससु्राको नाम',
            'district': 'जिल्ला',
            'municipality_vdc': 'नगरपालिका/गाउँपालिका',
            'sheet_no': 'सिट नं.',
            'ward_no': 'वडा नं.',
            'plot_no': 'कित्ता नं.',
            'area': 'क्षेत्रफल',
            'land_type': 'जग्गाको किसिम',

        }

class CollateralFamilyDetailForm(forms.ModelForm):
    class Meta:
        model = CollateralFamilyDetail
        exclude = ['member']
        widgets = {
            'name': text_input('नाम'),
            'age': text_input('उमेर'),
            'relation': text_input('नाता'),
            'member_of_other_coop': text_input('अन्य संस्थाको सदस्य'),
            'occupation': text_input('पेशा'),
            'monthly_income': text_input('मासिक आम्दानी'),
        }
        
        labels = {
            'name': 'नाम',
            'age': 'उमेर',
            'relation': 'नाता',
            'member_of_other_coop': 'अन्य संस्थाको सदस्य',
            'occupation': 'पेशा',
            'monthly_income': 'मासिक आम्दानी',
        }

class CollateralIncomeExpenseForm(forms.ModelForm):
    class Meta:
        model = CollateralIncomeExpense
        exclude = ['member', 'type'] # type is set in view
        widgets = {
            'field': text_input('शीर्षक'),
            'amount': text_input('रकम (रु.)'),
        }

        labels = {
            'field': 'शीर्षक',
            'amount': 'रकम (रु.)',
        }

class CollateralAffiliationForm(forms.ModelForm):
    class Meta:
        model = CollateralAffiliation
        exclude = ['member']
        widgets = {
            'institution': text_input('संस्थाको नाम'),
            'address_of_institution': text_input('संस्थाको ठेगाना'),
            'position': text_input('पद'),
            'estimated_income': text_input('अनुमानित आय'),
            'remarks': forms.Textarea(attrs={
                'class': INPUT_CLASS,
                'rows': 2,
                'placeholder': 'कैफियत',
            }),
        }
        labels = {
            'institution': 'संस्थाको नाम',
            'address_of_institution': 'संस्थाको ठेगाना',
            'position': 'पद',
            'estimated_income': 'अनुमानित आय',
            'remarks': 'कैफियत',
        }