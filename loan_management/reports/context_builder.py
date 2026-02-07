from members.models import Member
from loans.models import LoanInfo, ApprovalInfo, WitnessInfo, GuarantorDetails
from collateral.models import (
    CollateralBasic, CollateralProperty, CollateralFamilyDetail,
    CollateralAffiliation, CollateralIncomeExpense
)
from projects.models import ProjectDetail
from dashboard.models import OrganatizationProfile

class ReportContextBuilder:
    """Build context dictionary for report templates"""

    @staticmethod
    def build_loan_application_context(member_number, entered_by, entered_post,
                                       approved_by, approver_post):
        """Build complete context for loan application"""
        try:
            member = Member.objects.get(member_number=member_number)
            loan = LoanInfo.objects.filter(member=member).latest('created_at')

            # Get related data
            approval = ApprovalInfo.objects.filter(member=member).first()
            collateral_basic = CollateralBasic.objects.filter(member=member).first()
            properties = CollateralProperty.objects.filter(member=member)
            family_details = CollateralFamilyDetail.objects.filter(member=member)
            income_expenses = CollateralIncomeExpense.objects.filter(member=member)
            projects = ProjectDetail.objects.filter(member=member)
            witnesses = WitnessInfo.objects.filter(member=member)
            guarantors = GuarantorDetails.objects.filter(member=member)

            # Get organization profile
            org = OrganatizationProfile.objects.first()

            context = {
                # Organization Info
                'company_name': org.company_name if org else '',
                'company_address': org.address if org else '',

                # Member Info
                'member_number': member.member_number,
                'member_name': member.member_name,
                'phone': member.phone or '',
                'email': member.email or '',
                'citizenship_no': member.citizenship_no or '',
                'father_name': member.father_name or '',
                'grandfather_name': member.grandfather_name or '',
                'spouse_name': member.spouse_name or '',
                'address': member.add_to_class or '',
                'ward_no': member.ward_no or '',
                'profession': member.profession or '',

                # Loan Info
                'loan_type': loan.loan_type,
                'interest_rate': loan.interest_rate,
                'loan_duration': loan.loan_duration,
                'repayment_duration': loan.repayment_duration,
                'loan_amount': loan.loan_amount,
                'loan_amount_in_words': loan.loan_amount_in_words,
                'loan_completion_year': loan.loan_completion_year,
                'loan_completion_month': loan.loan_completion_month,
                'loan_completion_day': loan.loan_completion_day,

                # Approval Info
                'approval_date': approval.approval_date if approval else '',
                'entered_by': entered_by,
                'entered_post': entered_post,
                'approved_by': approved_by,
                'approver_post': approver_post,
                'approved_loan_amount': approval.approved_loan_amount if approval else '',
                'approved_loan_amount_words': approval.approved_loan_amount_words if approval else '',
                'remarks': approval.remarks if approval else '',

                # Collateral Basic
                'monthly_saving': collateral_basic.monthly_saving if collateral_basic else '',
                'child_saving': collateral_basic.child_saving if collateral_basic else '',
                'total_saving': collateral_basic.total_saving if collateral_basic else '',
                'share_amount': collateral_basic.share_amount if collateral_basic else '',

                # Properties (as list)
                'properties': [
                    {
                        'owner_name': p.owner_name,
                        'district': p.district,
                        'municipality_vdc': p.municipaliy_vdc,
                        'ward_no': p.ward_no,
                        'plot_no': p.plot_no,
                        'area': p.area,
                        'land_type': p.land_type,
                    }
                    for p in properties
                ],

                # Family Details
                'family_members':[
                    {
                        'name': f.name,
                        'age': f.age,
                        'relation': f.relation,
                        'occupation': f.occupation,
                        'monthly_income': f.monthly_income,
                    }
                    for f in family_details
                ],

                # Income / Expenses
                'income_items': [
                    {'field': ie.field, 'amount':ie.amount}
                    for ie in income_expenses if ie.type == 'income'
                ], 
                'expense_items': [
                    {'field': ie.field, 'amount': ie.amount}
                    for ie in income_expenses if ie.type == 'expense'
                ],

                # Projects
                'projects': [
                    {
                        'project_name': p.project_name,
                        'self_investment': p.self_investment,
                        'requested_loan_amount': p.requested_loan_amount,
                        'total_cost': p.total_cost,
                        'remarks': p.remarks or '',
                        
                    }                    
                    for p in projects
                ],

                # Witness
                'witnesses': [
                    {
                        'witness_name': w.name,
                        'relation': w.relation,
                        'ward': w.ward,
                        'age': w.age,
                    }
                    for w in witnesses
                ],

                # Guarantors
                'guarantors': [
                    {
                        'guarantor_name': g.guarantor_name,
                        'guarantor_address': g.guarantor_address,
                        'guarantor_phone': g.guarantor_phone,
                        'guarantor_citizenship': g.guarantor_citizenship,
                        'guarantor_age': g.gurantor_age,
                    }
                    for g in guarantors
                ],
            }
            
            return context
        
        except Member.DoesNotExist:
            raise Exception(f"Member {member_number} not found!")
        except LoanInfo.DoesNotExist:
            raise Exception(f"No loan found for member {member_number}!")
        

