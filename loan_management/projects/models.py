from django.db import models
from members.models import Member

class ProjectDetail(models.Model):
    """Project details for loan purpose"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, to_field='member_number', db_column='member_number')
    project_name = models.CharField(max_length=200)
    self_investment = models.CharField(max_length=50)
    request_loan_amount = models.CharField(max_length=50)
    total_budget_for_project = models.CharField(max_length=50)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'project_detail'

    def __str__(self):
        return f"{self.member.member_number} - {self.project_name}"

