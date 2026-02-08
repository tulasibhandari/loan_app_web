from django import forms
from django.forms import inlineformset_factory
from .models import ProjectDetail
from members.models import Member

class ProjectDetailForm(forms.ModelForm):
    """ Form for single project detail"""
    
    class Meta:
        model = ProjectDetail
        exclude = ['member']
        widgets = {
            'project_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project Name'
            }),
            'self_investment': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Self Investment',
                'type': 'number',
                'step': '0.01'
            }),
            'requested_loan_amount': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Requested Loan Amount',
                'type': 'number',
                'step': '0.01'
            }),
            'total_cost': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Total Cost',
                'type': 'number',
                'step': '0.01',
                'readonly': 'readonly'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Remarks',
                'rows': 3
            })
        }
        labels = {
            'project_name': 'Project Name',
            'self_investment': 'Self Investment',
            'requested_loan_amount': 'Requested Loan',
            'total_cost': 'Total Cost',
            'remarks': 'remarks'
        }
    def clean(self):
        cleaned_data = super().clean()
        self_investment = cleaned_data.get('self_investment', '0')
        requested_loan = cleaned_data.get('requested_loan_amount', '0')

        try:
            # Convert to float for calculation
            self_inv = float(self_investment) if self_investment else 0
            req_loan = float(requested_loan) if requested_loan else 0
            total = self_inv + req_loan
            cleaned_data['total_cost'] = str(total)
        except (ValueError, TypeError):
            pass

        return cleaned_data

# Create formset for multiple projects
ProjectDetailFormSet = inlineformset_factory(
    Member,
    ProjectDetail,
    form = ProjectDetailForm,
    extra=1, # Number of empty forms to display
    can_delete=True, # Allow deletion
    min_num=0, # Minimum number of forms
    validate_min=False,
    max_num=10 # Maxmimum number of projects
)  