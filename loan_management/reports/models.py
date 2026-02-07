from django.db import models
from members.models import Member
from accounts.models import User

class ReportTracking(models.Model):
    """Track generated reports"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, to_field='member_number', db_column='member_number')
    report_type = models.CharField(max_length=100)
    file_path = models.CharField(max_length=500)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    generated_date = models.DateField()

    class Meta:
        db_table = 'report_tracking'
        ordering = ['-generated_date']
    
    def __str__(self):
        return f"{self.report_type} - {self.member.member_number}, - {self.generated_date}"
    
