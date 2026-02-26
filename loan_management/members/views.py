from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .utils.excel_handler import ExcelHandler
import os
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models import Q
from .models import Member
from .forms import MemberForm


# updated code
@login_required
def member_list(request):
    """List all members with statistics"""
    # Get all members
    members = Member.objects.all().order_by('-date')

    # Calculate statistics
    total_members = members.count()

    # Members added this month
    today = datetime.now()
    first_day_of_month = today.replace(day=1)
    new_this_month = members.filter(date__gte=first_day_of_month).count()

    # Active loans count (if loan model is available)
    try:
        from loans.models import LoanInfo
        active_loans = LoanInfo.objects.filter(
            status__in=['pending', 'approved', 'disbursed']
        ).count()
    except:
        active_loans = 0
    
    context = {
        'members': members,
        'total_members': total_members,
        'new_this_month': new_this_month,
        'active_loans': active_loans,
    }

    return render(request, 'members/member_list.html', context)


@login_required
def member_search_ajax(request):
    """AJAX endpoint for member search autocomplete"""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results':[]})
    
    members = Member.objects.filter(
        Q(member_number__icontains=query) |
        Q(member_name__icontains=query) |
        Q(phone__icontains=query) |
        Q(email__icontains=query)
    )[:10]

    results = [{
        'id': m.member_number,
        'text':f"{m.member_number} - {m.member_name}",
        'phone': m.phone or '',
        'email': m.email or '',
    } for m in members]

    return JsonResponse({'results': results})


@login_required
def member_create(request):
    """Create new member"""
    if request.method =='POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save()
            messages.success(
                request, 
                f'Member {member.member_number} added successfully'
            )
            return redirect('members:member_list')
    else:
        form = MemberForm()
    
    context = {
        'form': form,
        'action': 'Create',
        'title': 'Add New Member'
    }
    
    return render(request, 'members/member_form.html', context)


@login_required
def member_detail(request, member_number):
    """View member details"""
    member = get_object_or_404(Member, member_number=member_number)
    
    # Get related data
    try:
        from loans.models import LoanInfo
        loans = LoanInfo.objects.filter(member=member)
    except:
        loans = []

    try:
        from projects.models import ProjectDetail
        projects = ProjectDetail.objects.filter(member=member)
    except:
        projects = []

    context = {
        'member': member,
        'loans': loans,
        'projects': projects,
    }

    return render(request, 'members/member_details.html', context)

@login_required
def member_edit(request, member_number):
    """Edit existing member"""
    member = get_object_or_404(Member, member_number=member_number)

    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'Member {member.member_number} updated!'
            )
            return redirect('members:member_detail', member_number=member_number)
    else:
        form = MemberForm(instance=member)
    
    context = {
        'form': form,
        'member': member,
        'action': 'Edit',
        'title': 'Edit Member',
    }

    return render(request, 'members/member_form.html', context)

@login_required
def member_delete(request, member_number):
    """ Delete member with confirmation"""
    member = get_object_or_404(Member, member_number=member_number)
    
    if request.method == 'POST':
        member_name = member.member_name
        member.delete()
        messages.success(
            request,
            f"Member {member_name} deleted."
        )
        return redirect('members:member_list')
    
    context = {
        'member': member
    }

    return render(request, 'members/member_confirm_delete.html', context)



@login_required
def download_template(request):
    """Download Excel template for member import"""
    try:
        wb = ExcelHandler.generate_template()

        # Create response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=member_import_template.xlsx'

        wb.save(response)
        return response
    
    except Exception as e:
        messages.error(request, f"Failed to generate template: {str(e)}")
        return redirect('members:member_list')
    

@login_required
def import_members(request):
    """Import members from Excel file"""
    if request.method == 'POST':
        if 'excel_file' not in request.FILES:
            messages.error(request, 'Please select Excel file!')
            return redirect('members:import_page')
        
        excel_file = request.FILES['excel_file']

        # Validate file extension
        if not excel_file.name.endswith('.xlsx'):
            messages.error(request, 'Only .xlsx files allowed!')
            return redirect('members:import_page')
        
        # Save uploaded file temporarily
        file_path = os.path.join(settings.MEDIA_ROOT, 'temp', excel_file.name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb+') as destination:
            for chunk in excel_file.chunks():
                destination.write(chunk)

        # Import data
        success, message, errors, warnings = ExcelHandler.import_from_excel(file_path)

        # Clean up temp files
        try:
            os.remove(file_path)
        except:
            pass

        if success: 
            messages.success(request, message)
            if warnings:
                for warning in warnings:
                    messages.warning(request, warning)
        else:
            messages.error(request, message)
            for error in errors:
                messages.error(request, error)
            if warnings:
                for warning in warnings:
                    messages.warning(request, warning)
        
        return redirect('members:member_list')
    
    return render(request, 'members/import_members.html')
