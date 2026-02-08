from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import ProjectDetail
from .forms import ProjectDetailForm, ProjectDetailFormSet
from members.models import Member
from loans.models import LoanInfo

@login_required
def project_form(request, member_number):
    """ Add / Edit project details for a member"""
    member = get_object_or_404(Member, member_number=member_number)

    # Get existing projects for this member
    existing_projects = ProjectDetail.objects.filter(member=member)

    if request.method == 'POST':
        formset = ProjectDetailFormSet(request.POST, queryset=existing_projects)
        if formset.is_valid():
            projects = formset.save(commit=False)
            for project in projects:
                project.member = member
                project.save()
            
            # Delete projects marked for deletion
            for project in formset.deleted_objects:
                project.delete()
            
            messages.success(request, 'Project details saved successfully')

            # Redirect to approval or next step
            return redirect('loans:loan_approval', member_number=member_number)
    else:
        formset = ProjectDetailFormSet(queryset=existing_projects)   
    
    context = {
        'member': member,
        'formset': formset,
    }

    return render(request, 'projects/project_form.html', context)

@login_required
def project_create(request, member_number):
    """Create a single project for member"""
    member = get_object_or_404(Member, member_number=member_number)

    if request.method == 'POST':
        form = ProjectDetailForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.member = member
            project.save()
            messages.success(request, "Project added successfully")
            return redirect('project:project_form', member_number=member_number)
    else:
        form = ProjectDetailForm()

    context = {
        'form': form,
        'member': member,
        'action': 'Create'
    }

    return render(request, 'projects/project_single_form.html', context)

@login_required
def project_edit(request, project_id):
    """Edit a specific project"""
    project = get_object_or_404(ProjectDetail, id=project_id)
    
    if request.method == 'POST':
        form = ProjectDetailForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('projects:project_form', member_number = project.member.member_number)        
    else:
        form = ProjectDetailForm(instance=project)
    
    context = {
        'form': form, 
        'member': project.member,
        'action' : 'Edit',
        'project' : project
    }
    return render(request, 'projects/project_single_form.html', context)

@login_required
def project_delete(request, project_id):
    """ Delete a project"""
    project = get_object_or_404(ProjectDetail, id=project_id)
    member_number = project.member.member_number

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully')
        return redirect('projects:project_form', member_number=member_number)
    
    context = {
        'project': project,
        'member': project.member
    }
    return render(request, 'projects/project_confirm_delete.html', context)

@login_required
def project_list(request, member_number):
    """List all projects for a member"""
    member = get_object_or_404(Member, member_number=member_number)
    projects = ProjectDetail.objects.filter(member=member)

    context = {
        'member': member,
        'projects': projects
    }
    return render(request, 'projects/project_list.html', context)

@login_required
def project_detail(request, project_id):
    """View project details"""
    project = get_object_or_404(ProjectDetail, id=project_id)

    context = {
        'project': project,
        'member': project.member
    }
    return render(request, 'projects/project_detail.html', context)
