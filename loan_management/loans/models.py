from django.db import models
from members.models import Member

class LoanScheme(models.Model):
    """Loan schemes with interest rates"""
    loan_type = models.CharField(max_length=100, unique=True)
    interest_rate = models.FloatField()

    class Meta:
        db_table = 'loan_schemes'

    def __str__(self):
        return f"{self.loan_type} - {self.interest_rate}%"
    
class LoanInfo(models.Model):
    """Main loan information"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
        ('completed', 'Completed'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, to_field='member_number', db_column='member_number')
    loan_type = models.CharField(max_length=100)
    interest_rate = models.FloatField()
    loan_duration = models.CharField(max_length=50)
    repayment_duration = models.CharField(max_length=50)
    loan_amount = models.CharField(max_length=50)
    loan_amount_in_words = models.TextField()
    loan_completion_year = models.CharField(max_length=10)
    loan_completion_month = models.CharField(max_length=10)
    loan_completion_day = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'loan_info'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.member.member_number} - {self.loan_type} - {self.loan_amount}"
    

class ApprovalInfo(models.Model):
    """ Loan approval details"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, to_field='member_number', db_column='member_number')
    approval_date = models.CharField(max_length=50)
    entered_by = models.CharField(max_length=200)
    entered_post = models.CharField(max_length=100)
    approved_by = models.CharField(max_length=200)
    approver_post = models.CharField(max_length=100)
    remarks = models.TextField(max_length=50)
    approved_loan_amount = models.CharField(max_length=50)
    approved_loan_amount_words = models.TextField()

    class Meta:
        db_table = 'approval_info'

    def __str__(self):
        return f"{self.member.member_number} - Approved: Rs. {self.approved_loan_amount}"

class WitnessInfo(models.Model):
    """Witness information"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, to_field='member_number', db_column='member_number')
    name = models.CharField(max_length=200)
    relation = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    tole = models.CharField(max_length=100, blank=True, null=True)
    ward = models.CharField(max_length=10)
    age = models.CharField(max_length=10)

    class Meta:
        db_table = 'witness_info'
    
    def __str__(self):
        return f"{self.member.member_number} - {self.name}"
    
class GuarantorDetails(models.Model):
    """Guarantor information"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, to_field='member_number', db_column='member_number')
    guarantor_member_number = models.CharField(max_length=50, blank=True, null=True)
    guarantor_name = models.CharField(max_length=200)
    guarantor_address = models.CharField(max_length=300)
    guarantor_ward = models.CharField(max_length=10)
    guarantor_phone = models.CharField(max_length=20)
    guarantor_citizenship = models.CharField(max_length=50)
    guarantor_grandfather = models.CharField(max_length=200)
    guarantor_father = models.CharField(max_length=200)
    guarantor_citizenship_issue_district = models.CharField(max_length=100)
    guarantor_age = models.CharField(max_length=10)

    class Meta:
        db_name = 'guarantor_details'

    def __str__(self):
        return f"{self.member.member_number} - {self.guarantor_name}"
    
class ManjurinamaDetails(models.Model):
    """Manjurinama Details"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, to_field='member_number', db_column='member_number')
    person_name = models.CharField(max_length=200)
    grandfather_name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    age = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    wada_no = models.CharField(max_length=10)
    tole = models.CharField(max_length=100)

    class Meta:
        db_table = 'manjurinama_details'