from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import (LoanInfo, LoanScheme, ApprovalInfo,
                     WitnessInfo, GuarantorDetails, ManjurinamaDetails)
from .forms import LoanInfoForm, ApprovalForm, WitnessInfoForm, GuarantorForm, ManjurinamaForm
from members.models import Member
from collateral.models import (CollateralBasic, CollateralProperty,
                               CollateralFamilyDetail, CollateralIncomeExpense,
                               CollateralAffiliation)

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

            return redirect('loans:witness_form', member_number=member_number)
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
        
    # Collateral data
    collateral_basic = CollateralBasic.objects.filter(member=loan.member).first()
    collateral_properties = CollateralProperty.objects.filter(member=loan.member)
    collateral_family = CollateralFamilyDetail.objects.filter(member=loan.member)
    collateral_income = CollateralIncomeExpense.objects.filter(member=loan.member, type="income")
    collateral_expense = CollateralIncomeExpense.objects.filter(member=loan.member, type="expense")
    collateral_affiliations = CollateralAffiliation.objects.filter(member=loan.member)

    total_income = sum(float(i.amount or 0) for i in collateral_income)
    total_expense = sum(float(e.amount or 0) for e in collateral_expense)

    context = {
        'loan': loan,
        'member': loan.member,
        'approval': approval,
        # Collateral
        'collateral_basic':collateral_basic,
        'collateral_properties': collateral_properties,
        'collateral_family': collateral_family,
        'collateral_affiliations': collateral_affiliations,
        'collateral_income': collateral_income,
        'collateral_expense': collateral_expense,
        'total_income': total_income,
        'total_expense': total_expense,
        'net_income': total_income - total_expense,        
    }

    return render(request, 'loans/loan_detail.html', context)

@login_required
def loan_approval(request, loan_id):
    """Approve a loan"""
    loan = get_object_or_404(LoanInfo, id=loan_id)
    
    # ✨ NEW: Check if already approved
    if loan.status == 'approved':
        messages.warning(request, '⚠️ This loan is already approved')
        return redirect('loans:loan_detail', loan_id=loan_id)
    
    if request.method == 'POST':
        # ✨ NEW: Direct form data extraction (no Django form)
        approval_data = {
            'approval_date': request.POST.get('approval_date'),
            'entered_by': request.user.full_name_nepali or request.user.username,
            'entered_post': request.user.post or 'Officer',
            'approved_by': request.POST.get('approved_by'),
            'approved_post': request.POST.get('approved_post'),
            'approved_loan_amount': request.POST.get('approved_loan_amount'),
            'approved_loan_amount_words': request.POST.get('approved_loan_amount_words'),
            'remarks': request.POST.get('remarks', ''),
        }
        
        # ✨ NEW: Manual validation
        if not all([approval_data['approval_date'], approval_data['approved_by'], 
                   approval_data['approved_post'], approval_data['approved_loan_amount']]):
            messages.error(request, '❌ कृपया सबै आवश्यक फिल्डहरू भर्नुहोस् (Please fill all required fields)')
            return redirect('loans:loan_approval', loan_id=loan_id)
        
        try:
            # ✨ NEW: Create approval with unpacked data
            ApprovalInfo.objects.create(
                member=loan.member,
                **approval_data
            )
            
            # Update loan status
            loan.status = 'approved'
            loan.save()
            
            # ✨ NEW: Better success message with amount
            messages.success(
                request, 
                f'✅ ऋण सफलतापूर्वक स्वीकृत भयो (Loan approved successfully) - रु. {approval_data["approved_loan_amount"]}'
            )
            # ✨ NEW: Redirect to loan detail instead of list
            return redirect('loans:loan_detail', loan_id=loan_id)
            
        except Exception as e:
            messages.error(request, f'❌ Error approving loan: {str(e)}')
            return redirect('loans:loan_approval', loan_id=loan_id)
    
    # ✨ NEW: Simpler context (no form object)
    context = {
        'loan': loan,
        'member': loan.member,
        'user': request.user
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

@login_required
def witness_form(request, member_number):
    """ Witness information form"""
    member = get_object_or_404(Member, member_number=member_number)

    # Get current loan from session
    loan_id = request.session.get('current_loan_id')
    loan = LoanInfo.objects.filter(id=loan_id, member=member).first() if loan_id else None

    if request.method == 'POST':
        form = WitnessInfoForm(request.POST)
        if form.is_valid():
            witness = form.save(commit=False)
            witness.member = member
            witness.save()
            messages.success(request, 'साक्षी जानकारी सफलतापूर्वक रेकर्ड भयो।')
            return redirect('loans:guarantor_form', member_number=member_number)
    else:
        form = WitnessInfoForm()

    context = {
        'form': form,
        'member': member,
        'loan': loan,
        'step': 'witness',
        'next_step': 'guarantor'
    }

    return render(request, 'loans/supporting_docs.html', context)

@login_required
def guarantor_form(request, member_number):
    """Guarantor information form"""
    member = get_object_or_404(Member, member_number=member_number)
    loan_id = request.session.get('current_loan_id')
    loan = LoanInfo.objects.filter(id=loan_id, member=member).first() if loan_id else None

    if request.method == 'POST':
        form = GuarantorForm(request.POST)
        if form.is_valid():
            guarantor = form.save(commit=False)
            guarantor.member = member
            guarantor.save()
            messages.success(request, 'जमानी विवरण सफलतापूर्वक रेकर्ड भयो।')
            return redirect('loans:manjurinama_form', member_number=member_number)
    else:
        form = GuarantorForm()

    context = {
        'form': form,
        'member': member,
        'loan': loan,
        'step': 'guarantor',
        'prev_step': 'witness',
        'next_step': 'manjurinama',
        'member_number': member_number
    }

    return render(request, 'loans/supporting_docs.html', context)

@login_required
def manjurinama_form(request, member_number):
    """Manjurinama details form"""
    member = get_object_or_404(Member, member_number=member_number)
    loan_id = request.session.get('current_loan_id')
    loan = LoanInfo.objects.filter(member=member, status__in=['pending', 'draft']).last() 

    if request.method == 'POST':
        form = ManjurinamaForm(request.POST)
        if form.is_valid():
            manjuri = form.save(commit=False)
            manjuri.member = member
            manjuri.save()
            messages.success(request, 'मञ्जुरीनामा दिनेको विवरण सफलतापूर्वक रेकर्ड भयो।')

            if loan:
            # Clear session
                if 'current_loan_id' in request.session:
                    del request.session['current_loan_id']
                return redirect('loans:loan_detail', loan_id=loan.id)
            else:
                messages.warning(request, '⚠️ Loan not found. Please create loan first.')
                return redirect('loans:loan_list')
    else:
        form = ManjurinamaForm()

    context = {
        'form': form,
        'member': member,
        'loan': loan,
        'step': 'manjurinama',
        'prev_step': 'guarantor',
        'member_number': member_number
    }

    return render(request, 'loans/supporting_docs.html', context)
