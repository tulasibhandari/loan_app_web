from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Username'        
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label = "Password",
        widget = forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Password'
        }),
    )
    password2 = forms.CharField(
        label = 'Retype Password',
        widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        }),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name_nepali', 'role', 'post']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }),
            'full_name_nepali': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'पूरा नाम (नेपालीमा)',
            }),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'post': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'पद'
            }),
        }

        labels = {
            'username': 'Username',
            'email': 'Email',
            'full_name_nepali': 'पूरा नाम (नेपालीमा)',
            'role': 'Role',
            'post': 'पद',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f"{self.username} is already taken.")
        return username
    
    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Password doesnot match')
        validate_password(p2)
        return p2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
