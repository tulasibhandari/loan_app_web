from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
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
# Create your views here.
