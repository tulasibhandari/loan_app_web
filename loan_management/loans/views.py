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
    loans = LoanInfo.objects.select_related('member').all().order_by('-created_at')

    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        loans = loans.filter(status=status)
    
    # Filter by member if provided
    member_number = request.GET.get('member')
    if member_number:
        loans = loans.filter(member__number_number=member_number)
    
    context = {
        'loans': loans,
        'status_filter': status,
    }
    return render(request, 'loans/loan_list.html', context)

@login_required
def loan_detail(request, loan_id):
    """View loan detail"""
    loan = get_object_or_404(LoanInfo, id=loan_id)

    # Get related data
    try:
        approval = ApprovalInfo.objects.filter(member=loan.member).first()
    except:
        approval = None
    
    context = {
        'loan': loan,
        'member': loan.member,
        'approval': approval,
    }

    return render(request, 'loans/loan_detail.html', context)

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


@login_required
def loan_schemes_list(request):
    """List all loan schemes"""
    schemes = LoanScheme.objects.all().order_by('loan_type')

    context = {
        'schemes': schemes
    }

    return render(request, 'loans/loan_schemes.html', context)

@login_required
def scheme_create(request):
    """Create new loan scheme"""
    if request.method == 'POST':
        loan_type = request.POST.get('loan_type')
        interest_rate = request.POST.get('interest_rate')

        # Validation
        if not loan_type or not interest_rate:
            messages.error(request, '❌ कृपया सबै फिल्ड भर्नुहोस् (Please fill all fields)')
            return redirect('loans:schemes_list')

        try:
            # Check if already exists
            if LoanScheme.objects.filter(loan_type=loan_type).exists():
                messages.error(request, f'Loan scheme "{loan_type}" already exists.')
            else:
                LoanScheme.objects.create(
                    loan_type=loan_type,
                    interest_rate=float(interest_rate)
                )
                messages.success(request, f'Loan scheme "{loan_type}" created successfully.')
        except Exception as e:
            messages.error(request, f"Error Occured: {str(e)}")
    
    return redirect('loans:schemes_list')

@login_required
def scheme_edit(request, scheme_id):
    """Edit loan scheme"""
    scheme = get_object_or_404(LoanScheme, id=scheme_id)

    if request.method == 'POST':
        loan_type = request.POST.get('loan_type')
        interest_rate = request.POST.get('interest_rate')

        try:
            # Check if loan_type changed and already exists
            if loan_type != scheme.loan_type:
                if LoanScheme.objects.filter(loan_type=loan_type).exists():
                    messages.error(request, f'Loan type "{loan_type}" already exists.')
                    return redirect('loans:schemes_list')
                
                scheme.loan_type = loan_type
                scheme.interest_rate = float(interest_rate)
                scheme.save()

                messages.success(request, 'Loan scheme updated successfully.')
        except Exception as e:
            messages.error(request, f'Error occured: {str(e)}')

    return redirect('loans:schemes_list')

@login_required
def scheme_delete(request, scheme_id):
    """Delete loan scheme"""
    scheme = get_object_or_404(LoanScheme, id=scheme_id)

    if request.method == 'POST':
        loan_type = scheme.loan_type
        scheme.delete()
        messages.success(request, f"Loan scheme '{loan_type}' deleted successfully.")

    return redirect('loans:schemes_list')

