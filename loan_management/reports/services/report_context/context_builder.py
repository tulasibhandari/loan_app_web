from members.models import Member
from loans.models import LoanInfo, ApprovalInfo
from collateral.models import (
    CollateralBasic, CollateralProperty, CollateralFamilyDetail,
    CollateralAffiliation, CollateralIncomeExpense
)
from projects.models import ProjectDetail

from reports.services.report_context.member_context import get_member_context
from reports.services.report_context.loan import get_loan_context
from reports.services.report_context.collateral import get_collateral_context
from reports.services.report_context.financial import get_financial_context
from reports.services.report_context.parties import get_parties_context
from reports.services.report_context.organization_context import get_organization_context

from reports.services.report_context.utils import np

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
    def build(member_number, entered_by, entered_post, approved_by, approver_post):
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

            member_ctx = get_member_context(member)
            loan_ctx = get_loan_context(loan)
            org_ctx = get_organization_context(org)
            collateral_ctx = get_collateral_context(member)
            financial_ctx = get_financial_context(member)
            parties_ctx = get_parties_context(member)    

            context = {
                **member_ctx,
                **loan_ctx,
                **org_ctx,
                **collateral_ctx,
                **financial_ctx,
                **parties_ctx,

                # Approval + date
                'approval_date': np(approval.approval_date if approval else ''),
                'entered_by': entered_by,
                'entered_post': entered_post,
                'approved_by': approved_by,
                'approver_post': approver_post,
            }
            return context
        except Member.DoesNotExist:
            raise Exception(f"Member {member_number} not found!")
        except LoanInfo.DoesNotExist:
            raise Exception(f"No loan found for member {member_number}!")

         