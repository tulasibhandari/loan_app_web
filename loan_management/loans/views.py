from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LoanInfo, LoanScheme, ApprovalInfo
from .forms import LoanInfoForm, ApprovalForm
from members.models import Member

@login_required
def loan_create(request, member_number):
    """Create loan application for a member """
    member = get_object_or_404(Member, member_number=member_number)
    loan_schemes = LoanScheme.objects.all()

    if request.method == 'POST':
        form = LoanInfoForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.member = member
            loan.save()
            messages.success(request, 'Loan application saved successfully!')

            # Store in session for multi-step process
            request.session['current_loan_id'] = loan.id
            request.session['member_number'] = member_number

            return redirect('collateral:basic_form', member_number=member_number)
    else:
        form = LoanInfoForm()

    context = {
        'form': form,
        'member': member,
        'loan_schemes': loan_schemes
    }
    return render(request, 'loans/loan_form.html', context)

@login_required
def loan_list(request):
    """List all loans"""
    loans = LoanInfo.objects.select_related('member').all()
    return render(request, 'loans/loan_list.html', {'loans': loans})

@login_required
def loan_approval(request, loan_id):
    """ Approve a loan"""
    loan = get_object_or_404(LoanInfo, id=loan_id)

    if request.method == 'POST':
        form = ApprovalForm(request.POST)
        if form.is_valid():
            approval = form.save(commit=False)
            approval.member = loan.member
            approval.entered_by = request.user.full_name_nepali or request.user.username
            approval.entered_post = request.user.post or 'Officer'
            approval.save()

            # Update loan status
            loan.status = 'approved'
            loan.save()

            messages.success(request, 'Loan approved successfully')
            return redirect('loans:loan_list')
    else:
        form = ApprovalForm()

    context = {
        'form': form, 
        'loan': loan,
        'member': loan.member
    }
    return render(request, 'loans/loan_approval.html', context)
# Create your views here.
