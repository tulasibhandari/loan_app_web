from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from loans.models import LoanInfo
from members.models import Member

@login_required
def home(request):
    """Main Dashboard"""

    #Get statistics
    total_members = Member.objects.count()
    total_loans = LoanInfo.objects.count()
    pending_loans = LoanInfo.objects.filter(status='pending').count()
    approved_loans = LoanInfo.objects.filter(status='approved').count()

    # Recent Loans
    recent_loans = LoanInfo.objects.select_related('member').order_by('-created_at')[:10]

    context = {
        'total_members': total_members,
        'total_loans': total_loans,
        'pending_loans': pending_loans,
        'approved_loans': approved_loans,
        'recent_loans': recent_loans,
        'user': request.user
    }
    return render(request, 'dashboard/home.html', context)

# Create your views here.
