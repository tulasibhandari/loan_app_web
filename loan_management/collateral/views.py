from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    CollateralBasicForm,  # CollateralPropertyForm,
    # CollateralFamilyDetailForm, CollateralIncomeExpenseForm
)
from members.models import Member

@login_required
def basic_form(request, member_number):
    """ Collateral Basic information form for kharkhacho loan type"""
    member = get_object_or_404(Member, member_number=member_number)

    if request.method == 'POST':
        form = CollateralBasicForm(request.POST)
        collateral = form.save(commit=False)
        collateral.member = member
        collateral.save()
        messages.success(request, 'Basic collateral info saved')
        return redirect('collateral:property_form', member_number=member_number)
    else:
        form = CollateralBasicForm()

    return render(request, 'collateral/basic_form.html', {
        'form': form,
        'member': member
    })

# Create your views here.
