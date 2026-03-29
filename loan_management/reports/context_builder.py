from members.models import Member
from loans.models import LoanInfo, ApprovalInfo
from collateral.models import (
    CollateralBasic, CollateralProperty, CollateralFamilyDetail,
    CollateralAffiliation, CollateralIncomeExpense
)
from projects.models import ProjectDetail
from .services.report_context.utils import np


try:
    from loans.models import WitnessInfo, GuarantorDetails
except ImportError:
    WitnessInfo = None
    GuarantorDetails = None

# Organization profile
try:
    from dashboard.models import OrganizationProfile  # Fix: typo thiyo OrganatizationProfile
except ImportError:
    try:
        from dashboard.models import OrganatizationProfile as OrganizationProfile
    except ImportError:
        OrganizationProfile = None

# Nepali datetime — installed chhaina bhane fallback
try:
    from nepali_datetime import date as nepali_date
    HAS_NEPALI_DATETIME = True
except ImportError:
    HAS_NEPALI_DATETIME = False
    from datetime import date


def num_to_nepali_words(num):
    """Convert number to Nepali words"""
    try:
        num = float(num)
    except (TypeError, ValueError):
        return "शून्य"

    if num == 0:
        return "शून्य रुपैयाँ"

    ones = ["", "एक", "दुई", "तीन", "चार", "पाँच", "छ", "सात", "आठ", "नौ",
            "दश", "एघार", "बाह्र", "तेह्र", "चौध", "पन्ध्र", "सोह्र", "सत्र",
            "अठार", "उन्नाइस"]
    tens = ["", "दश", "बीस", "तीस", "चालिस", "पचास", "साठी", "सत्तरी", "असी", "नब्बे"]

    def convert_below_100(n):
        if n < 20:
            return ones[n]
        return tens[n // 10] + (" " + ones[n % 10] if n % 10 else "")

    def convert_below_1000(n):
        if n < 100:
            return convert_below_100(n)
        hundreds = ones[n // 100] + " सय"
        remainder = n % 100
        return hundreds + (" " + convert_below_100(remainder) if remainder else "")

    n = int(num)
    if n < 1000:
        return convert_below_1000(n) + " रुपैयाँ"

    parts = []
    crore = n // 10000000
    n %= 10000000
    lakh = n // 100000
    n %= 100000
    hazar = n // 1000
    n %= 1000

    if crore:
        parts.append(convert_below_1000(crore) + " करोड")
    if lakh:
        parts.append(convert_below_1000(lakh) + " लाख")
    if hazar:
        parts.append(convert_below_1000(hazar) + " हजार")
    if n:
        parts.append(convert_below_1000(n))

    return " ".join(parts) + " रुपैयाँ"


class ReportContextBuilder:
    """Build context dictionary for report templates"""

    @staticmethod
    def build_loan_application_context(member_number, entered_by, entered_post,
                                       approved_by, approver_post):
        """Build complete context for all report types"""
        try:
            member = Member.objects.get(member_number=member_number)
            loan = LoanInfo.objects.filter(member=member).latest('id')

            # Related data
            approval          = ApprovalInfo.objects.filter(member=member).first()
            collateral_basic  = CollateralBasic.objects.filter(member=member).first()
            properties        = CollateralProperty.objects.filter(member=member)
            family_details    = CollateralFamilyDetail.objects.filter(member=member)
            income_expenses   = CollateralIncomeExpense.objects.filter(member=member)
            affiliations      = CollateralAffiliation.objects.filter(member=member)
            projects          = ProjectDetail.objects.filter(member=member)

            witnesses  = WitnessInfo.objects.filter(member=member) if WitnessInfo else []
            guarantors = GuarantorDetails.objects.filter(member=member) if GuarantorDetails else []

            # Organization profile
            org = None
            if OrganizationProfile:
                org = OrganizationProfile.objects.first()

            # BS Date
            if HAS_NEPALI_DATETIME:
                today_bs = nepali_date.today()
                bs_year  = str(today_bs.year)
                bs_month = str(today_bs.month).zfill(2)   
                bs_day   = str(today_bs.day).zfill(2)
                date_nepali = today_bs.strftime('%Y/%m/%d')
            else:
                from datetime import date as dt_date
                today = dt_date.today()
                bs_year = str(today.year)
                bs_month = str(today.month).zfill(2)
                bs_day   = str(today.day).zfill(2)
                date_nepali = today.strftime('%Y/%m/%d')

            context = {
                # Organization
                'company_name':    org.company_name if org else '',
                'company_address': org.address if org else '',

                # Member
                'member_number':    np(member.member_number),
                'member_name':      member.member_name,
                'phone':            np(member.phone or ''),
                'email':            member.email or '',
                'citizenship_no':   np(member.citizenship_no or ''),
                'father_name':      member.father_name or '',
                'grandfather_name': member.grandfather_name or '',
                'spouse_name':      member.spouse_name or '',
                'spouse_phone':     np(member.spouse_phone) or '',
                'address':          member.address or '',       # Fix: add_to_class -> address
                'ward_no':          np(member.ward_no or ''),
                'profession':       member.profession or '',
                'dob_bs':           np(member.dob_bs or ''),
                'business_name':    member.business_name or '',
                'business_address': member.business_address or '',

                # Loan
                'loan_type':            loan.loan_type,
                'interest_rate':        np(loan.interest_rate),
                'loan_duration':        np(loan.loan_duration),
                'repayment_duration':   np(loan.repayment_duration),
                'loan_amount':          np(loan.loan_amount),
                'loan_amount_in_words': loan.loan_amount_in_words or num_to_nepali_words(loan.loan_amount),
                'loan_status':          loan.status,
                'loan_completion_year':  np(loan.loan_completion_year or ''),
                'loan_completion_month': np(loan.loan_completion_month or ''),
                'loan_completion_day':   np(loan.loan_completion_day or ''),

                # Date (BS)
                'bs_year':    np(bs_year),
                'bs_month':   np(bs_month),
                'bs_day':     np(bs_day),
                'date_nepali': np(date_nepali),

                # Approval
                'approval_date':             np(approval.approval_date if approval else ''),
                'entered_by':                entered_by,
                'entered_post':              entered_post,
                'approved_by':               approved_by,
                'approver_post':             approver_post,
                'approved_loan_amount':      np(approval.approved_loan_amount if approval else ''),
                'approved_loan_amount_words': approval.approved_loan_amount_words if approval else '',
                'remarks':                   approval.remarks if approval else '',

                # Collateral Basic
                'monthly_saving': np(collateral_basic.monthly_saving if collateral_basic else ''),
                'child_saving':   np(collateral_basic.child_saving if collateral_basic else ''),
                'total_saving':   np(collateral_basic.total_saving if collateral_basic else ''),
                'share_amount':   np(collateral_basic.share_amount if collateral_basic else ''),

                # Properties list
                'properties': [
                    {
                        'owner_name':       p.owner_name,
                        'father_or_spouse': p.father_or_spouse_name,
                        'grandfather':      p.grandfather_or_father_inlaw_name,
                        'district':         p.district,
                        'municipality_vdc': p.municipality_vdc,   # Fix: municipaliy_vdc typo
                        'ward_no':          np(p.ward_no),
                        'sheet_no':         np(p.sheet_no),
                        'plot_no':          np(p.plot_no),
                        'area':             np(p.area),
                        'land_type':        p.land_type,
                    }
                    for p in properties
                ],

                # Family
                'family_members': [
                    {
                        'name':           f.name,
                        'age':            np(f.age),
                        'relation':       f.relation,
                        'occupation':     f.occupation,
                        'monthly_income': np(f.monthly_income),
                        'member_of_coop': f.member_of_other_coop,
                    }
                    for f in family_details
                ],

                # Income / Expense
                'income_items': [
                    {'field': ie.field, 'amount': ie.amount}
                    for ie in income_expenses if ie.type == 'income'
                ],
                'expense_items': [
                    {'field': ie.field, 'amount': ie.amount}
                    for ie in income_expenses if ie.type == 'expense'
                ],
                'total_income':  np(sum(float(ie.amount or 0) for ie in income_expenses if ie.type == 'income')),
                'total_expense': np(sum(float(ie.amount or 0) for ie in income_expenses if ie.type == 'expense')),

                # Affiliations
                'affiliations': [
                    {
                        'institution':  a.institution,
                        'address':      a.address_of_institution,
                        'position':     a.position,
                        'income':       np(a.estimated_income),
                        'remarks':      a.remarks or '',
                    }
                    for a in affiliations
                ],

                # Projects
                'projects': [
                    {
                        'project_name':           p.project_name,
                        'self_investment':        np(p.self_investment),
                        'requested_loan_amount':  np(p.requested_loan_amount),
                        'total_cost':             np(p.total_cost),
                        'remarks':                p.remarks or '',
                    }
                    for p in projects
                ],

                # Witnesses
                'witnesses': [
                    {
                        'name':     w.name,
                        'relation': w.relation,
                        'address':  w.address,
                        'tole':     w.tole,
                        'ward':     np(w.ward),
                        'age':      np(w.age),
                    }
                    for w in witnesses
                ],

                # Guarantors
                'guarantors': [
                    {
                        'guarantor_name':        g.guarantor_name,
                        'guarantor_address':     g.guarantor_address,
                        'guarantor_ward':        np(g.guarantor_ward),
                        'guarantor_phone':       np(g.guarantor_phone),
                        'guarantor_citizenship': np(g.guarantor_citizenship),
                        'guarantor_grandfather': g.guarantor_grandfather,
                        'guarantor_father':      g.guarantor_father,
                        'guarantor_age':         np(g.guarantor_age),  
                        'guarantor_citizenship_issue_district':  g.guarantor_citizenship_issue_district,
                    }
                    for g in guarantors
                ],
            }

            return context

        except Member.DoesNotExist:
            raise Exception(f"Member {member_number} not found!")
        except LoanInfo.DoesNotExist:
            raise Exception(f"No loan found for member {member_number}!")