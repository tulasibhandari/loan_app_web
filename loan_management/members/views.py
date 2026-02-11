from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from utils.excel_handler import ExcelHandler
import os
from django.conf import settings
from django.db.models import Q
from .models import Member
from .forms import MemberForm

@login_required
def member_search_ajax(request):
    """AJAX endpoint for member search autocomplete"""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results':[]})
    
    members = Member.objects.filter(
        Q(member_number__icontains=query) |
        Q(member_name__icontains=query)
    )[:10]

    results = [{
        'id': m.member_number,
        'text':f"{m.member_number} - {m.member_name}"
    } for m in members]

    return JsonResponse({'results': results})

@login_required
def member_list(request):
    """ List all Members"""
    members = Member.objects.all()
    return render(request, 'members/member_list.html', {'members':members})

@login_required
def member_create(request):
    """Create new member"""
    if request.method =='POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member created successfully')
            return redirect('members:member_list')
    else:
        form = MemberForm()
    
    return render(request, 'members/member_form.html', {'form': form, 'action':'Create'})

@login_required
def member_detail(request, member_number):
    """View member details"""
    member = get_object_or_404(Member, member_number=member_number)
    return render(request, 'members/member_details.html', {'member':member})


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
