from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import LoanInfo, LoanScheme, ApprovalInfo, WitnessInfo, GuarantorDetails

@admin.register(LoanInfo)
class LoanInfoAdmin(ModelAdmin):
    list_display = ['id', 'member', 'loan_type', 'loan_amount', 'status']
    list_filter = ['status', 'loan_type']
    search_fields = ['member__member_number', 'member__member_name']

@admin.register(LoanScheme)
class LoanSchemeAdmin(ModelAdmin):
    list_display = ['loan_type', 'interest_rate']

@admin.register(ApprovalInfo)
class ApprovalInfoAdmin(ModelAdmin):
    list_display = ['member', 'approved_by', 'approval_date', 'approved_loan_amount']