from members.models import Member
from loans.models import LoanInfo, ApprovalInfo

from .organization_context import get_organization_context
from .member_context import get_member_context
from .loan import get_loan_context
from .collateral import get_collateral_context
from .financial import get_financial_context
from .parties import get_parties_context
from .utils import np




class ReportContextBuilder:
    @staticmethod
    def build(member_number, entered_by, entered_post, approved_by, approver_post ):
        member = Member.objects.prefetch_related(
            'collateralproperty_set',
            'collateralfamilydetail_set',
            'collateralincomeexpense_set',
            'witnessinfo_set',
            'guarantordetails_set'
        ).get(member_number=member_number)

        loan = LoanInfo.objects.filter(member=member).order_by('-id').first()
        if not loan:
            raise Exception("Loan not found!")
        
        approval = ApprovalInfo.objects.filter(member=member).first()

        context = {
            **get_organization_context(),
            **get_member_context(member),
            **get_loan_context(loan),
            **get_collateral_context(member),
            **get_financial_context(member),
            **get_parties_context(member),

            'entered_by': entered_by,
            'entered_post': entered_post,
            'approved_by': approved_by,
            'approver_post': approver_post,

            'approval_date': approval.approval_date if approval else '',
            'approved_loan_amount': np(approval.approval_loan_amount) if approval else '',

        }

