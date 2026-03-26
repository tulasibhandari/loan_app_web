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
    approved_loans = LoanInfo.objects.filter(
        status='approved'
    ).select_related('member')

    return render(request, 'reports/report_center.html', {
        'approved_loans': approved_loans,
    })


@login_required
def generate_report(request):
    """Generate selected reports"""
    if request.method != 'POST':
        return redirect('reports:report_center')

    member_number = request.POST.get('member_number')
    loan_type     = request.POST.get('loan_type')
    report_types  = request.POST.getlist('report_types')

    entered_by   = request.user.full_name_nepali or request.user.username
    entered_post = request.user.post or 'Officer'
    approved_by  = request.POST.get('approved_by', '')
    approver_post = request.POST.get('approver_post', '')

    if not all([member_number, report_types]):
        messages.error(request, 'कृपया सदस्य र कम्तिमा एक रिपोर्ट छान्नुहोस्।')
        return redirect('reports:report_center')

    try:
        member = get_object_or_404(Member, member_number=member_number)

        context = ReportContextBuilder.build_loan_application_context(
            member_number, entered_by, entered_post, approved_by, approver_post
        )

        today_str = date.today().strftime('%Y%m%d')
        generated_files = []

        template_map = {
            'loan_application': 'loan_application.docx',
            'tamasuk':          'tamasuk.docx',
            'loan_approval':    'loan_approval.docx',
            'debit_authority':  'debit_authority.docx',
            'manjurinama':      'manjurinama.docx',
            'guarantor':        'guarantor.docx',
        }

        for report_type in report_types:
            if report_type not in template_map:
                continue

            template_name   = template_map[report_type]
            output_filename = f"{report_type}_{member_number}_{today_str}.docx"

            generator   = DocumentGenerator(template_name)
            output_path = generator.generate(context, output_filename)

            ReportTracking.objects.create(
                member         = member,
                report_type    = report_type,
                file_path      = output_filename,
                generated_by   = request.user,
                generated_date = date.today(),
            )

            generated_files.append({
                'type':     report_type,
                'path':     output_path,
                'filename': output_filename,
            })

        messages.success(request, f"{len(generated_files)} वटा रिपोर्ट सफलतापूर्वक बनाइयो!")

        request.session['generated_files'] = [
            {'type': f['type'], 'filename': f['filename']}
            for f in generated_files
        ]

        return redirect('reports:report_success')   # Fix: space thiyo

    except Exception as e:
        messages.error(request, f"रिपोर्ट बनाउन असफल: {str(e)}")
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
    # Security: prevent path traversal
    filename = os.path.basename(filename)
    file_path = os.path.join(settings.MEDIA_ROOT, 'generated_reports', filename)

    if not os.path.exists(file_path):   # Fix: exits -> exists
        raise Http404("File not found")

    return FileResponse(
        open(file_path, 'rb'),
        as_attachment=True,
        filename=filename
    )


@login_required
def report_history(request):
    """View report generation history"""
    reports = ReportTracking.objects.select_related('member').order_by('-generated_date')

    member_number = request.GET.get('member_number')
    if member_number:
        reports = reports.filter(member__member_number=member_number)

    return render(request, 'reports/report_history.html', {
        'reports': reports
    })