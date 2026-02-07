from django.db import models
from members.models import Member

class CollateralBasic(models.Model):
    """ Basic collateral information for Kharkhacho loan type"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, to_field='member_number', db_column='member_number')
    monthly_saving = models.CharField(max_length=50)
    child_saving = models.CharField(max_length=50)
    total_saving = models.CharField(max_length=50)
    share_amount = models.CharField(max_length=50)

    class Meta:
        db_table = 'collateral_basic'

    def __str__(self):
        return f"{self.member.member_number} - Basic Collateral"
    
class CollateralProperty(models.Model):
    """Property collateral details (Dhito bibaran)"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, to_field='member_number', db_column='member_number')
    owner_name = models.CharField(max_length=200)
    father_or_spouse_name = models.CharField(max_length=200)
    grandfather_or_father_inlaw_name = models.CharField(max_length=200)
    district = models.CharField(max_length=100)
    municipality_vdc = models.CharField(max_length=100)
    sheet_no = models.CharField(max_length=50)
    ward_no = models.CharField(max_length=10)
    plot_no = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    land_type = models.CharField(max_length=100)

    class Meta:
        db_table = 'collateral_properties'
    
class CollateralFamilyDetail(models.Model):
    """Family details for collteral"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, to_field='member_number', db_column='member_number')
    name = models.CharField(max_length=200)
    age = models.CharField(max_length=10)
    relation = models.CharField(max_length=100)
    member_of_other_coop = models.CharField(max_length=200)
    occupation = models.CharField(max_length=100)
    monthly_income = models.CharField(max_length=50)

    class Meta:
        db_table = 'collateral_family_details'

class CollateralIncomeExpense(models.Model):
    """Income and expense tracking"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, to_field='member_number', db_column='member_number')
    field = models.CharField(max_length=200)
    amount = models.CharField(max_length=50)
    type = models.CharField(max_length=20) # 'income' or 'expense'

    class Meta:
        db_table = 'collateral_income_expense'

class CollateralAffiliation(models.Model):
    """ Organizational Affiliations"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, to_field='member_number', db_column='member_number')
    institution = models.CharField(max_length=200)
    address_of_institution = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    estimated_income = models.CharField(max_length=50)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'collateral_affiliations'



