from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import LoginForm, UserRegistrationForm
from .models import User

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('dashboard:home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('accounts:login')

def can_manage_users(user):
    return user.role in ('admin', 'officer')

@login_required
def user_list(request):
    if not can_manage_users(request.user):
        raise PermissionError
    users = User.objects.all().order_by('role', 'username')
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required
def register_user(request):
    if not can_manage_users(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account creted for '{user.username}'")
            return redirect('accounts:user_list')
        else:
            messages.error(request, 'Please fill all required fields')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

@login_required
def user_delete(request, user_id):
    if request.user.role != 'admin':
        raise PermissionDenied
    
    target_user = get_object_or_404(User, id=user_id)

    if target_user == request.user:
        messages.error(request, "User cannot delete own account!")
        return redirect('accounts:user_list')
    
    if request.method == 'POST':
        username = target_user.username
        target_user.delete()
        messages.success(request, f"OOPs! '{username}' is deleted.")
        return redirect('accounts:user_list')

    return render(request, 'accounts/user_confirm_delete.html', {'target_user': target_user})


