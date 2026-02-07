from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from django.conf import settings
from .document_generator import DocumentGenerator
from .context_builder import ReportContextBuilder
from .models import ReportTracking
from loans.models import LoanInfo
from members.models import Member
from datetime import date
import os

@login_required
def report_center(request):
    """Report generation center"""
    # Get approved loans for dropdown
    approved_loans = LoanInfo.objects.filter(
        status='approved'
    ).select_related('member')

    context = {
        'approved_loans': approved_loans,
        'user': request.user
    }
    return render(request, 'reports/report_center.html', context)

@login_required
def generate_report(request):
    """"Genereate selected reports"""
    if request.method != 'POST':
        return redirect('reports:report_center')
    
    member_number = request.POST.get('member_number')
    loan_type = request.POST.get('loan_type')
    report_types = request.POST.getlist('report_types') # Multiple checkboxes

    # Get approval info from session or form
    entered_by = request.user.full_name_nepali or request.user.username
    entered_post = request.user.post or 'Officer'
    approved_by = request.POST.get('approved_by', '')
    approved_post = request.POST.get('approver_post', '')

    if not all([member_number, loan_type, report_types]):
        messages.error(request, 'Please fill all required fields')
        return redirect('reports:report_center')
    
    try:
        member = get_object_or_404(Member, member_number=member_number)

        # Build context
        context = ReportContextBuilder.build_loan_application_context(member_number, entered_by,         
                                                                      entered_post, approved_by, 
                                                                      approved_post)
        today_str = date.today().strftime('%Y%m%d')
        generated_files = []

        # Template mapping
        template_map = {
            'loan_application': 'loan_application.docx',
            'tamasuk': 'tamasuk.docx',
            'loan_approval': 'loan_approval.docx',
            'debit_authority': 'debit_authority.docx',
            'manjurinama': 'manjurinama.docx',
            'guarantor': 'guarantor.docx',
        }

        # Generate each selected report
        for report_type in report_types:
            if report_type in template_map:
                template_name = template_map[report_type]
                output_filename = f"{report_type}_{member_number}_{today_str}.docx"

                generator = DocumentGenerator(template_name)
                output_path = generator.generate(context, output_filename)

                # Save to tracking
                ReportTracking.objects.create(
                    member = member,
                    report_type = report_type,
                    file_path = output_path,
                    generated_by = request.user,
                    generated_date = date.today() 
                )
                generated_files.append({
                    'type': report_type,
                    'path': output_path,
                    'filename': output_filename
                })
        
        messages.success(
            request,
            f"Successfully generated {len(generated_files)} report(s)"
        )

        # Store generated files in session for download
        request.session['generated_files'] = [
            {'type': f['type'], 'filename': f['filename']}
            for f in generated_files
        ]

        return redirect('reports: report_success')
    
    except Exception as e:
        messages.error(request, f"Failed to generate reports: {str(e)}")
        return redirect('reports:report_center')

@login_required
def report_success(request):
    """Show success page with download links"""
    generated_files = request.session.get('generated_files', [])
    return render(request, 'reports/report_success.html', {
        'files': generated_files
    })

@login_required
def download_report(request, filename):
    """Download generated report"""
    file_path = os.path.join(
        settings.MEDIA_ROOT, 'generated_reports' , filename
    )

    if not os.path.exits(file_path):
        raise Http404("File not found")
    
    return FileResponse(
        open(file_path, 'rb'),
        as_attachment=True,
        filename=filename
    )

@login_required
def report_history(request):
    """View report generating history"""
    reports = ReportTracking.objects.select_related(
        'member', 'generated_by'
    ).order_by('-generated_date')

    # Filter by member if provided
    member_number = request.GET.get('member_number')
    if member_number:
        reports = reports.filter(member__member_number=member_number)
    
    return render(request, 'reports/report_history.html',{
        'reports':reports
    })
    
