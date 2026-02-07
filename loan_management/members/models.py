from django.db import models

class Member(models.Model):
    """ Member information matching member_info table in PyQt5 app"""
    date = models.DateField()
    member_number = models.CharField(max_length=50, unique=True)
    member_name = models.CharField(max_length=200)
    member_name_nepali = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    dob_bs = models.CharField(max_length=20, blank=True, null=True) # Nepali date
    citizenship_no = models.CharField(max_length=50, blank=True, null=True)
    national_id_no = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    facebook_detail = models.CharField(max_length=100, blank=True, null=True)
    whatsapp_detail = models.CharField(max_length=100, blank=True, null=True)
    grandfather_name = models.CharField(max_length=200, blank=True, null=True)
    father_name = models.CharField(max_length=200, blank=True, null=True)
    spouse_name = models.CharField(max_length=200, blank=True, null=True)
    spouse_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    ward_no = models.CharField(max_length=10, blank=True, null=True)
    business_name = models.CharField(max_length=200, blank=True, null=True)
    business_address = models.CharField(max_length=300, blank=True, null=True)
    job = models.CharField(max_length=200, blank=True, null=True)
    job_address = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        db_table = 'member_info'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.member_number} - {self.member_name}"

