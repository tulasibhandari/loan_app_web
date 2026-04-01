from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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

    # Status filter
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('q', '')

    loans_qs = LoanInfo.objects.select_related('member').order_by('-id')

    if status_filter:
        loans_qs = loans_qs.filter(status=status_filter)

    if search_query:
        loans_qs = loans_qs.filte(
            member__member_name__icontains=search_query
        ) | loans_qs.filter(
            member__member_number__icontains=search_query
        )

    # Pagination - 10 per page
    paginator = Paginator(loans_qs, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Recent Loans
    # recent_loans = LoanInfo.objects.select_related('member').order_by('-created_at')[:10]

    context = {
        'total_members': total_members,
        'total_loans': total_loans,
        'pending_loans': pending_loans,
        'approved_loans': approved_loans,
        'page_obj': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    return render(request, 'dashboard/home.html', context)

